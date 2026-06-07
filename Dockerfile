FROM python:3.11-alpine AS builder

WORKDIR /build

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip wheel setuptools jaraco.context && \
    pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.11-alpine

LABEL org.opencontainers.image.authors="Wiktor Luksik"
LABEL org.opencontainers.image.title="Pogoda - zad1"

RUN pip install --no-cache-dir --upgrade pip wheel setuptools jaraco.context

COPY --from=builder /install /usr/local

WORKDIR /pogoda-app
COPY main.py .

HEALTHCHECK --interval=30s --timeout=3s \
  CMD python -c "import requests; requests.get('http://localhost:8080/')" || exit 1

EXPOSE 8080

CMD ["python", "main.py"]