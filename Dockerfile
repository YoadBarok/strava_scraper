FROM python:3.12.4 AS builder

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1
WORKDIR /app

RUN python -m venv venv
COPY requirements.txt ./
RUN venv/bin/pip install --no-cache-dir -r requirements.txt

FROM python:3.12.4-slim
WORKDIR /app
COPY --from=builder /app/venv venv/
COPY . .

WORKDIR /app/src

CMD ["/app/venv/bin/gunicorn", "server:app", "-c", "gunicorn.config.py"]
