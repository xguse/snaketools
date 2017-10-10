"""Unit test the snaketools classes."""
from pathlib import Path

from munch import Munch

from snaketools import snaketools

from tests.test_snaketools import *   # noqa: F403,F401


def test_init_snakerun(snakerun_1, config_1, snakefile_1):
    """Ensure SnakeRule objects look as expected."""
    # GIVEN an init'd SnakeRun obj
    # THEN its attributes should look as expected
    run = snakerun_1
    cfg = config_1
    snakefile = snakefile_1

    assert run.snakefile == snakefile
    assert isinstance(run.globals, Munch)
    assert run.cfg == cfg
    assert run.name == cfg.COMMON["RUN_NAME"]
    assert isinstance(run.interim_dir, (type(None), Path))
    assert isinstance(run.out_dir, Path)
    assert run.out_dir.name == str(cfg.COMMON["RUN_NAME"])
    assert isinstance(run.pretty_names, dict)
    assert len(run.pretty_names) == 0
    assert isinstance(run.log_dir, Path)
    assert run.log_dir.name == 'logs'


def test_init_snakerule(snakerun_1):
    """Ensure SnakeRule objects look as expected."""
    # GIVEN an init'd SnakeRule obj
    # THEN its attributes should look as expected
    run = snakerun_1
    name = "RULE_1"
    pretty_name = "Rule One"
    rule = snaketools.SnakeRule(run=run, name=name, pretty_name=pretty_name)

    # expect to have a SnakeRule obj
    assert isinstance(rule, snaketools.SnakeRule)
    assert rule.pretty_name == pretty_name

    # expect that inputs are stored correctly
    assert rule.run == run
    assert rule.name == name.lower()

    # expect that files and dirs deduced are Path objects
    assert isinstance(rule.out_dir, (Path))
    assert isinstance(rule.log_dir, (Path))
    assert isinstance(rule.log, (Path))

    # expect that quick access in/out/param storage are Munch
    assert isinstance(rule.i, (Munch))
    assert isinstance(rule.o, (Munch))
    assert isinstance(rule.p, (Munch))

    # expect that configuration values for this rule are directly accessable as attributes
    assert hasattr(rule, 'IN')
    assert hasattr(rule, 'PARAMS')
    # expect this rule NOT to have 'OUT' bc it is not defined in the config
    assert not hasattr(rule, 'OUT')
