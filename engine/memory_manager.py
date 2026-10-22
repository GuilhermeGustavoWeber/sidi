"""
Fachada unificada para o sistema de memoria em quatro camadas (working, episodic, semantic, procedural).
"""
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from .config import settings, setup_logger
from .memory_models import MemoryItem, MemoryMetadata, MemoryType

logger = setup_logger("memory_manager")


class MemoryManager:
    def __init__(self):
        self.brain = settings.brain

    def record_episodic(self, title: str, content: str, projects: Optional[List[str]] = None) -> Path:
        date_str = datetime.now().strftime("%Y-%m-%d")
        slug = "".join(c if c.isalnum() or c in ("-", "_") else "_" for c in title.lower())
        filename = f"{date_str}_{slug}.md"
        target_path = self.brain.episodic_dir / filename
        self.brain.episodic_dir.mkdir(parents=True, exist_ok=True)

        doc = [
            f"# Episodio: {title}",
            f"Data: {datetime.now().isoformat()}",
            f"Projetos: {', '.join(projects or ['geral'])}",
            "",
            "## Conteudo",
            content,
        ]
        target_path.write_text("\n".join(doc), encoding="utf-8")
        logger.info(f"Memoria episodica registrada: {target_path.name}")
        return target_path

    def record_procedural(self, name: str, steps: List[str], intent: str) -> Path:
        filename = f"{name.lower().replace(' ', '_')}.md"
        target_path = self.brain.procedural_dir / filename
        self.brain.procedural_dir.mkdir(parents=True, exist_ok=True)

        doc = [
            f"# Procedimento Operacional Padrao (SOP): {name}",
            f"Objetivo: {intent}",
            "",
            "## Passos de Execucao",
        ]
        for idx, step in enumerate(steps, 1):
            doc.append(f"{idx}. {step}")

        target_path.write_text("\n".join(doc), encoding="utf-8")
        logger.info(f"SOP registrado: {target_path.name}")
        return target_path

    def get_recent_episodes(self, limit: int = 5) -> List[MemoryItem]:
        items: List[MemoryItem] = []
        if not self.brain.episodic_dir.exists():
            return items

        files = sorted(self.brain.episodic_dir.glob("*.md"), reverse=True)[:limit]
        for f in files:
            try:
                text = f.read_text(encoding="utf-8", errors="ignore")
                meta = MemoryMetadata(type=MemoryType.EPISODIC)
                items.append(MemoryItem(title=f.stem, content=text, metadata=meta, filepath=f))
            except Exception as e:
                logger.warning(f"Erro ao ler episodio {f.name}: {e}")
        return items
