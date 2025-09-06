# Critical Error Ledger

## Schema
| ID | First seen | Status | Severity | Affected area | Link to fix |
|----|------------|--------|----------|---------------|-------------|

## Active Errors

## Resolved Errors
[Resolved errors moved here with resolution date and links to fixes]

## Error ID Format
ERR-YYYY-MM-DD-001 (increment for multiple per day)

## Severity Definitions
- **P0**: Complete outage, data loss, security breach
- **P1**: Major functionality broken, significant performance degradation
- **P2**: Minor functionality (not tracked in ERRORS.md)
- **P3**: Cosmetic issues (not tracked in ERRORS.md)

## Claude's Error Logging Process
1. When P0/P1 error occurs, immediately add to Active Errors
2. Create corresponding JOURNAL.md entry with `|ERROR:ERR-ID|` tag
3. When resolved:
   - Move to Resolved Errors section
   - Update status to "resolved"
   - Add commit hash and PR link
   - Link back to JOURNAL.md entry from ERRORS.md

## Common Error Patterns
- **Model Load Failures**: Check HF_TOKEN and network connectivity
- **CUDA Memory Errors**: Increase GPU memory allocation or reduce batch size
- **Container Startup Failures**: Verify NVIDIA driver compatibility
- **Hugging Face Rate Limits**: Implement retry logic with exponential backoff