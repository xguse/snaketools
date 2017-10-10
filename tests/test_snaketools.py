#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `snaketools` package."""

from pathlib import Path

import pytest

import yaml

from munch import munchify, Munch

from snaketools import snaketools  # noqa: F403,F401

__all__ = ["config_1_dict",
           "config_1",
           "snakefile_1",
           "snakerun_1"]


def process_config(config=None):
    """Prepare single config file."""
    if config is None:
        return Munch()
    else:
        if isinstance(config, str):
            config = Path(config)
        return munchify(yaml.safe_load(config.open()))


@pytest.fixture()
def config_1_dict():
    """Provide dict version of config_1.yaml."""
    config = process_config(config=Path("tests/files/configs/conf_1.yaml"))
    return config


@pytest.fixture()
def config_1(config_1_dict):
    """Provide fully processed config_1.yaml."""
    config = config_1_dict
    return snaketools.pathify_by_key_ends(config)


@pytest.fixture()
def snakefile_1():
    """Provide path to snakefile_1.yaml."""
    return Path('tests/files/snakefiles/Snakefile_1')


@pytest.fixture()
def snakerun_1(config_1, snakefile_1):
    """Provide empty SnakeRun object."""
    snakefile = snakefile_1
    cfg = config_1
    run = snaketools.SnakeRun(cfg=cfg, snakefile=snakefile)
    return run
