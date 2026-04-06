import textwrap
from urllib.parse import urlparse

import requests

GRAPHQL_URL = "https://api.github.com/graphql"
BATCH_SIZE = 100


def build_batch_query(repos):
    """Build a GraphQL query to fetch stargazerCount and description for repos.

    Args:
        repos: List of dicts with "url" key (e.g., "https://github.com/owner/name").

    Returns:
        GraphQL query string.
    """
    fragments = []
    for i, repo in enumerate(repos):
        path = urlparse(repo["url"]).path.strip("/")
        owner, name = path.split("/")
        fragments.append(
            'repo_{0}: repository(owner: "{1}", name: "{2}") '
            '{{ stargazerCount description }}'.format(i, owner, name)
        )
    return "query { " + " ".join(fragments) + " }"


def enrich_descriptions(session, repos, token):
    """Fetch descriptions via GitHub GraphQL API in batches of 100.

    Args:
        session: requests.Session instance.
        repos: List of repo dicts (already sorted top-N).
        token: GitHub API token string.

    Returns:
        New list of dicts with "description" key added.
        Falls back to the original list on any error.
    """
    if not repos:
        return repos

    enriched = []
    headers = {
        "Authorization": "bearer {0}".format(token),
        "Content-Type": "application/json",
    }

    for batch_start in range(0, len(repos), BATCH_SIZE):
        batch = repos[batch_start:batch_start + BATCH_SIZE]
        query = build_batch_query(batch)

        try:
            resp = session.post(
                GRAPHQL_URL,
                json={"query": query},
                headers=headers,
            )
        except requests.RequestException:
            return repos

        if resp.status_code != 200:
            return repos

        data = resp.json()
        if "data" not in data:
            return repos

        for i, repo in enumerate(batch):
            repo_data = data["data"].get("repo_{0}".format(i))
            new_repo = dict(repo)
            if repo_data and repo_data.get("description"):
                new_repo["description"] = textwrap.shorten(
                    repo_data["description"], width=60, placeholder="..."
                )
            else:
                new_repo["description"] = " "
            enriched.append(new_repo)

    return enriched
