# Fusion 360 MCP Server - Working Status

Quick reference for which AI agents currently support the MCP server.

---

## ✅ FULLY WORKING

These clients have **stable MCP support** and work perfectly:

⚠️ **IMPORTANT:** Always use `python fusion_mcp_server.py` directly for MCP clients, NOT `start.sh`!
- `start.sh` is for interactive/manual testing only
- It prints UI text that breaks MCP's stdio protocol

### 1. Claude Code ⭐ RECOMMENDED
**Status:** ✅ Fully functional
**Setup:** Copy `mcp_config_claude_code.json` to `~/.config/claude-code/mcp_config.json`
**Notes:** Best MCP implementation, official support from Anthropic

```bash
cp mcp_config_claude_code.json ~/.config/claude-code/mcp_config.json
```

### 2. Cursor
**Status:** ✅ Fully functional
**Setup:** Copy `mcp_config_generic.json` to `~/.cursor/mcp.json`
**Notes:** Stable MCP support, good integration

```bash
mkdir -p ~/.cursor
cp mcp_config_generic.json ~/.cursor/mcp.json
```

### 3. VSCode MCP Extension
**Status:** ✅ Fully functional
**Setup:** Copy `mcp_config_vscode.json` to `.vscode/mcp_config.json`
**Notes:** Works well for project-specific MCP servers

```bash
mkdir -p .vscode
cp mcp_config_vscode.json .vscode/mcp_config.json
```

### 4. Cline (VSCode Extension)
**Status:** ✅ Fully functional
**Setup:** Copy config to Cline's settings directory
**Notes:** Good VSCode integration

**Linux:**
```bash
cp mcp_config_generic.json ~/.config/Code/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json
```

**macOS:**
```bash
cp mcp_config_generic.json ~/Library/Application\ Support/Code/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json
```

---

### 5. Codex
**Status:** ✅ Fully functional (when configured correctly!)
**Important:** Must use `python fusion_mcp_server.py` directly, NOT `start.sh`

**Setup via config.toml (recommended for WSL):**
```toml
[mcpServers."fusion360-api"]
command = "wsl"
args = [
  "bash",
  "-c",
  "cd /home/lulubas/TOOLS/adk_API && source venv/bin/activate && python fusion_mcp_server.py"
]
disabled = false
autoApprove = []
```

**Why not start.sh?**
- start.sh prints UI/debug text that interferes with MCP's stdio protocol
- MCP requires clean stdin/stdout for communication
- Always use the python script directly for MCP clients

---

## ❓ UNKNOWN / REQUIRES GATEWAY

### 6. Google Gemini
**Status:** ❓ Requires third-party gateway
**Issue:** No native MCP support
**Workaround:** Use MCP-to-API gateway (community project)

**Notes:** Not officially supported. Would require:
1. MCP gateway service
2. API proxy setup
3. Custom integration

**Recommendation:** Use Gemini through compatible clients (Cursor, Claude Code) if they support model switching.

---

## Quick Recommendations

### For Production Use NOW:
1. **Claude Code** - Best choice, official support
2. **Cursor** - Great alternative
3. **Codex** - Full MCP support (use config.toml, not start.sh)
4. **VSCode MCP Extension** - Good for project-specific needs
5. **Cline** - Full support via VSCode

### For Future Use:
- **Gemini** - Use through compatible clients or wait for native support

---

## Testing Your Setup

### Test with Claude Code (Recommended):
```bash
# 1. Copy config
cp mcp_config_claude_code.json ~/.config/claude-code/mcp_config.json

# 2. Start Claude Code
claude-code

# 3. Test a tool
> explore_ui()

# Should return: Complete list of UI/GUI classes
```

### Test with Cursor:
```bash
# 1. Copy config
mkdir -p ~/.cursor
cp mcp_config_generic.json ~/.cursor/mcp.json

# 2. Restart Cursor

# 3. Check MCP servers in settings

# 4. Test a tool
> find_class("BRepBody")
```

---

## Troubleshooting

### Server Not Appearing
**Check:** Configuration file location and format
**Verify:** Paths are correct for your system
**Test:** Run `./start.sh` manually to verify server works

### Server Shows but Tools Don't Work
**Check:** Virtual environment exists
**Verify:** MCP packages installed
**Test:** Run server manually: `source venv/bin/activate && python fusion_mcp_server.py`

### Codex Shows "Unsupported"
**This is expected** - Codex MCP support is incomplete
**Wait for:** Future Codex updates
**Use instead:** Claude Code or Cursor

---

## Version Compatibility

| Client | Version | MCP Support | Status | Note |
|--------|---------|-------------|--------|------|
| Claude Code | Latest | ✅ Full | Working | Best choice |
| Cursor | Latest | ✅ Stable | Working | Great alternative |
| Codex | Latest | ✅ Stable | Working | Use python directly, not start.sh |
| VSCode MCP Ext | Latest | ✅ Stable | Working | Project-specific |
| Cline | Latest | ✅ Stable | Working | VSCode extension |
| Gemini | - | ❌ None | Not working | Requires gateway |

---

## Summary

**Working NOW (5 options):**
- ✅ Claude Code (recommended)
- ✅ Cursor
- ✅ Codex (use python directly, not start.sh)
- ✅ VSCode MCP Extension
- ✅ Cline

**Not Working Yet (1 option):**
- ❓ Gemini (requires custom gateway)

**Best Choice:** Use **Claude Code** for best experience, or **Cursor** as alternative.

---

## Documentation

- **[CODEX_SETUP.md](CODEX_SETUP.md)** - Codex setup (when it works)
- **[CONFIG_EXAMPLES.md](CONFIG_EXAMPLES.md)** - All configuration examples
- **[MCP_SETUP_GUIDE.md](MCP_SETUP_GUIDE.md)** - Complete setup guide
- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - Tool usage reference

---

**Last Updated:** 2025-11-20
**Server Version:** 2.1
**MCP Support:** 4 working clients, 2 experimental/unsupported
