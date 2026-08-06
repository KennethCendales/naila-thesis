FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    gcc \
    && pip install --no-cache-dir trac \
    && apt-get clean

RUN mkdir -p /var/trac/myproject

EXPOSE 8000

CMD ["tracd", "--port", "8000", "/var/trac/myproject"]