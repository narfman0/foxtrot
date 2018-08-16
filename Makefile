.DEFAULT_GOAL := run

init:
	pipenv install

init-dev:
	pipenv install -d

run:
	pipenv run python -m foxtrot.app

test:
	pipenv run pytest --cov=foxtrot --cov-report term-missing --pylint
