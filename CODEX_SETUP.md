# Codex Quick Setup Guide - Fusion 360 MCP Server

Complete guide for configuring the Fusion 360 MCP Server with Codex.

---

## Important: Don't Use start.sh for MCP!

**start.sh** is for interactive/manual use only. It prints UI text that interferes with MCP's stdio protocol.

**For MCP clients (Codex, Claude Code, etc.):** Always run `python fusion_mcp_server.py` directly.

---

## Quick Setup (2 Commands)

```bash
# 1. Add the MCP server
codex mcp add fusion360-api -- \
  /home/lulubas/TOOLS/adk_API/venv/bin/python \
  /home/lulubas/TOOLS/adk_API/fusion_mcp_server.py

# 2. Verify it's enabled
codex mcp list
```

**Expected Output:**
```
Name           Command                                      Args  Status
fusion360-api  /home/lulubas/TOOLS/adk_API/venv/bin/python  -     enabled
```

Done! The server is now configured and should work with Codex.

---

## Codex MCP Commands

### List all configured servers
```bash
codex mcp list
```

### Get server details
```bash
codex mcp get fusion360-api
```

### Remove the server
```bash
codex mcp remove fusion360-api
```

---

## Testing the Server

Test in Codex:

```bash
# Start a Codex session
codex

# Use MCP tools - they should now appear!
# Try: explore_ui()
```

The server should now connect and tools should be available.

---

## Alternative: Using config.toml

If you prefer to use a config file instead of CLI:

### Location
`~/.codex/config.toml` or project-specific `config.toml`

### Configuration

**For native Linux/macOS:**
```toml
[mcpServers."fusion360-api"]
command = "/home/lulubas/TOOLS/adk_API/venv/bin/python"
args = ["/home/lulubas/TOOLS/adk_API/fusion_mcp_server.py"]
disabled = false
autoApprove = []
```

**For WSL users:**
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

**Important:** Use `python fusion_mcp_server.py` directly, NOT `./start.sh` - start.sh prints UI text that breaks MCP protocol!

### Apply configuration
```bash
# Copy the config file
cp config.toml ~/.codex/

# Or copy to your project directory for project-specific config
cp config.toml /path/to/your/project/
```

---

## Server Information

Once configured, you'll have access to:

### 9 Intelligent Tools:

**v2.0 Tools:**
1. `explore_ui()` - Discover all UI/GUI classes
2. `search_by_category()` - Search by semantic category
3. `get_full_class()` - Extract complete class definition
4. `search_api()` - Smart search (10+30 context)
5. `search_fusion_api()` - General search (20+20 context)

**v2.1 NEW Tools (10x faster):**
6. `find_class()` - Fast lookup with fuzzy search
7. `find_method()` - Find method across all classes
8. `get_class_hierarchy()` - Show inheritance tree
9. `list_all_classes()` - Instant class listing

### 9 Resources:
- `fusion://info` - Server information
- `fusion://version` - API version
- `fusion://core` - Core module
- `fusion://fusion` - Fusion module
- `fusion://cam` - CAM module
- `fusion://drawing` - Drawing module
- `fusion://volume` - Volume module
- `fusion://sim` - Simulation module
- `fusion://all` - All modules

---

## Example Usage in Codex

```bash
# Start Codex
codex

# In Codex session:
> explore_ui()
# Returns: Complete list of UI/GUI classes

> find_class("BRepBody")
# Returns: Fast lookup of BRepBody class

> search_api("CommandInput")
# Returns: Smart search with 10+30 context

> get_full_class("Sketch")
# Returns: Complete Sketch class definition
```

---

## Troubleshooting

### Server not appearing
```bash
# Check if it's configured
codex mcp list

# Should show fusion360-api as enabled
```

### Server status is "disabled"
```bash
# Remove and re-add
codex mcp remove fusion360-api
codex mcp add fusion360-api -- \
  /home/lulubas/TOOLS/adk_API/venv/bin/python \
  /home/lulubas/TOOLS/adk_API/fusion_mcp_server.py
```

### Tools not working
```bash
# Test the server manually first
cd /home/lulubas/TOOLS/adk_API
./start.sh

# If manual start works, check Codex configuration
codex mcp get fusion360-api
```

### Path issues
```bash
# Verify paths exist
ls -l /home/lulubas/TOOLS/adk_API/fusion_mcp_server.py
ls -l /home/lulubas/TOOLS/adk_API/venv/bin/python

# Both should exist and be accessible
```

---

## Configuration Comparison

### CLI Method (Recommended)
**Pros:**
- ✅ Global configuration (works everywhere)
- ✅ One command to set up
- ✅ Easy to manage (`list`, `get`, `remove`)
- ✅ No file editing required

**Cons:**
- ❌ Requires Codex CLI

### TOML Method
**Pros:**
- ✅ More configuration options
- ✅ Project-specific configs
- ✅ Version control friendly
- ✅ Can set environment variables

**Cons:**
- ❌ Manual file editing
- ❌ Must restart Codex after changes
- ❌ Path updates need manual editing

---

## Advanced Configuration

### Setting environment variables (TOML only)
```toml
[mcpServers."fusion360-api"]
command = "/home/lulubas/TOOLS/adk_API/venv/bin/python"
args = ["/home/lulubas/TOOLS/adk_API/fusion_mcp_server.py"]
disabled = false
autoApprove = []

[mcpServers."fusion360-api".env]
PYTHONUNBUFFERED = "1"
FUSION_API_PATH = "/custom/path"
MCP_DEBUG = "1"
```

### Auto-approve tools (use with caution)
```toml
[mcpServers."fusion360-api"]
command = "/home/lulubas/TOOLS/adk_API/venv/bin/python"
args = ["/home/lulubas/TOOLS/adk_API/fusion_mcp_server.py"]
disabled = false
autoApprove = ["explore_ui", "search_api", "find_class"]  # Specific tools
# OR
autoApprove = ["*"]  # All tools (not recommended for security)
```

---

## Multiple Codex Profiles

If you use different Codex profiles:

```bash
# Add to specific profile
codex --config profile=work mcp add fusion360-api -- ...

# Or add to global config (works for all profiles)
# Edit: ~/.codex/config.toml
```

---

## Updating the Server

When you update `fusion_mcp_server.py`:

```bash
# No need to reconfigure!
# Codex will use the updated version automatically

# Just restart your Codex session
```

If you move the server location:

```bash
# Remove old configuration
codex mcp remove fusion360-api

# Add with new path
codex mcp add fusion360-api -- \
  /new/path/to/venv/bin/python \
  /new/path/to/fusion_mcp_server.py
```

---

## Summary

**Fastest Setup:**
```bash
codex mcp add fusion360-api -- /home/lulubas/TOOLS/adk_API/venv/bin/python /home/lulubas/TOOLS/adk_API/fusion_mcp_server.py
```

**Verify:**
```bash
codex mcp list
```

**Test:**
```bash
codex
> explore_ui()
```

**That's it!** 🎉

---

## See Also

- [Complete Configuration Examples](CONFIG_EXAMPLES.md)
- [Full Setup Guide](MCP_SETUP_GUIDE.md)
- [Quick Reference](QUICK_REFERENCE.md)
- [Tool Documentation](README_MCP.md)

---

**Last Updated:** 2025-11-20
**Codex Version:** Experimental MCP support
**Status:** ⚠️ Configured but not yet functional (Codex MCP is experimental)

---

## 🔧 Working Alternatives Right Now

Since Codex MCP support is still experimental, use these **fully working** alternatives:

### 1. Claude Code (✅ WORKS NOW)
```bash
cp mcp_config_claude_code.json ~/.config/claude-code/mcp_config.json
```
Claude Code has full MCP support and works perfectly!

### 2. Cursor (✅ WORKS NOW)
```bash
mkdir -p ~/.cursor
cp mcp_config_generic.json ~/.cursor/mcp.json
```
Cursor has stable MCP support.

### 3. VSCode with MCP Extension (✅ WORKS NOW)
```bash
mkdir -p .vscode
cp mcp_config_vscode.json .vscode/mcp_config.json
```
VSCode MCP extension is working.

### 4. Cline (✅ WORKS NOW)
Full MCP support through VSCode extension.

**Recommendation:** Use Claude Code or Cursor while waiting for Codex MCP to mature.

---

## When Will Codex MCP Work?

Codex has added MCP commands (`codex mcp add/list/get/remove`), but the actual MCP protocol support appears incomplete. Monitor:
- Codex release notes
- Check `codex mcp list` for status changes
- Look for "Auth: Supported" instead of "Auth: Unsupported"
