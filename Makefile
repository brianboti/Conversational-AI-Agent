.POSIX:

run:
	ENVFILE=.env . ./.env || true; PYTHONPATH=src FLASK_APP=wsgi.py flask run --host=0.0.0.0 --port=8080

serve:
	PYTHONPATH=src gunicorn -c gunicorn.conf.py wsgi:app

fmt:
	ruff check --fix .
	black .

typecheck:
	mypy src

test:
	pytest -q

docker-build:
	docker build -t callbot:latest .

docker-run:
	docker run -p 8080:8080 --env-file .env callbot:latest
