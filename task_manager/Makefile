dev:
	uv run python3 manage.py runserver

translate:
	uv run django-admin makemessages -a
	uv run python manage.py compilemessages

migr:
	uv run python3 manage.py makemigrations
	uv run python3 manage.py migrate

tests:
	uv run python3 manage.py test