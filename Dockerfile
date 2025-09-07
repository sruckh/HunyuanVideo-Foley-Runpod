FROM nvidia/cuda:12.1.1-cudnn8-runtime-ubuntu22.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    git \
    wget \
    curl \
    build-essential \
    && /usr/bin/python3 -m pip install --upgrade pip \
    && rm -rf /var/lib/apt/lists/*

# Create working directory
WORKDIR /app

# Copy runtime installation script
COPY runtime_install.sh /app/runtime_install.sh
COPY gradio_app.py /app/gradio_app.py
COPY model_setup.py /app/model_setup.py

# Make scripts executable
RUN chmod +x /app/runtime_install.sh

# Expose port for Gradio
EXPOSE 7860

# Set up entrypoint to run everything at runtime
ENTRYPOINT ["/app/runtime_install.sh"]