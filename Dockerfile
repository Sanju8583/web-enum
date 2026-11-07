FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py wsgi.py ./
COPY templates ./templates
COPY ctf.sqlite3 ./ctf.sqlite3

RUN useradd --system --uid 10001 --create-home appuser \
    && chown -R appuser:appuser /app

USER appuser

EXPOSE 5000

CMD ["waitress-serve", "--host=0.0.0.0", "--port=5000", "wsgi:app"]
