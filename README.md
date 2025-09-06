# HunyuanVideo-Foley-RunPod

AI-powered video generation with synchronized Foley sound effects, containerized for RunPod deployment.

## ⚡ Quick Start

### On RunPod
1. Deploy the container: `gemneye/hunyuanvideo-foley-runpod:latest`
2. Port: 7860
3. GPU: Required (NVIDIA recommended)
4. Access: `http://your-runpod-url:7860`

### Local Development
```bash
# Build and run locally (requires CUDA)
docker compose up --build

# Access at http://localhost:7860
```

## 🏗️ Architecture

- **Base Image**: `nvidia/cuda:12.8.1-cudnn-devel-ubuntu24.04`
- **Runtime Installation**: All dependencies installed at container startup
- **Model**: Tencent HunyuanVideo-Foley (`tencent/HunyuanVideo-Foley` from Hugging Face)
- **Web Interface**: Gradio-based UI for video generation
- **Platform**: AMD64 only (as per requirements)

## 📋 Requirements

- **GPU**: NVIDIA GPU with CUDA support
- **RAM**: Minimum 16GB
- **Storage**: 50GB+ for models and generated content
- **Platform**: Linux (RunPod deployment)

## 🚀 How It Works

1. **Runtime Setup**: Container installs all dependencies when started (PyTorch, Hugging Face Hub, etc.)
2. **Model Download**: Downloads HunyuanVideo-Foley model from Hugging Face
3. **Flash Attention**: Installs optimized attention layers for performance
4. **Gradio Interface**: Launches web UI for video generation with audio

## 🛠️ Technical Details

### Runtime Installation Steps
1. Install PyTorch with CUDA support
2. Clone and set up HunyuanVideo-Foley repository
3. Download models from Hugging Face
4. Set up environment variables
5. Install Flash Attention
6. Launch Gradio application

### Environment Variables
- `HIFI_FOLEY_MODEL_PATH`: Path to downloaded models
- `HF_TOKEN`: Optional Hugging Face token for private models
- `CUDA_VISIBLE_DEVICES`: GPU device selection

### Port Configuration
- **Gradio Web UI**: 7860

## 🔐 Security Notes

- No hardcoded secrets or API keys
- All sensitive data handled through environment variables
- Models downloaded at runtime when container starts
- No persistent storage of credentials

## 📂 Project Structure

```
/opt/docker/HunyuanVideo-Foley-RunPod/
├── Dockerfile                 # CUDA base image with system deps
├── docker-compose.yml         # Local development setup
├── runtime_install.sh         # Runtime dependency installation
├── gradio_app.py             # Gradio web interface
├── model_setup.py            # Model download utilities
├── README.md                 # This file
├── .github/
│   └── workflows/
│       └── docker-build.yml  # GitHub Actions CI/CD
└── GOALS.md                  # Original project requirements
```

## 🐳 Docker Information

- **Repository**: `gemneye/hunyuanvideo-foley-runpod`
- **Base Image**: `nvidia/cuda:12.8.1-cudnn-devel-ubuntu24.04`
- **GPU Requirements**: CUDA-compatible NVIDIA GPU
- **Ports**: 7860 (Gradio web interface)

## 🤝 Contributing

This project containerizes the original [Tencent HunyuanVideo-Foley](https://github.com/Tencent-Hunyuan/HunyuanVideo-Foley) for cloud deployment.

### Development Guidelines
- Never install dependencies on local server
- All setup happens at runtime in containers
- No persistent secrets or credentials
- AMD64 architecture only
- GitHub builds container, RunPod deploys it

## 📄 License

Follows the same license as the original [HunyuanVideo-Foley project](https://github.com/Tencent-Hunyuan/HunyuanVideo-Foley).

## 🙏 Acknowledgments

- [Tencent HunyuanVideo-Foley](https://github.com/Tencent-Hunyuan/HunyuanVideo-Foley) - Original AI video generation project
- [RunPod](https://runpod.io) - Cloud GPU platform for deployment
- [Hugging Face](https://huggingface.co) - Model hosting and distribution