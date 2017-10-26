.PHONY: clean clean-test clean-pyc clean-build docs help
.DEFAULT_GOAL := help


PACKAGE_NAME = snaketools


define BROWSER_PYSCRIPT
import os, webbrowser, sys
try:
	from urllib import pathname2url
except:
	from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

#################################################################################
# COMMANDS                                                                      #
#################################################################################


## alias for show-help
help: show-help


## remove all build, test, coverage and Python artifacts
clean: clean-build clean-pyc clean-test


## remove build artifacts
clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

## remove Python file artifacts
clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

## remove test and coverage artifacts
clean-test:
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/

## remove docs artifacts
clean-docs:
	$(MAKE) -C docs clean

## check style with flake8
lint:
	flake8 $(PACKAGE_NAME) tests

## run tests quickly with the default Python
test:
	py.test

## run tests on every Python version with tox
test-all:
	tox

## check code coverage quickly with the default Python
coverage:
	coverage run --source snaketools -m pytest
	coverage report -m
	coverage html
	$(BROWSER) htmlcov/index.html

## generate Sphinx HTML documentation, including API docs
docs:
	rm -f docs/snaketools.rst
	rm -f docs/modules.rst
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	$(BROWSER) docs/_build/html/index.html

## compile the docs watching for changes
servedocs: docs
	watchmedo shell-command -p '*.rst' -c '$(MAKE) -C docs html' -R -D .

## package and upload a release
release: clean
	python setup.py sdist upload
	python setup.py bdist_wheel upload

## builds source and wheel package
dist: clean
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist



uninstall_python:
	source activate $(CONDA_ENV_NAME); \
	rm -rf $$(jupyter --data-dir)/kernels/$(CONDA_ENV_NAME); \
	rm -rf $(CONDA_ENV_DIR)


## Install Python Dependencies
requirements: test_environment
	pip install -r requirements.txt


## Delete all compiled Python files
clean_bytecode:
	find . -name "__pycache__" -type d -exec rm -r {} \; ; \
	find . -name "*.pyc" -exec rm {} \;




#################################################################################
# Self Documenting Commands                                                     #
#################################################################################

.DEFAULT_GOAL := show-help

# Inspired by <http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html>
# sed script explained:
# /^##/:
# 	* save line in hold space
# 	* purge line
# 	* Loop:
# 		* append newline + line to hold space
# 		* go to next line
# 		* if line starts with doc comment, strip comment character off and loop
# 	* remove target prerequisites
# 	* append hold space (+ newline) to line
# 	* replace newline plus comments by `---`
# 	* print line
# Separate expressions are necessary because labels cannot be delimited by
# semicolon; see <http://stackoverflow.com/a/11799865/1968>
.PHONY: show-help
## Show the available make targets
show-help:
	@echo "$$(tput bold)Available rules:$$(tput sgr0)"
	@echo
	@sed -n -e "/^## / { \
		h; \
		s/.*//; \
		:doc" \
		-e "H; \
		n; \
		s/^## //; \
		t doc" \
		-e "s/:.*//; \
		G; \
		s/\\n## /---/; \
		s/\\n/ /g; \
		p; \
	}" ${MAKEFILE_LIST} \
	| LC_ALL='C' sort --ignore-case \
	| awk -F '---' \
		-v ncol=$$(tput cols) \
		-v indent=19 \
		-v col_on="$$(tput setaf 6)" \
		-v col_off="$$(tput sgr0)" \
	'{ \
		printf "%s%*s%s ", col_on, -indent, $$1, col_off; \
		n = split($$2, words, " "); \
		line_length = ncol - indent; \
		for (i = 1; i <= n; i++) { \
			line_length -= length(words[i]) + 1; \
			if (line_length <= 0) { \
				line_length = ncol - indent - length(words[i]) - 1; \
				printf "\n%*s ", -indent, " "; \
			} \
			printf "%s ", words[i]; \
		} \
		printf "\n"; \
	}' \
	| more $(shell test $(shell uname) = Darwin && echo '--no-init --raw-control-chars')
