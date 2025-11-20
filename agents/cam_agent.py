"""
CAM agent for adsk.cam (operations, toolpaths, strategies, posting).
"""

from __future__ import annotations

from typing import Any, Dict

from .base_agent import DomainAgent


_AGENT = DomainAgent(
    domain_name="CAM",
    module_names=["cam"],
    focus_keywords=["operation", "toolpath", "setup", "strategy", "post", "ncprogram", "tool"],
)


def run_agent(request: Dict[str, Any]) -> str:
    """
    Entry point for the CAM agent.
    Args:
        request: {"query": str, "mode": str=\"auto\", "limit": int=20}
    """
    query = (request.get("query") or request.get("task") or "").strip()
    mode = (request.get("mode") or "auto").strip()
    limit = int(request.get("limit") or 20)
    return _AGENT.run(query=query, mode=mode, limit=limit)
