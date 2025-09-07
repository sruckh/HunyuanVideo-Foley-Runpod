#!/bin/bash

# HunyuanVideo-Foley-Runpod Runtime Installation Script
# This script runs at container startup to install everything at runtime

set -e

echo "🚀 Starting HunyuanVideo-Foley Runtime Installation..."

# 1. Install PyTorch via requirements.txt to ensure torch 2.5 compatibility

# 2. Clone repository
echo "📥 Cloning HunyuanVideo-Foley repository..."
git clone https://github.com/Tencent-Hunyuan/HunyuanVideo-Foley
cd HunyuanVideo-Foley

# 3. Install PyTorch ecosystem with specific versions for cu121 compatibility
echo "📦 Installing PyTorch ecosystem with CUDA 12.1 consistency..."
python3 -m pip install torch==2.5.1 torchvision==0.20.1 torchaudio==2.5.1 --index-url https://download.pytorch.org/whl/cu121

# 5. Install remaining requirements
echo "📋 Installing additional requirements..."
python3 -m pip install -r requirements.txt

# 6. Clone model repository (handle existing directories)
echo "🎯 Downloading model from Hugging Face..."
if [ ! -d "HunyuanVideo-Foley" ]; then
    git clone https://huggingface.co/tencent/HunyuanVideo-Foley
else
    echo "📁 Model repository already exists, skipping clone..."
fi

# 7. Install Hugging Face CLI
echo "🔧 Installing huggingface_hub CLI..."
python3 -m pip install huggingface_hub[cli]

# 8. Download the model using hf
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

# 9. Set model environment variable
export HIFI_FOLEY_MODEL_PATH=/app/HunyuanVideo-Foley/HunyuanVideo-Foley
echo "📝 Model path set to: $HIFI_FOLEY_MODEL_PATH"

# 10. Install flash_attn (torch 2.5 compatibility with dynamic Python detection)
echo "⚡ Installing flash-attention..."
python3 -c "
import sys
python_version = f'{sys.version_info.major}{sys.version_info.minor}'
print(f'Detected Python version: {python_version}')

# Generate flash_attn URL based on detected Python version - CUDA 12.1 compatible
flash_attn_url = f'https://github.com/Dao-AILab/flash-attention/releases/download/v2.4.2/flash_attn-2.4.2+cu121torch2.5cxx11abiFALSE-cp{python_version}-cp{python_version}-linux_x86_64.whl'
print(f'Flash Attention URL: {flash_attn_url}')

import subprocess
try:
    result = subprocess.run(['python3', '-m', 'pip', 'install', flash_attn_url], capture_output=True, text=True)
    if result.returncode == 0:
        print('✅ Flash-attention installed successfully')
    else:
        print(f'❌ Installation failed: {result.stderr}')
        sys.exit(1)
except Exception as e:
    print(f'❌ Installation error: {e}')
    sys.exit(1)
"

# 11. Return to app directory
cd /app

# 12. Launch the gradio app
echo "🚀 Launching Gradio application..."
python3 gradio_app.py