# Use Python 3.8 with Debian Buster
FROM python:3.8-buster

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1-mesa-glx \
    libglib2.0-0 \
    ffmpeg \
    libsm6 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip, setuptools, and wheel
RUN python -m pip install --no-cache-dir --upgrade pip setuptools wheel

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Ensure model directory exists before copying
RUN mkdir -p /app/models

# Copy application code
COPY . .

# Copy YOLO model and PaddleOCR models
COPY models/best.pt /app/models/best.pt
COPY models/en_PP-OCRv3_det_infer /app/models/en_PP-OCRv3_det_infer
COPY models/en_PP-OCRv3_rec_infer /app/models/en_PP-OCRv3_rec_infer
COPY models/ch_ppocr_mobile_v2.0_cls_infer /app/models/ch_ppocr_mobile_v2.0_cls_infer

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose Django’s default port
EXPOSE 8000

# Start Django application with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "basic.wsgi:application"]
