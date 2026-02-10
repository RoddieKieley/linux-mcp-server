# Data Model: linux-mcp-server sosreport tool

## Entities

### SosreportArchive

- **id**: unique handle for retrieval (string)
- **remote_path**: absolute path on remote host (string)
- **filename**: archive file name (string)
- **size_bytes**: archive size in bytes (integer)
- **created_at**: report creation timestamp (string, ISO 8601)
- **host**: remote host identifier (string)

### SosreportOptions

- **only_plugins**: list of plugin names to include (string list)
- **enable_plugins**: list of plugin names to enable (string list)
- **disable_plugins**: list of plugin names to disable (string list)
- **log_size**: log size limit (string, tool-validated)
- **redaction**: whether redaction is enabled (boolean, default true)

## Relationships

- `SosreportOptions` are supplied to generate one `SosreportArchive`.
