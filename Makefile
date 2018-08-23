.DEFAULT_GOAL := run

clean: clean-build clean-pyc

clean-build:
	rm -fr build/ dist/ *.log
	rm -fr *.egg-info *.spec

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

init:
	pipenv install

init-dev:
	pipenv install -d

run:
	pipenv run python -m foxtrot.app

run-test:
	pipenv run pytest --cov=foxtrot --cov-report term-missing --pylint

test: init-dev run-test
t: run-test
