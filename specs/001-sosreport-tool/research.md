# Research: linux-mcp-server sosreport tool

## Sosreport structure and contents

**Decision**: Treat sosreport as a read-only diagnostic snapshot and expose metadata plus a separate fetch step.
**Rationale**: Sosreport is a read-only archive that bundles system configuration, logs, and runtime information.
It is commonly produced as a compressed archive and later uploaded or retrieved for support review.
**Alternatives considered**: Inline payload return for all cases, but large archives make this impractical.

**Supporting details (reference)**:
- Sosreport is a standardized diagnostic snapshot that collects configuration, logs, and hardware details.
- Typical output is a compressed archive like `sosreport-<host>-<date>-<id>.tar.xz`.
- The extracted archive contains a predictable structure with `sosreport.log`, `sos_commands/`, `etc/`,
  `proc/`, `sys/`, `var/`, `usr/`, and `version.txt`.

## Redaction and privacy expectations

**Decision**: Provide explicit redaction control while defaulting to redaction enabled.
**Rationale**: Sosreport supports redaction and is commonly reviewed for sensitive data before sharing;
operators require control in support workflows.
**Alternatives considered**: Always redacted, but this can remove data needed for diagnosis.

## Retrieval workflow

**Decision**: Use a separate fetch tool that retrieves the report using a returned reference.
**Rationale**: Separate retrieval avoids large inline payloads and aligns with command execution limitations.
**Alternatives considered**: Inline payloads or dual-mode responses, but they add response size risks.
