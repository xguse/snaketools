==========
SnakeTools
==========


.. image:: https://img.shields.io/pypi/v/snaketools.svg
        :target: https://pypi.python.org/pypi/snaketools

.. image:: https://img.shields.io/travis/xguse/snaketools.svg?style=flat-square
   :target: https://travis-ci.org/xguse/snaketools

.. image:: https://readthedocs.org/projects/snaketools/badge/?version=latest
        :target: https://snaketools.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://coveralls.io/repos/github/xguse/snaketools/badge.svg?branch=master
        :target: https://coveralls.io/github/xguse/snaketools?branch=master
        :alt: Test Coverage Status


.. image:: https://pyup.io/repos/github/xguse/snaketools/shield.svg
     :target: https://pyup.io/repos/github/xguse/snaketools/
     :alt: Updates


Small library of helper tools for setting up, graphing, and working with Snakemake rules.


* Free software: MIT license
* Documentation: https://snaketools.readthedocs.io.


Features
--------

- ``SnakeRun`` object to initialize and manage information common to the whole run, such as:
    - a copy of the config values from the config file provided to ``snakemake``.
    - a place to store global variables needed throughout the run.
    - more

- ``SnakeRule`` object to manage the initialization and deployment of rule-specific information including:
    - the rule name
    - a default out directory deduced from the SnakeRun object
    - a default log file path
    - a "pretty name" for the rule to be displayed in the DAG graphs.
    - attributes that store the input, output, and params values for later use.
    - a copy of the values specific to this rule from the original configuration file.
    - more

- ``recode_graph`` function that cleans up the default output of ``snakemake --dag`` and allows the use of pretty names stored in the ``SnakeRule`` objects.

Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
