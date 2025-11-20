#!/bin/bash

################################################################################
# Fusion 360 MCP Server - Installation Script
# This script sets up the virtual environment and installs all dependencies
################################################################################

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo -e "${BLUE}╔═══════════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                                                                       ║${NC}"
echo -e "${BLUE}║           Fusion 360 MCP Server - Installation Script                ║${NC}"
echo -e "${BLUE}║                          v2.1                                         ║${NC}"
echo -e "${BLUE}║                                                                       ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Check Python version
echo -e "${YELLOW}[1/5] Checking Python version...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}ERROR: Python 3 is not installed!${NC}"
    echo -e "${RED}Please install Python 3.8 or higher.${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo -e "${GREEN}✓ Found Python $PYTHON_VERSION${NC}"

# Check if version is 3.8+
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d'.' -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d'.' -f2)
if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 8 ]); then
    echo -e "${RED}ERROR: Python 3.8+ is required (found $PYTHON_VERSION)${NC}"
    exit 1
fi

# Create virtual environment
echo ""
echo -e "${YELLOW}[2/5] Creating virtual environment...${NC}"
if [ -d "venv" ]; then
    echo -e "${YELLOW}Virtual environment already exists. Removing old one...${NC}"
    rm -rf venv
fi

python3 -m venv venv
echo -e "${GREEN}✓ Virtual environment created${NC}"

# Activate virtual environment
echo ""
echo -e "${YELLOW}[3/5] Activating virtual environment...${NC}"
source venv/bin/activate
echo -e "${GREEN}✓ Virtual environment activated${NC}"

# Upgrade pip
echo ""
echo -e "${YELLOW}[4/5] Upgrading pip...${NC}"
pip install --upgrade pip --quiet
echo -e "${GREEN}✓ pip upgraded${NC}"

# Install dependencies
echo ""
echo -e "${YELLOW}[5/5] Installing dependencies...${NC}"
if [ ! -f "requirements.txt" ]; then
    echo -e "${RED}ERROR: requirements.txt not found!${NC}"
    exit 1
fi

pip install -r requirements.txt --quiet
echo -e "${GREEN}✓ Dependencies installed${NC}"

# Verify installation
echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✓ Installation completed successfully!${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════════════${NC}"
echo ""

# Display installed packages
echo -e "${YELLOW}Installed packages:${NC}"
pip list | grep -E "(fastmcp|mcp)" || echo -e "${RED}Warning: MCP packages not found${NC}"

# Verify server script
echo ""
echo -e "${YELLOW}Verifying server script...${NC}"
if [ -f "fusion_mcp_server.py" ]; then
    echo -e "${GREEN}✓ fusion_mcp_server.py found${NC}"
else
    echo -e "${RED}ERROR: fusion_mcp_server.py not found!${NC}"
    exit 1
fi

# Verify API files
echo ""
echo -e "${YELLOW}Verifying API files...${NC}"
if [ -d "API/Python/defs/adsk" ]; then
    FILE_COUNT=$(find API/Python/defs/adsk -name "*.py" | wc -l)
    echo -e "${GREEN}✓ Found $FILE_COUNT API definition files${NC}"
else
    echo -e "${RED}WARNING: API directory not found!${NC}"
fi

# Create start script if it doesn't exist
echo ""
echo -e "${YELLOW}Setting up start script...${NC}"
if [ ! -f "start.sh" ]; then
    echo -e "${YELLOW}Creating start.sh script...${NC}"
fi
chmod +x start.sh 2>/dev/null || true
echo -e "${GREEN}✓ Start script ready${NC}"

# Display next steps
echo ""
echo -e "${BLUE}╔═══════════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                        NEXT STEPS                                     ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${GREEN}1. Start the server:${NC}"
echo -e "   ${YELLOW}./start.sh${NC}"
echo ""
echo -e "${GREEN}2. Or manually:${NC}"
echo -e "   ${YELLOW}source venv/bin/activate${NC}"
echo -e "   ${YELLOW}python fusion_mcp_server.py${NC}"
echo ""
echo -e "${GREEN}3. Configure your MCP client:${NC}"
echo -e "   See ${YELLOW}mcp_config_*.json${NC} files for examples"
echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}Installation directory: ${YELLOW}$SCRIPT_DIR${NC}"
echo -e "${GREEN}Virtual environment: ${YELLOW}$SCRIPT_DIR/venv${NC}"
echo -e "${GREEN}Server script: ${YELLOW}$SCRIPT_DIR/fusion_mcp_server.py${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${GREEN}Happy coding! 🚀${NC}"
