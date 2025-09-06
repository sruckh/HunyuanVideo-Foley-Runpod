#!/usr/bin/env python3
"""
Model setup and download utilities for HunyuanVideo-Foley
"""

import os
import sys
from pathlib import Path
from huggingface_hub import snapshot_download
import subprocess

def download_models():
    """Download required models from Hugging Face"""
    
    print("🎯 Starting model download process...")
    
    # Create models directory
    models_dir = Path("/app/models")
    models_dir.mkdir(exist_ok=True)
    
    try:
        # Download HunyuanVideo-Foley model
        print("⬇️ Downloading tencent/HunyuanVideo-Foley model...")
        snapshot_download(
            repo_id="tencent/HunyuanVideo-Foley",
            local_dir=str(models_dir / "HunyuanVideo-Foley"),
            local_dir_use_symlinks=False
        )
        print("✅ HunyuanVideo-Foley model downloaded successfully")
        
        # Set environment variable
        model_path = str(models_dir / "HunyuanVideo-Foley")
        os.environ["HIFI_FOLEY_MODEL_PATH"] = model_path
        print(f"📝 Set HIFI_FOLEY_MODEL_PATH={model_path}")
        
        return model_path
        
    except Exception as e:
        print(f"❌ Model download failed: {str(e)}")
        return None

def install_flash_attention():
    """Install flash-attention for performance optimization"""
    
    print("⚡ Installing flash-attention...")
    
    try:
        # Install flash-attention from pre-built wheel
        wheel_url = "https://github.com/Dao-AILab/flash-attention/releases/download/v2.8.3/flash_attn-2.8.3+cu12torch2.8cxx11abiFALSE-cp310-cp310-linux_x86_64.whl"
        
        result = subprocess.run([
            "pip", "install", wheel_url
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Flash-attention installed successfully")
            return True
        else:
            print(f"❌ Flash-attention installation failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Flash-attention installation error: {str(e)}")
        return False

def setup_environment():
    """Set up the complete environment"""
    
    print("🚀 Setting up HunyuanVideo-Foley environment...")
    
    # Download models
    model_path = download_models()
    if not model_path:
        print("❌ Model download failed, exiting...")
        return False
    
    # Install flash-attention
    if not install_flash_attention():
        print("⚠️  Flash-attention installation failed, continuing without it...")
    
    print("✅ Environment setup complete!")
    return True

if __name__ == "__main__":
    success = setup_environment()
    sys.exit(0 if success else 1)