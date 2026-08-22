FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_ENV production

# Set work directory
WORKDIR /app

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
# Note: Database migrations will be handled via Coolify Pre-Deployment Hook
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8080", "--workers", "3"]
