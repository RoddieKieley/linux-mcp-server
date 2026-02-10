# Tasks: linux-mcp-server sosreport tool

**Input**: Design documents from `/specs/001-sosreport-tool/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Not requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create sosreport tool module scaffold in `src/linux_mcp_server/tools/sosreport.py`
- [ ] T002 [P] Add tool export in `src/linux_mcp_server/tools/__init__.py`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T003 [P] Add `SosreportArchive` and `SosreportOptions` models in `src/linux_mcp_server/models.py`
- [ ] T004 [P] Add sosreport option validation helpers in `src/linux_mcp_server/utils/validation.py`

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Generate sosreport (Priority: P1) 🎯 MVP

**Goal**: Generate a sosreport on a remote host, return metadata, and provide a fetch reference.

**Independent Test**: Call `generate_sosreport` against a host with `sos` installed and confirm metadata + fetch reference.

### Implementation for User Story 1

- [ ] T005 [US1] Implement `generate_sosreport` tool in `src/linux_mcp_server/tools/sosreport.py`
- [ ] T005A [US1] Add explicit timeout handling and error mapping in `src/linux_mcp_server/tools/sosreport.py`
- [ ] T005B [US1] Add explicit missing sos/privilege error mapping in `src/linux_mcp_server/tools/sosreport.py`
- [ ] T006 [US1] Implement `fetch_sosreport` tool in `src/linux_mcp_server/tools/sosreport.py`
- [ ] T007 [US1] Register sosreport commands in `src/linux_mcp_server/commands.py`
- [ ] T008 [US1] Wire tool metadata and schemas in `src/linux_mcp_server/tools/__init__.py`

**Checkpoint**: User Story 1 is functional, returns a fetch reference, and returns clear timeout/privilege/missing-sos errors.

---

## Phase 4: User Story 2 - Scoped report (Priority: P2)

**Goal**: Support plugin scoping and log size limits for targeted reports.

**Independent Test**: Call `generate_sosreport` with plugin and log size options and verify the applied scope.

### Implementation for User Story 2

- [ ] T009 [US2] Apply plugin scoping options in `src/linux_mcp_server/tools/sosreport.py`
- [ ] T010 [US2] Apply log size option mapping in `src/linux_mcp_server/tools/sosreport.py`

**Checkpoint**: User Story 2 is functional with validated scope options.

---

## Phase 5: User Story 3 - Redaction control (Priority: P2)

**Goal**: Allow operators to enable or disable redaction.

**Independent Test**: Call `generate_sosreport` with redaction disabled and confirm the report runs without redaction.

### Implementation for User Story 3

- [ ] T011 [US3] Map redaction toggle to sosreport flags in `src/linux_mcp_server/tools/sosreport.py`

**Checkpoint**: User Story 3 is functional with explicit redaction control.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T012 [P] Document new tools in `docs/api/tools/sosreport.md`
- [ ] T013 [P] Add tool links in `docs/api/tools/index.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after User Story 1 baseline tool behavior is in place
- **User Story 3 (P2)**: Can start after User Story 1 baseline tool behavior is in place

### Within Each User Story

- Models and validation before tool behavior
- Tool behavior before documentation
- Story complete before moving to next priority

### Parallel Opportunities

- Setup tasks marked [P] can run in parallel
- Foundational tasks marked [P] can run in parallel
- Polish tasks marked [P] can run in parallel

---

## Parallel Example: User Story 1

```bash
# Implementation tasks for User Story 1:
Task: "Implement generate_sosreport tool in src/linux_mcp_server/tools/sosreport.py"
Task: "Register sosreport commands in src/linux_mcp_server/commands.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → MVP ready
3. Add User Story 2 → Test independently → Expand scope controls
4. Add User Story 3 → Test independently → Add redaction control

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
