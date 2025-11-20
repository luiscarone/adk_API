#!/bin/bash

################################################################################
# Fusion 360 MCP Server - Installation Test Script
# Verifies that everything is properly installed and configured
################################################################################

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Test counters
PASS=0
FAIL=0

echo -e "${BLUE}╔═══════════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                                                                       ║${NC}"
echo -e "${BLUE}║        Fusion 360 MCP Server - Installation Test                     ║${NC}"
echo -e "${BLUE}║                                                                       ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Test 1: Python version
echo -e "${YELLOW}[TEST 1/10] Checking Python version...${NC}"
if command -v python3 &> /dev/null; then
    VERSION=$(python3 --version | cut -d' ' -f2)
    MAJOR=$(echo $VERSION | cut -d'.' -f1)
    MINOR=$(echo $VERSION | cut -d'.' -f2)
    if [ "$MAJOR" -ge 3 ] && [ "$MINOR" -ge 8 ]; then
        echo -e "${GREEN}✓ Python $VERSION (OK)${NC}"
        ((PASS++))
    else
        echo -e "${RED}✗ Python $VERSION (Need 3.8+)${NC}"
        ((FAIL++))
    fi
else
    echo -e "${RED}✗ Python not found${NC}"
    ((FAIL++))
fi

# Test 2: Virtual environment
echo -e "${YELLOW}[TEST 2/10] Checking virtual environment...${NC}"
if [ -d "venv" ]; then
    echo -e "${GREEN}✓ Virtual environment exists${NC}"
    ((PASS++))
else
    echo -e "${RED}✗ Virtual environment not found${NC}"
    echo -e "${YELLOW}  Run: ./install.sh${NC}"
    ((FAIL++))
fi

# Test 3: Virtual environment Python
echo -e "${YELLOW}[TEST 3/10] Checking venv Python...${NC}"
if [ -f "venv/bin/python" ]; then
    VENV_VERSION=$(venv/bin/python --version 2>&1 | cut -d' ' -f2)
    echo -e "${GREEN}✓ venv Python $VENV_VERSION${NC}"
    ((PASS++))
else
    echo -e "${RED}✗ venv/bin/python not found${NC}"
    ((FAIL++))
fi

# Test 4: Server script
echo -e "${YELLOW}[TEST 4/10] Checking server script...${NC}"
if [ -f "fusion_mcp_server.py" ]; then
    SIZE=$(stat -f%z "fusion_mcp_server.py" 2>/dev/null || stat -c%s "fusion_mcp_server.py" 2>/dev/null)
    echo -e "${GREEN}✓ fusion_mcp_server.py ($SIZE bytes)${NC}"
    ((PASS++))
else
    echo -e "${RED}✗ fusion_mcp_server.py not found${NC}"
    ((FAIL++))
fi

# Test 5: Requirements file
echo -e "${YELLOW}[TEST 5/10] Checking requirements.txt...${NC}"
if [ -f "requirements.txt" ]; then
    echo -e "${GREEN}✓ requirements.txt exists${NC}"
    ((PASS++))
else
    echo -e "${RED}✗ requirements.txt not found${NC}"
    ((FAIL++))
fi

# Test 6: MCP packages (if venv exists)
echo -e "${YELLOW}[TEST 6/10] Checking MCP packages...${NC}"
if [ -d "venv" ]; then
    source venv/bin/activate 2>/dev/null
    if python -c "import mcp" 2>/dev/null; then
        echo -e "${GREEN}✓ mcp package installed${NC}"
        ((PASS++))
    else
        echo -e "${RED}✗ mcp package not found${NC}"
        echo -e "${YELLOW}  Run: ./install.sh${NC}"
        ((FAIL++))
    fi
else
    echo -e "${YELLOW}⊘ Skipped (no venv)${NC}"
fi

# Test 7: FastMCP package
echo -e "${YELLOW}[TEST 7/10] Checking FastMCP package...${NC}"
if [ -d "venv" ]; then
    source venv/bin/activate 2>/dev/null
    if python -c "import mcp.server.fastmcp" 2>/dev/null; then
        echo -e "${GREEN}✓ fastmcp package installed${NC}"
        ((PASS++))
    else
        echo -e "${RED}✗ fastmcp package not found${NC}"
        echo -e "${YELLOW}  Run: ./install.sh${NC}"
        ((FAIL++))
    fi
else
    echo -e "${YELLOW}⊘ Skipped (no venv)${NC}"
fi

# Test 8: API directory
echo -e "${YELLOW}[TEST 8/10] Checking API directory...${NC}"
if [ -d "API/Python/defs/adsk" ]; then
    FILE_COUNT=$(find API/Python/defs/adsk -name "*.py" -type f | wc -l)
    echo -e "${GREEN}✓ API directory exists ($FILE_COUNT files)${NC}"
    ((PASS++))
else
    echo -e "${RED}✗ API directory not found${NC}"
    ((FAIL++))
fi

# Test 9: API files
echo -e "${YELLOW}[TEST 9/10] Checking critical API files...${NC}"
CRITICAL_FILES=("core.py" "fusion.py" "cam.py")
FOUND=0
for file in "${CRITICAL_FILES[@]}"; do
    if [ -f "API/Python/defs/adsk/$file" ]; then
        ((FOUND++))
    fi
done
if [ $FOUND -eq 3 ]; then
    echo -e "${GREEN}✓ All critical API files found${NC}"
    ((PASS++))
else
    echo -e "${RED}✗ Missing API files ($FOUND/3 found)${NC}"
    ((FAIL++))
fi

# Test 10: Scripts executable
echo -e "${YELLOW}[TEST 10/10] Checking scripts permissions...${NC}"
if [ -x "install.sh" ] && [ -x "start.sh" ]; then
    echo -e "${GREEN}✓ Scripts are executable${NC}"
    ((PASS++))
else
    echo -e "${YELLOW}⚠ Scripts not executable${NC}"
    echo -e "${YELLOW}  Run: chmod +x install.sh start.sh${NC}"
fi

# Summary
echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}                          TEST SUMMARY                                 ${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${GREEN}Passed: $PASS${NC}"
echo -e "${RED}Failed: $FAIL${NC}"
TOTAL=$((PASS + FAIL))
echo -e "Total:  $TOTAL"
echo ""

if [ $FAIL -eq 0 ]; then
    echo -e "${GREEN}╔═══════════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║                                                                       ║${NC}"
    echo -e "${GREEN}║                    ✓ ALL TESTS PASSED!                                ║${NC}"
    echo -e "${GREEN}║                                                                       ║${NC}"
    echo -e "${GREEN}║              Server is ready to start!                                ║${NC}"
    echo -e "${GREEN}║                                                                       ║${NC}"
    echo -e "${GREEN}╚═══════════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${YELLOW}Next steps:${NC}"
    echo -e "  1. Start server: ${GREEN}./start.sh${NC}"
    echo -e "  2. Configure client: See ${GREEN}MCP_SETUP_GUIDE.md${NC}"
    echo ""
    exit 0
else
    echo -e "${RED}╔═══════════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${RED}║                                                                       ║${NC}"
    echo -e "${RED}║                    ✗ SOME TESTS FAILED                                ║${NC}"
    echo -e "${RED}║                                                                       ║${NC}"
    echo -e "${RED}║              Please fix the issues above                              ║${NC}"
    echo -e "${RED}║                                                                       ║${NC}"
    echo -e "${RED}╚═══════════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${YELLOW}Recommended fix:${NC}"
    echo -e "  Run: ${GREEN}./install.sh${NC}"
    echo ""
    exit 1
fi
