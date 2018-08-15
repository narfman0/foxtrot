.DEFAULT_GOAL := run

init:
	pipenv install

run:
	pipenv run python -m foxtrot.app
