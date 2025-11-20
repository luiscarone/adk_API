# Repository Guidelines: Fusion 360 MCP Agents

- **Always start sessions by reading** `fusion://init` (or `fusion://guide`) so the agent remembers to use MCP tools and domain agents instead of guessing Fusion APIs.
- **Domain agents (MCP tools):** `ui_agent`, `fusion_agent`, `cam_agent`, `core_agent`, `drawing_agent`, `volume_agent`, `sim_agent`. Use `task`, `mode` (`auto|class|method|all`), and `limit` to scope results.
- **Lookup tools:** `search_api`, `get_full_class`, `search_by_category`, `explore_ui`, `search_fusion_api`, `find_class`, `find_method`, `get_class_hierarchy`, `list_all_classes`.
- **Resources:** `fusion://info`, `fusion://guide`, `fusion://guide/ui`, `fusion://guide/cam`, `fusion://core|fusion|cam|drawing|volume|sim`, `fusion://full_context`.
- **Never guess methods or imports;** rely on module+line from tool outputs.
- **VS Code Codex:** run the MCP server, then in chat request `fusion://init` once per session; afterward, call the agents/tools directly. No HTTP/model calls inside agents.***
