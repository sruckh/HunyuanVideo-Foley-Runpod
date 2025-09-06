# HunyuanVideo-Foley PyTorch Installation Fix

Date: 2025-09-06

## Summary
Restored PyTorch installation command in runtime_install.sh to exact specification from GOALS.md: "pip3 install torch torchvision" without version pinning.

## Rationale
- Project must follow GOALS.md exactly for runtime compatibility
- Base image uses CUDA 12.8.1, making version pinning unnecessary and potentially problematic
- Flash Attention wheel compatibility requires matching PyTorch version
- Version pinning was causing installation conflicts

## Implementation
Modified runtime_install.sh line 12 to use generic PyTorch installation command as specified in GOALS.md.

## Verification
- Confirmed installation works with CUDA 12.8.1 base image
- Verified compatibility with Flash Attention wheel
- Ensured no version conflicts during runtime installation

## Related Files
- runtime_install.sh:12
- GOALS.md:37
- JOURNAL.md:2025-09-06 entry
- TASKS.md: TASK-2025-09-06-001