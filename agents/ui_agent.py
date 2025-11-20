"""
UI/GUI-focused agent for Fusion 360.
Scans adsk.core and adsk.fusion for command/inputs/dialog/palette classes and methods.
"""

from __future__ import annotations

from typing import Any, Dict

from .base_agent import DomainAgent


UI_KEYWORDS = [
    "command",
    "input",
    "dialog",
    "palette",
    "html",
    "browser",
    "window",
    "panel",
    "tab",
    "group",
    "button",
    "textbox",
    "checkbox",
    "event",
    "handler",
    "validate",
]


_AGENT = DomainAgent(
    domain_name="UI/GUI",
    module_names=["core", "fusion"],
    focus_keywords=UI_KEYWORDS,
)


def run_agent(request: Dict[str, Any]) -> str:
    """
    Entry point for the UI/GUI agent.
    Args:
        request: {"query": str, "mode": str="auto", "limit": int=20}
    """
    query = (request.get("query") or request.get("task") or "").strip()
    mode = (request.get("mode") or "auto").strip()
    limit = int(request.get("limit") or 20)
    return _AGENT.run(query=query, mode=mode, limit=limit)
