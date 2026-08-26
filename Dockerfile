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
    apt-get update && apt-get install -y libgl1 libglib2.0-0 curl wget

# Copy ML requirements first to leverage Docker layer caching
COPY backend/requirements-ml.txt /app/
# Split into batches to prevent Out Of Memory (OOM) crashes during Docker build on low-RAM servers
RUN pip install --no-cache-dir --default-timeout=100 --extra-index-url https://download.pytorch.org/whl/cpu torch torchvision onnx onnxruntime
RUN pip install --no-cache-dir --default-timeout=100 transformers diffusers accelerate huggingface_hub
RUN pip install --no-cache-dir --default-timeout=100 opencv-python-headless opencv-contrib-python-headless mediapipe
RUN pip install --no-cache-dir --default-timeout=100 -r requirements-ml.txt

# Copy standard requirements
COPY backend/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY backend/ /app/

# Collect static files for production
RUN python manage.py collectstatic --noinput

# Expose both ports (Traefik fallback)
EXPOSE 80 8080

# Start Gunicorn WSGI server
CMD ["/bin/bash", "-c", "python manage.py migrate && gunicorn config.wsgi:application --bind 0.0.0.0:80 --bind 0.0.0.0:8080 --workers 1 --access-logfile -"]
