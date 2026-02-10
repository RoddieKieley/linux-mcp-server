# Implementation Plan: linux-mcp-server sosreport tool

**Branch**: `001-sosreport-tool` | **Date**: 2026-02-06 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-sosreport-tool/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Add MCP tools that generate sosreport archives on remote hosts and fetch them separately to the MCP host.
The plan builds on existing SSH command execution and tool patterns, adds explicit validation, and
documents the report structure and retrieval workflow.

## Technical Context

**Language/Version**: Python >=3.10  
**Primary Dependencies**: fastmcp, asyncssh, pydantic, pydantic-settings  
**Storage**: N/A (file system for report staging only)  
**Testing**: pytest, pytest-asyncio, pytest-mock  
**Target Platform**: Linux server (MCP host) and remote Linux hosts (Fedora 43+, RHEL 9+)  
**Project Type**: single service (MCP server library + CLI)  
**Performance Goals**: default report completes under 10 minutes; fetch for <500 MB completes under 2 minutes on LAN  
**Constraints**: read-only tool behavior; command timeouts enforced; avoid large inline payloads  
**Scale/Scope**: per-host on-demand report generation; no concurrent batch processing assumptions

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- No constitution content defined in `.specify/memory/constitution.md`; no explicit gates to evaluate.

## Project Structure

### Documentation (this feature)

```text
specs/001-sosreport-tool/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)
<!--
  ACTION REQUIRED: Replace the placeholder tree below with the concrete layout
  for this feature. Delete unused options and expand the chosen structure with
  real paths (e.g., apps/admin, packages/something). The delivered plan must
  not include Option labels.
-->

```text
src/linux_mcp_server/
├── commands.py
├── tools/
│   ├── __init__.py
│   └── sosreport.py          # new tool(s)
├── utils/
└── connection/

tests/
├── tools/
│   └── test_sosreport.py
└── utils/
```

**Structure Decision**: Single project layout; new MCP tools live in `src/linux_mcp_server/tools/`,
with tests in `tests/tools/` and tool registry updates in `src/linux_mcp_server/commands.py`.

## Complexity Tracking

No constitution violations to justify.
