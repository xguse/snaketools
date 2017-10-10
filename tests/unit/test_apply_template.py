"""Unit test the apply_template function."""
from munch import Munch

import pytest

from snaketools import errors as e
from snaketools import snaketools

from tests.test_snaketools import *  # noqa: F403,F401


@pytest.fixture()
def keywords():
    """Provide sets of keywords for testing."""
    keywords = Munch()
    keywords.one_kw = {"ith": ["1st", "2nd"]}
    keywords.two_kw = {"ith": ["1st", "2nd"],
                       "jth": ["1", "2"]}
    keywords.two_kw_uneven = {"ith": ["1st", "2nd"],
                              "jth": ["1", "2", "3"]}
    keywords.munch = Munch(keywords.one_kw)
    return keywords


@pytest.fixture()
def templates():
    """Provide sets of templates for testing."""
    templates = Munch()
    templates.one_kw = "Here is the {ith} keyword."
    templates.two_kw = "Here is the {ith} keyword. Here is the {jth} keyword."
    return templates


def test_results_one_kw(templates, keywords):
    """Ensure results objects look as expected."""
    # GIVEN a template and keywords
    results_expected = ["Here is the 1st keyword.", "Here is the 2nd keyword."]

    # THEN it should return a list of strings of form `template`
    #      with values in `keywords` inserted.
    results = snaketools.apply_template(templates.one_kw, keywords.one_kw)
    assert len(results) == len(keywords.one_kw['ith'])
    assert results[0] == results_expected[0]
    assert results[1] == results_expected[1]

    # THEN ditto when passed a non-dict dict-like `keywords`.
    results_munch = snaketools.apply_template(templates.one_kw, keywords.munch)
    assert len(results) == len(keywords.one_kw['ith'])
    assert results_munch[0] == results_expected[0]
    assert results_munch[1] == results_expected[1]

    # THEN ditto when passed a `keywords` with unused keywords.
    results_unused = snaketools.apply_template(templates.one_kw, keywords.two_kw)
    assert len(results) == len(keywords.one_kw['ith'])
    assert results_unused[0] == results_expected[0]
    assert results_unused[1] == results_expected[1]


def test_unequal_kw_lists(templates, keywords):
    """Handle unequal kw lists."""
    # GIVEN a template and keywords where keywords have unequal lengths
    # THEN raise ValidationError
    with pytest.raises(e.ValidationError):
        snaketools.apply_template(templates.one_kw, keywords.two_kw_uneven)
