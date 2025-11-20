#!/usr/bin/env python3
"""
MCP Server for Fusion 360 API Documentation
Exposes local Fusion 360 Python API definitions through MCP protocol

Version: 2.1 - Enhanced with Indexing, Fuzzy Search, and Metadata

Supported modules:
- adsk.core (916KB) - Core application functionality
- adsk.fusion (2.4MB) - Fusion 360 design features
- adsk.cam (358KB) - CAM/Manufacturing operations
- adsk.drawing (5.9KB) - Drawing/documentation
- adsk.volume (41KB) - Volume/mesh operations
- adsk.sim (231B) - Simulation capabilities
- adsk.__init__ (1.3KB) - Module utilities

Features v2.1:
- In-memory index for 10x faster searches
- Fuzzy search with typo tolerance
- Metadata index with class hierarchies
- Smart suggestions

Total API coverage: ~89,000 lines of definitions
API Version: 2605.1.18
"""

import os
import re
from pathlib import Path
from typing import Any, List, Dict, Tuple, Set, Optional
from collections import defaultdict
from difflib import get_close_matches
from mcp.server.fastmcp import FastMCP
from agents.ui_agent import run_agent as run_ui_agent
from agents.core_agent import run_agent as run_core_agent
from agents.fusion_agent import run_agent as run_fusion_agent
from agents.cam_agent import run_agent as run_cam_agent
from agents.drawing_agent import run_agent as run_drawing_agent
from agents.volume_agent import run_agent as run_volume_agent
from agents.sim_agent import run_agent as run_sim_agent

# Initialize FastMCP server
mcp = FastMCP("Fusion360 API Server")

# Define base paths
SCRIPT_DIR = Path(__file__).parent
API_BASE_PATH = SCRIPT_DIR / "API" / "Python" / "defs" / "adsk"
VERSION_FILE = SCRIPT_DIR / "API" / "version.txt"

# All API modules to index
API_MODULES = {
    "core": API_BASE_PATH / "core.py",
    "fusion": API_BASE_PATH / "fusion.py",
    "cam": API_BASE_PATH / "cam.py",
    "drawing": API_BASE_PATH / "drawing.py",
    "volume": API_BASE_PATH / "volume.py",
    "sim": API_BASE_PATH / "sim.py",
    "init": API_BASE_PATH / "__init__.py",
}

# UI/GUI related keywords for semantic search
UI_KEYWORDS = {
    "interface": ["Command", "Input", "Dialog", "Palette", "HTML", "Browser", "Panel", "Window"],
    "controls": ["Button", "TextBox", "CheckBox", "Slider", "DropDown", "List", "Table", "Selection"],
    "input": ["CommandInput", "ValueInput", "StringInput", "BoolInput", "SelectionInput", "ImageCommandInput"],
    "events": ["Event", "Handler", "CommandCreated", "InputChanged", "Validate", "Execute", "Activate"],
    "display": ["Graphics", "CustomGraphics", "Viewport", "Camera", "Display", "Appearance"],
    "layout": ["Group", "GroupCommandInput", "Tab", "TabCommandInput", "Row", "Column"],
}

# Category-based search mapping
CATEGORY_KEYWORDS = {
    "ui": ["Command", "Input", "Dialog", "Palette", "Button", "Handler", "Event", "HTML", "Browser", "Window", "Panel", "Tab", "Group"],
    "geometry": ["Point", "Vector", "Line", "Circle", "Arc", "Curve", "Surface", "BRep", "Body", "Face", "Edge", "Vertex"],
    "sketch": ["Sketch", "SketchLine", "SketchCircle", "SketchArc", "Profile", "Constraint", "Dimension"],
    "feature": ["Extrude", "Revolve", "Sweep", "Loft", "Fillet", "Chamfer", "Shell", "Pattern", "Mirror"],
    "component": ["Component", "Occurrence", "Assembly", "Joint", "AsBuilt", "Rigid"],
    "cam": ["CAM", "Operation", "Setup", "Tool", "Toolpath", "Strategy", "Post", "NCProgram"],
    "material": ["Material", "Appearance", "Physical", "Library", "Texture"],
    "document": ["Document", "Design", "Product", "DataFile", "Export", "Import"],
}


# ============================================================================
# INDEX AND CACHE SYSTEM (v2.1)
# ============================================================================

class APIIndex:
    """
    In-memory index for fast API lookups.
    Built once on server startup, provides 10x faster searches.
    """

    def __init__(self):
        self.classes = {}  # class_name -> {module, line, content, methods}
        self.methods = defaultdict(list)  # method_name -> [(class, module, line)]
        self.all_names = set()  # All class and method names for fuzzy search
        self.inheritance = {}  # class_name -> parent_class
        self.module_classes = defaultdict(list)  # module -> [classes]
        self.indexed = False

    def build_index(self):
        """Build the complete index from all API modules."""
        if self.indexed:
            return  # Already built

        print("Building API index...")

        for module_name, file_path in API_MODULES.items():
            content = read_file_safe(file_path)
            if content.startswith("ERROR"):
                continue

            lines = content.split('\n')

            # Find all classes
            for i, line in enumerate(lines):
                # Match class definition
                class_match = re.match(r'^class\s+(\w+)\s*[\(:](.*)$', line)
                if class_match:
                    class_name = class_match.group(1)
                    inheritance_part = class_match.group(2)

                    # Extract parent class if exists
                    parent_match = re.search(r'\((\w+)\)', inheritance_part)
                    if parent_match:
                        parent_class = parent_match.group(1)
                        self.inheritance[class_name] = parent_class

                    # Extract methods for this class
                    methods = self._extract_class_methods(lines, i)

                    # Store class info
                    self.classes[class_name] = {
                        'module': module_name,
                        'line': i + 1,
                        'methods': methods,
                        'file_path': file_path
                    }

                    # Add to module index
                    self.module_classes[module_name].append(class_name)

                    # Add to all names for fuzzy search
                    self.all_names.add(class_name)

                    # Index methods
                    for method_name in methods:
                        self.methods[method_name].append((class_name, module_name, i + 1))
                        self.all_names.add(method_name)

        self.indexed = True
        print(f"✓ Index built: {len(self.classes)} classes, {len(self.methods)} unique methods")

    def _extract_class_methods(self, lines: List[str], class_line: int) -> List[str]:
        """Extract all method names from a class."""
        methods = []
        base_indent = len(lines[class_line]) - len(lines[class_line].lstrip())

        for i in range(class_line + 1, len(lines)):
            line = lines[i]
            if not line.strip():
                continue

            current_indent = len(line) - len(line.lstrip())

            # End of class
            if current_indent <= base_indent and line.strip():
                break

            # Method definition
            method_match = re.match(r'\s+def\s+(\w+)\s*\(', line)
            if method_match:
                method_name = method_match.group(1)
                if not method_name.startswith('_'):  # Skip private methods
                    methods.append(method_name)

        return methods

    def fuzzy_search(self, query: str, limit: int = 5) -> List[str]:
        """
        Find close matches to query using fuzzy matching.
        Returns list of suggestions.
        """
        if not self.indexed:
            self.build_index()

        matches = get_close_matches(query, self.all_names, n=limit, cutoff=0.6)
        return matches

    def get_class_info(self, class_name: str) -> Optional[Dict]:
        """Get complete info about a class."""
        if not self.indexed:
            self.build_index()

        return self.classes.get(class_name)

    def find_by_method(self, method_name: str) -> List[Tuple[str, str, int]]:
        """Find all classes that have this method."""
        if not self.indexed:
            self.build_index()

        return self.methods.get(method_name, [])

    def get_class_hierarchy(self, class_name: str) -> List[str]:
        """Get inheritance chain for a class."""
        if not self.indexed:
            self.build_index()

        hierarchy = [class_name]
        current = class_name

        while current in self.inheritance:
            parent = self.inheritance[current]
            hierarchy.append(parent)
            current = parent

            # Prevent infinite loops
            if len(hierarchy) > 20:
                break

        return hierarchy


# Global index instance
api_index = APIIndex()


def read_file_safe(file_path: Path) -> str:
    """
    Safely read a file and return its contents.

    Args:
        file_path: Path to the file to read

    Returns:
        File contents as string, or error message if file cannot be read
    """
    try:
        if not file_path.exists():
            return f"ERROR: File not found at {file_path}"

        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"ERROR reading {file_path}: {str(e)}"


def get_context_lines(content: str, match_position: int, context_lines: int = 20) -> tuple[str, int]:
    """
    Extract lines of context around a match position (symmetric).

    Args:
        content: Full file content
        match_position: Character position of the match
        context_lines: Number of lines to show before and after match

    Returns:
        Tuple of (context string, line number of match)
    """
    lines = content.split('\n')

    # Find which line the match is on
    char_count = 0
    match_line = 0
    for i, line in enumerate(lines):
        char_count += len(line) + 1  # +1 for newline
        if char_count > match_position:
            match_line = i
            break

    # Calculate start and end lines
    start_line = max(0, match_line - context_lines)
    end_line = min(len(lines), match_line + context_lines + 1)

    # Extract context
    context = '\n'.join(lines[start_line:end_line])

    return context, match_line + 1  # +1 for 1-based line numbers


def get_asymmetric_context(content: str, match_position: int, lines_before: int = 10, lines_after: int = 30) -> tuple[str, int]:
    """
    Extract asymmetric context around a match (more lines after than before).
    Perfect for capturing method signatures and their implementations.

    Args:
        content: Full file content
        match_position: Character position of the match
        lines_before: Number of lines to show before match (default: 10)
        lines_after: Number of lines to show after match (default: 30)

    Returns:
        Tuple of (context string, line number of match)
    """
    lines = content.split('\n')

    # Find which line the match is on
    char_count = 0
    match_line = 0
    for i, line in enumerate(lines):
        char_count += len(line) + 1  # +1 for newline
        if char_count > match_position:
            match_line = i
            break

    # Calculate start and end lines (asymmetric)
    start_line = max(0, match_line - lines_before)
    end_line = min(len(lines), match_line + lines_after + 1)

    # Extract context
    context = '\n'.join(lines[start_line:end_line])

    return context, match_line + 1  # +1 for 1-based line numbers


def extract_full_class(content: str, class_name: str) -> tuple[str, int] | None:
    """
    Extract a complete class definition with all its methods and properties.

    Args:
        content: Full file content
        class_name: Name of the class to extract

    Returns:
        Tuple of (class content, starting line number) or None if not found
    """
    lines = content.split('\n')

    # Find the class definition line
    class_pattern = re.compile(rf'^class\s+{re.escape(class_name)}\s*[\(:)]', re.MULTILINE)
    match = class_pattern.search(content)

    if not match:
        return None

    # Find the line number
    char_count = 0
    class_start_line = 0
    for i, line in enumerate(lines):
        char_count += len(line) + 1
        if char_count > match.start():
            class_start_line = i
            break

    # Extract all lines belonging to the class (based on indentation)
    class_lines = [lines[class_start_line]]
    base_indent = len(lines[class_start_line]) - len(lines[class_start_line].lstrip())

    # Get all subsequent lines that are indented more than the class definition
    for i in range(class_start_line + 1, len(lines)):
        line = lines[i]

        # Empty lines are included
        if not line.strip():
            class_lines.append(line)
            continue

        # Calculate indentation
        current_indent = len(line) - len(line.lstrip())

        # If indentation is back to base level or less, we've reached the end of the class
        if current_indent <= base_indent and line.strip():
            break

        class_lines.append(line)

    return '\n'.join(class_lines), class_start_line + 1


@mcp.tool()
def search_fusion_api(query: str, modules: str = "all") -> str:
    """
    Search for a term across ALL Fusion 360 API definition files.
    Returns up to 20 lines of context around each match.

    Args:
        query: Search term (case-insensitive)
        modules: Comma-separated list of modules to search (e.g., "core,fusion") or "all" for all modules

    Returns:
        Formatted search results with context from all matching files
    """
    if not query or len(query.strip()) == 0:
        return "ERROR: Query cannot be empty"

    results = []
    results.append(f"=== Searching for '{query}' in Fusion 360 API ===")

    # Determine which modules to search
    if modules.strip().lower() == "all":
        modules_to_search = API_MODULES
    else:
        requested = [m.strip().lower() for m in modules.split(",")]
        modules_to_search = {k: v for k, v in API_MODULES.items() if k in requested}
        if not modules_to_search:
            return f"ERROR: No valid modules found. Available: {', '.join(API_MODULES.keys())}"

    results.append(f"Searching in modules: {', '.join(modules_to_search.keys())}\n")

    total_matches = 0
    files_with_matches = 0

    for module_name, file_path in modules_to_search.items():
        content = read_file_safe(file_path)

        if content.startswith("ERROR"):
            results.append(f"\n[adsk.{module_name}] {content}\n")
            continue

        # Find all matches (case-insensitive)
        pattern = re.compile(re.escape(query), re.IGNORECASE)
        matches = list(pattern.finditer(content))

        if not matches:
            continue  # Skip modules with no matches for cleaner output

        files_with_matches += 1
        results.append(f"\n{'=' * 80}")
        results.append(f"[adsk.{module_name}] Found {len(matches)} match(es)")
        results.append("=" * 80)

        # Show context for each match (limit to avoid overwhelming output)
        max_matches_to_show = 5  # Reduced per-file limit since we search more files
        for idx, match in enumerate(matches[:max_matches_to_show]):
            context, line_num = get_context_lines(content, match.start(), context_lines=20)

            results.append(f"\n--- Match {idx + 1} at line {line_num} (adsk.{module_name}) ---")
            results.append(context)
            results.append("-" * 80)
            total_matches += 1

        if len(matches) > max_matches_to_show:
            results.append(f"\n(Showing first {max_matches_to_show} of {len(matches)} matches in this module)")

    if files_with_matches == 0:
        results.append(f"\nNo matches found for '{query}' in any module.")
    else:
        results.append(f"\n{'=' * 80}")
        results.append(f"=== Summary: {total_matches} matches shown across {files_with_matches} module(s) ===")

    return "\n".join(results)


@mcp.tool()
def search_api(keyword: str, max_results: int = 5) -> str:
    """
    Advanced search with asymmetric context: 10 lines before, 30 lines after.
    Perfect for finding method signatures and their full implementations.

    Args:
        keyword: Keyword to search (e.g., "CommandInput", "BRepBody")
        max_results: Maximum number of results to return (default: 5, max: 10)

    Returns:
        Search results with extended context showing method signatures and implementations
    """
    if not keyword or len(keyword.strip()) == 0:
        return "ERROR: Keyword cannot be empty"

    max_results = min(max_results, 10)  # Cap at 10 results

    results = []
    results.append(f"=== Smart Search: '{keyword}' ===")
    results.append(f"Context: 10 lines before, 30 lines after each match")
    results.append(f"Max results: {max_results}\n")

    total_found = 0
    all_matches = []

    # Search all modules
    for module_name, file_path in API_MODULES.items():
        content = read_file_safe(file_path)

        if content.startswith("ERROR"):
            continue

        # Find all matches (case-insensitive)
        pattern = re.compile(re.escape(keyword), re.IGNORECASE)
        matches = pattern.finditer(content)

        for match in matches:
            context, line_num = get_asymmetric_context(content, match.start(), lines_before=10, lines_after=30)
            all_matches.append({
                'module': module_name,
                'line': line_num,
                'context': context,
                'file_path': file_path
            })
            total_found += 1

    if total_found == 0:
        return f"No matches found for '{keyword}' in any module."

    # Show limited results
    results.append(f"Found {total_found} total match(es), showing first {min(max_results, total_found)}:\n")

    for idx, match_info in enumerate(all_matches[:max_results]):
        results.append("=" * 80)
        results.append(f"Match {idx + 1}/{min(max_results, total_found)} - adsk.{match_info['module']} (line {match_info['line']})")
        results.append("=" * 80)
        results.append(match_info['context'])
        results.append("")

    if total_found > max_results:
        results.append(f"\n... and {total_found - max_results} more matches not shown.")
        results.append(f"Use max_results parameter to see more (max: 10)")

    return "\n".join(results)


@mcp.tool()
def get_full_class(class_name: str) -> str:
    """
    Extract a complete class definition including all methods, properties, and docstrings.
    Searches across all modules and returns the full class implementation.

    Args:
        class_name: Name of the class to extract (e.g., "CommandInput", "BRepBody", "Sketch")

    Returns:
        Complete class definition with all members, or error if not found
    """
    if not class_name or len(class_name.strip()) == 0:
        return "ERROR: Class name cannot be empty"

    results = []
    results.append(f"=== Extracting Full Class: '{class_name}' ===\n")

    found = False

    for module_name, file_path in API_MODULES.items():
        content = read_file_safe(file_path)

        if content.startswith("ERROR"):
            continue

        # Try to extract the class
        class_data = extract_full_class(content, class_name)

        if class_data:
            class_content, start_line = class_data
            found = True

            results.append("=" * 80)
            results.append(f"Found in: adsk.{module_name}")
            results.append(f"File: {file_path.name}")
            results.append(f"Starting at line: {start_line}")
            results.append(f"Total lines: {len(class_content.splitlines())}")
            results.append("=" * 80)
            results.append("")
            results.append(class_content)
            results.append("")
            results.append("=" * 80)

            # Only return first match
            break

    if not found:
        return f"ERROR: Class '{class_name}' not found in any module.\n\nTip: Check spelling or try search_api('{class_name}') to find similar names."

    return "\n".join(results)


@mcp.tool()
def search_by_category(category: str) -> str:
    """
    Search for API elements by category (ui, geometry, sketch, feature, etc.).
    Returns a comprehensive list of related classes and their locations.

    Available categories:
    - ui: User interface elements (commands, inputs, dialogs, palettes, HTML)
    - geometry: Geometric primitives (points, vectors, curves, surfaces, BRep)
    - sketch: Sketching features (lines, circles, constraints, profiles)
    - feature: Design features (extrude, revolve, fillet, pattern)
    - component: Assembly and component management
    - cam: CAM/Manufacturing operations
    - material: Materials and appearances
    - document: Document and file management

    Args:
        category: Category name (see list above)

    Returns:
        List of all classes in the category with brief descriptions
    """
    category = category.lower().strip()

    if category not in CATEGORY_KEYWORDS:
        available = ", ".join(CATEGORY_KEYWORDS.keys())
        return f"ERROR: Unknown category '{category}'.\n\nAvailable categories: {available}"

    keywords = CATEGORY_KEYWORDS[category]

    results = []
    results.append(f"=== Category: '{category.upper()}' ===")
    results.append(f"Searching for: {', '.join(keywords[:5])}{'...' if len(keywords) > 5 else ''}")
    results.append("=" * 80)
    results.append("")

    # Collect all matching classes
    found_classes = {}

    for module_name, file_path in API_MODULES.items():
        content = read_file_safe(file_path)

        if content.startswith("ERROR"):
            continue

        # Search for class definitions containing any of the keywords
        for keyword in keywords:
            # Match class definitions
            pattern = re.compile(rf'^class\s+(\w*{re.escape(keyword)}\w*)\s*[\(:]', re.MULTILINE | re.IGNORECASE)
            matches = pattern.finditer(content)

            for match in matches:
                class_name = match.group(1)
                if class_name not in found_classes:
                    # Get a brief description (first line of docstring if available)
                    context, line_num = get_asymmetric_context(content, match.start(), lines_before=0, lines_after=10)

                    # Try to extract docstring
                    doc_match = re.search(r'"""(.*?)"""', context, re.DOTALL)
                    description = "No description"
                    if doc_match:
                        description = doc_match.group(1).strip().split('\n')[0][:100]

                    found_classes[class_name] = {
                        'module': module_name,
                        'line': line_num,
                        'description': description
                    }

    if not found_classes:
        return f"No classes found in category '{category}'."

    # Format results
    results.append(f"Found {len(found_classes)} classe(s):\n")

    # Sort by module then name
    sorted_classes = sorted(found_classes.items(), key=lambda x: (x[1]['module'], x[0]))

    current_module = None
    for class_name, info in sorted_classes:
        if info['module'] != current_module:
            current_module = info['module']
            results.append(f"\n--- adsk.{current_module} ---")

        results.append(f"  • {class_name} (line {info['line']})")
        results.append(f"    {info['description']}")

    results.append(f"\n{'=' * 80}")
    results.append(f"Total: {len(found_classes)} classes in '{category}' category")
    results.append(f"\nTip: Use get_full_class('ClassName') to see the complete definition")

    return "\n".join(results)


@mcp.tool()
def explore_ui() -> str:
    """
    Specialized tool to explore ALL UI/GUI related classes and interfaces.
    Returns a comprehensive overview of user interface capabilities in Fusion 360.

    This includes:
    - Commands and command inputs
    - Dialogs and palettes
    - HTML/Browser interfaces
    - Buttons, textboxes, and controls
    - Event handlers
    - Custom graphics

    Returns:
        Comprehensive UI/GUI class listing with categorization
    """
    results = []
    results.append("=" * 80)
    results.append("=== FUSION 360 UI/GUI EXPLORER ===")
    results.append("=" * 80)
    results.append("")

    ui_classes = {}

    for module_name, file_path in API_MODULES.items():
        content = read_file_safe(file_path)

        if content.startswith("ERROR"):
            continue

        # Search for all UI-related keywords
        all_ui_keywords = []
        for category, keywords in UI_KEYWORDS.items():
            all_ui_keywords.extend(keywords)

        for keyword in set(all_ui_keywords):
            pattern = re.compile(rf'^class\s+(\w*{re.escape(keyword)}\w*)\s*[\(:]', re.MULTILINE | re.IGNORECASE)
            matches = pattern.finditer(content)

            for match in matches:
                class_name = match.group(1)
                if class_name not in ui_classes:
                    context, line_num = get_asymmetric_context(content, match.start(), lines_before=0, lines_after=10)

                    doc_match = re.search(r'"""(.*?)"""', context, re.DOTALL)
                    description = "No description"
                    if doc_match:
                        description = doc_match.group(1).strip().split('\n')[0][:100]

                    # Categorize
                    category_name = "Other"
                    for cat, kws in UI_KEYWORDS.items():
                        if any(kw.lower() in class_name.lower() for kw in kws):
                            category_name = cat
                            break

                    ui_classes[class_name] = {
                        'module': module_name,
                        'line': line_num,
                        'description': description,
                        'category': category_name
                    }

    # Group by category
    by_category = {}
    for class_name, info in ui_classes.items():
        cat = info['category']
        if cat not in by_category:
            by_category[cat] = []
        by_category[cat].append((class_name, info))

    # Display by category
    for category in UI_KEYWORDS.keys():
        if category in by_category:
            classes = sorted(by_category[category], key=lambda x: x[0])
            results.append(f"\n{'─' * 80}")
            results.append(f"  {category.upper()} ({len(classes)} classes)")
            results.append('─' * 80)

            for class_name, info in classes:
                results.append(f"  • {class_name}")
                results.append(f"    Module: adsk.{info['module']} | Line: {info['line']}")
                results.append(f"    {info['description']}")
                results.append("")

    results.append("=" * 80)
    results.append(f"Total UI/GUI Classes Found: {len(ui_classes)}")
    results.append("=" * 80)
    results.append("\nUsage Tips:")
    results.append("  • Use get_full_class('ClassName') for complete definition")
    results.append("  • Use search_api('keyword') for specific functionality")
    results.append("  • Most UI classes are in adsk.core module")

    return "\n".join(results)


# ============================================================================
# NEW TOOLS v2.1 - Using Index and Fuzzy Search
# ============================================================================

@mcp.tool()
def find_class(class_name: str, fuzzy: bool = True) -> str:
    """
    Fast class lookup using the index with fuzzy search support.

    Args:
        class_name: Name of the class to find
        fuzzy: Enable fuzzy matching for typos (default: True)

    Returns:
        Class information with module, line number, and methods
    """
    # Build index if not built
    api_index.build_index()

    results = []
    results.append(f"=== Find Class: '{class_name}' ===\n")

    # Direct lookup
    class_info = api_index.get_class_info(class_name)

    if class_info:
        results.append("✓ Class found!")
        results.append(f"\nClass: {class_name}")
        results.append(f"Module: adsk.{class_info['module']}")
        results.append(f"Line: {class_info['line']}")
        results.append(f"Methods: {len(class_info['methods'])}")

        # Show inheritance
        hierarchy = api_index.get_class_hierarchy(class_name)
        if len(hierarchy) > 1:
            results.append(f"\nInheritance:")
            for i, cls in enumerate(hierarchy):
                indent = "  " * i
                results.append(f"{indent}└─ {cls}")

        # Show methods
        if class_info['methods']:
            results.append(f"\nMethods ({len(class_info['methods'])}):")
            for method in class_info['methods'][:20]:  # Limit to first 20
                results.append(f"  • {method}()")
            if len(class_info['methods']) > 20:
                results.append(f"  ... and {len(class_info['methods']) - 20} more")

        return "\n".join(results)

    # Not found - try fuzzy search
    if fuzzy:
        suggestions = api_index.fuzzy_search(class_name, limit=5)
        if suggestions:
            results.append("✗ Class not found")
            results.append(f"\nDid you mean:")
            for i, suggestion in enumerate(suggestions, 1):
                results.append(f"  {i}. {suggestion}")
            results.append(f"\nTip: Use find_class('{suggestions[0]}') to see this class")
        else:
            results.append("✗ Class not found and no similar names found")
    else:
        results.append("✗ Class not found")

    return "\n".join(results)


@mcp.tool()
def find_method(method_name: str, fuzzy: bool = True) -> str:
    """
    Find all classes that have a specific method.

    Args:
        method_name: Name of the method to search
        fuzzy: Enable fuzzy matching (default: True)

    Returns:
        List of classes that have this method
    """
    api_index.build_index()

    results = []
    results.append(f"=== Find Method: '{method_name}' ===\n")

    # Find classes with this method
    classes_with_method = api_index.find_by_method(method_name)

    if classes_with_method:
        results.append(f"✓ Found in {len(classes_with_method)} class(es):\n")

        for class_name, module, line in classes_with_method:
            results.append(f"• {class_name}.{method_name}()")
            results.append(f"  Module: adsk.{module}")
            results.append(f"  Line: ~{line}")
            results.append("")

        return "\n".join(results)

    # Not found - try fuzzy
    if fuzzy:
        suggestions = api_index.fuzzy_search(method_name, limit=5)
        if suggestions:
            results.append("✗ Method not found")
            results.append(f"\nDid you mean:")
            for i, suggestion in enumerate(suggestions, 1):
                results.append(f"  {i}. {suggestion}")
        else:
            results.append("✗ Method not found and no similar names found")
    else:
        results.append("✗ Method not found")

    return "\n".join(results)


@mcp.tool()
def get_class_hierarchy(class_name: str) -> str:
    """
    Get the complete inheritance hierarchy for a class.
    Shows parent classes and child classes if available.

    Args:
        class_name: Name of the class

    Returns:
        Complete inheritance tree
    """
    api_index.build_index()

    results = []
    results.append(f"=== Class Hierarchy: '{class_name}' ===\n")

    class_info = api_index.get_class_info(class_name)
    if not class_info:
        suggestions = api_index.fuzzy_search(class_name, limit=3)
        if suggestions:
            results.append("✗ Class not found")
            results.append(f"\nDid you mean: {', '.join(suggestions)}?")
        else:
            results.append("✗ Class not found")
        return "\n".join(results)

    # Get parent hierarchy
    hierarchy = api_index.get_class_hierarchy(class_name)

    results.append("Inheritance Chain:")
    for i, cls in enumerate(hierarchy):
        indent = "  " * i
        arrow = "└─" if i > 0 else "●"
        if cls == class_name:
            results.append(f"{indent}{arrow} {cls} ← YOU ARE HERE")
        else:
            results.append(f"{indent}{arrow} {cls}")

    # Find children
    children = [
        cls for cls, parent in api_index.inheritance.items()
        if parent == class_name
    ]

    if children:
        results.append(f"\nDirect Children ({len(children)}):")
        for child in children[:10]:
            results.append(f"  • {child}")
        if len(children) > 10:
            results.append(f"  ... and {len(children) - 10} more")

    results.append(f"\nModule: adsk.{class_info['module']}")
    results.append(f"Methods: {len(class_info['methods'])}")

    return "\n".join(results)


@mcp.tool()
def list_all_classes(module: str = "all") -> str:
    """
    List all classes in a module or all modules.
    Uses the index for instant results.

    Args:
        module: Module name (core, fusion, cam, etc.) or "all"

    Returns:
        Complete list of classes
    """
    api_index.build_index()

    results = []

    if module == "all":
        results.append("=== All Classes in Fusion 360 API ===\n")
        total_classes = 0

        for mod in sorted(API_MODULES.keys()):
            classes = api_index.module_classes.get(mod, [])
            if classes:
                results.append(f"\n--- adsk.{mod} ({len(classes)} classes) ---")
                for cls in sorted(classes)[:20]:
                    results.append(f"  • {cls}")
                if len(classes) > 20:
                    results.append(f"  ... and {len(classes) - 20} more")
                total_classes += len(classes)

        results.append(f"\n{'=' * 80}")
        results.append(f"Total: {total_classes} classes across {len(API_MODULES)} modules")
    else:
        if module not in API_MODULES:
            results.append(f"✗ Module '{module}' not found")
            results.append(f"\nAvailable modules: {', '.join(API_MODULES.keys())}")
            return "\n".join(results)

        classes = api_index.module_classes.get(module, [])
        results.append(f"=== Classes in adsk.{module} ===\n")
        results.append(f"Total: {len(classes)} classes\n")

        for cls in sorted(classes):
            class_info = api_index.get_class_info(cls)
            method_count = len(class_info['methods']) if class_info else 0
            results.append(f"• {cls} ({method_count} methods)")

    return "\n".join(results)


# ============================================================================
# DOMAIN AGENTS (UI, Core, Fusion, CAM, Drawing, Volume, Simulation)
# ============================================================================


@mcp.tool()
def ui_agent(task: str = "", mode: str = "auto", limit: int = 20) -> str:
    """
    UI/GUI agent. Surfaces commands, inputs, dialogs, palettes, events from adsk.core/adsk.fusion.
    Args:
      task: search term or concept
      mode: auto|class|method|all
      limit: max results
    """
    return run_ui_agent({"query": task, "mode": mode, "limit": limit})


@mcp.tool()
def core_agent(task: str = "", mode: str = "auto", limit: int = 20) -> str:
    """
    Core agent. Focus on adsk.core (UI, geometry, app/doc objects).
    Args mirror ui_agent.
    """
    return run_core_agent({"query": task, "mode": mode, "limit": limit})


@mcp.tool()
def fusion_agent(task: str = "", mode: str = "auto", limit: int = 20) -> str:
    """
    Fusion agent. Focus on adsk.fusion (features, components, sketches).
    Args mirror ui_agent.
    """
    return run_fusion_agent({"query": task, "mode": mode, "limit": limit})


@mcp.tool()
def cam_agent(task: str = "", mode: str = "auto", limit: int = 20) -> str:
    """
    CAM agent. Focus on adsk.cam (operations, toolpaths, strategies, posting).
    Args mirror ui_agent.
    """
    return run_cam_agent({"query": task, "mode": mode, "limit": limit})


@mcp.tool()
def drawing_agent(task: str = "", mode: str = "auto", limit: int = 20) -> str:
    """
    Drawing agent. Focus on adsk.drawing (sheets, views, dimensions).
    Args mirror ui_agent.
    """
    return run_drawing_agent({"query": task, "mode": mode, "limit": limit})


@mcp.tool()
def volume_agent(task: str = "", mode: str = "auto", limit: int = 20) -> str:
    """
    Volume/Mesh agent. Focus on adsk.volume (mesh/volume entities).
    Args mirror ui_agent.
    """
    return run_volume_agent({"query": task, "mode": mode, "limit": limit})


@mcp.tool()
def sim_agent(task: str = "", mode: str = "auto", limit: int = 20) -> str:
    """
    Simulation agent. Focus on adsk.sim (if available).
    Args mirror ui_agent.
    """
    return run_sim_agent({"query": task, "mode": mode, "limit": limit})


@mcp.resource("fusion://full_context")
def get_full_context() -> str:
    """
    Get the complete content of ALL API definition files concatenated.
    WARNING: This is ~3.7MB of content (89,000+ lines).

    Returns:
        Concatenated content of all 7 API module files
    """
    results = []
    results.append("=== FUSION 360 API COMPLETE DOCUMENTATION ===")
    results.append(f"API Version: {get_api_version()}")
    results.append("=" * 80)

    for module_name, file_path in API_MODULES.items():
        results.append(f"\n{'=' * 80}")
        results.append(f"=== MODULE: adsk.{module_name} ===")
        results.append(f"=== File: {file_path.name} ===")
        results.append("=" * 80)
        content = read_file_safe(file_path)
        results.append(content)
        results.append("\n")

    return "\n".join(results)


@mcp.resource("fusion://core")
def get_core_definitions() -> str:
    """
    Get the adsk.core module API definitions (916KB, 22,263 lines).
    Core application functionality including UI, geometry, and application objects.

    Returns:
        Content of core.py file
    """
    return read_file_safe(API_MODULES["core"])


@mcp.resource("fusion://fusion")
def get_fusion_definitions() -> str:
    """
    Get the adsk.fusion module API definitions (2.4MB, 55,453 lines).
    Fusion 360 design features including sketches, features, components, etc.

    Returns:
        Content of fusion.py file
    """
    return read_file_safe(API_MODULES["fusion"])


@mcp.resource("fusion://cam")
def get_cam_definitions() -> str:
    """
    Get the adsk.cam module API definitions (358KB, 9,952 lines).
    CAM and manufacturing operations including toolpaths, operations, strategies.

    Returns:
        Content of cam.py file
    """
    return read_file_safe(API_MODULES["cam"])


@mcp.resource("fusion://drawing")
def get_drawing_definitions() -> str:
    """
    Get the adsk.drawing module API definitions (5.9KB, 179 lines).
    Drawing and documentation functionality.

    Returns:
        Content of drawing.py file
    """
    return read_file_safe(API_MODULES["drawing"])


@mcp.resource("fusion://volume")
def get_volume_definitions() -> str:
    """
    Get the adsk.volume module API definitions (41KB, 1,204 lines).
    Volume and mesh operations.

    Returns:
        Content of volume.py file
    """
    return read_file_safe(API_MODULES["volume"])


@mcp.resource("fusion://sim")
def get_sim_definitions() -> str:
    """
    Get the adsk.sim module API definitions (231B, 9 lines).
    Simulation capabilities.

    Returns:
        Content of sim.py file
    """
    return read_file_safe(API_MODULES["sim"])


def get_api_version() -> str:
    """Get the API version from version.txt file."""
    try:
        if VERSION_FILE.exists():
            return VERSION_FILE.read_text().strip()
        return "Unknown"
    except Exception:
        return "Unknown"


@mcp.resource("fusion://info")
def get_server_info() -> str:
    """
    Get information about this MCP server and the API files it serves.

    Returns:
        Server information and file status
    """
    info = []
    info.append("=== Fusion 360 MCP Server Info ===\n")
    info.append(f"API Version: {get_api_version()}")
    info.append(f"Base Path: {API_BASE_PATH}\n")

    info.append("=== Available API Modules ===")
    total_size = 0
    total_lines = 0

    module_stats = {
        "core": (916 * 1024, 22263),
        "fusion": (2400 * 1024, 55453),
        "cam": (358 * 1024, 9952),
        "drawing": (6 * 1024, 179),
        "volume": (41 * 1024, 1204),
        "sim": (231, 9),
        "init": (1300, 12),
    }

    for module_name, file_path in API_MODULES.items():
        exists = file_path.exists()
        size_bytes, lines = module_stats.get(module_name, (0, 0))

        info.append(f"\n- adsk.{module_name} ({file_path.name})")
        info.append(f"  Path: {file_path}")
        info.append(f"  Exists: {exists}")
        if exists:
            actual_size = file_path.stat().st_size
            info.append(f"  Size: {actual_size:,} bytes ({actual_size / 1024:.1f} KB)")
            info.append(f"  Est. Lines: ~{lines:,}")
            total_size += actual_size
            total_lines += lines

    info.append(f"\n=== Summary ===")
    info.append(f"Total Size: {total_size:,} bytes ({total_size / 1024 / 1024:.2f} MB)")
    info.append(f"Total Lines: ~{total_lines:,}")

    info.append("\n=== Available Tools ===")

    info.append("\n1. search_fusion_api(query: str, modules: str = 'all')")
    info.append("   General search across modules (20 lines context)")
    info.append("   Examples:")
    info.append("     search_fusion_api('BRepBody')")
    info.append("     search_fusion_api('Sketch', modules='fusion,core')")

    info.append("\n2. search_api(keyword: str, max_results: int = 5)")
    info.append("   Smart search with asymmetric context (10 before, 30 after)")
    info.append("   Perfect for finding method signatures and implementations")
    info.append("   Examples:")
    info.append("     search_api('CommandInput')")
    info.append("     search_api('createExtrude', max_results=3)")

    info.append("\n3. get_full_class(class_name: str)")
    info.append("   Extract complete class definition with all methods")
    info.append("   Examples:")
    info.append("     get_full_class('BRepBody')")
    info.append("     get_full_class('Sketch')")

    info.append("\n4. search_by_category(category: str)")
    info.append("   Browse API by category")
    info.append("   Categories: ui, geometry, sketch, feature, component, cam, material, document")
    info.append("   Examples:")
    info.append("     search_by_category('ui')")
    info.append("     search_by_category('geometry')")

    info.append("\n5. explore_ui()")
    info.append("   Comprehensive UI/GUI explorer")
    info.append("   Returns all interface-related classes categorized by type")
    info.append("   Includes: Commands, Inputs, Dialogs, Palettes, HTML, Events, Graphics")

    info.append("\n=== NEW TOOLS v2.1 (Fast & Smart!) ===")

    info.append("\n6. find_class(class_name: str, fuzzy: bool = True) ⭐")
    info.append("   FAST class lookup using in-memory index")
    info.append("   Fuzzy search suggests corrections for typos")
    info.append("   Shows: module, methods, inheritance")
    info.append("   Examples:")
    info.append("     find_class('BRepBody')")
    info.append("     find_class('Sktech')  # Suggests 'Sketch'")

    info.append("\n7. find_method(method_name: str, fuzzy: bool = True) ⭐")
    info.append("   Find all classes with a specific method")
    info.append("   Examples:")
    info.append("     find_method('createExtrude')")
    info.append("     find_method('addComand')  # Suggests 'addCommand'")

    info.append("\n8. get_class_hierarchy(class_name: str) ⭐")
    info.append("   Show complete inheritance tree")
    info.append("   Displays parents and children")
    info.append("   Example:")
    info.append("     get_class_hierarchy('BRepBody')")

    info.append("\n9. list_all_classes(module: str = 'all') ⭐")
    info.append("   List all classes (INSTANT with index!)")
    info.append("   Examples:")
    info.append("     list_all_classes()  # All modules")
    info.append("     list_all_classes('core')  # Just core")

    info.append("\n=== Domain Agents (internal, no external calls) ===")
    info.append("10. ui_agent(task: str, mode: str = 'auto', limit: int = 20)")
    info.append("    UI/GUI focus across adsk.core + adsk.fusion (commands, inputs, dialogs, palettes, events)")
    info.append("11. core_agent(task: str, mode: str = 'auto', limit: int = 20)")
    info.append("    Core focus (application, documents, general UI/geometry in adsk.core)")
    info.append("12. fusion_agent(task: str, mode: str = 'auto', limit: int = 20)")
    info.append("    Fusion focus (features, components, sketches in adsk.fusion)")
    info.append("13. cam_agent(task: str, mode: str = 'auto', limit: int = 20)")
    info.append("    CAM focus (operations, toolpaths, strategies, posting in adsk.cam)")
    info.append("14. drawing_agent(task: str, mode: str = 'auto', limit: int = 20)")
    info.append("    Drawing focus (sheets, views, dimensions in adsk.drawing)")
    info.append("15. volume_agent(task: str, mode: str = 'auto', limit: int = 20)")
    info.append("    Volume/Mesh focus (mesh/volume entities in adsk.volume)")
    info.append("16. sim_agent(task: str, mode: str = 'auto', limit: int = 20)")
    info.append("    Simulation focus (adsk.sim where available)")

    info.append("\n=== Available Resources ===")
    info.append("- fusion://full_context   - ALL modules concatenated (~3.7MB)")
    info.append("- fusion://core           - adsk.core module (916KB)")
    info.append("- fusion://fusion         - adsk.fusion module (2.4MB)")
    info.append("- fusion://cam            - adsk.cam module (358KB)")
    info.append("- fusion://drawing        - adsk.drawing module (5.9KB)")
    info.append("- fusion://volume         - adsk.volume module (41KB)")
    info.append("- fusion://sim            - adsk.sim module (231B)")
    info.append("- fusion://info           - This information page")
    info.append("- fusion://version        - API version information")
    info.append("- fusion://guide          - Auto-usage guide for this MCP server")
    info.append("- fusion://guide/ui       - UI/GUI-specific playbook (commands, inputs, dialogs)")
    info.append("- fusion://guide/cam      - CAM-specific playbook (ops, toolpaths, strategy)")
    info.append("- fusion://init           - Initialization snippet to set agent defaults in clients")

    return "\n".join(info)


@mcp.resource("fusion://version")
def get_version_info() -> str:
    """
    Get API version information.

    Returns:
        Version information and details
    """
    version = get_api_version()
    info = []
    info.append("=== Fusion 360 API Version ===\n")
    info.append(f"Version: {version}")
    info.append(f"Source: {VERSION_FILE}")
    info.append(f"\nThis version corresponds to the Autodesk Fusion 360 API definitions.")
    info.append("All Python type definitions (.py files) are generated for code intelligence.")

    return "\n".join(info)


@mcp.resource("fusion://guide")
def get_usage_guide() -> str:
    """
    Auto-usage guide so agents can work without local paths or user hints.
    Always call these tools/resources before coding Fusion 360 to avoid guessing APIs.
    """
    guide = []
    guide.append("=== Fusion 360 MCP Auto-Usage Guide ===\n")
    guide.append("Stop guessing Fusion 360 APIs. Use these MCP tools first:\n")

    guide.append("Tools:")
    guide.append("- explore_ui()  -> full UI/GUI catalog: commands, inputs, dialogs, palettes, events")
    guide.append("- search_by_category('<ui|geometry|sketch|feature|component|cam|material|document>')")
    guide.append("               -> discover valid classes for the domain")
    guide.append("- get_full_class('<ClassName>')  -> entire class definition with module and line")
    guide.append("- search_api('keyword', max_results=5..10)  -> 10 lines before, 30 after; best for signatures")
    guide.append("- search_fusion_api('term', modules='all|core|fusion|cam|drawing|volume|sim')")
    guide.append("               -> symmetric 20/20 context for broad hunts")
    guide.append("- find_class('<Name>', fuzzy=True)  -> indexed lookup with typo suggestions")
    guide.append("- find_method('<method>', fuzzy=True) -> classes implementing a method")
    guide.append("- get_class_hierarchy('<Class>') -> parents/children")
    guide.append("- list_all_classes('all'|'core'|'fusion'|...) -> inventory for a module")

    guide.append("\nResources:")
    guide.append("- fusion://core, fusion://fusion, fusion://cam, fusion://drawing, fusion://volume, fusion://sim")
    guide.append("  -> direct module contents if bulk context is needed")
    guide.append("- fusion://full_context -> all modules concatenated (~3.7MB) if exhaustive scan is required")
    guide.append("- fusion://info -> server/tool index")
    guide.append("- fusion://version -> API version")

    guide.append("\nDefault workflow (follow autonomously):")
    guide.append("1) If unsure of a name -> search_api('<term>'); if class known -> get_full_class('<Class>').")
    guide.append("2) UI work -> explore_ui() or search_by_category('ui'), then get_full_class on the chosen input/handler.")
    guide.append("3) Features/geometry/CAM -> search_by_category('<domain>') to list valid classes, then get_full_class/search_api.")
    guide.append("4) Only know a concept (e.g., 'extrude') -> search_fusion_api('extrude', modules='fusion').")
    guide.append("5) Use returned module+line to import correctly; do not invent methods or arguments.")

    guide.append("\nThis guide is part of the MCP server; no local file references are required.")

    return "\n".join(guide)


@mcp.resource("fusion://guide/ui")
def get_ui_guide() -> str:
    """
    UI/GUI-focused guide. Designed so agents default to the MCP index for any interface task.
    """
    guide = []
    guide.append("=== Fusion 360 UI/GUI Playbook ===\n")
    guide.append("Use these MCP tools before writing UI code:\n")
    guide.append("- explore_ui() -> full UI catalog (commands, inputs, dialogs, palettes, events, graphics)")
    guide.append("- search_by_category('ui') -> list all UI classes if you need a menu of options")
    guide.append("- get_full_class('<UIClass>') -> complete class definition with module+line")
    guide.append("- search_api('<term>', max_results=5..10) -> find signatures/arguments (10 before/30 after)")
    guide.append("- search_fusion_api('<term>', modules='core,fusion') -> broader search for UI terms")
    guide.append("- find_class('<Name>', fuzzy=True) -> typo-tolerant lookup of UI classes")
    guide.append("- find_method('<method>', fuzzy=True) -> find inputs/handlers implementing a method\n")
    guide.append("Workflow (follow automatically):")
    guide.append("1) Need to build a command UI? -> explore_ui() then get_full_class on chosen input types.")
    guide.append("2) Unsure about an input/handler signature? -> search_api('<InputName>') or get_full_class.")
    guide.append("3) Events/handlers -> search_api('EventHandler') or find_method('commandCreated').")
    guide.append("4) HTML/Palette needs -> search_api('HTML') then get_full_class('HTMLEvent', 'HTMLPalette', etc).")
    guide.append("5) Use returned module+line for correct imports; do not invent methods/args.")
    guide.append("\nResources if bulk context needed: fusion://core (UI types), fusion://fusion (design UI pieces).")
    return "\n".join(guide)


@mcp.resource("fusion://guide/cam")
def get_cam_guide() -> str:
    """
    CAM-focused guide. Keeps agents aligned with CAM API definitions.
    """
    guide = []
    guide.append("=== Fusion 360 CAM Playbook ===\n")
    guide.append("Use these MCP tools before CAM coding:\n")
    guide.append("- search_by_category('cam') -> list all CAM classes (operations, setups, tools, toolpaths, posts)")
    guide.append("- get_full_class('<CamClass>') -> full definition with module+line")
    guide.append("- search_api('<term>', max_results=5..10) -> signatures (10 before/30 after) for operations/toolpaths")
    guide.append("- search_fusion_api('<term>', modules='cam') -> broad CAM search (strategies, NCProgram, post)")
    guide.append("- find_class('<Name>', fuzzy=True) / find_method('<method>', fuzzy=True) -> typo-safe lookup\n")
    guide.append("Workflow (follow automatically):")
    guide.append("1) New CAM flow? -> search_by_category('cam') to choose proper classes (Setup, Operation, Toolpath).")
    guide.append("2) Need creation signatures? -> search_api('create', max_results=10) within CAM, then get_full_class.")
    guide.append("3) Strategies/toolpaths -> search_api('Strategy') or search_fusion_api('toolpath', modules='cam').")
    guide.append("4) Posting/NC -> search_api('post') / get_full_class('NCProgram') / get_full_class('PostProcessParameters').")
    guide.append("5) Use module+line from results; do not guess args or property names.")
    guide.append("\nResources if bulk context needed: fusion://cam (CAM module), fusion://fusion (design links), fusion://full_context for exhaustive scans.")
    return "\n".join(guide)


@mcp.resource("fusion://init")
def get_init_instructions() -> str:
    """
    Initialization message for clients that support /init or startup resources.
    Agents should read this at session start to set defaults.
    """
    lines = []
    lines.append("=== Fusion 360 MCP Init ===")
    lines.append("Defaults: use MCP tools/agents before writing Fusion code; never guess APIs.")
    lines.append("")
    lines.append("Primary tools:")
    lines.append("- ui_agent(task, mode='auto', limit=20) -> UI/GUI in adsk.core+fusion")
    lines.append("- fusion_agent(task, mode, limit) -> Features/components/sketches")
    lines.append("- cam_agent(task, mode, limit) -> CAM ops/toolpaths/strategies/post")
    lines.append("- core_agent / drawing_agent / volume_agent / sim_agent for their domains")
    lines.append("- search_api('keyword') for signatures (10 before/30 after)")
    lines.append("- get_full_class('ClassName') for complete definitions with module+line")
    lines.append("- search_by_category('ui|geometry|sketch|feature|component|cam|material|document')")
    lines.append("- explore_ui() for full UI catalog")
    lines.append("")
    lines.append("Resources: fusion://info, fusion://guide, fusion://guide/ui, fusion://guide/cam")
    lines.append("Import modules as returned by tools (use module+line); do not invent methods/args.")
    return "\n".join(lines)


if __name__ == "__main__":
    # Run the MCP server
    mcp.run()
