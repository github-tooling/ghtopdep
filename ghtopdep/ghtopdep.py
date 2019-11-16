import calendar
import json
import sys
import textwrap
from urllib.parse import urlparse
from collections import namedtuple
from datetime import datetime, timedelta
from email.utils import formatdate, parsedate
from operator import attrgetter

import click
import github3
import requests
from cachecontrol import CacheControl
from cachecontrol.caches import FileCache
from cachecontrol.heuristics import BaseHeuristic
from halo import Halo
from selectolax.parser import HTMLParser
from tabulate import tabulate
import appdirs

CACHE_DIR = appdirs.user_cache_dir("ghtopdep")
NEXT_BUTTON_SELECTOR = "#dependents > div.paginate-container > div > a"
ITEM_SELECTOR = "#dependents > div.Box > div.flex-items-center"
REPO_SELECTOR = "span > a.text-bold"
STARS_SELECTOR = "div > span:nth-child(1)"
GITHUB_URL = "https://github.com"


class OneDayHeuristic(BaseHeuristic):

    def update_headers(self, response):
        date = parsedate(response.headers["date"])
        expires = datetime(*date[:6]) + timedelta(days=1)
        return {"expires": formatdate(calendar.timegm(expires.timetuple())), "cache-control": "public"}

    def warning(self, response):
        msg = "Automatically cached! Response is Stale."
        return "110 - {0}".format(msg)


def already_added(repo_url, repos):
    for repo in repos:
        if repo.url == repo_url:
            return True


def fetch_description(gh, relative_url):
    _, owner, repository = relative_url.split("/")
    repository = gh.repository(owner, repository)
    repo_description = " "
    if repository.description:
        repo_description = textwrap.shorten(repository.description, width=60, placeholder="...")
    return repo_description


def sort_repos(repos, rows):
    sorted_repos = sorted(repos, key=attrgetter("stars"), reverse=True)
    return sorted_repos[:rows]


def show_result(repos, total_repos_count, more_than_zero_count, destination, destinations, table):
    if table:
        if repos:
            click.echo(tabulate(repos, headers="keys", tablefmt="grid"))
            click.echo("found {0} {1} others {2} are private".format(total_repos_count, destinations, destinations))
            click.echo("found {0} {1} with more than zero star".format(more_than_zero_count, destinations))
        else:
            click.echo("Doesn't find any {0} that match search request".format(destination))
    else:
        click.echo(json.dumps([repo._asdict() for repo in repos]))


@click.command()
@click.argument("url")
@click.option("--repositories/--packages", default=True, help="Sort repositories or packages (default repositories)")
@click.option("--table/--json", default=True, help="View mode")
@click.option("--description", is_flag=True, help="Show description of packages or repositories (performs additional "
                                                  "request per repository)")
@click.option("--rows", default=10, help="Number of showing repositories (default=10)")
@click.option("--minstar", default=5, help="Minimum number of stars (default=5)")
@click.option("--search", help="search code at dependents (repositories/packages)")
@click.option("--token", envvar="GHTOPDEP_TOKEN")
def cli(url, repositories, search, table, rows, minstar, description, token):
    if (description or search) and token:
        gh = github3.login(token=token)
        CacheControl(gh.session, cache=FileCache(CACHE_DIR), heuristic=OneDayHeuristic())
    elif (description or search) and not token:
        click.echo("Please provide token")
        sys.exit()

    if description:
        Repo = namedtuple("Repo", ["url", "stars", "description"])
    else:
        Repo = namedtuple("Repo", ["url", "stars"])

    destination = "repository"
    destinations = "repositories"
    if not repositories:
        destination = "package"
        destinations = "packages"
    page_url = "{0}/network/dependents?dependent_type={1}".format(url, destination.upper())

    repos = []
    more_than_zero_count = 0
    total_repos_count = 0
    spinner = Halo(text="Fetching information about {0}".format(destinations), spinner="dots")
    spinner.start()
    sess = requests.session()
    cached_sess = CacheControl(sess, cache=FileCache(CACHE_DIR), heuristic=OneDayHeuristic())
    while True:
        response = cached_sess.get(page_url)
        parsed_node = HTMLParser(response.text)
        dependents = parsed_node.css(ITEM_SELECTOR)
        total_repos_count += len(dependents)
        for dep in dependents:
            repo_stars_list = dep.css(STARS_SELECTOR)
            # only for ghost or private? packages
            if repo_stars_list:
                repo_stars = dep.css(STARS_SELECTOR)[0].text().strip()
                repo_stars_num = int(repo_stars.replace(",", ""))
            else:
                continue

            if repo_stars_num != 0:
                more_than_zero_count += 1
            if repo_stars_num >= minstar:
                relative_repo_url = dep.css(REPO_SELECTOR)[0].attributes["href"]
                repo_url = "{0}{1}".format(GITHUB_URL, relative_repo_url)

                # can be listed same package
                is_already_added = already_added(repo_url, repos)
                if not is_already_added and repo_url != url:
                    if description:
                        repo_description = fetch_description(gh, relative_repo_url)
                        repos.append(Repo(repo_url, repo_stars_num, repo_description))
                    else:
                        repos.append(Repo(repo_url, repo_stars_num))

        node = parsed_node.css(NEXT_BUTTON_SELECTOR)
        if len(node) == 2:
            page_url = node[1].attributes["href"]
        elif len(node) == 0 or node[0].text() == "Previous":
            spinner.stop()
            break
        elif node[0].text() == "Next":
            page_url = node[0].attributes["href"]

    sorted_repos = sort_repos(repos, rows)

    if search:
        for repo in repos:
            repo_path = urlparse(repo.url).path[1:]
            for s in gh.search_code("{0} repo:{1}".format(search, repo_path)):
                click.echo("{0} with {1} stars".format(s.html_url, repo.stars))
    else:
        show_result(sorted_repos, total_repos_count, more_than_zero_count, destination, destinations, table)
