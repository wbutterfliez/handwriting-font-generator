FROM python:3.11-slim

# Install system dependencies (fontforge, potrace, cairo, etc.)
RUN apt-get update && apt-get install -y \
    fontforge \
    potrace \
    libcairo2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-0 \
    libgtk-3-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy project
WORKDIR /app
COPY . .

# Install python deps
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 5000

# Run Flask app
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
