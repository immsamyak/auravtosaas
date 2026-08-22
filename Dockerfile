FROM python:3.12-slim

# Install system dependencies
# libgl1 and libglib2.0-0 are required for OpenCV and MediaPipe
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_ENV production

# Set work directory
WORKDIR /app

# Install dependencies
COPY backend/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY backend/ /app/

# Collect static files for production
RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8080

# Run migrations and start Gunicorn WSGI server
CMD ["/bin/bash", "-c", "python manage.py migrate && gunicorn config.wsgi:application --bind 0.0.0.0:8080 --workers 3"]
