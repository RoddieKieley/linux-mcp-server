# Implementation Plan: Sosreport Test Coverage

**Branch**: `002-sosreport-test-coverage` | **Date**: 2026-02-11 | **Spec**: `specs/002-sosreport-test-coverage/spec.md`  
**Input**: Feature specification from `specs/002-sosreport-test-coverage/spec.md`

## Summary

Add deterministic, CI-safe automated tests for `generate_sosreport` and `fetch_sosreport` that verify success behavior, permission and timeout error mapping, archive path resolution, option handling, and checksum integrity. Implementation is limited to test additions plus minimal behavior fixes required to match specified outcomes and prevent regressions in command construction and retrieval flow.

## Technical Context

**Language/Version**: Python 3.10+  
**Primary Dependencies**: FastMCP, pydantic, pytest, pytest-asyncio, pytest-mock, ruff, pyright  
**Storage**: Local filesystem writes for fetched archive test outputs (temporary directories only)  
**Testing**: `pytest` with async tests and mocked command execution (no VM/SSH dependency)  
**Target Platform**: Linux CI and local Linux development environments  
**Project Type**: Single Python package (`src/` + `tests/`)  
**Performance Goals**: Targeted sosreport test suite completes in under 10 seconds in CI; full verification remains within existing CI budget  
**Constraints**: No real VM access, no real remote SSH, no privileged system dependency, deterministic output assertions, minimal production-code changes  
**Scale/Scope**: 1 new focused test module, optional small fixes in `sosreport`/validation parsing logic, FR-001..FR-011 and SC-001..SC-005 traceability

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- Constitution file at `.specify/memory/constitution.md` is a placeholder template and defines no enforceable project-specific gates.
- Effective gates applied from repository standards:
  - Preserve read-only tool behavior semantics.
  - Keep changes small and focused to sosreport test coverage and parity fixes.
  - Ensure lint/type/test verification commands are documented and runnable.
- **Pre-Phase 0 gate result**: PASS (no explicit constitution violations; repo standards accommodated).
- **Post-Phase 1 gate result**: PASS (artifacts remain scoped, deterministic, and aligned with repo verification workflow).

## Project Structure

### Documentation (this feature)

```text
specs/002-sosreport-test-coverage/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── sosreport-tool-behavior.yaml
└── tasks.md              # Generated later by /speckit.tasks
```

### Source Code (repository root)

```text
src/
└── linux_mcp_server/
    ├── tools/
    │   └── sosreport.py              # Minimal parity fixes only if required
    └── utils/
        └── validation.py             # Minimal parity fixes only if required

tests/
├── tools/
│   └── test_sosreport.py             # Primary feature test coverage
└── utils/
    └── test_validation.py            # Regression checks for validation behavior
```

**Structure Decision**: Use the existing single-package Python layout and concentrate work in one new sosreport-focused test module plus minimal bug-fix touches in affected production files only when needed to satisfy specified behavior.

## File-by-File Change Plan

1. `tests/tools/test_sosreport.py`
   - Add deterministic async tests covering generation and retrieval success/failure paths.
   - Assert command construction, option passthrough, path resolution behavior, timeout mapping, privilege error mapping, and checksum integrity.
2. `src/linux_mcp_server/tools/sosreport.py` (minimal parity fixes only if needed)
   - Adjust path/filename extraction behavior only when required to satisfy specified real-world output patterns.
3. `src/linux_mcp_server/utils/validation.py` (minimal parity fixes only if needed)
   - Correct validation edge behavior only if required for specified option handling and invalid-input expectations.
4. `tests/utils/test_validation.py` (optional targeted additions)
   - Add/extend tests if validation fixes require explicit regression coverage.

## Test Case Matrix (Requirements to Coverage)

| Requirement / Criterion | Planned Test Coverage |
|-------------------------|-----------------------|
| FR-001, SC-001 | Generation success test verifies archive metadata and fetch reference |
| FR-002, SC-002 | Generation sudo password-required test verifies actionable NOPASSWD error |
| FR-003, SC-002 | Generation timeout test verifies explicit timeout mapping |
| FR-004, SC-005 | Path extraction tests for absolute output and `/var/tmp` filename pattern resolution |
| FR-005, SC-001 | Retrieval success test verifies privileged-read execution path and local archive output |
| FR-006, SC-002 | Retrieval access-denied and timeout tests verify clear error mapping |
| FR-007, SC-003 | Retrieval binary integrity test verifies size and checksum match source bytes |
| FR-008, SC-004 | Option-handling tests for `only_plugins`, `enable_plugins`, `disable_plugins`, `log_size`, `redaction` |
| FR-009, SC-004 | Invalid-input tests for option conflicts/format and fetch reference path validation |
| FR-010, SC-004 | All sosreport tests rely on mocks and temp files; no VM/SSH dependency |
| FR-011, SC-005 | Explicit assertions on constructed command args and error strings catch regressions |

## Verification Plan

1. Run targeted suite:
   - `uv run pytest tests/tools/test_sosreport.py`
2. Run related validation tests when validation behavior changes:
   - `uv run pytest tests/utils/test_validation.py`
3. Run project verification gate before handoff:
   - `make verify`

## Complexity Tracking

No constitution violations identified; complexity justification table not required.
