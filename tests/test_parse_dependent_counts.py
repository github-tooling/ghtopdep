from ghtopdep.ghtopdep import parse_dependent_counts


SAMPLE_HTML = """
<div class="table-list-header-toggle">
  <a class="btn-link selected" href="/owner/repo/network/dependents?dependent_type=REPOSITORY">
    2,295 Repositories
  </a>
  <a class="btn-link" href="/owner/repo/network/dependents?dependent_type=PACKAGE">
    44 Packages
  </a>
</div>
<div id="dependents">
  <div class="Box">
  </div>
</div>
"""


def test_parses_both_counts():
    counts = parse_dependent_counts(SAMPLE_HTML)
    assert counts["REPOSITORY"] == 2295
    assert counts["PACKAGE"] == 44


def test_single_repository():
    html = """
    <div class="table-list-header-toggle">
      <a class="btn-link selected" href="#">1 Repository</a>
    </div>
    """
    counts = parse_dependent_counts(html)
    assert counts["REPOSITORY"] == 1


def test_single_package():
    html = """
    <div class="table-list-header-toggle">
      <a class="btn-link" href="#">1 Package</a>
    </div>
    """
    counts = parse_dependent_counts(html)
    assert counts["PACKAGE"] == 1


def test_large_numbers_with_commas():
    html = """
    <div class="table-list-header-toggle">
      <a class="btn-link selected" href="#">1,234,567 Repositories</a>
    </div>
    """
    counts = parse_dependent_counts(html)
    assert counts["REPOSITORY"] == 1234567


def test_returns_empty_dict_on_missing_elements():
    html = "<html><body>nothing here</body></html>"
    counts = parse_dependent_counts(html)
    assert counts == {}


def test_returns_empty_dict_on_malformed_text():
    html = """
    <div class="table-list-header-toggle">
      <a class="btn-link" href="#">not a number Repositories</a>
    </div>
    """
    counts = parse_dependent_counts(html)
    assert counts == {}
