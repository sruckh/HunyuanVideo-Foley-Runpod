# BUILD.md

## Prerequisites
- **Docker**: Version 24.0+ installed locally
- **NVIDIA GPU**: With CUDA 12.1+ drivers for local development
- **Git**: For version control
- **SSH Keys**: Configured for GitHub authentication
- **GitHub Account**: With access to sruckh/HunyuanVideo-Foley-Runpod
- **Docker Hub Account**: For image distribution (gemneye)
- **RunPod Account**: For cloud GPU deployment

## Environment Setup

### Local Development
```bash
# Clone the repository
git clone git@github.com:sruckh/HunyuanVideo-Foley-Runpod.git
cd HunyuanVideo-Foley-RunPod

# Set up SSH keys for GitHub (if not already configured)
ssh-keygen -t ed25519 -C "your_email@example.com"
# Add public key to GitHub account

# Optional: Set Hugging Face token for model downloads
export HF_TOKEN=your_huggingface_token
```

### Development Tools
- **Docker Desktop**: With NVIDIA GPU support enabled
- **VS Code**: With Docker extension for container management
- **GitHub Desktop**: For version control workflow
- **NVIDIA Container Toolkit**: For GPU passthrough in containers

## Build Commands

### Local Development Build
```bash
# Build the container locally (without models)
docker build -t hunyuanvideo-foley-runpod:dev .

# Run with local GPU
docker run --gpus all \
  -p 7860:7860 \
  -e HF_TOKEN=${HF_TOKEN:-} \
  -v ./models:/app/models \
  -v ./outputs:/app/outputs \
  hunyuanvideo-foley-runpod:dev

# Access at http://localhost:7860
```

### Production Build
```bash
# Tag for Docker Hub upload
docker tag hunyuanvideo-foley-runpod:dev gemneye/hunyuanvideo-foley-runpod:latest

# Push to Docker Hub (requires authentication)
docker push gemneye/hunyuanvideo-foley-runpod:latest
```

### Multi-Architecture Build (GitHub Actions)
The CI/CD pipeline automatically handles:
- AMD64 architecture builds only (as per requirements)
- CUDA compatibility validation
- Model download verification (no models included)
- Security scanning for dependencies

## CI/CD Pipeline

### GitHub Actions Workflow
```yaml
# .github/workflows/docker-build.yml
name: Build and Push Docker Image
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: actions/setup-docker-buildx@v3

      - name: Log in to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}

      - name: Build and push Docker image
        uses: docker/build-push-action@v5
        with:
          context: .
          platforms: linux/amd64
          push: true
          tags: gemneye/hunyuanvideo-foley-runpod:latest
```

## Deployment

### RunPod Deployment
1. **Create RunPod Pod**:
   - Select NVIDIA GPU with 16GB+ RAM
   - Choose Ubuntu base image
   - Allocate 50GB+ storage
   - Open ports: 7860 (TCP)

2. **Deploy Container**:
   ```bash
   # From RunPod terminal
   docker run -d --gpus all \
     -p 7860:7860 \
     --name hunyuanvideo-foley \
     gemneye/hunyuanvideo-foley-runpod:latest
   ```

3. **Environment Configuration**:
   ```bash
   # Set environment variables in RunPod
   HF_TOKEN=your_huggingface_token
   HIFI_FOLEY_MODEL_PATH=/app/models/HunyuanVideo-Foley
   CUDA_VISIBLE_DEVICES=0
   ```

4. **Access Application**:
   - Open browser to: `http://your-runpod-url:7860`
   - Wait 10-15 minutes for initial model download and setup

### Local Development
1. **Start Services**:
   ```bash
   docker-compose up --build
   ```

2. **Verify GPU Access**:
   ```bash
   docker run --gpus all nvidia/cuda:12.8.1-base nvidia-smi
   ```

3. **Monitor Startup**:
   ```bash
   # Watch container logs during initialization
   docker-compose logs -f hunyuanvideo-foley
   ```

## Rollback Procedures

### Emergency Rollback (RunPod)
```bash
# Stop current container
docker stop hunyuanvideo-foley

# Remove container
docker rm hunyuanvideo-foley

# Pull previous version
docker pull gemneye/hunyuanvideo-foley-runpod:previous-version

# Restart with previous version
docker run -d --gpus all -p 7860:7860 gemneye/hunyuanvideo-foley-runpod:previous-version
```

### Git Rollback
```bash
# Revert to previous commit
git log --oneline
git revert <commit-hash>

# Force push updated version
git push origin main --force
```

## Troubleshooting

### Build Failures
**Issue**: CUDA version incompatibility
**Solution**: Use nvidia/cuda:12.8.1-cudnn-devel-ubuntu24.04 base image

**Issue**: Model download timeout
**Solution**: Increase timeout in Hugging Face client or use HF_TOKEN for authenticated downloads

**Issue**: GPU memory allocation errors
**Solution**: Ensure NVIDIA Container Toolkit is properly installed and configured

### Runtime Issues
**Issue**: Container fails to start
**Solution**:
```bash
docker-compose logs hunyuanvideo-foley
# Check for Python dependency conflicts or network timeouts
```

**Issue**: Model download fails
**Solution**: Verify HF_TOKEN environment variable and check Hugging Face rate limits

**Issue**: CUDA out of memory
**Solution**: Increase GPU memory allocation or reduce model complexity

### Deployment Issues
**Issue**: RunPod GPU not detected
**Solution**: Ensure --gpus all flag is used and NVIDIA drivers are installed

**Issue**: Port 7860 already in use
**Solution**: Change port mapping in docker run command or stop conflicting service

**Issue**: Model files too large for storage
**Solution**: Use larger storage allocation (50GB+ recommended) or external storage mount

## Keywords <!-- #keywords -->
- build
- docker
- deployment
- ci/cd
- cuda
- gpu
- huggingface
- runpod
- containerization
- ai models