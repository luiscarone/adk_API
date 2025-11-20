# Fusion 360 MCP: Automatic Usage Playbook

Goal: remove guessing. Anytime the agent touches Fusion 360 code, it should consult the MCP tools in this repo to fetch the exact class/method signatures from the bundled API docs (see `API/Python/defs/adsk/`).

### What the agent must do
- Load the `fusion360-api` MCP server (already configured in `codex_config.toml`).
- Resolve questions with the tools below **before** writing code instead of inferring from memory.

### Tools to call (no paths needed)
- `explore_ui()` — list every UI/GUI class (commands, inputs, dialogs, palettes, events).
- `search_by_category("<category>")` — discover classes by domain: `ui`, `geometry`, `sketch`, `feature`, `component`, `cam`, `material`, `document`.
- `get_full_class("<ClassName>")` — retrieve a full class definition with all methods/properties/docstrings and its module/line.
- `search_api("keyword", max_results=5..10)` — 10 lines before, 30 after; best for method signatures/implementation context.
- `search_fusion_api("term", modules="all|core|fusion|cam|drawing|volume|sim")` — 20/20 context; good for broad term hunts.
- Resources (read directly): `fusion://info`, `fusion://version`, `fusion://core`, `fusion://fusion`, `fusion://cam`, `fusion://drawing`, `fusion://volume`, `fusion://sim`, `fusion://full_context` (entire API; large).

### Automatic workflow the agent should follow
1) If unsure of a method or class name, call `search_api("<term>")`; if the class is known, call `get_full_class("<ClassName>")`.
2) For UI tasks, start with `explore_ui()` or `search_by_category("ui")`, then drill into specific inputs/handlers with `get_full_class`.
3) For feature/geometry/CAM tasks, use `search_by_category("<domain>")` to list valid classes, then `get_full_class` or `search_api` to confirm signatures.
4) When only a concept is known (e.g., “extrude”), use `search_fusion_api("extrude", modules="fusion")` to find the correct API entry and arguments.
5) Always rely on the returned module + line info to import from the correct module; do not guess or invent methods.

Keep this file as the default reference so the agent always queries the MCP server instead of guessing Fusion 360 APIs.***
