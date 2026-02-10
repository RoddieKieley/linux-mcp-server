# Feature Specification: linux-mcp-server sosreport tool

**Feature Branch**: `001-sosreport-tool`  
**Created**: 2026-02-06  
**Status**: Draft  
**Input**: User description: "Develop a linux-mcp-server MCP tool that generates an sosreport on a remote host using the installed sos utility. It must run non-interactively, support plugin scoping (only_plugins, enable_plugins, disable_plugins), log size limits, and allow redaction control (default redaction on, allow disabling). It should return report metadata (remote path, name, size, timestamp) and provide a way to fetch the archive back to the MCP host. If sos is missing or privileges are insufficient, return a clear, actionable error. Target Fedora 43+ and RHEL 9+, and enforce timeouts with clear error messaging."

## Clarifications

### Session 2026-02-06

- Q: Should report retrieval be handled via a separate fetch tool rather than inline payloads? → A: Yes, return a reference and use a separate fetch tool.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Generate sosreport (Priority: P1)

An operator needs to generate a full sosreport on a remote Fedora or RHEL host through the MCP server and retrieve it.

**Why this priority**: This is the core diagnostic workflow and replaces manual SSH execution.

**Independent Test**: Call the tool against a remote host with `sos` installed and verify a new archive is generated and returned with metadata and a retrieval option.

**Acceptance Scenarios**:

1. **Given** a remote host with `sos` installed, **When** the tool is called with default options, **Then** a new sosreport archive is generated and returned with a path or download reference.
2. **Given** a remote host without `sos`, **When** the tool is called, **Then** the response explains the missing dependency and how to install it.

---

### User Story 2 - Scoped report (Priority: P2)

An operator limits the scope or size of the report by selecting plugins and log size options.

**Why this priority**: Targeted, smaller reports reduce transfer time and focus diagnostics.

**Independent Test**: Call the tool with `only_plugins`, `enable_plugins`, `disable_plugins`, and `log_size` options and verify they are applied.

**Acceptance Scenarios**:

1. **Given** plugin and log size options, **When** the tool is called, **Then** the report is generated using the specified scope and limits.
2. **Given** invalid plugin names, **When** the tool is called, **Then** the response reports the validation failure.

---

### User Story 3 - Redaction control (Priority: P2)

An operator chooses whether to use default redaction or disable it.

**Why this priority**: Operators need explicit control over sensitive data handling for support workflows.

**Independent Test**: Call the tool with redaction disabled and confirm the report is generated without redaction.

**Acceptance Scenarios**:

1. **Given** redaction is enabled, **When** the tool is called, **Then** the report uses default redaction behavior.
2. **Given** redaction is disabled, **When** the tool is called, **Then** the report is generated without redaction.

---

### Edge Cases

- What happens when the report generation exceeds the configured timeout?
- How does the system handle insufficient privileges to run the report?
- What happens when the remote host is unreachable during report generation?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST provide an MCP tool that generates a sosreport on a remote host.
- **FR-002**: The tool MUST run non-interactively without prompting for input.
- **FR-003**: The tool MUST accept plugin scoping options (`only_plugins`, `enable_plugins`, `disable_plugins`) and a log size limit.
- **FR-004**: The tool MUST support a redaction toggle with redaction enabled by default.
- **FR-005**: The tool MUST return report metadata including remote path, report name, size, and timestamp.
- **FR-006**: The tool MUST provide a separate fetch tool that retrieves the report archive using the returned reference.
- **FR-007**: The tool MUST return a clear, actionable error when `sos` is missing or privileges are insufficient.
- **FR-008**: The tool MUST enforce a configurable execution timeout and return a clear timeout error.

### Key Entities *(include if feature involves data)*

- **SosreportArchive**: Generated report metadata (remote path, name, size, timestamp).
- **SosreportOptions**: Requested scope and safety settings (plugins, log size, redaction).

## Assumptions & Dependencies

- The remote host is reachable via the configured MCP connection.
- The MCP host has storage available for the retrieved archive.
- Remote access has the permissions required to execute the report or is configured to elevate privileges.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A default sosreport completes successfully on Fedora 43+ and RHEL 9+ in under 10 minutes.
- **SC-002**: Reports under 500 MB can be fetched to the MCP host in under 2 minutes on a typical LAN connection.
- **SC-003**: At least 95% of valid requests return report metadata and a retrieval option without manual intervention.
- **SC-004**: Invalid plugin options result in a clear, actionable error within 1 minute.
