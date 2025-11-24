default:
    just --list

# Run tests
test *args:
    uv run manage.py test
