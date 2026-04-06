from unittest.mock import MagicMock
from ghtopdep.graphql_enrich import build_batch_query, enrich_descriptions


def test_build_batch_query_single_repo():
    repos = [{"url": "https://github.com/facebook/react", "stars": 200000}]
    query = build_batch_query(repos)
    assert "repo_0" in query
    assert 'owner: "facebook"' in query
    assert 'name: "react"' in query
    assert "stargazerCount" in query
    assert "description" in query


def test_build_batch_query_multiple_repos():
    repos = [
        {"url": "https://github.com/facebook/react", "stars": 200000},
        {"url": "https://github.com/vuejs/vue", "stars": 180000},
    ]
    query = build_batch_query(repos)
    assert "repo_0" in query
    assert "repo_1" in query
    assert 'owner: "vuejs"' in query


def test_enrich_descriptions_success():
    repos = [
        {"url": "https://github.com/facebook/react", "stars": 200000},
        {"url": "https://github.com/vuejs/vue", "stars": 180000},
    ]

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "data": {
            "repo_0": {
                "stargazerCount": 200000,
                "description": "A JavaScript library for building user interfaces",
            },
            "repo_1": {
                "stargazerCount": 180000,
                "description": "A progressive framework for building UIs",
            },
        }
    }

    mock_session = MagicMock()
    mock_session.post.return_value = mock_response

    result = enrich_descriptions(mock_session, repos, "fake-token")

    assert len(result) == 2
    assert result[0]["description"] == "A JavaScript library for building user interfaces"
    assert result[1]["description"] == "A progressive framework for building UIs"
    # Original repos should not be mutated
    assert "description" not in repos[0]


def test_enrich_descriptions_truncates_long_description():
    repos = [{"url": "https://github.com/owner/repo", "stars": 100}]
    long_desc = "A" * 100  # longer than 60 chars

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "data": {
            "repo_0": {"stargazerCount": 100, "description": long_desc},
        }
    }

    mock_session = MagicMock()
    mock_session.post.return_value = mock_response

    result = enrich_descriptions(mock_session, repos, "fake-token")
    assert len(result[0]["description"]) <= 60


def test_enrich_descriptions_handles_null_description():
    repos = [{"url": "https://github.com/owner/repo", "stars": 100}]

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "data": {
            "repo_0": {"stargazerCount": 100, "description": None},
        }
    }

    mock_session = MagicMock()
    mock_session.post.return_value = mock_response

    result = enrich_descriptions(mock_session, repos, "fake-token")
    assert result[0]["description"] == " "


def test_enrich_descriptions_falls_back_on_http_error():
    repos = [{"url": "https://github.com/owner/repo", "stars": 100}]

    mock_response = MagicMock()
    mock_response.status_code = 401

    mock_session = MagicMock()
    mock_session.post.return_value = mock_response

    result = enrich_descriptions(mock_session, repos, "bad-token")
    # Should return original repos unchanged
    assert result is repos


def test_enrich_descriptions_falls_back_on_network_error():
    import requests

    repos = [{"url": "https://github.com/owner/repo", "stars": 100}]

    mock_session = MagicMock()
    mock_session.post.side_effect = requests.RequestException("connection failed")

    result = enrich_descriptions(mock_session, repos, "fake-token")
    assert result is repos


def test_enrich_descriptions_empty_list():
    result = enrich_descriptions(MagicMock(), [], "fake-token")
    assert result == []
