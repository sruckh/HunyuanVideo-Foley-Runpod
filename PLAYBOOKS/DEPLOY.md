# DEPLOY.md - Operational Playbooks

## Overview
Step-by-step procedures for deploying the HunyuanVideo-Foley containerized application to cloud GPU infrastructure.

## Prerequisites
- ✅ Docker Hub account (gemneye)
- ✅ RunPod account with billing enabled
- ✅ SSH keys configured for GitHub access
- ✅ NVIDIA GPU availability (local or cloud)
- ✅ Stable internet connection (50GB+ download for models)

## Deployment Options

### Option 1: RunPod Cloud Deployment (Recommended)

#### Pre-deployment checklist:
- [ ] Verify Docker Hub image availability (`gemneye/hunyuanvideo-foley-runpod:latest`)
- [ ] Confirm RunPod account has sufficient credits (~$0.50/hour)
- [ ] Check Hugging Face token validity (if using private models)
- [ ] Ensure target region has GPU availability
- [ ] Verify firewall allows port 7860

#### Step-by-step deployment:

1. **Create RunPod Pod**
   ```bash
   # Access RunPod dashboard
   # Navigate: Pods → Create Pod
   ```

2. **Configure Pod Specifications**
   ```
   Template: Custom
   Base Image: Ubuntu 22.04
   GPU: NVIDIA RTX A4000 or higher (16GB+ VRAM)
   vCPUs: 4 cores minimum
   RAM: 16GB minimum
   Storage: 50GB+ SSD
   Ports: TCP 7860 (add to firewall rules)
   ```

3. **Deploy Container**
   ```bash
   # From RunPod terminal or SSH
   docker run -d --gpus all \
     --name hunyuanvideo-foley \
     -p 7860:7860 \
     --restart unless-stopped \
     -e HF_TOKEN=your_huggingface_token \
     gemneye/hunyuanvideo-foley-runpod:latest
   ```

4. **Monitor Startup Process**
   ```bash
   # Watch logs during initial setup
   docker logs -f hunyuanvideo-foley
   ```

5. **Verify Deployment**
   ```bash
   # Check container status
   docker ps

   # Verify web interface
   curl -I http://localhost:7860/

   # Monitor GPU usage
   nvidia-smi
   ```

6. **Access Application**
   ```
   URL: https://[runpod-instance].runpod.net:7860
   Expected startup time: 10-15 minutes (model download)
   ```

### Option 2: Local Development Deployment

#### Pre-deployment checklist:
- [ ] NVIDIA GPU with CUDA 12.1+ drivers
- [ ] Docker Desktop with GPU support enabled
- [ ] 16GB+ system RAM
- [ ] 50GB+ available disk space
- [ ] Port 7860 available

#### Step-by-step deployment:

1. **Prepare Environment**
   ```bash
   # Install NVIDIA Container Toolkit (Ubuntu)
   sudo apt-get update
   sudo apt-get install -y nvidia-docker2
   sudo systemctl restart docker

   # Verify GPU access
   docker run --rm --gpus all nvidia/cuda:12.8.1-base nvidia-smi
   ```

2. **Build and Deploy**
   ```bash
   # Clone repository
   git clone git@github.com:sruckh/HunyuanVideo-Foley-Runpod.git
   cd HunyuanVideo-Foley-RunPod

   # Build container
   docker build -t hunyuanvideo-foley:local .

   # Run with local GPU
   docker run --gpus all \
     -p 7860:7860 \
     -v ./models:/app/models \
     -v ./outputs:/app/outputs \
     hunyuanvideo-foley:local
   ```

3. **Verify Local Deployment**
   ```bash
   # Check GPU utilization
   docker stats

   # Access application
   open http://localhost:7860
   ```

### Option 3: Docker Compose Deployment

#### Pre-deployment checklist:
- [ ] docker-compose.yml configured correctly
- [ ] Environment variables set (optional HF_TOKEN)
- [ ] Local volumes created (`models/`, `outputs/`)

#### Step-by-step deployment:

1. **Environment Setup**
   ```bash
   # Create required directories
   mkdir -p models outputs

   # Set optional environment variables
   export HF_TOKEN=your_huggingface_token
   ```

2. **Deploy with Docker Compose**
   ```bash
   # Start services
   docker-compose up --build

   # Run in background
   docker-compose up -d --build
   ```

3. **Verify Deployment**
   ```bash
   # Check service status
   docker-compose ps

   # View logs
   docker-compose logs -f hunyuanvideo-foley
   ```

## Post-deployment Verification

### Health Checks
```bash
# Container status
docker ps | grep hunyuanvideo-foley

# GPU utilization
nvidia-smi

# Web interface response
curl -s http://localhost:7860/ | head -10
```

### Application Readiness
- [ ] Gradio interface loads successfully
- [ ] Model initialization completes (no errors in logs)
- [ ] GPU memory allocation successful
- [ ] Video generation test successful

### Performance Validation
```bash
# Monitor resource usage during generation
docker stats

# Check GPU memory usage
nvidia-smi --query-gpu=memory.used,memory.free --format=csv

# Verify generation performance
time curl -X POST http://localhost:7860/gradio_api/call/generate_video
```

## Troubleshooting

### Common Deployment Issues

#### Container Won't Start
```bash
# Check Docker logs
docker logs hunyuanvideo-foley

# Verify GPU availability
docker run --rm --gpus all nvidia/cuda:12.8.1-base nvidia-smi

# Check port conflicts
netstat -an | grep 7860
```

#### Model Download Failures
```bash
# Verify HF_TOKEN
echo $HF_TOKEN

# Check Hugging Face API status
curl -s https://huggingface.co/api/status

# Manual model download test
python3 -c "from huggingface_hub import snapshot_download; snapshot_download('tencent/HunyuanVideo-Foley')"
```

#### GPU Memory Issues
```bash
# Check available GPU memory
nvidia-smi --query-gpu=memory.free --format=csv,noheader,nounits

# Restart with lower memory usage (not recommended)
docker run --gpus all --memory=8g gemneye/hunyuanvideo-foley-runpod:latest
```

#### Network Connectivity
```bash
# Test internet connectivity
curl -s https://huggingface.co

# Check DNS resolution
nslookup huggingface.co

# Verify firewall settings
ufw status
```

## Rollback Procedures

### Emergency Rollback
```bash
# Stop current container
docker stop hunyuanvideo-foley

# Remove failed container
docker rm hunyuanvideo-foley

# Deploy previous version
docker run -d --gpus all \
  -p 7860:7860 \
  -e HF_TOKEN=$HF_TOKEN \
  gemneye/hunyuanvideo-foley-runpod:v1.0.0
```

### Git-based Rollback
```bash
# Identify last stable commit
git log --oneline

# Revert to previous version
git checkout [previous-commit-hash]

# Rebuild and redeploy
docker build -t hunyuanvideo-foley:rollback .
docker run --gpus all -p 7860:7860 hunyuanvideo-foley:rollback
```

## Maintenance Procedures

### Updating Models
```bash
# Pull latest image
docker pull gemneye/hunyuanvideo-foley-runpod:latest

# Stop current container
docker stop hunyuanvideo-foley

# Remove old models directory to force fresh download
docker run --rm -v $(pwd)/models:/app/models alpine rm -rf /app/models/*

# Start updated container
docker run -d --gpus all -p 7860:7860 gemneye/hunyuanvideo-foley-runpod:latest
```

### Log Management
```bash
# View real-time logs
docker logs -f hunyuanvideo-foley

# Export logs for analysis
docker logs hunyuanvideo-foley > deployment_logs_$(date +%Y%m%d).txt

# Clean old logs (if using log rotation)
docker run --rm -v hunyuanvideo-foley_logs:/app/logs alpine find /app/logs -name "*.log" -mtime +7 -delete
```

### Backup Procedures
```bash
# Backup generated outputs
docker run --rm -v $(pwd)/outputs:/app/outputs -v $(pwd)/backup:/backup alpine tar czf /backup/outputs_$(date +%Y%m%d).tar.gz -C /app outputs

# Backup configuration
cp docker-compose.yml docker-compose.yml.backup
cp .env .env.backup
```

## Scaling Considerations

### Vertical Scaling
- Increase GPU memory allocation
- Upgrade to better GPU models
- Add more vCPUs for parallel processing

### Horizontal Scaling
- Deploy multiple containers across pods
- Use load balancer for request distribution
- Implement queue system for batch processing

## Cost Optimization

### RunPod Cost Management
- Use spot instances for development
- Set resource limits to avoid over-provisioning
- Monitor usage patterns for optimal instance selection

### Storage Optimization
- Use compressed model formats when available
- Implement cleanup policies for temporary files
- Use external storage for large outputs

## Security Considerations

### Network Security
- Enable SSL/TLS for production deployments
- Configure firewall rules for port 7860 only
- Use VPN for accessing cloud instances

### Access Control
- Implement authentication for web interface
- Set up API keys for external integrations
- Regularly rotate Hugging Face tokens

## Keywords <!-- #keywords -->
- deployment
- runpod
- docker
- containerization
- production
- ci/cd
- dockerhub
- gpu
- cloud
- infrastructure

### Data Protection
- Encrypt sensitive model data at rest
- Use secure channels for model downloads
- Implement audit logging for access patterns