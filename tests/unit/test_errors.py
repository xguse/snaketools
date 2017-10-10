"""Unit test snaketools.errors."""
from snaketools import errors as e

from tests.test_snaketools import *  # noqa: F403,F401


def test_snaketoolserror_inheritance():
    """Ensure inheritance membership."""
    tests = (issubclass(e.SnaketoolsError, Exception), )
    assert all(tests)


def test_notimplementedyet_inheritance():
    """Ensure inheritance membership."""
    tests = (issubclass(e.NotImplementedYet, Exception),
             issubclass(e.NotImplementedYet, NotImplementedError),
             issubclass(e.NotImplementedYet, e.SnaketoolsError))
    assert all(tests)


def test_validationerror_inheritance():
    """Ensure inheritance membership."""
    tests = (issubclass(e.ValidationError, Exception),
             issubclass(e.ValidationError, e.SnaketoolsError))
    assert all(tests)
