"""
Configuracao central do ecossistema SIDI. Caminhos, constantes de runtime e logging.
"""
from dataclasses import dataclass, field
import logging
from pathlib import Path


@dataclass
class BrainConfig:
    brain_dir: Path = field(default_factory=lambda: Path(__file__).resolve().parent.parent / "brain")

    @property
    def core_dir(self) -> Path:
        return self.brain_dir / "core"

    @property
    def profile_dir(self) -> Path:
        return self.brain_dir / "profile"

    @property
    def memories_dir(self) -> Path:
        return self.brain_dir / "memories"

    @property
    def episodic_dir(self) -> Path:
        return self.memories_dir / "episodic"

    @property
    def semantic_dir(self) -> Path:
        return self.memories_dir / "semantic"

    @property
    def procedural_dir(self) -> Path:
        return self.memories_dir / "procedural"

    @property
    def nodes_dir(self) -> Path:
        return self.brain_dir / "nodes"

    @property
    def lobes_dir(self) -> Path:
        return self.brain_dir / "lobes"

    @property
    def knowledge_graph_path(self) -> Path:
        return self.brain_dir / "knowledge_graph.json"

    @property
    def directives_path(self) -> Path:
        return self.core_dir / "directives.json"

    @property
    def user_profile_path(self) -> Path:
        return self.profile_dir / "user.md"

    @property
    def personality_path(self) -> Path:
        return self.core_dir / "personality.md"


@dataclass
class AppSettings:
    project_root: Path = field(default_factory=lambda: Path(__file__).resolve().parent.parent)
    brain: BrainConfig = field(default_factory=BrainConfig)
    state_dir: Path = field(default_factory=lambda: Path(__file__).resolve().parent.parent / "state")

    @property
    def handoff_path(self) -> Path:
        return self.state_dir / "handoff.json"

    @property
    def goals_path(self) -> Path:
        return self.state_dir / "goals.json"


settings = AppSettings()


def setup_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter("[SIDI :: %(name)s] %(levelname)s: %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    logger.setLevel(level)
    return logger
