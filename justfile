default:
    just --list

serve:
    uv run manage.py runserver

# Run tests
test *args:
    uv run manage.py test
