#!/bin/bash

################################################################################
# Fusion 360 MCP Server - Start Script
# Activates virtual environment and starts the MCP server
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

# Clear screen
clear

echo -e "${BLUE}╔═══════════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                                                                       ║${NC}"
echo -e "${BLUE}║             Fusion 360 MCP Server - Starting...                      ║${NC}"
echo -e "${BLUE}║                          v2.1                                         ║${NC}"
echo -e "${BLUE}║                                                                       ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${RED}ERROR: Virtual environment not found!${NC}"
    echo -e "${YELLOW}Please run ./install.sh first${NC}"
    exit 1
fi

# Check if server script exists
if [ ! -f "fusion_mcp_server.py" ]; then
    echo -e "${RED}ERROR: fusion_mcp_server.py not found!${NC}"
    exit 1
fi

# Display server information
echo -e "${GREEN}Server Location:${NC}"
echo -e "  ${YELLOW}$SCRIPT_DIR/fusion_mcp_server.py${NC}"
echo ""

echo -e "${GREEN}Virtual Environment:${NC}"
echo -e "  ${YELLOW}$SCRIPT_DIR/venv${NC}"
echo ""

# Activate virtual environment
echo -e "${YELLOW}[1/3] Activating virtual environment...${NC}"
source venv/bin/activate
echo -e "${GREEN}✓ Virtual environment activated${NC}"
echo ""

# Verify MCP packages
echo -e "${YELLOW}[2/3] Verifying MCP packages...${NC}"
if python -c "import mcp" 2>/dev/null; then
    echo -e "${GREEN}✓ MCP package found${NC}"
else
    echo -e "${RED}ERROR: MCP package not installed!${NC}"
    echo -e "${YELLOW}Run ./install.sh to install dependencies${NC}"
    exit 1
fi

if python -c "import mcp.server.fastmcp" 2>/dev/null; then
    echo -e "${GREEN}✓ FastMCP package found${NC}"
else
    echo -e "${RED}ERROR: FastMCP package not installed!${NC}"
    echo -e "${YELLOW}Run ./install.sh to install dependencies${NC}"
    exit 1
fi
echo ""

# Display API coverage
echo -e "${YELLOW}[3/3] Checking API files...${NC}"
if [ -d "API/Python/defs/adsk" ]; then
    API_FILES=$(find API/Python/defs/adsk -name "*.py" -type f | wc -l)
    echo -e "${GREEN}✓ Found $API_FILES API modules${NC}"

    # List API files
    echo -e "${BLUE}  • core.py${NC}"
    echo -e "${BLUE}  • fusion.py${NC}"
    echo -e "${BLUE}  • cam.py${NC}"
    echo -e "${BLUE}  • drawing.py${NC}"
    echo -e "${BLUE}  • volume.py${NC}"
    echo -e "${BLUE}  • sim.py${NC}"
else
    echo -e "${RED}WARNING: API directory not found at ./API/${NC}"
fi
echo ""

# Display connection information
echo -e "${BLUE}╔═══════════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                    SERVER READY TO START                              ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${GREEN}MCP Server Configuration:${NC}"
echo -e "  Command: ${YELLOW}python${NC}"
echo -e "  Script:  ${YELLOW}$SCRIPT_DIR/fusion_mcp_server.py${NC}"
echo -e "  Venv:    ${YELLOW}$SCRIPT_DIR/venv/bin/python${NC}"
echo ""
echo -e "${GREEN}Available Tools (9 total):${NC}"
echo -e "  ${BLUE}v2.0 Tools:${NC}"
echo -e "  ${BLUE}1.${NC} explore_ui()             - Discover all UI/GUI classes"
echo -e "  ${BLUE}2.${NC} search_by_category()     - Search by semantic category"
echo -e "  ${BLUE}3.${NC} get_full_class()         - Extract complete class definition"
echo -e "  ${BLUE}4.${NC} search_api()             - Smart search (10+30 context)"
echo -e "  ${BLUE}5.${NC} search_fusion_api()      - General search (20+20 context)"
echo -e ""
echo -e "  ${GREEN}v2.1 NEW Tools (10x faster):${NC}"
echo -e "  ${BLUE}6.${NC} find_class()             - Fast lookup with fuzzy search"
echo -e "  ${BLUE}7.${NC} find_method()            - Find method across all classes"
echo -e "  ${BLUE}8.${NC} get_class_hierarchy()    - Show inheritance tree"
echo -e "  ${BLUE}9.${NC} list_all_classes()       - Instant class listing"
echo ""
echo -e "${GREEN}Available Resources:${NC}"
echo -e "  ${BLUE}•${NC} fusion://info            - Server information"
echo -e "  ${BLUE}•${NC} fusion://version         - API version"
echo -e "  ${BLUE}•${NC} fusion://core            - Core module"
echo -e "  ${BLUE}•${NC} fusion://fusion          - Fusion module"
echo -e "  ${BLUE}•${NC} fusion://cam             - CAM module"
echo -e "  ${BLUE}•${NC} And 4 more resources..."
echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}Starting server... (Press Ctrl+C to stop)${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════════════${NC}"
echo ""

# Start the server
python fusion_mcp_server.py

# This will only execute if the server exits
echo ""
echo -e "${YELLOW}Server stopped.${NC}"
