# Paths to lint/format/check (exclude Django-generated files)
paths := "lists functional_tests main.py"

# Runners
UV := "uv run"

default: 
    just --list

# Private recipe to run Django commands (uses UV runner)
_django cmd *args:
    {{UV}} manage.py {{cmd}} {{args}}

serve:
    @just _django runserver

# Run tests: e.g. `just test lists` will run unit tests for the test app
test *args:
    @just _django test {{args}}

# Create migration based on model changes 
migrations:
    @just _django makemigrations

# Apply migrations
migrate:
    @just _django migrate

# Delete data
flush:
    @just _django flush

# Run linter
lint: _ruff _isort

# Format code
format: _ruff-fix _isort-fix

# Run type check
typecheck: _mypy

# Run all static code analysis tools
check: lint typecheck

_ruff: 
    {{UV}} ruff check {{paths}}

_ruff-fix:
    {{UV}} ruff check --fix {{paths}}

_isort:
    {{UV}} isort --check-only {{paths}}

_isort-fix:
    {{UV}} isort {{paths}}

_mypy:
    {{UV}} mypy {{paths}}
