"""
Volume/Mesh agent for adsk.volume (mesh and volumetric operations).
"""

from __future__ import annotations

from typing import Any, Dict

from .base_agent import DomainAgent


_AGENT = DomainAgent(
    domain_name="Volume/Mesh",
    module_names=["volume"],
    focus_keywords=["mesh", "volume", "facet", "triangle"],
)


def run_agent(request: Dict[str, Any]) -> str:
    """
    Entry point for the volume/mesh agent.
    Args:
        request: {"query": str, "mode": str=\"auto\", "limit": int=20}
    """
    query = (request.get("query") or request.get("task") or "").strip()
    mode = (request.get("mode") or "auto").strip()
    limit = int(request.get("limit") or 20)
    return _AGENT.run(query=query, mode=mode, limit=limit)
