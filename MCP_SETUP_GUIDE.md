# Fusion 360 MCP Server - Setup Guide

## 📋 Quick Setup (3 Steps)

### 1. Install Dependencies
```bash
cd /home/lubas/TOOLS/adk_API
./install.sh
```

### 2. Start Server
```bash
./start.sh
```

### 3. Configure Your MCP Client
Use one of the configuration files below based on your client.

---

## 🔧 Installation Details

### Automated Installation (Recommended)
The `install.sh` script will:
- ✅ Check Python version (3.8+ required)
- ✅ Create virtual environment
- ✅ Install all dependencies
- ✅ Verify installation
- ✅ Set up start script

```bash
./install.sh
```

### Manual Installation
If you prefer manual setup:

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## 🚀 Starting the Server

### Automated Start (Recommended)
```bash
./start.sh
```

The script will:
- ✅ Activate virtual environment
- ✅ Verify dependencies
- ✅ Check API files
- ✅ Display server info
- ✅ Start the MCP server

### Manual Start
```bash
# Activate virtual environment
source venv/bin/activate

# Start server
python fusion_mcp_server.py
```

---

## 📡 MCP Client Configuration

### For Claude Code

**File:** `~/.config/claude-code/mcp_config.json`

```json
{
  "mcpServers": {
    "fusion360-api": {
      "command": "/home/lubas/TOOLS/adk_API/venv/bin/python",
      "args": [
        "/home/lubas/TOOLS/adk_API/fusion_mcp_server.py"
      ],
      "env": {}
    }
  }
}
```

**Or copy the provided config:**
```bash
cp mcp_config_claude_code.json ~/.config/claude-code/mcp_config.json
```

---

### For VSCode with MCP Extension

**File:** `.vscode/mcp_config.json` (in your project root)

```json
{
  "mcpServers": {
    "fusion360-api": {
      "command": "/home/lubas/TOOLS/adk_API/venv/bin/python",
      "args": [
        "/home/lubas/TOOLS/adk_API/fusion_mcp_server.py"
      ],
      "env": {
        "PYTHONUNBUFFERED": "1"
      }
    }
  }
}
```

**Or copy:**
```bash
cp mcp_config_vscode.json /path/to/your/project/.vscode/mcp_config.json
```

---

### For Codex (using config.toml)

**File:** `config.toml` (in your Codex workspace)

```toml
[mcpServers."fusion360-api"]
command = "wsl"
args = [
  "bash",
  "-c",
  "cd /home/lulubas/TOOLS/adk_API && ./start.sh"
]
disabled = false
autoApprove = []
```

**Alternative for native Linux/macOS (without WSL):**
```toml
[mcpServers."fusion360-api"]
command = "/home/lulubas/TOOLS/adk_API/venv/bin/python"
args = ["/home/lulubas/TOOLS/adk_API/fusion_mcp_server.py"]
disabled = false
autoApprove = []
```

**Or copy the provided config:**
```bash
cp config.toml /path/to/your/codex/workspace/
```

---

### For Cline (VSCode Extension)

**File:** `~/Library/Application Support/Code/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json`

**Linux:** `~/.config/Code/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json`

```json
{
  "mcpServers": {
    "fusion360-api": {
      "command": "/home/lubas/TOOLS/adk_API/venv/bin/python",
      "args": [
        "/home/lubas/TOOLS/adk_API/fusion_mcp_server.py"
      ]
    }
  }
}
```

---

### For Cursor

**File:** `~/.cursor/mcp.json`

```json
{
  "mcpServers": {
    "fusion360-api": {
      "command": "/home/lubas/TOOLS/adk_API/venv/bin/python",
      "args": [
        "/home/lubas/TOOLS/adk_API/fusion_mcp_server.py"
      ],
      "env": {}
    }
  }
}
```

---

### For Gemini (via MCP Gateway)

**Note:** Google Gemini does not natively support MCP, so you'll need a gateway/proxy.

**Setup Steps:**

1. **Install MCP Gateway** (optional third-party tool):
   ```bash
   # Example using a hypothetical MCP-to-API gateway
   npm install -g mcp-gateway
   ```

2. **Configure Gateway:**
   ```bash
   mcp-gateway configure --server fusion360-api \
     --command "/home/lulubas/TOOLS/adk_API/venv/bin/python" \
     --args "/home/lulubas/TOOLS/adk_API/fusion_mcp_server.py" \
     --port 8080
   ```

3. **Connect Gemini:**
   Point Gemini API client to the gateway endpoint: `http://localhost:8080`

**Alternative:** Use Gemini through compatible MCP clients (Claude Code, Cursor, etc.) that support model switching.

---

### For Windows Users

Update paths in `mcp_config_windows.json`:

```json
{
  "mcpServers": {
    "fusion360-api": {
      "command": "C:\\Users\\YourUser\\TOOLS\\adk_API\\venv\\Scripts\\python.exe",
      "args": [
        "C:\\Users\\YourUser\\TOOLS\\adk_API\\fusion_mcp_server.py"
      ],
      "env": {
        "PYTHONUNBUFFERED": "1"
      }
    }
  }
}
```

**Replace:**
- `YourUser` with your Windows username
- Path separators to `\\` (double backslash)

---

## 🔍 Verifying Installation

### 1. Check Server Paths

**Server Location:**
```
/home/lubas/TOOLS/adk_API/fusion_mcp_server.py
```

**Python Interpreter:**
```
/home/lubas/TOOLS/adk_API/venv/bin/python
```

**API Files:**
```
/home/lubas/TOOLS/adk_API/API/Python/defs/adsk/
```

### 2. Test Server Manually

```bash
# Activate venv
source /home/lubas/TOOLS/adk_API/venv/bin/activate

# Test import
python -c "from mcp.server.fastmcp import FastMCP; print('✓ MCP OK')"

# Start server
python /home/lubas/TOOLS/adk_API/fusion_mcp_server.py
```

### 3. Verify in Client

After configuring your MCP client, you should see:
- **Server:** fusion360-api
- **Tools:** 5 tools available
- **Resources:** 9 resources available

---

## 📋 Configuration Templates

### Template 1: Using System Python

```json
{
  "mcpServers": {
    "fusion360-api": {
      "command": "python3",
      "args": ["/home/lubas/TOOLS/adk_API/fusion_mcp_server.py"],
      "env": {}
    }
  }
}
```

**Pros:** Simple
**Cons:** Requires MCP packages installed globally

---

### Template 2: Using Virtual Environment (Recommended)

```json
{
  "mcpServers": {
    "fusion360-api": {
      "command": "/home/lubas/TOOLS/adk_API/venv/bin/python",
      "args": ["/home/lubas/TOOLS/adk_API/fusion_mcp_server.py"],
      "env": {}
    }
  }
}
```

**Pros:** Isolated dependencies
**Cons:** Path-specific

---

### Template 3: With Environment Variables

```json
{
  "mcpServers": {
    "fusion360-api": {
      "command": "/home/lubas/TOOLS/adk_API/venv/bin/python",
      "args": ["/home/lubas/TOOLS/adk_API/fusion_mcp_server.py"],
      "env": {
        "PYTHONUNBUFFERED": "1",
        "FUSION_API_PATH": "/home/lubas/TOOLS/adk_API/API"
      }
    }
  }
}
```

**Pros:** Custom configuration
**Cons:** More complex

---

## 🐛 Troubleshooting

### Server Won't Start

**Problem:** Virtual environment not found
```bash
# Solution: Run install script
./install.sh
```

**Problem:** MCP packages not installed
```bash
# Solution: Activate venv and install
source venv/bin/activate
pip install -r requirements.txt
```

**Problem:** Python version too old
```bash
# Check version
python3 --version

# Must be 3.8 or higher
```

---

### Client Can't Connect

**Problem:** Wrong path in config
```bash
# Verify path exists
ls -l /home/lubas/TOOLS/adk_API/fusion_mcp_server.py

# If not, update the path in your mcp config
```

**Problem:** Python interpreter not found
```bash
# Verify venv python
ls -l /home/lubas/TOOLS/adk_API/venv/bin/python

# If not found, reinstall
./install.sh
```

---

### API Files Missing

**Problem:** No API definitions found
```bash
# Check API directory
ls -R /home/lubas/TOOLS/adk_API/API/Python/defs/adsk/

# Should see: core.py, fusion.py, cam.py, etc.
```

---

## 📂 Directory Structure

```
/home/lubas/TOOLS/adk_API/
├── fusion_mcp_server.py       # Main server script
├── requirements.txt           # Python dependencies
├── install.sh                 # Installation script
├── start.sh                   # Start script
├── venv/                      # Virtual environment (created by install.sh)
│   └── bin/
│       └── python             # Python interpreter for MCP
├── API/                       # Fusion 360 API definitions
│   └── Python/
│       └── defs/
│           └── adsk/
│               ├── core.py
│               ├── fusion.py
│               ├── cam.py
│               └── ...
└── mcp_config_*.json          # Configuration templates
```

---

## 🔄 Updating the Server

### Update Code Only
```bash
# If you modify fusion_mcp_server.py
# Just restart the server
./start.sh
```

### Update Dependencies
```bash
# If requirements.txt changed
source venv/bin/activate
pip install -r requirements.txt --upgrade
```

### Full Reinstall
```bash
# Remove old venv
rm -rf venv

# Reinstall
./install.sh
```

---

## 🌍 Environment Variables (Optional)

You can set these in the MCP config `env` section:

```json
"env": {
  "PYTHONUNBUFFERED": "1",          # Disable Python buffering (recommended)
  "FUSION_API_PATH": "/custom/path", # Custom API path (optional)
  "MCP_DEBUG": "1"                   # Enable debug mode (optional)
}
```

---

## 📝 Quick Reference

### Essential Paths

| Item | Path |
|------|------|
| Server Script | `/home/lubas/TOOLS/adk_API/fusion_mcp_server.py` |
| Python Venv | `/home/lubas/TOOLS/adk_API/venv/bin/python` |
| API Files | `/home/lubas/TOOLS/adk_API/API/Python/defs/adsk/` |
| Install Script | `/home/lubas/TOOLS/adk_API/install.sh` |
| Start Script | `/home/lubas/TOOLS/adk_API/start.sh` |

### Essential Commands

| Action | Command |
|--------|---------|
| Install | `./install.sh` |
| Start | `./start.sh` |
| Test | `python -c "import mcp; print('OK')"` |
| Check Venv | `source venv/bin/activate && which python` |

---

## ✅ Quick Setup Checklist

- [ ] Run `./install.sh`
- [ ] Verify virtual environment created (`venv/` directory exists)
- [ ] Copy appropriate `mcp_config_*.json` to your client config location
- [ ] Update paths in config if needed
- [ ] Restart your MCP client
- [ ] Verify server appears in client
- [ ] Test with `fusion://info` resource or `explore_ui()` tool

---

## 🆘 Support

If you encounter issues:

1. Check `./install.sh` output for errors
2. Verify paths in your MCP config
3. Test server manually: `source venv/bin/activate && python fusion_mcp_server.py`
4. Check client logs for connection errors
5. Ensure Python 3.8+ is installed

---

## 🎯 Next Steps

After setup:

1. Read [QUICK_REFERENCE.md](QUICK_REFERENCE.md) for tool usage
2. Try [test_examples.py](test_examples.py) for examples
3. Explore with `explore_ui()` or `search_by_category("ui")`

---

**Version:** 2.0
**Last Updated:** 2025
**Status:** Production Ready ✅
