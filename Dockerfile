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
# Use --no-cache-dir to prevent pip from storing massive ML wheels on the server disk
RUN pip install --no-cache-dir --default-timeout=100 -r requirements-ml.txt

# Copy standard requirements
COPY backend/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY backend/ /app/

# Collect static files for production
RUN python manage.py collectstatic --noinput

# Expose port (Matches Coolify Traefik routing)
EXPOSE 8080

# Start Gunicorn WSGI server
# Adding '|| sleep 3600' prevents the container from crashing immediately so we can read the logs if it fails!
CMD ["/bin/bash", "-c", "(python fix_db.py && python manage.py migrate && gunicorn config.wsgi:application --bind 0.0.0.0:8080 --workers 1) || sleep 3600"]
