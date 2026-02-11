# Tasks: Sosreport Test Coverage

**Input**: Design documents from `/specs/002-sosreport-test-coverage/`  
**Prerequisites**: `plan.md` (required), `spec.md` (required), `research.md`, `data-model.md`, `contracts/`, `quickstart.md`

**Tests**: Tests are explicitly required by the feature specification.  
**Organization**: Tasks are grouped by user story so each story can be implemented and validated independently.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependency on incomplete tasks)
- **[Story]**: User story label (`[US1]`, `[US2]`, `[US3]`) for story-phase tasks only
- Every task includes explicit file path(s) and FR/SC mapping

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Confirm task scope and baseline test harness behavior before story work.

- [X] T001 Confirm scope constraints and update `specs/002-sosreport-test-coverage/tasks.md` notes to limit code changes to `tests/tools/test_sosreport.py`, `src/linux_mcp_server/tools/sosreport.py`, `src/linux_mcp_server/utils/validation.py`, and optional `tests/utils/test_validation.py` (FR-010)
- [X] T002 Run baseline command `uv run pytest tests/tools/test_sosreport.py` and document current failures in `specs/002-sosreport-test-coverage/tasks.md` implementation notes (FR-011, SC-005)

**Phase 1 Verification**

- Run: `uv run pytest tests/tools/test_sosreport.py`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Establish shared deterministic fixtures and command-mocking strategy used by all stories.

**⚠️ CRITICAL**: Complete this phase before any user story implementation.

- [X] T003 Add deterministic command-mocking helpers/fixtures in `tests/tools/test_sosreport.py` for ordered `execute_with_fallback` outcomes and host-aware assertions (FR-010, FR-011)
- [X] T004 [P] Add helper assertions in `tests/tools/test_sosreport.py` for structured content extraction and error text matching across MCP tool calls (FR-001, FR-006, SC-001)
- [X] T005 [P] Add deterministic payload/checksum helper in `tests/tools/test_sosreport.py` for binary retrieval integrity checks (FR-007, SC-003)

**Checkpoint**: Shared test harness is ready; story phases can proceed.

**Phase 2 Verification**

- Run: `uv run pytest tests/tools/test_sosreport.py`

---

## Phase 3: User Story 1 - Validate Sosreport Generation Behavior (Priority: P1) 🎯 MVP

**Goal**: Cover generation success, sudo/permission/timeout failures, and archive path resolution behavior.

**Independent Test**: `uv run pytest tests/tools/test_sosreport.py -k "generate_sosreport"`

### Tests for User Story 1

- [X] T006 [US1] Add generation success test in `tests/tools/test_sosreport.py` validating archive metadata, fetch reference, and generated command arguments (FR-001, FR-011, SC-001, SC-005)
- [X] T007 [US1] Add generation sudo-password-required error test in `tests/tools/test_sosreport.py` validating actionable NOPASSWD messaging (FR-002, SC-002)
- [X] T008 [US1] Add generation permission-denied and timeout mapping tests in `tests/tools/test_sosreport.py` validating clear error outcomes (FR-003, FR-006, SC-002)
- [X] T009 [US1] Add output path resolution tests in `tests/tools/test_sosreport.py` for absolute-path output, `/var/tmp` filename pattern output, and latest-named fallback behavior (FR-004, SC-005)

### Implementation for User Story 1 (minimal parity fixes only)

- [X] T010 [US1] Apply minimal parsing/parity fixes in `src/linux_mcp_server/tools/sosreport.py` only if US1 tests fail due to path extraction or error-mapping mismatches (FR-004, FR-011, SC-005)
- [X] T011 [US1] Re-run generation-focused suite and update notes in `specs/002-sosreport-test-coverage/tasks.md` with pass/fail status (FR-001, FR-002, FR-003, FR-004, SC-001, SC-002)

**Checkpoint**: User Story 1 is independently functional and testable.

**Phase 3 Verification**

- Run: `uv run pytest tests/tools/test_sosreport.py -k "generate_sosreport"`

---

## Phase 4: User Story 2 - Validate Sosreport Retrieval and Integrity (Priority: P2)

**Goal**: Cover archive retrieval success/failure and binary integrity guarantees.

**Independent Test**: `uv run pytest tests/tools/test_sosreport.py -k "fetch_sosreport"`

### Tests for User Story 2

- [X] T012 [US2] Add retrieval success test in `tests/tools/test_sosreport.py` validating privileged read path usage, local archive path, and size reporting (FR-005, SC-001)
- [X] T013 [US2] Add retrieval access-denied and sudo-password-required tests in `tests/tools/test_sosreport.py` validating clear actionable errors (FR-006, SC-002)
- [X] T014 [US2] Add retrieval timeout mapping test in `tests/tools/test_sosreport.py` for deterministic timeout behavior (FR-006, SC-002)
- [X] T015 [US2] Add binary integrity test in `tests/tools/test_sosreport.py` validating checksum and byte-for-byte payload preservation (FR-007, SC-003)

### Implementation for User Story 2 (minimal parity fixes only)

- [X] T016 [US2] Apply minimal parity fixes in `src/linux_mcp_server/tools/sosreport.py` only if retrieval tests expose behavioral mismatches (FR-005, FR-006, FR-007, FR-011, SC-005)
- [X] T017 [US2] Re-run retrieval-focused suite and record status in `specs/002-sosreport-test-coverage/tasks.md` notes (FR-005, FR-006, FR-007, SC-001, SC-002, SC-003)

**Checkpoint**: User Story 2 is independently functional and testable.

**Phase 4 Verification**

- Run: `uv run pytest tests/tools/test_sosreport.py -k "fetch_sosreport"`

---

## Phase 5: User Story 3 - Validate Input and Option Contract (Priority: P3)

**Goal**: Cover option handling and invalid input validation for both tools.

**Independent Test**: `uv run pytest tests/tools/test_sosreport.py -k "invalid or options" && uv run pytest tests/utils/test_validation.py`

### Tests for User Story 3

- [X] T018 [US3] Add option-handling tests in `tests/tools/test_sosreport.py` for `only_plugins`, `enable_plugins`, `disable_plugins`, `log_size`, and `redaction` behavior preservation (FR-008, SC-004)
- [X] T019 [US3] Add invalid generation-option tests in `tests/tools/test_sosreport.py` for empty/invalid/conflicting values with deterministic errors (FR-009, SC-004)
- [X] T020 [US3] Add invalid retrieval-reference path tests in `tests/tools/test_sosreport.py` validating deterministic input-validation errors (FR-009, SC-004)

### Implementation for User Story 3 (minimal parity fixes only)

- [X] T021 [US3] Apply minimal validation parity fixes in `src/linux_mcp_server/utils/validation.py` only if US3 tests reveal contract mismatches (FR-008, FR-009, FR-011, SC-004, SC-005)
- [X] T022 [US3] [P] Add or update regression tests in `tests/utils/test_validation.py` only for behaviors changed by T021 (FR-009, SC-004)
- [X] T023 [US3] Re-run option/validation-focused suites and record outcome in `specs/002-sosreport-test-coverage/tasks.md` notes (FR-008, FR-009, SC-004)

**Checkpoint**: User Story 3 is independently functional and testable.

**Phase 5 Verification**

- Run: `uv run pytest tests/tools/test_sosreport.py -k "invalid or options"`
- Run: `uv run pytest tests/utils/test_validation.py`

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final integration verification and quality gates across all stories.

- [X] T024 [P] Ensure FR/SC traceability comments remain clear and complete in `tests/tools/test_sosreport.py` and `specs/002-sosreport-test-coverage/tasks.md` (FR-011, SC-005)
- [X] T025 Execute full targeted regression run `uv run pytest tests/tools/test_sosreport.py tests/utils/test_validation.py` and capture results in `specs/002-sosreport-test-coverage/tasks.md` notes (SC-001, SC-002, SC-003, SC-004, SC-005)
- [X] T026 Execute repository quality gate `make verify` and capture final pass confirmation in `specs/002-sosreport-test-coverage/tasks.md` notes (FR-010, SC-004)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: starts immediately.
- **Phase 2 (Foundational)**: depends on Phase 1; blocks story work.
- **Phase 3 (US1)**: depends on Phase 2.
- **Phase 4 (US2)**: depends on Phase 2; can run after US1 or in parallel if staffing allows.
- **Phase 5 (US3)**: depends on Phase 2; can run after US1 or in parallel if staffing allows.
- **Phase 6 (Polish)**: depends on completion of desired user story phases.

### User Story Dependencies

- **US1 (P1)**: no dependency on other stories after foundational setup.
- **US2 (P2)**: no functional dependency on US1, but may share parity fixes in `src/linux_mcp_server/tools/sosreport.py`.
- **US3 (P3)**: no functional dependency on US1/US2, but may require minor shared validation behavior.

### Within Each User Story

- Tests first, then minimal parity fixes only if tests expose mismatch.
- Story-specific verification must pass before moving to next checkpoint.

### Parallel Opportunities

- T004 and T005 can run in parallel after T003.
- In US2, T012-T015 can be split across collaborators by scenario.
- In US3, T022 can run in parallel with documentation updates after T021.
- Final polish T024 and result-capture prep can run in parallel before final gate.

---

## Parallel Example: User Story 2

```bash
# Parallelizable retrieval scenario work:
Task: "T012 [US2] Add retrieval success test in tests/tools/test_sosreport.py"
Task: "T013 [US2] Add retrieval access-denied/sudo-required tests in tests/tools/test_sosreport.py"
Task: "T014 [US2] Add retrieval timeout test in tests/tools/test_sosreport.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1 and Phase 2.
2. Complete US1 (Phase 3).
3. Validate generation-focused behavior with targeted pytest run.
4. Stop for review before expanding to US2/US3.

### Incremental Delivery

1. Deliver US1 (generation behavior).
2. Deliver US2 (retrieval + integrity).
3. Deliver US3 (options + validation contract).
4. Run final polish verification and `make verify`.

### Team Parallel Strategy

1. One contributor stabilizes foundational harness (Phase 2).
2. Then split by stories:
   - Contributor A: US1
   - Contributor B: US2
   - Contributor C: US3
3. Rejoin for Phase 6 final integration gates.

---

## Notes

- `[P]` tasks are safe parallel candidates based on file/dependency separation.
- All story tasks are explicitly scoped to approved files.
- Every task includes FR/SC mapping for traceability.
- Use deterministic mocks only; do not introduce VM/SSH runtime dependencies.
- Implementation baseline (T002): `uv run pytest tests/tools/test_sosreport.py` failed with `file or directory not found: tests/tools/test_sosreport.py` (exit code 4), as expected before test creation.
- Phase 2 verification: `uv run pytest tests/tools/test_sosreport.py` passed (18 passed) after minimal parity fixes in `src/linux_mcp_server/tools/sosreport.py` and `src/linux_mcp_server/utils/validation.py`.
- Phase 3 verification: `uv run pytest tests/tools/test_sosreport.py -k "generate_sosreport"` passed (10 passed).
- Phase 4 verification: `uv run pytest tests/tools/test_sosreport.py -k "fetch_sosreport"` passed (8 passed).
- Phase 5 verification: `uv run pytest tests/tools/test_sosreport.py -k "invalid or options"` passed (9 passed); `uv run pytest tests/utils/test_validation.py` passed (50 passed).
- Phase 6 verification: `uv run pytest tests/tools/test_sosreport.py tests/utils/test_validation.py` passed (68 passed); `make verify` passed (441 passed, 1 warning).
- T022 note: no additional updates were needed in `tests/utils/test_validation.py` beyond existing coverage; current tests validated the behavior changes introduced in T021.
