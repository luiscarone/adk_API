"""
Core agent for adsk.core utilities (general UI/geometry/application objects).
"""

from __future__ import annotations

from typing import Any, Dict

from .base_agent import DomainAgent


_AGENT = DomainAgent(
    domain_name="Core",
    module_names=["core"],
    focus_keywords=["core", "ui", "application", "document", "geometry"],
)


def run_agent(request: Dict[str, Any]) -> str:
    """
    Entry point for the core agent.
    Args:
        request: {"query": str, "mode": str="auto", "limit": int=20}
    """
    query = (request.get("query") or request.get("task") or "").strip()
    mode = (request.get("mode") or "auto").strip()
    limit = int(request.get("limit") or 20)
    return _AGENT.run(query=query, mode=mode, limit=limit)
