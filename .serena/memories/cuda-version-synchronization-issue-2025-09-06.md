# CUDA Version Synchronization Issue (2025-09-06)

## Problem Summary
Runtime container has CUDA version mismatches causing TorchAudio errors:
- Base image: nvidia/cuda:12.8.1-cudnn-devel-ubuntu24.04 
- PyTorch installed with CUDA 12.1 (cu121)
- TorchAudio installed with CUDA 12.4 (cu124)
- Error: "PyTorch has CUDA version 12.1 whereas TorchAudio has CUDA version 12.4"

## Root Cause Analysis
1. **Base Image Mismatch**: Container base has CUDA 12.8.1 but PyTorch packages are installed with older CUDA versions
2. **Requirements.txt Conflicts**: HunyuanVideo-Foley requirements.txt installs PyTorch with specific CUDA versions that don't match the base image
3. **Flash Attention Compatibility**: Current flash_attn wheel may not match the CUDA/runtime versions

## Investigation Findings
- Dockerfile: `nvidia/cuda:12.8.1-cudnn-devel-ubuntu24.04` (CUDA 12.8.1)
- Current runtime_install.sh: Lets requirements.txt handle PyTorch installation  
- Error message: PyTorch cu121 vs TorchAudio cu124 mismatch
- Need: All packages synchronized to CUDA 12.8.1

## Required Solutions
1. **PyTorch Installation**: Replace requirements.txt PyTorch with explicit CUDA 12.8.1 compatible version
2. **Force CUDA Synchronization**: All PyTorch packages must use same CUDA version 
3. **Dynamic Flash Attention**: Implement runtime Python version detection for correct wheel URL
4. **Version Pinning**: Ensure all dependencies are aligned with CUDA 12.8.1

## Next Steps
- Identify correct PyTorch wheel URL for CUDA 12.8 (cu128 or equivalent)
- Implement version detection and URL generation scripts
- Update runtime_install.sh with synchronized installations
- Test compatibility between PyTorch, TorchAudio, and Flash Attention