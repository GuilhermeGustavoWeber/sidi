"""
Gerenciamento de handoff e persistencia de estado entre sessoes ativas do SIDI.
"""
from dataclasses import asdict, dataclass, field
from datetime import datetime
import json
from pathlib import Path
from typing import List, Optional
import uuid

from .config import settings, setup_logger

logger = setup_logger("session_state")


@dataclass
class SessionState:
    session_id: str = field(
        default_factory=lambda: f"{datetime.utcnow().strftime('%Y-%m-%dT%H-%M-%SZ')}_{uuid.uuid4().hex[:6]}"
    )
    current_project: str = ""
    current_goal: str = ""
    next_action: str = ""
    pending_steps: List[str] = field(default_factory=list)
    completed_steps: List[str] = field(default_factory=list)
    context_notes: str = ""
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())


class HandoffManager:
    def __init__(self, handoff_path: Optional[Path] = None):
        self.handoff_path = handoff_path or settings.handoff_path
        self.handoff_path.parent.mkdir(parents=True, exist_ok=True)

    def save_session(self, state: SessionState) -> None:
        state.updated_at = datetime.now().isoformat()
        self.handoff_path.write_text(
            json.dumps(asdict(state), indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    def load_handoff(self) -> Optional[SessionState]:
        if not self.handoff_path.exists():
            return None
        try:
            data = json.loads(self.handoff_path.read_text(encoding="utf-8"))
            return SessionState(**data)
        except Exception as e:
            logger.warning(f"Falha ao carregar estado de handoff: {e}")
            return None
