# API.md

## API Contracts

### Overview
The HunyuanVideo-Foley application provides a web interface through Gradio for video generation with synchronized audio effects. The interface is accessible via a web browser at the container's exposed port (default: 7860).

## Main Application Endpoint

### Video Generation Interface
```
METHOD: Web Interface
ENDPOINT: http://[host]:[port]/
AUTHENTICATION: None required (web interface)
PROTOCOL: HTTP via Gradio
```

#### Request Format
The interface accepts video generation prompts through the web form:

```json
{
  "video_prompt": "string (required)",
  "audio_prompt": "string (optional)",
  "duration": "number (seconds, default: 10)",
  "quality": "string (low|medium|high, default: medium)",
  "output_format": "string (mp4|webm, default: mp4)"
}
```

#### Response Format
Generated video file is downloaded directly through the web interface:

```json
{
  "status": "success|error",
  "message": "string",
  "file_url": "string (temporary download URL)",
  "duration": "number (processing time in seconds)",
  "file_size": "number (bytes)"
}
```

#### Interface Components
1. **Text Input**: Video generation prompt
2. **Number Input**: Video duration (1-30 seconds)
3. **Dropdown**: Quality preset selection
4. **Button**: Generate video
5. **Video Player**: Display generated content
6. **Download Button**: Save generated video

## Technical Details

### Request Parameters

#### Video Prompt
- **Type**: String
- **Required**: Yes
- **Constraints**: 1-500 characters
- **Description**: Natural language description of the desired video content

#### Audio Prompt (Optional)
- **Type**: String
- **Required**: No
- **Constraints**: 1-200 characters
- **Description**: Optional audio effects description to sync with video

#### Duration
- **Type**: Number
- **Required**: No
- **Constraints**: 1-30 seconds
- **Default**: 10 seconds
- **Description**: Length of generated video

#### Quality
- **Type**: String
- **Required**: No
- **Constraints**: ["low", "medium", "high"]
- **Default**: "medium"
- **Description**:
  - Low: 480p, basic compression
  - Medium: 720p, balanced quality/size
  - High: 1080p, maximum quality

#### Output Format
- **Type**: String
- **Required**: No
- **Constraints**: ["mp4", "webm"]
- **Default**: "mp4"
- **Description**: Container format for the video output

## Supported File Formats

### Input Formats
- **Text**: Plain text prompts and descriptions
- **Parameters**: JSON-structured configuration options
- **URLs**: Optional reference URLs for style guidance

### Output Formats
- **Video**: MP4 (H.264 codec), WebM (VP9 codec)
- **Audio**: Integrated within video container
- **Metadata**: Video duration, file size, generation parameters

## Authentication

### Interface Access
```http
GET / HTTP/1.1
Host: localhost:7860
User-Agent: Mozilla/5.0 (compatible)
Accept: text/html,application/xhtml+xml,application/xml

HTTP/1.1 200 OK
Content-Type: text/html
```

### Security Considerations
- No authentication required for basic video generation
- Rate limiting: 10 requests per minute per IP
- Input validation on all text parameters
- File size limits: 100MB maximum output
- Content filtering: Basic prompt sanitization

## Error Responses

### Common Errors

```json
{
  "error": "InvalidPromptError",
  "message": "Video prompt must be 1-500 characters",
  "code": 400
}
```

```json
{
  "error": "ModelLoadError",
  "message": "Failed to load HunyuanVideo-Foley model",
  "code": 503
}
```

```json
{
  "error": "GPUUnavailableError",
  "message": "CUDA GPU not available or out of memory",
  "code": 503
}
```

```json
{
  "error": "GenerationTimeoutError",
  "message": "Video generation exceeded time limit (600 seconds)",
  "code": 408
}
```

### Error Codes
- **400**: Bad Request (invalid parameters)
- **408**: Request Timeout (generation too slow)
- **413**: Payload Too Large (output exceeds limits)
- **429**: Too Many Requests (rate limit exceeded)
- **500**: Internal Server Error (unexpected failure)
- **503**: Service Unavailable (model/GPU unavailable)

## Rate Limiting

### Request Limits
```json
{
  "requests_per_minute": 10,
  "requests_per_hour": 100,
  "burst_limit": 20,
  "cooldown_period": 60
}
```

### Rate Limit Headers
```http
X-RateLimit-Limit: 10
X-RateLimit-Remaining: 8
X-RateLimit-Reset: 1640995200
X-RateLimit-Retry-After: 60
```

## Response Time Optimization

### Performance Targets
- **Interface Load**: <2 seconds
- **Video Generation**: 10-300 seconds (depends on duration/quality)
- **File Download**: <5 seconds for generated content

### Caching Strategies
- Model weights cached in persistent volumes
- Generated content temporarily cached for download
- Interface assets cached for faster reloads

### Concurrency Control
- Single concurrent generation per container
- Queue management for multiple requests
- Automatic cleanup of temporary files

## Integration Examples

### Python Integration
```python
import requests
from gradio_client import Client

# Initialize Gradio client
client = Client("http://localhost:7860/")

# Generate video
result = client.predict(
    "A cat playing with yarn",  # video_prompt
    "",                        # audio_prompt
    15,                        # duration
    "medium",                  # quality
    "mp4"                      # output_format
)

print(f"Generated video available at: {result}")
```

### cURL Integration
```bash
# Check interface availability
curl -I http://localhost:7860/

# Note: Direct API calls require Gradio's internal API
# Use web interface for programmatic access
```

### Docker Integration
```bash
# Run container with external access
docker run --gpus all -p 7860:7860 gemneye/hunyuanvideo-foley-runpod:latest

# Access via port mapping
curl http://localhost:7860/  # Returns HTML interface
```

## Monitoring and Debugging

### Health Checks
```bash
# Container health endpoint
docker exec hunyuanvideo-foley curl -f http://localhost:7860/ || exit 1

# Model loading verification
docker logs hunyuanvideo-foley | grep "Model loaded successfully"
```

### Debug Mode
```bash
# Enable debug mode
docker run --env GRADIO_DEBUG=true gemneye/hunyuanvideo-foley-runpod:latest
```

### Log Access
```bash
# View generation logs
docker logs -f hunyuanvideo-foley

# Filter for errors
docker logs hunyuanvideo-foley 2>&1 | grep ERROR
```

## Notes

### Special Considerations
- **GPU Requirements**: NVIDIA GPU with CUDA support required
- **Memory Usage**: 8GB+ GPU memory recommended
- **Storage**: 50GB+ for models, 10GB+ for outputs
- **Network**: Stable internet connection for model downloads
- **Browser**: Modern web browser with WebGL support

### Limitations
- Single video generation at a time per container
- Maximum 30-second video duration
- Output limited to 100MB file size
- Requires active CUDA GPU for processing

### Future Enhancements
- Batch processing support
- Custom model training integration
- Real-time video streaming
- Multi-language prompt support

## Keywords <!-- #keywords -->
- api
- gradio
- interface
- web
- contracts
- endpoints
- requests
- responses
- authentication
- validation