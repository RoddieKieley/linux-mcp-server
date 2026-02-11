# Phase 0 Research: Sosreport Test Coverage

## Decision 1: Use command-layer mocking for all sosreport tests

- **Decision**: Mock command execution at `linux_mcp_server.commands.execute_with_fallback` for both `run` and `run_bytes` paths.
- **Rationale**: This yields deterministic, CI-safe tests while still verifying command construction and behavior mapping in tool logic.
- **Alternatives considered**:
  - Mocking higher-level tool functions only: rejected because command-construction regressions could be missed.
  - Running against a real VM/SSH host: rejected due to nondeterminism, environment coupling, and CI complexity.

## Decision 2: Validate behavior through MCP tool calls for end-user parity

- **Decision**: Prefer `mcp_client.call_tool()` flows for primary coverage instead of directly invoking wrapped tool functions.
- **Rationale**: Ensures tests exercise validation and error surfaces as users encounter them through MCP.
- **Alternatives considered**:
  - Direct function invocation everywhere: rejected because decorators/wrappers and MCP error boundaries are bypassed.

## Decision 3: Include minimal production fixes only when tests reveal parity gaps

- **Decision**: Allow small targeted bug fixes in `sosreport` parsing/validation when required to match specified behavior.
- **Rationale**: Scope remains test-first while avoiding false negatives caused by existing defects.
- **Alternatives considered**:
  - Tests only, no production changes: rejected because known parity defects would keep required scenarios failing.
  - Broad refactoring: rejected as out-of-scope for this focused feature.

## Decision 4: Verify binary integrity with deterministic payload hashing

- **Decision**: Use fixed byte payloads and assert checksum and byte count equivalence after fetch writes.
- **Rationale**: Directly validates end-to-end archive integrity behavior without external data dependencies.
- **Alternatives considered**:
  - Checksum-only assertion: rejected because byte-size regressions could be missed.
  - Size-only assertion: rejected because corruption can preserve size.

## Decision 5: Keep test matrix explicitly mapped to FR and SC identifiers

- **Decision**: Track each planned test class/scenario against FR-001..FR-011 and SC-001..SC-005 in plan artifacts.
- **Rationale**: Provides auditable coverage and simplifies review of specification completeness.
- **Alternatives considered**:
  - Implicit narrative mapping only: rejected due to weaker traceability during review and regression triage.
