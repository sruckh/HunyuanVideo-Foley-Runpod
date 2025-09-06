## Runtime Installation Fixes for Python 3.12 and Directory Handling

### Problem Description
Additional runtime errors were encountered when testing the containerized HunyuanVideo-Foley application beyond the PEP 668 fixes:

### Issues Identified
1. **Python 3.12 Compatibility**: Flash Attention wheel was compiled for Python 3.10 (cp310) but Ubuntu 24.04 uses Python 3.12
2. **Directory Conflicts**: Git clone operations fail when HunyuanVideo-Foley directory already exists from previous runs

### Solutions Implemented

#### Python 3.12 Flash Attention Support
- Updated Flash Attention wheel URL from cp310 to cp312
- Wheel: `flash_attn-2.8.3+cu12torch2.8cxx11abiFALSE-cp312-cp312-linux_x86_64.whl`
- Ensures compatibility with Python 3.12 in Ubuntu 24.04 containers

#### Directory Conflict Resolution
- Added conditional check before git clone operations
- Logic: `if [ ! -d "HunyuanVideo-Foley" ]; then git clone ...`
- Prevents failures when container restarts with existing directories
- Maintains idempotent behavior for repeated container starts

### Technical Details
- **Container Base**: `nvidia/cuda:12.8.1-cudnn-devel-ubuntu24.04` includes Python 3.12
- **Wheel Compatibility**: Must match Python version exactly (cp312 for Python 3.12)
- **CUDA Wheel**: cu12 torch compatibility maintained
- **Directory Handling**: Bash conditional logic with proper directory existence checks

### Impact Assessment
- **Compatibility**: Full support for Ubuntu 24.04 with Python 3.12
- **Reliability**: Eliminates directory conflict errors on container restarts
- **Performance**: Maintains original startup time (10-15 minutes)
- **Idempotency**: Script can be safely re-run without errors

### Integration Points
- Works with existing PEP 668 fixes (`--break-system-packages`)
- Maintains all security requirements from original GOALS.md
- Compatible with GitHub Actions CI/CD pipeline
- Supports both local development and RunPod deployment

### Testing Considerations
- Verify Python 3.12 compatibility in container environment
- Test directory handling on container restarts
- Confirm Flash Attention installation without errors
- Validate complete runtime setup flow