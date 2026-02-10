# Sosreport Tools

## Sudoers setup (required)

The sosreport tools run with `sudo -n` and require NOPASSWD entries on the
remote host. Add the following lines to `/etc/sudoers.d/mcp-sos`:

```
mcp ALL=(root) NOPASSWD: /usr/bin/sos report --batch --tmp-dir /var/tmp --name linux-mcp-sos
mcp ALL=(root) NOPASSWD: /usr/bin/cat /var/tmp/sosreport-*-linux-mcp-sos-*.tar.xz
mcp ALL=(root) NOPASSWD: /usr/bin/cat /var/tmp/sosreport-*-linux-mcp-sos-*.tar.xz.sha256
```

Ensure the sudoers drop-in is owned by `root:root` and has permissions `0440`.

::::: linux_mcp_server.tools.sosreport
    options:
      show_root_heading: true
      show_root_full_path: false
