# CONFIG.md

## Runtime Configuration

### Required Environment Variables

#### Model Configuration
```bash
# Required: Path where models are downloaded (default: /app/models)
HIFI_FOLEY_MODEL_PATH=/app/models/HunyuanVideo-Foley

# Optional: Hugging Face authentication token for private models
HF_TOKEN=hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Required: GPU device selection (0-based indexing)
CUDA_VISIBLE_DEVICES=0
```

#### Gradio Interface Settings
```bash
# Optional: Gradio sharing token (default: disabled)
GRADIO_SHARE=false

# Optional: Gradio server port (default: 7860)
GRADIO_SERVER_PORT=7860

# Optional: Gradio server host (default: 0.0.0.0)
GRADIO_SERVER_NAME=0.0.0.0

# Optional: Enable Gradio debug mode (default: false)
GRADIO_DEBUG=false
```

#### Application Settings
```bash
# Optional: Maximum video length in seconds (default: 30)
MAX_VIDEO_DURATION=30

# Optional: Video output format (default: mp4)
VIDEO_FORMAT=mp4

# Optional: Audio sample rate (default: 44100)
AUDIO_SAMPLE_RATE=44100

# Optional: Enable model caching (default: true)
MODEL_CACHE_ENABLED=true
```

## Development Environment Variables

### Local Development
```bash
# Enable development mode
DEVELOPMENT_MODE=true

# Log level (DEBUG, INFO, WARNING, ERROR)
LOG_LEVEL=DEBUG

# Temporary file cleanup interval (seconds)
CLEANUP_INTERVAL=3600
```

### GPU Settings
```bash
# CUDA memory fraction (0.0-1.0, default: 0.9)
CUDA_MEMORY_FRACTION=0.9

# Enable CUDA memory pool
CUDA_MEMORY_POOL=true

# TensorRT optimization flag
TRT_ENABLED=false
```

## Feature Flags

### Model Features
```bash
# Enable Flash Attention optimization (default: true)
FLASH_ATTENTION_ENABLED=true

# Enable model quantization (default: false)
QUANTIZATION_ENABLED=false

# Enable model compilation (default: false)
TORCH_COMPILE_ENABLED=false
```

### Interface Features
```bash
# Enable advanced video controls (default: true)
ADVANCED_CONTROLS_ENABLED=true

# Enable batch processing (default: false)
BATCH_PROCESSING_ENABLED=false

# Enable custom model prompts (default: true)
CUSTOM_PROMPTS_ENABLED=true
```

### Debugging Features
```bash
# Enable performance profiling (default: false)
PROFILING_ENABLED=false

# Enable model validation (default: true)
VALIDATION_ENABLED=true

# Enable error reporting (default: false)
ERROR_REPORTING_ENABLED=false
```

## Application Configuration Constants

### Video Generation Settings
```python
# Maximum concurrent requests
MAX_CONCURRENT_REQUESTS = 1

# Video quality settings
VIDEO_QUALITY = {
    "resolution": "720x480",
    "fps": 30,
    "bitrate": "2000k"
}

# Supported audio formats
SUPPORTED_AUDIO_FORMATS = ["wav", "mp3", "aac"]

# Model timeout settings (seconds)
MODEL_LOAD_TIMEOUT = 300
VIDEO_GENERATION_TIMEOUT = 600
```

### System Limits
```python
# Memory limits (MB)
GPU_MEMORY_LIMIT = 8192
CPU_MEMORY_LIMIT = 4096

# Storage limits (GB)
MODEL_STORAGE_LIMIT = 100
OUTPUT_STORAGE_LIMIT = 50
TEMP_STORAGE_LIMIT = 10
```

### Performance Settings
```python
# PyTorch settings
TORCH_NUM_THREADS = 4
TORCH_CUDA_ALLOC_CONF = "max_split_size_mb:512"

# Gradio settings
GRADIO_MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB
GRADIO_QUEUE_MAX_SIZE = 10
GRADIO_QUEUE_CONCURRENCY_COUNT = 1
```

## Security Configuration

### Authentication
```bash
# API key for external integrations
API_KEY=your_secure_api_key_here

# Enable external authentication
EXTERNAL_AUTH_ENABLED=false

# Authentication timeout (seconds)
AUTH_TIMEOUT=3600
```

### Model Security
```bash
# Enable model validation
MODEL_VALIDATION_ENABLED=true

# Checksum verification
CHECKSUM_VALIDATION_ENABLED=true

# Secure model download
SECURE_DOWNLOAD_ENABLED=true
```

### Network Security
```bash
# Allowed origins for CORS
ALLOWED_ORIGINS=["http://localhost:7860", "https://your-domain.com"]

# Rate limiting (requests per minute)
RATE_LIMIT_REQUESTS=10
RATE_LIMIT_WINDOW=60

# SSL/TLS enforcement
SSL_ENABLED=false
SSL_CERT_PATH=/path/to/ssl/cert
SSL_KEY_PATH=/path/to/ssl/key
```

## Common Patterns for Configuration Changes

### Environment Override Pattern
```bash
# Pattern for overriding defaults with environment variables
def get_config_value(key: str, default: Any) -> Any:
    return os.environ.get(f"HIFI_{key}", default)
```

### Feature Flag Pattern
```bash
# Pattern for conditional feature activation
def is_feature_enabled(feature_name: str) -> bool:
    env_var = f"{feature_name.upper()}_ENABLED"
    return os.environ.get(env_var, "false").lower() == "true"
```

### Configuration Validation Pattern
```python
# Pattern for validating configuration values
def validate_config(config: Dict) -> Dict:
    validated = {}
    for key, value in config.items():
        if key in REQUIRED_CONFIGS and not value:
            raise ValueError(f"Required configuration missing: {key}")
        validated[key] = value
    return validated
```

## Docker Configuration Overrides

### Docker Compose Overrides
```yaml
# docker-compose.override.yml for development
version: '3.8'
services:
  hunyuanvideo-foley:
    environment:
      - DEVELOPMENT_MODE=true
      - LOG_LEVEL=DEBUG
      - PROFILING_ENABLED=true
    volumes:
      - ./outputs:/app/outputs
      - ./logs:/app/logs
```

### Conditional Configuration
```python
# PyTorch optimizations for different environments
if os.environ.get("DEVELOPMENT_MODE") == "true":
    torch.set_num_threads(1)  # Single thread for debugging
else:
    torch.set_num_threads(multiprocessing.cpu_count())

# Memory optimizations
if torch.cuda.is_available():
    torch.cuda.set_per_process_memory_fraction(
        float(os.environ.get("CUDA_MEMORY_FRACTION", "0.9"))
    )
```

## Keywords <!-- #keywords -->
- configuration
- environment variables
- feature flags
- runtime settings
- docker
- security
- validation
- performance