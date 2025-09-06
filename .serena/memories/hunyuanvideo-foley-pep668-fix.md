## Runtime Installation Fix for Ubuntu 24.04 PEP 668 Compatibility

### Problem Description
Ubuntu 24.04 implements PEP 668 (Externally Managed Environment) which prevents system-wide pip installations to avoid conflicts with system Python packages. This caused runtime installation failures in the HunyuanVideo-Foley container.

### Error Manifestation
```
error: externally-managed-environment
× This environment is externally managed
╰─> To install Python packages system-wide, try apt install
```

### Solution Implemented
Added `--break-system-packages` flag to all pip install commands in `runtime_install.sh`. This flag overrides PEP 668 restrictions, which is safe in controlled container environments.

### Files Modified
- `runtime_install.sh`: Updated all pip install commands with `--break-system-packages` flag

### Commands Updated
1. `pip3 install torch torchvision --break-system-packages`
2. `pip install -r requirements.txt --break-system-packages`
3. `pip install hf-hub --break-system-packages`
4. `pip install [flash-attention wheel] --break-system-packages`

### Impact Assessment
- **Positive**: Resolves runtime installation errors in Ubuntu 24.04 containers
- **Compatibility**: Maintains functionality across different Python environments
- **Security**: Acceptable risk in containerized, sandboxed environments
- **Base Image**: Compatible with `nvidia/cuda:12.8.1-cudnn-devel-ubuntu24.04`

### Related Components
- Dockerfile base image selection
- Runtime installation architecture
- Container security model
- Python dependency management strategy

### Testing Considerations
- Verify installation completes successfully in container environment
- Confirm PyTorch CUDA compatibility
- Validate model download functionality
- Test full application startup sequence

### Future Considerations
- Monitor for alternative approaches (virtual environments)
- Consider package installation optimization
- Evaluate system package alternatives where available