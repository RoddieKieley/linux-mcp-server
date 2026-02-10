# Quickstart: linux-mcp-server sosreport tool

## Prerequisites

- Remote host reachable via SSH
- `sos` package installed on the remote host
- Permissions to run `sos report` (direct or via sudo)

## Example Flow

1. Call `generate_sosreport` with `host` and any optional scope or redaction settings.
2. Record the returned `fetch_reference` and archive metadata.
3. Call `fetch_sosreport` with the `fetch_reference` to retrieve the archive to the MCP host.
4. Verify the returned checksum if required by workflow.

## Expected Outcomes

- A compressed sosreport archive is generated on the remote host.
- The archive is retrieved to the MCP host via the separate fetch tool.
