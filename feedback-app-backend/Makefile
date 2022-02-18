PYTHON = python3
POETRY = poetry run

setup:
	${PYTHON} -m pip install poetry

install:
	poetry install

sort:
	${POETRY} isort .

format:
	${POETRY} black .

lint:
	${POETRY} flake8

tidy: sort format lint

test:
	${POETRY} pytest

run-local:
	${POETRY} uvicorn app.main:app --reload --port 7000