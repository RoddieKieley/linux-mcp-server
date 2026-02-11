# Quickstart: Sosreport Test Coverage

## Goal

Implement deterministic, CI-safe test coverage for `generate_sosreport` and `fetch_sosreport` with mocked command execution and minimal parity fixes only when required.

## Prerequisites

- Repository checked out on branch `002-sosreport-test-coverage`
- Development dependencies installed (`uv sync`)
- No reliance on VM or remote SSH for this feature's test execution

## Implementation Steps

1. Add `tests/tools/test_sosreport.py` with scenario-driven async tests for:
   - generation success and archive metadata
   - permission and timeout error mapping
   - archive path resolution from full paths and `/var/tmp` filename patterns
   - retrieval success, access-denied, timeout
   - binary integrity (`size_bytes`, `sha256`)
   - option handling and invalid input validation
2. Add minimal production fixes only if tests expose parity gaps in:
   - `src/linux_mcp_server/tools/sosreport.py`
   - `src/linux_mcp_server/utils/validation.py`
3. Add/adjust regression coverage in `tests/utils/test_validation.py` only when validation behavior changes.

## Requirement Coverage Checklist

- FR-001..FR-004: generation success, privilege/timeout mapping, and path resolution
- FR-005..FR-007: retrieval success/failure mapping and integrity validation
- FR-008..FR-009: option and invalid-input contract coverage
- FR-010: mock-only deterministic CI execution, no VM dependency
- FR-011: command construction and behavior regression detection

## Validation Commands

Run in order:

```bash
uv run pytest tests/tools/test_sosreport.py
uv run pytest tests/utils/test_validation.py
make verify
```

## Expected Outcomes

- Targeted sosreport tests pass consistently in local and CI runs.
- Regression in command construction, error mapping, path resolution, or binary retrieval integrity causes test failure.
- Full repository verification (`make verify`) passes before merge handoff.
