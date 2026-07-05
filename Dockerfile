FROM python:3.14-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app/src

COPY src/ ./src/

CMD ["python", "-m", "flaskboard.script"]
