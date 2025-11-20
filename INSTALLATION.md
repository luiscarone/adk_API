# Fusion 360 MCP Server - Installation Guide

## 🚀 Quick Start (3 Commands)

```bash
# 1. Install
./install.sh

# 2. Test
./test_installation.sh

# 3. Start
./start.sh
```

**That's it!** Your server is running. 🎉

---

## 📋 Available Scripts

### `install.sh` - Installation Script

**Purpose:** Sets up the complete environment automatically.

**What it does:**
1. ✅ Checks Python 3.8+ is installed
2. ✅ Creates virtual environment in `venv/`
3. ✅ Activates virtual environment
4. ✅ Upgrades pip to latest version
5. ✅ Installs all dependencies from `requirements.txt`
6. ✅ Verifies installation succeeded
7. ✅ Displays next steps

**Usage:**
```bash
./install.sh
```

**Expected output:**
```
╔═══════════════════════════════════════════════════════════════════════╗
║           Fusion 360 MCP Server - Installation Script                ║
╚═══════════════════════════════════════════════════════════════════════╝

[1/5] Checking Python version...
✓ Found Python 3.11.0

[2/5] Creating virtual environment...
✓ Virtual environment created

[3/5] Activating virtual environment...
✓ Virtual environment activated

[4/5] Upgrading pip...
✓ pip upgraded

[5/5] Installing dependencies...
✓ Dependencies installed

✓ Installation completed successfully!
```

**Troubleshooting:**
- If Python < 3.8: Upgrade Python first
- If `venv` creation fails: Install `python3-venv` package
- If permission denied: Run `chmod +x install.sh`

---

### `start.sh` - Server Start Script

**Purpose:** Starts the MCP server with proper environment.

**What it does:**
1. ✅ Checks virtual environment exists
2. ✅ Activates virtual environment
3. ✅ Verifies MCP packages installed
4. ✅ Checks API files present
5. ✅ Displays server information
6. ✅ Starts the MCP server

**Usage:**
```bash
./start.sh
```

**Expected output:**
```
╔═══════════════════════════════════════════════════════════════════════╗
║             Fusion 360 MCP Server - Starting...                      ║
╚═══════════════════════════════════════════════════════════════════════╝

Server Location:
  /home/lubas/TOOLS/adk_API/fusion_mcp_server.py

Virtual Environment:
  /home/lubas/TOOLS/adk_API/venv

[1/3] Activating virtual environment...
✓ Virtual environment activated

[2/3] Verifying MCP packages...
✓ MCP package found
✓ FastMCP package found

[3/3] Checking API files...
✓ Found 7 API modules

╔═══════════════════════════════════════════════════════════════════════╗
║                    SERVER READY TO START                              ║
╚═══════════════════════════════════════════════════════════════════════╝

Starting server... (Press Ctrl+C to stop)
```

**To stop the server:**
Press `Ctrl+C`

---

### `test_installation.sh` - Installation Test Script

**Purpose:** Verifies everything is properly installed.

**What it does:**
Tests 10 critical components:
1. ✅ Python version (3.8+)
2. ✅ Virtual environment exists
3. ✅ Virtual environment Python works
4. ✅ Server script exists
5. ✅ Requirements file exists
6. ✅ MCP package installed
7. ✅ FastMCP package installed
8. ✅ API directory structure
9. ✅ Critical API files present
10. ✅ Scripts are executable

**Usage:**
```bash
./test_installation.sh
```

**Expected output (all pass):**
```
╔═══════════════════════════════════════════════════════════════════════╗
║        Fusion 360 MCP Server - Installation Test                     ║
╚═══════════════════════════════════════════════════════════════════════╝

[TEST 1/10] Checking Python version...
✓ Python 3.11.0 (OK)

[TEST 2/10] Checking virtual environment...
✓ Virtual environment exists

[TEST 3/10] Checking venv Python...
✓ venv Python 3.11.0

[TEST 4/10] Checking server script...
✓ fusion_mcp_server.py (29616 bytes)

[TEST 5/10] Checking requirements.txt...
✓ requirements.txt exists

[TEST 6/10] Checking MCP packages...
✓ mcp package installed

[TEST 7/10] Checking FastMCP package...
✓ fastmcp package installed

[TEST 8/10] Checking API directory...
✓ API directory exists (7 files)

[TEST 9/10] Checking critical API files...
✓ All critical API files found

[TEST 10/10] Checking scripts permissions...
✓ Scripts are executable

═══════════════════════════════════════════════════════════════════════
                          TEST SUMMARY
═══════════════════════════════════════════════════════════════════════

Passed: 10
Failed: 0
Total:  10

╔═══════════════════════════════════════════════════════════════════════╗
║                    ✓ ALL TESTS PASSED!                                ║
║              Server is ready to start!                                ║
╚═══════════════════════════════════════════════════════════════════════╝
```

**If tests fail:**
The script will indicate which test failed and suggest a fix (usually running `./install.sh`).

---

## 📁 File Structure After Installation

```
/home/lubas/TOOLS/adk_API/
├── install.sh                 # Installation script
├── start.sh                   # Start script
├── test_installation.sh       # Test script
├── fusion_mcp_server.py       # Main server (29KB)
├── requirements.txt           # Dependencies
├── venv/                      # Virtual environment (created by install.sh)
│   ├── bin/
│   │   └── python             # Python interpreter for MCP
│   ├── lib/
│   │   └── python3.x/
│   │       └── site-packages/
│   │           ├── mcp/       # MCP package
│   │           └── ...
│   └── ...
├── API/                       # Fusion 360 API
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

## 🔧 Manual Installation (Alternative)

If you prefer to install manually or need to troubleshoot:

### Step 1: Check Python
```bash
python3 --version
# Should be 3.8 or higher
```

### Step 2: Create Virtual Environment
```bash
python3 -m venv venv
```

### Step 3: Activate Virtual Environment
```bash
source venv/bin/activate
```

### Step 4: Upgrade pip
```bash
pip install --upgrade pip
```

### Step 5: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 6: Verify Installation
```bash
python -c "from mcp.server.fastmcp import FastMCP; print('✓ Installation OK')"
```

### Step 7: Test Server
```bash
python fusion_mcp_server.py
```

---

## 🌍 Server Paths for MCP Configuration

After installation, use these paths in your MCP client config:

### For Linux/Mac

**Python Interpreter:**
```
/home/lubas/TOOLS/adk_API/venv/bin/python
```

**Server Script:**
```
/home/lubas/TOOLS/adk_API/fusion_mcp_server.py
```

**Full JSON Config:**
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

### For Windows

**Python Interpreter:**
```
C:\Users\YourUser\TOOLS\adk_API\venv\Scripts\python.exe
```

**Server Script:**
```
C:\Users\YourUser\TOOLS\adk_API\fusion_mcp_server.py
```

**Full JSON Config:**
```json
{
  "mcpServers": {
    "fusion360-api": {
      "command": "C:\\Users\\YourUser\\TOOLS\\adk_API\\venv\\Scripts\\python.exe",
      "args": [
        "C:\\Users\\YourUser\\TOOLS\\adk_API\\fusion_mcp_server.py"
      ],
      "env": {}
    }
  }
}
```

---

## 🔄 Reinstalling

### Complete Reinstall
```bash
# Remove virtual environment
rm -rf venv

# Reinstall
./install.sh

# Test
./test_installation.sh
```

### Update Dependencies Only
```bash
# Activate venv
source venv/bin/activate

# Update packages
pip install -r requirements.txt --upgrade
```

---

## 🐛 Common Issues

### Issue 1: "command not found: ./install.sh"

**Cause:** Script not executable

**Solution:**
```bash
chmod +x install.sh start.sh test_installation.sh
./install.sh
```

---

### Issue 2: "Python 3.8+ required"

**Cause:** Old Python version

**Solution:**
```bash
# Check version
python3 --version

# Upgrade Python (Ubuntu/Debian)
sudo apt update
sudo apt install python3.11

# Upgrade Python (Mac)
brew install python@3.11
```

---

### Issue 3: "venv not found"

**Cause:** Installation incomplete

**Solution:**
```bash
./install.sh
```

---

### Issue 4: "MCP packages not found"

**Cause:** Dependencies not installed

**Solution:**
```bash
source venv/bin/activate
pip install -r requirements.txt
```

---

### Issue 5: "API files not found"

**Cause:** API directory missing or in wrong location

**Solution:**
```bash
# Check if API exists
ls -R API/Python/defs/adsk/

# Should see: core.py, fusion.py, cam.py, etc.
# If not, ensure API directory is in project root
```

---

## ✅ Installation Checklist

Use this checklist to verify your installation:

- [ ] Python 3.8+ installed
- [ ] `./install.sh` completed successfully
- [ ] `venv/` directory created
- [ ] `venv/bin/python` exists
- [ ] `./test_installation.sh` shows all tests passed
- [ ] API files exist in `API/Python/defs/adsk/`
- [ ] Scripts are executable (`chmod +x` applied)
- [ ] MCP config file created with correct paths
- [ ] `./start.sh` starts server without errors

---

## 📚 Next Steps

After successful installation:

1. **Configure Your Client**
   - See [MCP_SETUP_GUIDE.md](MCP_SETUP_GUIDE.md) for client-specific configs

2. **Learn to Use**
   - Read [QUICK_REFERENCE.md](QUICK_REFERENCE.md) for tool usage
   - Try [test_examples.py](test_examples.py) for examples

3. **Start Developing**
   - Use `explore_ui()` to discover UI classes
   - Use `search_by_category("ui")` to browse categories
   - Use `get_full_class("ClassName")` for reference

---

## 🆘 Getting Help

If you're still having issues:

1. Run `./test_installation.sh` and note which test fails
2. Check the error messages carefully
3. Verify all paths in your MCP config
4. Try manual installation steps
5. Check Python and pip versions

---

## 📊 System Requirements

| Component | Requirement |
|-----------|-------------|
| OS | Linux, macOS, Windows |
| Python | 3.8 or higher |
| Disk Space | ~100MB (including venv) |
| RAM | 256MB minimum |
| Dependencies | fastmcp, mcp |

---

**Installation Version:** 2.0
**Last Updated:** 2025
**Status:** Production Ready ✅
