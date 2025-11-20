# Fusion 360 MCP Server - Configuration Examples

Quick reference guide for configuring the Fusion 360 MCP Server with different AI agents and IDEs.

---

## Table of Contents

1. [Claude Code](#1-claude-code)
2. [Codex / VSCode (TOML)](#2-codex--vscode-toml)
3. [VSCode with MCP Extension](#3-vscode-with-mcp-extension)
4. [Cline (VSCode Extension)](#4-cline-vscode-extension)
5. [Cursor](#5-cursor)
6. [Google Gemini](#6-google-gemini-via-gateway)
7. [Windows Configuration](#7-windows-configuration)
8. [Pre-configured Files](#8-pre-configured-files)

---

## 1. Claude Code

**Config File:** `~/.config/claude-code/mcp_config.json`

```json
{
  "mcpServers": {
    "fusion360-api": {
      "command": "/home/lulubas/TOOLS/adk_API/venv/bin/python",
      "args": [
        "/home/lulubas/TOOLS/adk_API/fusion_mcp_server.py"
      ],
      "env": {}
    }
  }
}
```

**Quick Setup:**
```bash
cp mcp_config_claude_code.json ~/.config/claude-code/mcp_config.json
```

---

## 2. Codex / VSCode (CLI or TOML)

⚠️ **IMPORTANT: Don't use `start.sh` for MCP!**
- `start.sh` prints UI text that breaks MCP stdio protocol
- Always use `python fusion_mcp_server.py` directly for MCP clients

### Method 1: Codex CLI

```bash
# Add the MCP server globally
codex mcp add fusion360-api -- /home/lulubas/TOOLS/adk_API/venv/bin/python /home/lulubas/TOOLS/adk_API/fusion_mcp_server.py

# Verify it was added
codex mcp list

# Check server details
codex mcp get fusion360-api

# Remove if needed
codex mcp remove fusion360-api
```

**Status Check:**
```
Name           Command                                      Args  Status
fusion360-api  /home/lulubas/TOOLS/adk_API/venv/bin/python  -     enabled
```

Server should now connect and tools should be available in Codex!

### Method 2: Config File (TOML)

**Config File:** `config.toml` (in your Codex workspace)

#### For WSL Users:
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

**Important:** Use `python fusion_mcp_server.py` directly, NOT `./start.sh`!

#### For Native Linux/macOS:
```toml
[mcpServers."fusion360-api"]
command = "/home/lulubas/TOOLS/adk_API/venv/bin/python"
args = ["/home/lulubas/TOOLS/adk_API/fusion_mcp_server.py"]
disabled = false
autoApprove = []
```

**Quick Setup:**
```bash
cp config.toml /path/to/your/codex/workspace/
```

---

## 3. VSCode with MCP Extension

**Config File:** `.vscode/mcp_config.json` (in your project root)

```json
{
  "mcpServers": {
    "fusion360-api": {
      "command": "/home/lulubas/TOOLS/adk_API/venv/bin/python",
      "args": [
        "/home/lulubas/TOOLS/adk_API/fusion_mcp_server.py"
      ],
      "env": {
        "PYTHONUNBUFFERED": "1"
      }
    }
  }
}
```

**Quick Setup:**
```bash
mkdir -p .vscode
cp mcp_config_vscode.json .vscode/mcp_config.json
```

---

## 4. Cline (VSCode Extension)

**Config File (Linux):**
```
~/.config/Code/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json
```

**Config File (macOS):**
```
~/Library/Application Support/Code/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json
```

**Configuration:**
```json
{
  "mcpServers": {
    "fusion360-api": {
      "command": "/home/lulubas/TOOLS/adk_API/venv/bin/python",
      "args": [
        "/home/lulubas/TOOLS/adk_API/fusion_mcp_server.py"
      ]
    }
  }
}
```

---

## 5. Cursor

**Config File:** `~/.cursor/mcp.json`

```json
{
  "mcpServers": {
    "fusion360-api": {
      "command": "/home/lulubas/TOOLS/adk_API/venv/bin/python",
      "args": [
        "/home/lulubas/TOOLS/adk_API/fusion_mcp_server.py"
      ],
      "env": {}
    }
  }
}
```

**Quick Setup:**
```bash
mkdir -p ~/.cursor
cp mcp_config_generic.json ~/.cursor/mcp.json
```

---

## 6. Google Gemini (via Gateway)

**Note:** Gemini requires an MCP-to-API gateway as it doesn't natively support MCP.

### Option 1: Using MCP Gateway (Community)

1. **Install Gateway:**
   ```bash
   npm install -g mcp-gateway
   ```

2. **Configure:**
   ```bash
   mcp-gateway configure \
     --server fusion360-api \
     --command "/home/lulubas/TOOLS/adk_API/venv/bin/python" \
     --args "/home/lulubas/TOOLS/adk_API/fusion_mcp_server.py" \
     --port 8080
   ```

3. **Connect Gemini:**
   Point your Gemini API client to: `http://localhost:8080`

### Option 2: Using Compatible MCP Clients

Use Gemini through MCP clients that support model switching:
- Claude Code (with Gemini API key)
- Cursor (with Gemini integration)
- Custom MCP implementations

---

## 7. Windows Configuration

**Config File:** Same locations as above, but with Windows paths

### Example for Claude Code:
```json
{
  "mcpServers": {
    "fusion360-api": {
      "command": "C:\\Users\\YourUsername\\TOOLS\\adk_API\\venv\\Scripts\\python.exe",
      "args": [
        "C:\\Users\\YourUsername\\TOOLS\\adk_API\\fusion_mcp_server.py"
      ],
      "env": {
        "PYTHONUNBUFFERED": "1"
      }
    }
  }
}
```

**Important:**
- Use double backslashes `\\` for Windows paths
- Replace `YourUsername` with your actual Windows username
- Use `python.exe` instead of `python`
- Path: `venv\\Scripts\\python.exe` (not `venv/bin/python`)

**Quick Setup:**
```powershell
copy mcp_config_windows.json %USERPROFILE%\.config\claude-code\mcp_config.json
```

---

## 8. Pre-configured Files

This repository includes ready-to-use configuration files:

| File | For | Format |
|------|-----|--------|
| `config.toml` | Codex / VSCode | TOML |
| `mcp_config_claude_code.json` | Claude Code | JSON |
| `mcp_config_vscode.json` | VSCode MCP Extension | JSON |
| `mcp_config_generic.json` | Cursor / Other | JSON |
| `mcp_config_windows.json` | Windows Systems | JSON |

### Usage:

1. **Copy the appropriate file** to your config location
2. **Update paths** if your installation is in a different location
3. **Restart your MCP client** to load the configuration

---

## Path Reference

### Default Installation Paths:

| Component | Path |
|-----------|------|
| Server Script | `/home/lulubas/TOOLS/adk_API/fusion_mcp_server.py` |
| Python Venv | `/home/lulubas/TOOLS/adk_API/venv/bin/python` |
| Start Script | `/home/lulubas/TOOLS/adk_API/start.sh` |
| API Files | `/home/lulubas/TOOLS/adk_API/API/Python/defs/adsk/` |

### For Windows:

| Component | Path |
|-----------|------|
| Server Script | `C:\Users\YourUser\TOOLS\adk_API\fusion_mcp_server.py` |
| Python Venv | `C:\Users\YourUser\TOOLS\adk_API\venv\Scripts\python.exe` |
| API Files | `C:\Users\YourUser\TOOLS\adk_API\API\Python\defs\adsk\` |

---

## Environment Variables (Optional)

You can add these to the `env` section of your configuration:

```json
"env": {
  "PYTHONUNBUFFERED": "1",          // Disable Python output buffering (recommended)
  "FUSION_API_PATH": "/custom/path", // Custom API path (if needed)
  "MCP_DEBUG": "1"                   // Enable MCP debug mode (troubleshooting)
}
```

---

## Testing Your Configuration

After configuring, test the connection:

1. **Start your MCP client** (Claude Code, VSCode, Cursor, etc.)
2. **Check for the server** named `fusion360-api`
3. **Verify tools are available:**
   - Should see 9 tools listed
   - Should see 9 resources available
4. **Test a tool:**
   ```
   explore_ui()
   ```
5. **Test a resource:**
   ```
   fusion://info
   ```

---

## Troubleshooting

### Common Issues:

**Server not appearing in client:**
- Check path to `fusion_mcp_server.py` is correct
- Verify Python venv path is correct
- Check file permissions (should be executable)

**Connection errors:**
- Ensure virtual environment is created (`./install.sh`)
- Verify MCP packages are installed
- Check Python version is 3.8+

**Tools not working:**
- Verify API files exist in `./API/Python/defs/adsk/`
- Check server logs for errors
- Test manual start: `./start.sh`

---

## Quick Setup Commands

```bash
# 1. Clone/navigate to directory
cd /home/lulubas/TOOLS/adk_API

# 2. Install dependencies
./install.sh

# 3. Test the server
./start.sh

# 4. Copy configuration (choose one):
cp config.toml /path/to/codex/workspace/                          # For Codex
cp mcp_config_claude_code.json ~/.config/claude-code/mcp_config.json  # For Claude Code
cp mcp_config_vscode.json .vscode/mcp_config.json                 # For VSCode
cp mcp_config_generic.json ~/.cursor/mcp.json                     # For Cursor

# 5. Restart your MCP client
```

---

## Server Information

- **Name:** Fusion 360 API Server
- **Version:** 2.1
- **Tools:** 9 intelligent tools
- **Resources:** 9 resources
- **API Coverage:** ~89,000 lines (7 modules)
- **Python:** 3.8+ required

### Available Tools:

1. `explore_ui()` - Discover all UI/GUI classes
2. `search_by_category()` - Search by semantic category
3. `get_full_class()` - Extract complete class definition
4. `search_api()` - Smart search (10+30 context)
5. `search_fusion_api()` - General search (20+20 context)
6. `find_class()` - Fast lookup with fuzzy search (NEW v2.1)
7. `find_method()` - Find method across all classes (NEW v2.1)
8. `get_class_hierarchy()` - Show inheritance tree (NEW v2.1)
9. `list_all_classes()` - Instant class listing (NEW v2.1)

---

## Need Help?

- **Full Documentation:** [README_MCP.md](README_MCP.md)
- **Quick Reference:** [QUICK_REFERENCE.md](QUICK_REFERENCE.md)
- **Setup Guide:** [MCP_SETUP_GUIDE.md](MCP_SETUP_GUIDE.md)
- **Examples:** [test_examples.py](test_examples.py)

---

**Last Updated:** 2025
**Status:** Production Ready ✅
