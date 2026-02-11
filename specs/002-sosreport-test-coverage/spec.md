# Feature Specification: Sosreport Test Coverage

**Feature Branch**: `002-sosreport-test-coverage`  
**Created**: 2026-02-11  
**Status**: Draft  
**Input**: User description: "sosreport test coverage. For the new generate_sosreport and fetch_sosreport tools in linux-mcp-server. The goal is to verify success paths, permission handling, timeout handling, output path resolution, and checksum integrity based on real-world behavior observed during manual testing. Tests must validate that generate_sosreport correctly handles sudo-required execution, reports actionable errors when sudo NOPASSWD is not configured, handles long-running report generation timeout behavior, and resolves the produced archive path in /var/tmp with hostname/name-based file patterns. Tests must validate that fetch_sosreport can retrieve root-owned sosreport archives via configured command path, fails with clear errors when access is denied, and preserves binary integrity (including checksum validation). Include coverage for option handling (only_plugins, enable_plugins, disable_plugins, log_size, redaction) and invalid input validation. Success criteria: deterministic, isolated tests that run in CI without requiring a real VM and catch regressions in command construction, error mapping, and archive retrieval flow."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Validate Sosreport Generation Behavior (Priority: P1)

As a maintainer, I need automated tests for sosreport generation behavior so regressions in privilege handling, timeout behavior, and archive discovery are caught before release.

**Why this priority**: `generate_sosreport` is the entry point for report collection. If it fails silently or maps failures poorly, users cannot proceed with diagnostics.

**Independent Test**: Run only generation-focused tests with mocked command responses and verify success metadata plus user-facing error outcomes.

**Acceptance Scenarios**:

1. **Given** sosreport generation succeeds and returns an archive path, **When** generation is requested, **Then** the result includes archive metadata and a fetch reference for the produced archive.
2. **Given** sudo requires a password for report generation, **When** generation is requested, **Then** the returned error clearly instructs maintainers to configure passwordless sudo for the required command.
3. **Given** report generation exceeds the execution timeout, **When** generation is requested, **Then** the returned error explicitly states that generation timed out.
4. **Given** command output includes only a hostname/name-based archive filename, **When** generation is requested, **Then** the reported archive path resolves to `/var/tmp/<archive-name>`.

---

### User Story 2 - Validate Sosreport Retrieval and Integrity (Priority: P2)

As a maintainer, I need automated tests for archive retrieval so root-owned files can be fetched reliably, permission failures are understandable, and retrieved bytes are unmodified.

**Why this priority**: Retrieval is required to deliver generated artifacts to users. File access and integrity failures directly block support workflows.

**Independent Test**: Run only retrieval-focused tests with deterministic binary payloads and mocked command outcomes to validate path, size, and checksum behavior.

**Acceptance Scenarios**:

1. **Given** a root-owned archive is readable through the configured privileged read command, **When** fetch is requested, **Then** the archive is saved locally and reported size/checksum match the source payload.
2. **Given** read access is denied for the archive, **When** fetch is requested, **Then** the returned error message clearly states that the archive could not be read and includes actionable context.
3. **Given** archive fetch exceeds timeout limits, **When** fetch is requested, **Then** the returned error explicitly states that fetching timed out.

---

### User Story 3 - Validate Input and Option Contract (Priority: P3)

As a maintainer, I need automated validation coverage for generation options and invalid input handling so malformed inputs fail deterministically and valid options are preserved end-to-end.

**Why this priority**: Input validation and option mapping guard against unpredictable behavior and prevent subtle regressions in command construction.

**Independent Test**: Run option/validation tests in isolation and verify accepted values are preserved while invalid values fail with deterministic messages.

**Acceptance Scenarios**:

1. **Given** valid option combinations are provided, **When** generation is requested, **Then** the returned options reflect the same effective values used for execution.
2. **Given** unsupported or conflicting option values are provided, **When** generation is requested, **Then** the request fails with clear validation errors.
3. **Given** an invalid archive reference path is provided for retrieval, **When** fetch is requested, **Then** the request fails with deterministic path-validation errors.

---

### Edge Cases

- Generation output contains no absolute archive path and no filename pattern.
- Generation command succeeds, but archive metadata lookup returns malformed output.
- Retrieval command returns non-UTF-8 stderr bytes for permission failures.
- Retrieval receives empty binary payload but successful return code.
- Plugin options are supplied with invalid characters, empty lists, or mutually exclusive combinations.
- Archive naming uses multiple host/name tokens but still matches expected `/var/tmp/sosreport-...` patterns.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The specification MUST require deterministic automated tests that validate the successful generation flow for sosreport archives, including returned archive metadata and fetch reference.
- **FR-002**: The specification MUST require tests verifying generation behavior when elevated execution is required, including actionable user-facing errors when passwordless sudo is not configured.
- **FR-003**: The specification MUST require tests verifying generation timeout behavior with explicit timeout error mapping.
- **FR-004**: The specification MUST require tests validating archive output path resolution from both absolute-path output and hostname/name-based filename patterns under `/var/tmp`.
- **FR-005**: The specification MUST require tests verifying successful archive retrieval for root-owned archives through the configured privileged read path.
- **FR-006**: The specification MUST require tests verifying retrieval failure behavior for access-denied and timeout outcomes, with clear and actionable error messages.
- **FR-007**: The specification MUST require tests verifying retrieval integrity by validating local archive size and checksum values against known source bytes.
- **FR-008**: The specification MUST require tests covering generation option handling for `only_plugins`, `enable_plugins`, `disable_plugins`, `log_size`, and `redaction`.
- **FR-009**: The specification MUST require tests validating invalid input handling for generation options and retrieval references with deterministic error outcomes.
- **FR-010**: The specification MUST require tests to run in CI without requiring a real VM, remote host, or privileged system state.
- **FR-011**: The specification MUST require assertions that detect regressions in command construction, error mapping, and archive retrieval flow.

### Key Entities *(include if feature involves data)*

- **Generation Request Options**: User-provided report-generation settings, including plugin scope, log-size policy, and redaction preference.
- **Sosreport Archive Reference**: The canonical archive location identifier returned by generation and consumed by retrieval.
- **Archive Metadata Result**: Returned archive details required for diagnostics workflows, including path, filename, size, and creation timestamp.
- **Retrieval Result**: Local archive path plus integrity indicators (byte size and checksum) used to confirm a faithful transfer.
- **Diagnostic Error Outcome**: User-facing failure result category for permission, timeout, validation, and command-failure conditions.

### Assumptions

- Manual testing outcomes already define expected behavior for permission, timeout, and archive path patterns.
- Deterministic tests will use controlled command outcomes rather than external system dependencies.
- Checksums are treated as the authoritative integrity indicator for binary retrieval verification.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of required generation and retrieval behaviors listed in this specification have automated test coverage with deterministic pass/fail outcomes.
- **SC-002**: 100% of permission and timeout failure scenarios defined in this specification return explicit, actionable error messages in tests.
- **SC-003**: 100% of retrieval integrity tests verify that reported checksum and size match the known source payload.
- **SC-004**: 100% of specified option-handling and invalid-input scenarios are validated by automated tests in CI without requiring a real VM.
- **SC-005**: A regression that changes command construction, error mapping, archive path resolution, or archive retrieval flow causes at least one automated test failure.
