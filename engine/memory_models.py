"""
Definicoes de tipos de dados canonicos do sistema de memoria em quatro camadas do SIDI.
"""
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import List, Optional
import uuid


class MemoryType(str, Enum):
    WORKING = "working"
    EPISODIC = "episodic"
    SEMANTIC = "semantic"
    PROCEDURAL = "procedural"


@dataclass
class MemoryMetadata:
    id: str = field(default_factory=lambda: uuid.uuid4().hex[:8])
    type: MemoryType = MemoryType.EPISODIC
    importance: float = 0.5
    confidence: float = 1.0
    projects: List[str] = field(default_factory=list)
    entities: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)


@dataclass
class MemoryItem:
    title: str
    content: str
    metadata: MemoryMetadata = field(default_factory=MemoryMetadata)
    filepath: Optional[Path] = None
