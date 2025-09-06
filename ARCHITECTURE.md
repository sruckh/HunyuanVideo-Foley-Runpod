# ARCHITECTURE.md

## Tech Stack
- **Framework**: Python 3.10+, Gradio/FastAPI web interfaces
- **AI/ML Framework**: PyTorch with CUDA support
- **Model Architecture**: Tencent HunyuanVideo-Foley transformer model
- **Web Interface**: Gradio for video generation UI
- **Container Runtime**: Docker with NVIDIA GPU support
- **Cloud Platform**: RunPod GPU infrastructure
- **Model Hosting**: Hugging Face Hub for model distribution
- **Build Tools**: GitHub Actions for CI/CD, Docker Hub for image distribution

## Directory Structure
```
HunyuanVideo-Foley-RunPod/
├── Dockerfile                 # CUDA base image with system dependencies
├── docker-compose.yml         # Local development and testing configuration
├── runtime_install.sh         # Runtime dependency installation script (core mechanic)
├── gradio_app.py             # Gradio web interface for video generation (main file)
├── model_setup.py            # Hugging Face model download utilities
├── README.md                 # Project documentation and deployment guide
├── CLAUDE.md                 # AI developer guidelines
├── CONDUCTOR.md              # Documentation framework and project context
├── GOALS.md                  # Original project requirements and constraints
└── .github/
    └── workflows/
        └── docker-build.yml  # GitHub Actions CI/CD pipeline
```

## Key Architectural Decisions

### [Decision 1]: Runtime-Only Installation
**Context**: Security requirement to never install dependencies on local development servers
**Decision**: All dependencies installed at container runtime, no pre-built images with models
**Rationale**: Eliminates security risks of cached models, ensures fresh installations, allows for model updates without rebuilding
**Consequences**: Longer startup times (~10-15 minutes), no local development outside containers, simplified CI/CD

### [Decision 2]: CUDA Base Image Selection
**Context**: Need for NVIDIA GPU support with latest driver compatibility
**Decision**: Use nvidia/cuda:12.8.1-cudnn-devel-ubuntu24.04 base image
**Rationale**: Latest CUDA version ensures compatibility with Hugging Face models, Ubuntu 24.04 for modern package support, devel variant for PyTorch compilation
**Consequences**: Larger image size (~8GB), AMD64-only architecture as per requirements, GPU-only deployment model

### [Decision 3]: Model Download Strategy
**Context**: 50GB+ model files that must be downloaded securely
**Decision**: Runtime download via Hugging Face snapshot_download API
**Rationale**: Avoids storing large model files in GitHub repo, enables version control of models, automatic updates
**Consequences**: Extended container startup time, HF_TOKEN environment variable requirement, no offline deployment capability

## Component Architecture

### [HunyuanVideo-Foley] Model Component <!-- #video-model -->
```python
# Core AI model for video generation with Foley audio
class HunyuanVideoFoley:
    def __init__(self, model_path: str)
    def generate_video(self, prompt: str, duration: int) -> VideoResult
    def synthesize_audio(self, video_frames: List[Frame]) -> AudioTrack
```

### [GradioInterface] Web Interface Component <!-- #gradio-interface -->
```python
# Gradio web application for user interaction
class VideoGeneratorUI:
    def __init__(self, model: HunyuanVideoFoley)
    def create_interface(self) -> gr.Interface
    def handle_generation(self, inputs: Dict) -> Dict
```

### [RuntimeInstaller] System Setup Component <!-- #runtime-installer -->
```bash
# Bash script for complete system initialization
function install_pytorch() { ... }
function download_models() { ... }
function setup_flash_attention() { ... }
```

## System Flow Diagram
```
[User Request] → [Gradio UI] → [VideoGeneratorUI.handle_generation()]
                        ↓
                [HunyuanVideoFoley.generate_video()]
                        ↓
            [Tencent Transformer Model Processing]
                        ↓
        [PyTorch CUDA Acceleration + Flash Attention]
                        ↓
    [Video Frames + Foley Audio Synthesis Output]
                        ↓
                [Result Display in Gradio UI]
```

## Common Patterns

### [Runtime Installation Pattern]
**When to use**: Container startup and dependency management
**Implementation**: Bash script with error handling and logging
**Example**:
```bash
#!/bin/bash
set -e

echo "Installing PyTorch with CUDA..."
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

echo "Cloning HunyuanVideo-Foley..."
git clone https://github.com/Tencent-Hunyuan/HunyuanVideo-Foley

echo "Downloading models..."
python3 -c "from huggingface_hub import snapshot_download; snapshot_download('tencent/HunyuanVideo-Foley', local_dir='/app/models')"
```

### [Model Caching Pattern]
**When to use**: Large model file management and GPU memory optimization
**Implementation**: Environment variable configuration and container volumes
**Example**:
```yaml
environment:
  - HIFI_FOLEY_MODEL_PATH=/app/models/HunyuanVideo-Foley
volumes:
  - ./models:/app/models:cached
```

## Keywords <!-- #keywords -->
- architecture
- containerization
- AI
- video generation
- CUDA
- PyTorch
- runtime installation
- Hugging Face
- Gradio
- RunPod