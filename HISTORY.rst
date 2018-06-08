**********
Change Log
**********

v0.0.8 / 2018-06-08
===================

  * stopped using pinned versions.

v0.0.7 / 2017-12-18
===================

  * change pyup check to monthly
  * update reqs from PYUP
  * snaketools: SnakeRule now registers with SnakeRun
  * snaketools: added attr SnakeRule.extra for more params
  * snaketools: added attr SnakeRun.rules
  * snaketools: use __all__ for importing from file
  * update makefile
  * update reqs

v0.0.6 / 2017-10-26
===================

  * added rewrite_snakefile_no_rules()
  * flake8
  * requirements.txt: removed dev-reqs
  * requirements.txt: pinned flake8
  * setup.py: upgraded to read from req files
  * MANIFEST.in: include req files
  * upgraded Makefile
  * tox.ini: set line-length etc
  * setup.cfg: ignore W292
  * setup.cfg: exclude lib & bin from flake8
  * updated .gitignore
  * added coveralls badge
  * HISTORY.rst: replaced header text


v0.0.5 / 2017-10-10
===================

  * requirements_dev.txt: update and pin reqs
  * flake8 fixes
  * tox.ini: simplified config
  * added flake8 to reqs

v0.0.4 / 2017-10-10
===================

  * added preliminary test suite
  * Makefile: changed `install` to use `pip install -e .`
  * added example files for testing
  * requirements.txt: created with `pipreqs`
  * snaketools.py: reorder functions
  * snaketools.py: formatting
  * ignore .vscode/
  * pin all reqs since pyup now manages

v0.0.3 / 2017-09-15
===================

  * Configure pyup
  * SnakeRun.d -> SnakeRune.interim_dir

v0.0.2 / 2017-09-06
===================

  * fixed bumpversion artifact
  * errors.py: pulls metadata from top module
  * updated dev reqs for doc building
  * activated travis ci
  * Set up flake8 configuration
  * Docs build corrected

v0.0.1 / 2017-09-06
===================

* README.rst: added prelim description of features.
* snaketools.py: fixed typo
* Initial commit
