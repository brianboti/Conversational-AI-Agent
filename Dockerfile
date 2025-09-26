FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1     PYTHONUNBUFFERED=1     PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc curl ca-certificates && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src ./src
COPY wsgi.py .
COPY gunicorn.conf.py .
ENV PYTHONPATH=/app/src

CMD ["gunicorn", "-c", "gunicorn.conf.py", "wsgi:app"]
