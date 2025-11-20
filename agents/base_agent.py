"""
Shared utilities for domain-specific Fusion 360 agents.

Agents read local API definition files directly (no external calls) and provide
fast heuristics to surface classes/methods for a given domain/module set.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Sequence


DEFAULT_API_ROOT = Path(__file__).resolve().parent.parent / "API" / "Python" / "defs" / "adsk"


@dataclass
class MatchResult:
    """Container for a single match line."""

    module: str
    line: int
    kind: str  # "class" or "method"
    name: str
    snippet: str


class DomainAgent:
    """
    Base class to scan specific Fusion 360 API modules.

    It works entirely on local files: reads module text, indexes class/def lines,
    and returns lightweight snippets to guide the caller to the right API entry.
    """

    def __init__(
        self,
        domain_name: str,
        module_names: Sequence[str],
        api_root: Path = DEFAULT_API_ROOT,
        focus_keywords: Optional[Sequence[str]] = None,
    ) -> None:
        self.domain_name = domain_name
        self.api_root = api_root
        self.focus_keywords = [kw.lower() for kw in (focus_keywords or [])]
        self.module_paths: Dict[str, Path] = {
            name: api_root / f"{name}.py" for name in module_names
        }

    def run(self, query: str = "", mode: str = "auto", limit: int = 20) -> str:
        """
        Execute the domain agent.
        - query: search term. If empty, returns a domain summary.
        - mode: auto|class|method|all. Controls what to match.
        - limit: maximum matches to include in the response.
        """
        mode = (mode or "auto").lower()
        query = (query or "").strip()
        summary = self._summary_header()

        if not query:
            return self._compose_summary(summary)

        matches: List[MatchResult] = []
        for module_name, path in self.module_paths.items():
            module_matches = self._scan_module(module_name, path, query, mode, limit - len(matches))
            matches.extend(module_matches)
            if len(matches) >= limit:
                break

        if not matches:
            summary.append(f"No matches for '{query}' in domain '{self.domain_name}'.")
            summary.append("Try adjusting the query or mode (class/method/all).")
            return "\n".join(summary)

        summary.append(f"Found {len(matches)} match(es) for '{query}' in '{self.domain_name}':\n")
        for m in matches[:limit]:
            summary.append(f"[adsk.{m.module}] {m.kind.upper()} {m.name} @ line {m.line}")
            summary.append(m.snippet)
            summary.append("-" * 60)

        if len(matches) > limit:
            summary.append(f"... truncated to {limit} results.")

        return "\n".join(summary)

    def _summary_header(self) -> List[str]:
        lines = [
            f"=== Fusion 360 Domain Agent: {self.domain_name} ===",
            f"Modules: {', '.join(sorted(self.module_paths.keys()))}",
            f"API root: {self.api_root}",
        ]
        if self.focus_keywords:
            lines.append(f"Focus keywords: {', '.join(self.focus_keywords[:8])}"
                         + ("..." if len(self.focus_keywords) > 8 else ""))
        lines.append("")
        return lines

    def _compose_summary(self, header: List[str]) -> str:
        header.append("No query supplied. Domain overview:")
        for module_name, path in self.module_paths.items():
            classes = self._list_classes(path)
            header.append(f"- adsk.{module_name}: {len(classes)} classes detected")
        header.append("\nProvide a query to search classes/methods. modes: auto|class|method|all")
        return "\n".join(header)

    def _list_classes(self, path: Path) -> List[str]:
        text = self._read_file(path)
        if not text:
            return []
        return re.findall(r"^class\s+(\w+)", text, flags=re.MULTILINE)

    def _scan_module(self, module_name: str, path: Path, query: str, mode: str, limit: int) -> List[MatchResult]:
        text = self._read_file(path)
        if not text or limit <= 0:
            return []

        lines = text.splitlines()
        hits: List[MatchResult] = []
        query_lower = query.lower()

        for idx, line in enumerate(lines):
            is_class = line.startswith("class ")
            is_method = line.lstrip().startswith("def ") and line.startswith("    ")

            if mode in ("class",) and not is_class:
                continue
            if mode in ("method",) and not is_method:
                continue
            if mode in ("auto", "all"):
                if not (is_class or is_method):
                    continue

            if query_lower not in line.lower():
                # If no explicit query match, but we have focus keywords, allow focus hits.
                if self.focus_keywords and any(kw in line.lower() for kw in self.focus_keywords):
                    pass
                else:
                    continue

            kind = "class" if is_class else "method"
            name_match = re.search(r"(class|def)\s+(\w+)", line)
            name = name_match.group(2) if name_match else line.strip()

            snippet = self._context(lines, idx, context=3)
            hits.append(MatchResult(module=module_name, line=idx + 1, kind=kind, name=name, snippet=snippet))
            if len(hits) >= limit:
                break

        return hits

    def _context(self, lines: List[str], index: int, context: int = 3) -> str:
        start = max(0, index - context)
        end = min(len(lines), index + context + 1)
        block = lines[start:end]
        numbered = []
        for offset, line in enumerate(block, start=start):
            prefix = ">" if offset == index else " "
            numbered.append(f"{prefix}{offset+1:6d}: {line}")
        return "\n".join(numbered)

    def _read_file(self, path: Path) -> str:
        try:
            if not path.exists():
                return ""
            return path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            return ""
