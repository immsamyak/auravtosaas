FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_ENV production
ENV HF_HOME /app/models
ENV TORCH_HOME /app/models

# Set work directory
WORKDIR /app

# Install system dependencies (Required for MediaPipe)
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update && apt-get install -y libgl1 libglib2.0-0

# Copy ML requirements first to leverage Docker layer caching
COPY backend/requirements-ml.txt /app/
# Use Docker BuildKit cache to drastically speed up pip installs across rebuilds
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --default-timeout=100 -r requirements-ml.txt

# Copy standard requirements
COPY backend/requirements.txt /app/
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt

# Copy project files
COPY backend/ /app/

# Collect static files for production
RUN python manage.py collectstatic --noinput

# Expose port (Matches Coolify Traefik routing)
EXPOSE 8080

# Start Gunicorn WSGI server
# Migrations are removed to prevent crash loops from corrupted database schemas
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8080", "--workers", "1"]
