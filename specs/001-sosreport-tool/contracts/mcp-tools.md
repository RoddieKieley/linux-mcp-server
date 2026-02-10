# MCP Tool Contracts: sosreport

## Tool: generate_sosreport

**Purpose**: Generate a sosreport archive on a remote host and return metadata plus a fetch reference.

**Inputs**
- **host** (string, required): remote host identifier for SSH connection
- **only_plugins** (string list, optional)
- **enable_plugins** (string list, optional)
- **disable_plugins** (string list, optional)
- **log_size** (string, optional)
- **redaction** (boolean, optional, default true)

**Outputs**
- **archive**: SosreportArchive metadata
- **fetch_reference**: retrieval handle or reference string
- **warnings**: optional list of warnings (string list)

**Errors**
- `sos_not_installed`: sos package missing with installation guidance
- `insufficient_privileges`: cannot execute report with current permissions
- `timeout`: report generation exceeded configured timeout
- `validation_error`: invalid plugin names or invalid options

---

## Tool: fetch_sosreport

**Purpose**: Retrieve a generated sosreport archive using a reference from `generate_sosreport`.

**Inputs**
- **host** (string, required): remote host identifier for SSH connection
- **fetch_reference** (string, required)

**Outputs**
- **archive_path**: local path on MCP host where archive is stored
- **size_bytes**: file size in bytes
- **sha256**: checksum for integrity verification

**Errors**
- `not_found`: reference does not exist or remote file missing
- `timeout`: retrieval exceeded configured timeout
- `validation_error`: invalid reference or path
