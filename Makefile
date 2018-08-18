.DEFAULT_GOAL := run

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
