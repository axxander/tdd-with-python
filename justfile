# Paths to lint/format/check (exclude Django-generated files)
paths := "lists functional_tests.py main.py"


default: 
    just --list

serve:
    uv run manage.py runserver

# Run tests
test *args:
    uv run manage.py test

migrate:
    uv run manage.py makemigrations

# Run linter
lint: _ruff _isort

# Format code
format: _ruff-fix _isort-fix

# Run type check
typecheck: _mypy

# Run all static code analysis tools
check: lint typecheck

_ruff: 
    uv run ruff check {{paths}}

_ruff-fix:
    uv run ruff check --fix {{paths}}

_isort:
    uv run isort --check-only {{paths}}

_isort-fix:
    uv run isort {{paths}}

_mypy:
    uv run mypy {{paths}}
