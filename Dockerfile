# syntax=docker/dockerfile:1

FROM python:3.14-slim AS builder
WORKDIR /app
COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.14-slim AS runtime
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    HOST=0.0.0.0 \
    PORT=8000
WORKDIR /app

COPY --from=builder /install /usr/local

COPY . .

EXPOSE 8000

# Simple healthcheck pinging /ready using Python stdlib (no curl)
HEALTHCHECK --interval=30s --timeout=5s --retries=3 CMD [
  "python",
  "-c",
  "import sys,urllib.request; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:8000/ready', timeout=3).status==200 else 1)"
]

CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
