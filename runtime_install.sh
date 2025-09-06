#!/bin/bash

# HunyuanVideo-Foley-Runpod Runtime Installation Script
# This script runs at container startup to install everything at runtime

set -e

echo "🚀 Starting HunyuanVideo-Foley Runtime Installation..."

# 1. Install PyTorch (match GOALS.md requirements: PyTorch 2.8 for Flash Attention compatibility)
echo "📦 Installing PyTorch..."
pip3 install torch==2.5.1+cu121 torchvision --index-url https://download.pytorch.org/whl/cu121 --break-system-packages

# 2. Clone repository
echo "📥 Cloning HunyuanVideo-Foley repository..."
git clone https://github.com/Tencent-Hunyuan/HunyuanVideo-Foley
cd HunyuanVideo-Foley

# 3. Install requirements
echo "📋 Installing requirements..."
pip install -r requirements.txt --break-system-packages

# 4. Clone model repository (handle existing directories)
echo "🎯 Downloading model from Hugging Face..."
if [ ! -d "HunyuanVideo-Foley" ]; then
    git clone https://huggingface.co/tencent/HunyuanVideo-Foley
else
    echo "📁 Model repository already exists, skipping clone..."
fi

# Use hf to download the model (install hf first)
echo "🔧 Installing huggingface_hub CLI..."
pip install "huggingface_hub[cli]" --break-system-packages

# Download the model using hf
echo "⬇️ Downloading tencent/HunyuanVideo-Foley model..."
python3 -c "
import os
from huggingface_hub import snapshot_download
try:
    snapshot_download(repo_id='tencent/HunyuanVideo-Foley', local_dir='./pretrained_models', local_dir_use_symlinks=False)
    print('✅ Model downloaded successfully')
except Exception as e:
    print(f'❌ Failed to download model: {e}')
    exit(1)
"

# 5. Set model environment variable
export HIFI_FOLEY_MODEL_PATH=/app/HunyuanVideo-Foley/HunyuanVideo-Foley
echo "📝 Model path set to: $HIFI_FOLEY_MODEL_PATH"

# 6. Install flash_attn (Python 3.12 compatibility)
echo "⚡ Installing flash-attention..."
pip install https://github.com/Dao-AILab/flash-attention/releases/download/v2.8.3/flash_attn-2.8.3+cu12torch2.8cxx11abiFALSE-cp312-cp312-linux_x86_64.whl --break-system-packages

# 7. Return to app directory
cd /app

# 8. Launch the gradio app
echo "🚀 Launching Gradio application..."
python3 gradio_app.py