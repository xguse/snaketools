"""Unit test the pathify_by_key_ends function."""
from pathlib import Path

from snaketools import snaketools

from tests.test_snaketools import *  # noqa: F403,F401


def test_pathify_this():
    """Ensure pathify_this returns expected values."""
    assert snaketools.pathify_this("TEXT_FILE")
    assert snaketools.pathify_this("TEXT_PATH")
    assert snaketools.pathify_this("TEXT_DIR")
    assert snaketools.pathify_this("DIR")
    assert not snaketools.pathify_this("TEXT")


def test_pathify_by_key_ends(config_1_dict):
    """Ensure pathify_by_key_ends returns expected types."""
    original = config_1_dict
    pathified = snaketools.pathify_by_key_ends(dictionary=original)

    assert isinstance(pathified.COMMON, dict)
    assert isinstance(pathified.COMMON.RUN_NAME, str)
    assert isinstance(pathified.COMMON.OUT_DIR, Path)
    assert isinstance(pathified.COMMON.INTERIM_DIR, Path)
    assert isinstance(pathified.COMMON.DRAW_RULE, str)
    assert isinstance(pathified.COMMON.DRAW_PRETTY_NAMES, bool)
    assert isinstance(pathified.RULE_1, dict)
    assert isinstance(pathified.RULE_1.PARAMS, dict)
    assert isinstance(pathified.RULE_1.PARAMS.PARAM_1, int)
    assert isinstance(pathified.RULE_1.PARAMS.PARAM_2, str)
    assert isinstance(pathified.RULE_1.IN, dict)
    assert isinstance(pathified.RULE_1.IN.IN_FILE_1_PATH, Path)
