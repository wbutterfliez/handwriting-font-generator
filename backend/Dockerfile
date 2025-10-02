FROM python:3.11-slim

ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y \
    fontforge \
    potrace \
    libgl1 \
    libgomp1 \
    libsm6 \
    libxrender1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD gunicorn app:app --bind 0.0.0.0:$PORT