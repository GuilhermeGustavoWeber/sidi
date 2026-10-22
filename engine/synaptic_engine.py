"""
Motor de Ativacao Sinaptica Propagada e Plasticidade Hebbiana do SIDI.
Analisa grafos de wikilinks em arquivos Markdown e calcula pesos associativos.
"""
from datetime import datetime
import json
from pathlib import Path
import re
from typing import Any, Dict, List, Optional, Set, Tuple

from .config import settings, setup_logger

logger = setup_logger("synaptic_engine")


class SynapticEngine:
    def __init__(self, brain_dir: Optional[Path] = None, graph_file: Optional[Path] = None):
        self.brain_dir = brain_dir or settings.brain.brain_dir
        self.graph_file = graph_file or settings.brain.knowledge_graph_path
        self.nodes: Dict[str, Dict[str, Any]] = {}
        self.edges: Dict[Tuple[str, str], float] = {}
        self.load_or_build_graph()

    def load_or_build_graph(self) -> None:
        if not self.brain_dir.exists():
            return

        for md_file in self.brain_dir.rglob("*.md"):
            node_id = md_file.stem
            try:
                content = md_file.read_text(encoding="utf-8", errors="ignore")
            except Exception as e:
                logger.warning(f"Falha ao ler {md_file}: {e}")
                content = ""
            try:
                rel_path = str(md_file.relative_to(settings.project_root))
            except ValueError:
                rel_path = str(md_file)

            self.nodes[node_id] = {
                "id": node_id,
                "path": rel_path,
                "content": content,
                "keywords": self._extract_keywords(node_id, content),
                "lobe": self._detect_lobe(md_file, content),
            }

        persisted_edges: Dict[Tuple[str, str], float] = {}
        if self.graph_file.exists():
            try:
                data = json.loads(self.graph_file.read_text(encoding="utf-8"))
                for edge in data.get("edges", []):
                    persisted_edges[(edge["source"], edge["target"])] = float(edge.get("weight", 1.0))
            except Exception as e:
                logger.warning(f"Erro ao carregar knowledge_graph.json: {e}")

        for node_id, data in self.nodes.items():
            links = re.findall(r"\[\[(.*?)\]\]", data["content"])
            for target in links:
                clean = target.split("|")[0].strip()
                if clean in self.nodes:
                    pair = (node_id, clean)
                    self.edges[pair] = persisted_edges.get(pair, 1.0)

    def _extract_keywords(self, node_id: str, content: str) -> Set[str]:
        words = set(re.findall(r"\b[a-zA-Z0-9_-]{3,}\b", node_id.lower()))
        for line in content.splitlines()[:20]:
            words.update(re.findall(r"\b[a-zA-Z0-9_-]{4,}\b", line.lower()))
        return words

    def _detect_lobe(self, path: Path, content: str) -> str:
        p = str(path).lower()
        c_lower = content.lower()[:300]
        if "frontal" in p or "lei" in c_lower or "regra" in c_lower or "security" in c_lower:
            return "frontal"
        if "parietal" in p or "stack" in c_lower or "engine" in p or "code" in c_lower:
            return "parietal"
        if "temporal" in p or "episodic" in p or "sessao" in c_lower or "history" in c_lower:
            return "temporal"
        if "occipital" in p or "design" in c_lower or "ui" in c_lower or "css" in c_lower:
            return "occipital"
        if "limbico" in p or "profile" in p or "user" in p or "dossier" in p:
            return "limbico"
        return "cortex"

    def activate(self, query: str, max_hops: int = 2, decay: float = 0.65) -> Dict[str, Any]:
        query_tokens = set(re.findall(r"\b[a-zA-Z0-9_-]{3,}\b", query.lower()))
        energy: Dict[str, float] = {}
        seeds: List[str] = []

        for nid, node in self.nodes.items():
            matches = query_tokens.intersection(node["keywords"])
            if matches:
                score = len(matches) * 1.5
                if nid.lower() in query.lower():
                    score += 5.0
                energy[nid] = score
                seeds.append(nid)

        if not seeds:
            if "user" in self.nodes:
                energy["user"] = 1.0
                seeds.append("user")
            elif self.nodes:
                first = next(iter(self.nodes))
                energy[first] = 1.0
                seeds.append(first)

        for _ in range(max_hops):
            for src in list(energy.keys()):
                src_e = energy[src]
                if src_e <= 0.1:
                    continue
                for (s, t), w in self.edges.items():
                    target = t if s == src else (s if t == src else None)
                    if target and target in self.nodes:
                        transfer = src_e * (w / (w + 1.0)) * decay
                        energy[target] = energy.get(target, 0.0) + transfer

        sorted_nodes = sorted(energy.items(), key=lambda x: x[1], reverse=True)
        top_nodes = sorted_nodes[:10]
        self._hebbian_reinforce([n[0] for n in top_nodes[:5]])
        constraints = self._extract_constraints([n[0] for n in top_nodes])

        return {
            "query": query,
            "seeds": seeds,
            "top_activated": [
                {
                    "node": n[0],
                    "energy": round(n[1], 2),
                    "lobe": self.nodes[n[0]]["lobe"],
                }
                for n in top_nodes
            ],
            "inviolable_constraints": constraints,
        }

    def _hebbian_reinforce(self, active_nodes: List[str]) -> None:
        updated = False
        for i in range(len(active_nodes)):
            for j in range(i + 1, len(active_nodes)):
                for pair in [(active_nodes[i], active_nodes[j]), (active_nodes[j], active_nodes[i])]:
                    if pair in self.edges:
                        self.edges[pair] = min(5.0, self.edges[pair] + 0.05)
                        updated = True
        if updated:
            self._persist_graph()

    def _extract_constraints(self, active_node_ids: List[str]) -> List[str]:
        constraints: List[str] = []
        for nid in active_node_ids:
            content = self.nodes.get(nid, {}).get("content", "")
            for block in re.findall(
                r"(?:Lei|Mandato|Restri|Inegoci|Regra|Guardrail)[\w\s:]+\n([^\n#]+)",
                content,
                re.IGNORECASE,
            ):
                cleaned = block.strip().replace("- ", "").strip()
                if cleaned and cleaned not in constraints:
                    constraints.append(f"[{nid}] {cleaned}")
        return constraints[:6]

    def _persist_graph(self) -> None:
        edges_data = [{"source": s, "target": t, "weight": round(w, 3)} for (s, t), w in self.edges.items()]
        payload = {
            "version": "1.0.0",
            "updated_at": datetime.now().isoformat(),
            "total_nodes": len(self.nodes),
            "total_edges": len(self.edges),
            "edges": edges_data,
        }
        self.graph_file.parent.mkdir(parents=True, exist_ok=True)
        self.graph_file.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
