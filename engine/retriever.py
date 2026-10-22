"""
Mecanismo de busca e recuperacao hibrida (lexica + semantica via grafo neural).
"""
from pathlib import Path
import re
from typing import Any, Dict, List

from .config import settings
from .synaptic_engine import SynapticEngine


class CognitiveRetriever:
    def __init__(self):
        self.synaptic = SynapticEngine()

    def search(self, query: str, top_k: int = 5) -> Dict[str, Any]:
        neural_res = self.synaptic.activate(query)
        lexical_hits = self._lexical_search(query, limit=top_k)

        return {
            "query": query,
            "neural_activations": neural_res.get("top_activated", []),
            "constraints": neural_res.get("inviolable_constraints", []),
            "lexical_matches": lexical_hits,
        }

    def _lexical_search(self, query: str, limit: int = 5) -> List[Dict[str, str]]:
        tokens = set(re.findall(r"\b[a-zA-Z0-9_-]{3,}\b", query.lower()))
        results = []

        if not settings.brain.brain_dir.exists():
            return results

        for md_file in settings.brain.brain_dir.rglob("*.md"):
            try:
                text = md_file.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue

            lowered = text.lower()
            matches = sum(1 for t in tokens if t in lowered)
            if matches > 0:
                results.append({
                    "file": md_file.name,
                    "path": str(md_file),
                    "score": matches,
                    "excerpt": text[:200].replace("\n", " ").strip(),
                })

        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:limit]
