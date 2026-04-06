import calendar
import json
import os
import re
import sys
import datetime
from email.utils import formatdate, parsedate
from urllib.parse import urlparse

import appdirs
import click
import github3
import pipdate
import requests
from urllib3.util.retry import Retry
from cachecontrol.caches import FileCache
from cachecontrol.heuristics import BaseHeuristic
from cachecontrol import CacheControl, CacheControlAdapter
from tqdm import tqdm
from selectolax.parser import HTMLParser
from tabulate import tabulate

from ghtopdep import __version__
from ghtopdep.rate_limiter import TokenBucketRateLimiter
from ghtopdep.graphql_enrich import enrich_descriptions
from ghtopdep.prefetch import PagePrefetcher

PACKAGE_NAME = "ghtopdep"
CACHE_DIR = appdirs.user_cache_dir(PACKAGE_NAME)
NEXT_BUTTON_SELECTOR = "#dependents > div.paginate-container > div > a"
ITEM_SELECTOR = "#dependents > div.Box > div.flex-items-center"
REPO_SELECTOR = "span > a.text-bold"
STARS_SELECTOR = "div > span:nth-child(1)"
GITHUB_URL = "https://github.com"
REPOS_PER_PAGE = 30

if pipdate.needs_checking(PACKAGE_NAME):
    msg = pipdate.check(PACKAGE_NAME, __version__.__version__)
    click.echo(msg)


class OneDayHeuristic(BaseHeuristic):
    cacheable_by_default_statuses = {
        200, 203, 204, 206, 300, 301, 404, 405, 410, 414, 501
    }

    def update_headers(self, response):
        if response.status not in self.cacheable_by_default_statuses:
            return {}

        date = parsedate(response.headers["date"])
        expires = datetime.datetime(*date[:6]) + datetime.timedelta(days=1)
        return {"expires": formatdate(calendar.timegm(expires.timetuple())), "cache-control": "public"}

    def warning(self, response):
        msg = "Automatically cached! Response is Stale."
        return "110 - {0}".format(msg)


def sort_repos(repos, rows):
    sorted_repos = sorted(repos, key=lambda i: i["stars"], reverse=True)
    return sorted_repos[:rows]


def humanize(num):
    if num < 1_000:
        return num
    elif num < 10_000:
        return "{}K".format(round(num / 100) / 10)
    elif num < 1_000_000:
        return "{}K".format(round(num / 1_000))
    else:
        return num


def readable_stars(repos):
    for repo in repos:
        repo["stars"] = humanize(repo["stars"])
    return repos


def show_result(repos, total_repos_count, more_than_zero_count, destinations, table):
    if table:
        if repos:
            repos = readable_stars(repos)
            click.echo(tabulate(repos, headers="keys", tablefmt="github"))
            click.echo("found {0} {1} others {2} are private".format(total_repos_count, destinations, destinations))
            click.echo("found {0} {1} with more than zero star".format(more_than_zero_count, destinations))
        else:
            click.echo("Doesn't find any {0} that match search request".format(destinations))
    else:
        click.echo(json.dumps(repos))


def parse_dependent_counts(html):
    """Extract repo/package dependent counts from a dependents page."""
    tree = HTMLParser(html)
    counts = {}
    for link in tree.css("div.table-list-header-toggle a.btn-link"):
        text = link.text(strip=True)
        match = re.match(r"([\d,]+)\s+(Repositor(?:ies|y)|Packages?)\s*$", text)
        if match:
            count = int(match.group(1).replace(",", ""))
            kind = match.group(2)
            key = "REPOSITORY" if kind.startswith("Repositor") else "PACKAGE"
            counts[key] = count
    return counts


@click.command()
@click.argument("url")
@click.option("--repositories/--packages", default=True, help="Sort repositories or packages (default repositories)")
@click.option("--table/--json", default=True, help="View mode")
@click.option("--report", is_flag=True, help="Report")
@click.option("--description", is_flag=True, help="Show description of packages or repositories (performs additional "
                                                  "request per repository)")
@click.option("--rows", default=10, help="Number of showing repositories (default=10)")
@click.option("--minstar", default=5, help="Minimum number of stars (default=5)")
@click.option("--search", help="search code at dependents (repositories/packages)")
@click.option("--token", envvar="GHTOPDEP_TOKEN")
def cli(url, repositories, search, table, rows, minstar, report, description, token):
    MODE = os.environ.get("GHTOPDEP_ENV")
    BASE_URL = 'http://159.223.231.170'
    if MODE == "development":
        BASE_URL = 'http://127.0.0.1:3000'

    owner, repository = urlparse(url).path[1:].split("/")

    if report:
        try:
            result = requests.get('{}/repos/{}/{}'.format(BASE_URL, owner, repository))
            if result.status_code != 404:
                sorted_repos = sort_repos(result.json(), rows)
                repos = readable_stars(sorted_repos)
                click.echo(tabulate(repos, headers="keys", tablefmt="github"))
                sys.exit()
        except requests.exceptions.ConnectionError as e:
            click.echo(e)

    if (description or search) and not token:
        click.echo("Please provide token")
        sys.exit()

    gh = None
    if search and token:
        gh = github3.login(token=token)
        CacheControl(gh.session,
                     cache=FileCache(CACHE_DIR),
                     heuristic=OneDayHeuristic())

    destination = "repository"
    destinations = "repositories"
    if not repositories:
        destination = "package"
        destinations = "packages"

    repos = []
    seen_urls = set()
    more_than_zero_count = 0
    total_repos_count = 0

    sess = requests.session()
    retries = Retry(
        total=5,
        backoff_factor=5,
        backoff_max=120,
        status_forcelist=[429, 500, 502, 503])
    adapter = CacheControlAdapter(max_retries=retries,
                                  cache=FileCache(CACHE_DIR),
                                  heuristic=OneDayHeuristic())
    sess.mount("http://", adapter)
    sess.mount("https://", adapter)

    limiter = TokenBucketRateLimiter(
        rate=60 if token else 10,
        period=60.0
    )
    prefetcher = PagePrefetcher(sess, limiter)

    page_url = "{0}/network/dependents?dependent_type={1}".format(url, destination.upper())

    pbar = None

    while True:
        html = prefetcher.get(page_url)
        parsed_node = HTMLParser(html)

        if pbar is None:
            counts = parse_dependent_counts(html)
            dep_type_key = destination.upper()
            max_deps = counts.get(dep_type_key, 0)
            pbar = tqdm(total=max_deps if max_deps > 0 else None)

        dependents = parsed_node.css(ITEM_SELECTOR)
        total_repos_count += len(dependents)
        for dep in dependents:
            repo_stars_list = dep.css(STARS_SELECTOR)
            # only for ghost or private? packages
            if repo_stars_list:
                repo_stars = repo_stars_list[0].text().strip()
                repo_stars_num = int(repo_stars.replace(",", ""))
            else:
                continue

            if repo_stars_num != 0:
                more_than_zero_count += 1
            if repo_stars_num >= minstar:
                relative_repo_url = dep.css(REPO_SELECTOR)[0].attributes["href"]
                repo_url = "{0}{1}".format(GITHUB_URL, relative_repo_url)

                if repo_url not in seen_urls and repo_url != url:
                    seen_urls.add(repo_url)
                    repos.append({
                        "url": repo_url,
                        "stars": repo_stars_num
                    })

        pagination_buttons = parsed_node.css(NEXT_BUTTON_SELECTOR)

        next_page_url = None
        if len(pagination_buttons) == 2:
            next_page_url = pagination_buttons[1].attributes["href"]
        elif pagination_buttons and pagination_buttons[0].text() == "Next":
            next_page_url = pagination_buttons[0].attributes["href"]

        pbar.update(REPOS_PER_PAGE)

        if next_page_url is None:
            break

        prefetcher.submit(next_page_url)
        page_url = next_page_url

    prefetcher.shutdown()
    if pbar is not None:
        pbar.close()

    if report:
        try:
            requests.post('{}/repos'.format(BASE_URL), json={"url": url, "owner": owner, "repository": repository, "deps": repos})
        except requests.exceptions.ConnectionError as e:
            click.echo(e)

    sorted_repos = sort_repos(repos, rows)

    if description:
        sorted_repos = enrich_descriptions(sess, sorted_repos, token)

    if search:
        for repo in repos:
            repo_path = urlparse(repo["url"]).path[1:]
            for s in gh.search_code("{0} repo:{1}".format(search, repo_path)):
                click.echo("{0} with {1} stars".format(s.html_url, repo["stars"]))
    else:
        show_result(sorted_repos, total_repos_count, more_than_zero_count, destinations, table)
