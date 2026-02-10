"""sosreport generation and retrieval tools."""

import hashlib
import re
import typing as t

from datetime import datetime
from pathlib import Path

from fastmcp.exceptions import ToolError
from mcp.types import ToolAnnotations
from pydantic import Field

from linux_mcp_server.audit import log_tool_call
from linux_mcp_server.commands import get_command
from linux_mcp_server.config import CONFIG
from linux_mcp_server.models import SosreportArchive
from linux_mcp_server.models import SosreportOptions
from linux_mcp_server.server import mcp
from linux_mcp_server.utils.decorators import disallow_local_execution_in_containers
from linux_mcp_server.utils.types import Host
from linux_mcp_server.utils.validation import validate_log_size
from linux_mcp_server.utils.validation import validate_plugin_scope
from linux_mcp_server.utils.validation import validate_plugin_values
from linux_mcp_server.utils.validation import validate_path

_REPORT_PATH_RE = re.compile(r"(/[^\\s]+?sosreport[^\\s]+?\\.(?:tar\\.xz|tar\\.gz))")


def _extract_report_path(stdout: str, stderr: str) -> str:
    combined = "\n".join([stdout or "", stderr or ""])
    matches = _REPORT_PATH_RE.findall(combined)
    if not matches:
        raise ToolError("Unable to determine sosreport archive path from command output.")
    return matches[-1]


def _local_reports_dir() -> Path:
    return CONFIG.log_dir.parent / "reports"


@mcp.tool(
    title="Generate sosreport",
    description="Generate an sosreport archive on a remote host.",
    tags={"diagnostics", "support", "sosreport"},
    annotations=ToolAnnotations(readOnlyHint=True),
)
@log_tool_call
@disallow_local_execution_in_containers
async def generate_sosreport(
    host: Host = None,
    only_plugins: t.Annotated[
        list[str] | None,
        Field(description="List of plugin names to include", examples=[["kernel", "network"]]),
    ] = None,
    enable_plugins: t.Annotated[
        list[str] | None,
        Field(description="List of plugin names to enable", examples=[["systemd", "selinux"]]),
    ] = None,
    disable_plugins: t.Annotated[
        list[str] | None,
        Field(description="List of plugin names to disable", examples=[["docker", "podman"]]),
    ] = None,
    log_size: t.Annotated[
        str | None,
        Field(description="Log size limit passed to sosreport (e.g., 50M)"),
    ] = None,
    redaction: t.Annotated[
        bool,
        Field(description="Whether to keep sosreport redaction enabled (default true)"),
    ] = True,
) -> dict[str, t.Any]:
    """Generate a sosreport archive and return metadata plus a fetch reference."""
    try:
        validated_only = validate_plugin_values(only_plugins, "only_plugins")
        validated_enable = validate_plugin_values(enable_plugins, "enable_plugins")
        validated_disable = validate_plugin_values(disable_plugins, "disable_plugins")
        validate_plugin_scope(validated_only, validated_enable, validated_disable)
        validated_log_size = validate_log_size(log_size)
    except ValueError as exc:
        raise ToolError(str(exc)) from exc

    version_cmd = get_command("sosreport", "version")
    version_code, _, version_err = await version_cmd.run(host=host)
    if version_code != 0:
        raise ToolError(
            "sos is not installed on the target host. Install it with: dnf install sos"
            f" (error: {version_err.strip()})"
        )

    cmd = get_command("sosreport", "generate")
    try:
        returncode, stdout, stderr = await cmd.run(
            host=host,
            only_plugins=",".join(validated_only) if validated_only else None,
            enable_plugins=",".join(validated_enable) if validated_enable else None,
            disable_plugins=",".join(validated_disable) if validated_disable else None,
            log_size=validated_log_size,
            redaction_disabled=not redaction,
        )
    except ConnectionError as exc:
        message = str(exc)
        if "timed out" in message:
            raise ToolError("sosreport command timed out before completion.") from exc
        raise ToolError(f"Failed to execute sosreport: {message}") from exc

    if returncode != 0:
        combined = "\n".join([stdout or "", stderr or ""]).lower()
        if "permission denied" in combined or "superuser" in combined or "root" in combined:
            raise ToolError("Insufficient privileges to run sosreport on the target host.")
        raise ToolError(f"sosreport command failed with exit code {returncode}: {stderr or stdout}")

    report_path = _extract_report_path(stdout, stderr)
    validated_path = validate_path(report_path)

    stat_cmd = get_command("sosreport", "stat")
    stat_code, stat_out, stat_err = await stat_cmd.run(host=host, path=validated_path)
    if stat_code != 0:
        raise ToolError(f"Unable to stat sosreport archive: {stat_err or stat_out}")

    stat_parts = stat_out.strip().split()
    if len(stat_parts) != 2:
        raise ToolError(f"Unexpected stat output: {stat_out}")

    size_bytes = int(stat_parts[0])
    created_at = datetime.fromtimestamp(int(stat_parts[1]))

    archive = SosreportArchive(
        id=str(validated_path),
        remote_path=str(validated_path),
        filename=Path(validated_path).name,
        size_bytes=size_bytes,
        created_at=created_at,
        host=host or "",
    )

    options = SosreportOptions(
        only_plugins=validated_only,
        enable_plugins=validated_enable,
        disable_plugins=validated_disable,
        log_size=validated_log_size,
        redaction=redaction,
    )

    return {"archive": archive, "fetch_reference": archive.remote_path, "options": options}


@mcp.tool(
    title="Fetch sosreport",
    description="Fetch a generated sosreport archive to the MCP host.",
    tags={"diagnostics", "support", "sosreport"},
    annotations=ToolAnnotations(readOnlyHint=True),
)
@log_tool_call
@disallow_local_execution_in_containers
async def fetch_sosreport(
    fetch_reference: t.Annotated[
        str,
        Field(description="Reference returned by generate_sosreport (remote archive path)"),
    ],
    host: Host = None,
) -> dict[str, t.Any]:
    """Fetch a sosreport archive from the remote host."""
    validated_path = validate_path(fetch_reference)
    cmd = get_command("read_file")

    try:
        returncode, stdout, stderr = await cmd.run_bytes(host=host, path=validated_path)
    except ConnectionError as exc:
        message = str(exc)
        if "timed out" in message:
            raise ToolError("Fetching sosreport timed out before completion.") from exc
        raise ToolError(f"Failed to fetch sosreport: {message}") from exc

    if returncode != 0:
        raise ToolError(f"Unable to read sosreport archive: {stderr}")

    local_dir = _local_reports_dir()
    local_dir.mkdir(parents=True, exist_ok=True)
    local_path = local_dir / Path(validated_path).name
    local_path.write_bytes(stdout)

    sha256 = hashlib.sha256(stdout).hexdigest()
    return {
        "archive_path": str(local_path),
        "size_bytes": len(stdout),
        "sha256": sha256,
    }
