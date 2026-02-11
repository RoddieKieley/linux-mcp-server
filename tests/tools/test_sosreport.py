"""Tests for sosreport generation and retrieval tools."""

import hashlib

from pathlib import Path

import pytest

from fastmcp.exceptions import ToolError


@pytest.fixture
def patched_reports_dir(mocker, tmp_path):
    """Patch the local reports directory used by fetch_sosreport."""
    log_dir = tmp_path / "logs"
    log_dir.mkdir()
    mock_config = mocker.patch("linux_mcp_server.tools.sosreport.CONFIG")
    mock_config.log_dir = log_dir
    return tmp_path / "reports"


def _assert_tool_error(exc_info: pytest.ExceptionInfo[ToolError], expected_fragment: str) -> None:
    """Normalize error text matching across MCP tool call failures."""
    assert expected_fragment in str(exc_info.value)


def _sha256_hex(payload: bytes) -> str:
    """Create deterministic integrity values for retrieval assertions."""
    return hashlib.sha256(payload).hexdigest()


class TestGenerateSosreport:
    """Coverage for generate_sosreport command behavior and mapping."""

    async def test_generate_sosreport_success_with_options(self, mcp_client, mock_execute_with_fallback):
        """FR-001/FR-008/FR-011, SC-001/SC-005."""
        mock_execute_with_fallback.side_effect = [
            (0, "sos --help output", ""),
            (
                0,
                "Your sosreport has been generated and saved in: "
                "/var/tmp/sosreport-node1-linux-mcp-sos-2026-02-10-a1b2c3.tar.xz",
                "",
            ),
            (0, "4096 1700000000", ""),
        ]

        result = await mcp_client.call_tool(
            "generate_sosreport",
            arguments={
                "host": "remote.example.com",
                "only_plugins": ["kernel", "network"],
                "log_size": "50M",
                "redaction": False,
            },
        )
        content = result.structured_content

        assert content["fetch_reference"] == "/var/tmp/sosreport-node1-linux-mcp-sos-2026-02-10-a1b2c3.tar.xz"
        assert content["archive"]["remote_path"] == content["fetch_reference"]
        assert content["archive"]["filename"] == "sosreport-node1-linux-mcp-sos-2026-02-10-a1b2c3.tar.xz"
        assert content["archive"]["size_bytes"] == 4096
        assert content["options"]["only_plugins"] == ["kernel", "network"]
        assert content["options"]["enable_plugins"] == []
        assert content["options"]["disable_plugins"] == []
        assert content["options"]["log_size"] == "50M"
        assert content["options"]["redaction"] is False

        assert mock_execute_with_fallback.call_count == 3
        version_cmd = mock_execute_with_fallback.call_args_list[0].args[0]
        generate_cmd = mock_execute_with_fallback.call_args_list[1].args[0]
        stat_cmd = mock_execute_with_fallback.call_args_list[2].args[0]
        generate_kwargs = mock_execute_with_fallback.call_args_list[1].kwargs

        assert version_cmd == ("sos", "--help")
        assert generate_cmd[:6] == ("sudo", "-n", "/usr/bin/sos", "report", "--batch", "--tmp-dir")
        assert "--only-plugins" in generate_cmd
        assert "kernel,network" in generate_cmd
        assert "--log-size" in generate_cmd
        assert "50M" in generate_cmd
        assert "--no-clean" in generate_cmd
        assert stat_cmd[:3] == ("stat", "-c", "%s %Y")
        assert generate_kwargs["host"] == "remote.example.com"

    async def test_generate_sosreport_resolves_var_tmp_from_filename_pattern(
        self, mcp_client, mock_execute_with_fallback
    ):
        """FR-004, SC-005."""
        report_name = "sosreport-node2-linux-mcp-sos-2026-02-10-def456.tar.xz"
        mock_execute_with_fallback.side_effect = [
            (0, "sos --help output", ""),
            (0, f"Report archive: {report_name}", ""),
            (0, "1024 1700000001", ""),
        ]

        result = await mcp_client.call_tool("generate_sosreport", arguments={"host": "remote.example.com"})
        content = result.structured_content

        assert content["fetch_reference"] == f"/var/tmp/{report_name}"
        stat_cmd = mock_execute_with_fallback.call_args_list[2].args[0]
        assert stat_cmd[-1] == f"/var/tmp/{report_name}"

    async def test_generate_sosreport_uses_latest_named_fallback(self, mcp_client, mock_execute_with_fallback):
        """FR-004, SC-005."""
        mock_execute_with_fallback.side_effect = [
            (0, "sos --help output", ""),
            (0, "sos completed", ""),
            (0, "/var/tmp/sosreport-node3-linux-mcp-sos-2026-02-10-ghi789.tar.xz\n", ""),
            (0, "2048 1700000002", ""),
        ]

        result = await mcp_client.call_tool("generate_sosreport", arguments={"host": "remote.example.com"})
        content = result.structured_content

        assert content["fetch_reference"] == "/var/tmp/sosreport-node3-linux-mcp-sos-2026-02-10-ghi789.tar.xz"
        latest_named_cmd = mock_execute_with_fallback.call_args_list[2].args[0]
        assert latest_named_cmd[0] == "sh"
        assert "ls -t /var/tmp/sosreport-*-linux-mcp-sos-*.tar.xz" in latest_named_cmd[2]

    async def test_generate_sosreport_sudo_password_required(self, mcp_client, mock_execute_with_fallback):
        """FR-002, SC-002."""
        mock_execute_with_fallback.side_effect = [
            (0, "sos --help output", ""),
            (1, "", "sudo: a password is required"),
        ]

        with pytest.raises(ToolError) as exc_info:
            await mcp_client.call_tool("generate_sosreport", arguments={"host": "remote.example.com"})
        _assert_tool_error(exc_info, "Configure NOPASSWD for the sos command")

    async def test_generate_sosreport_permission_denied(self, mcp_client, mock_execute_with_fallback):
        """FR-003/FR-006, SC-002."""
        mock_execute_with_fallback.side_effect = [
            (0, "sos --help output", ""),
            (1, "", "permission denied"),
        ]

        with pytest.raises(ToolError) as exc_info:
            await mcp_client.call_tool("generate_sosreport", arguments={"host": "remote.example.com"})
        _assert_tool_error(exc_info, "Insufficient privileges to run sosreport")

    async def test_generate_sosreport_timeout(self, mcp_client, mock_execute_with_fallback):
        """FR-003, SC-002."""
        mock_execute_with_fallback.side_effect = [
            (0, "sos --help output", ""),
            ConnectionError("ssh command timed out after 300 seconds"),
        ]

        with pytest.raises(ToolError) as exc_info:
            await mcp_client.call_tool("generate_sosreport", arguments={"host": "remote.example.com"})
        _assert_tool_error(exc_info, "sosreport command timed out before completion")

    @pytest.mark.parametrize(
        ("kwargs", "match"),
        [
            ({"only_plugins": []}, "only_plugins cannot be empty"),
            ({"only_plugins": ["bad plugin"]}, "Invalid plugin name"),
            (
                {"only_plugins": ["kernel"], "enable_plugins": ["network"]},
                "only_plugins cannot be combined with enable_plugins or disable_plugins",
            ),
            ({"log_size": "ten-megabytes"}, "log_size must be a number optionally suffixed"),
        ],
    )
    async def test_generate_sosreport_invalid_inputs(self, mcp_client, mock_execute_with_fallback, kwargs, match):
        """FR-009, SC-004."""
        with pytest.raises(ToolError, match=match):
            await mcp_client.call_tool("generate_sosreport", arguments={"host": "remote.example.com", **kwargs})

        mock_execute_with_fallback.assert_not_called()


class TestFetchSosreport:
    """Coverage for fetch_sosreport command behavior and integrity."""

    async def test_fetch_sosreport_success_and_binary_integrity(
        self, mcp_client, mock_execute_with_fallback, patched_reports_dir
    ):
        """FR-005/FR-007/FR-011, SC-001/SC-003."""
        payload = b"\x1f\x8b\x08\x00\x00\x00\x00\x00binary-sosreport-content"
        remote_path = "/var/tmp/sosreport-node4-linux-mcp-sos-2026-02-10-xyz000.tar.xz"
        expected_sha256 = _sha256_hex(payload)

        mock_execute_with_fallback.return_value = (0, payload, b"")

        result = await mcp_client.call_tool(
            "fetch_sosreport",
            arguments={"fetch_reference": remote_path, "host": "remote.example.com"},
        )
        content = result.structured_content

        local_path = Path(content["archive_path"])
        assert local_path == patched_reports_dir / Path(remote_path).name
        assert local_path.read_bytes() == payload
        assert content["size_bytes"] == len(payload)
        assert content["sha256"] == expected_sha256

        cmd_args = mock_execute_with_fallback.call_args.args[0]
        call_kwargs = mock_execute_with_fallback.call_args.kwargs
        assert cmd_args[:3] == ("sudo", "-n", "/usr/bin/cat")
        assert cmd_args[-1] == remote_path
        assert call_kwargs["host"] == "remote.example.com"
        assert call_kwargs["encoding"] is None

    async def test_fetch_sosreport_sudo_password_required(self, mcp_client, mock_execute_with_fallback):
        """FR-006, SC-002."""
        mock_execute_with_fallback.return_value = (1, b"", b"sudo: a password is required")

        with pytest.raises(ToolError) as exc_info:
            await mcp_client.call_tool(
                "fetch_sosreport",
                arguments={
                    "fetch_reference": "/var/tmp/sosreport-node5-linux-mcp-sos-2026-02-10-aaa111.tar.xz",
                    "host": "remote.example.com",
                },
            )
        _assert_tool_error(exc_info, "Configure NOPASSWD for /usr/bin/cat")

    async def test_fetch_sosreport_access_denied_message(self, mcp_client, mock_execute_with_fallback):
        """FR-006, SC-002."""
        mock_execute_with_fallback.return_value = (
            1,
            b"",
            b"cat: /var/tmp/sosreport-node6.tar.xz: Permission denied",
        )

        with pytest.raises(ToolError, match="Unable to read sosreport archive: .*Permission denied"):
            await mcp_client.call_tool(
                "fetch_sosreport",
                arguments={"fetch_reference": "/var/tmp/sosreport-node6.tar.xz", "host": "remote.example.com"},
            )

    async def test_fetch_sosreport_timeout(self, mcp_client, mock_execute_with_fallback):
        """FR-006, SC-002."""
        mock_execute_with_fallback.side_effect = ConnectionError("scp timed out while reading archive")

        with pytest.raises(ToolError) as exc_info:
            await mcp_client.call_tool(
                "fetch_sosreport",
                arguments={"fetch_reference": "/var/tmp/sosreport-node7.tar.xz", "host": "remote.example.com"},
            )
        _assert_tool_error(exc_info, "Fetching sosreport timed out before completion")

    @pytest.mark.parametrize(
        ("fetch_reference", "match"),
        [
            ("", "Path cannot be empty"),
            ("relative/path.tar.xz", "Path must be absolute"),
            ("/var/tmp/bad\npath.tar.xz", "Path contains invalid characters"),
            ("-invalid.tar.xz", "Path cannot start with '-'"),
        ],
    )
    async def test_fetch_sosreport_invalid_fetch_reference(
        self, mcp_client, mock_execute_with_fallback, fetch_reference, match
    ):
        """FR-009, SC-004."""
        with pytest.raises(ToolError, match=match):
            await mcp_client.call_tool(
                "fetch_sosreport",
                arguments={"fetch_reference": fetch_reference, "host": "remote.example.com"},
            )

        mock_execute_with_fallback.assert_not_called()
