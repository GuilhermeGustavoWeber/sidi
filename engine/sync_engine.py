"""
Motor de Sincronizacao Git Autonomo do SIDI.
Executa commits semanticos e push reflexivo no repositorio GitHub.
"""
from datetime import datetime
from pathlib import Path
import subprocess
from typing import Any, Dict, Optional, Tuple

from .config import settings, setup_logger

logger = setup_logger("sync_engine")


class GitSyncEngine:
    def __init__(self, repo_path: Optional[Path] = None):
        self.repo_path = repo_path or settings.project_root

    def _run(self, *args: str) -> Tuple[int, str, str]:
        result = subprocess.run(
            args,
            cwd=self.repo_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore",
        )
        return result.returncode, result.stdout.strip(), result.stderr.strip()

    def get_status(self) -> Dict[str, Any]:
        _, branch, _ = self._run("git", "rev-parse", "--abbrev-ref", "HEAD")
        _, commit, _ = self._run("git", "rev-parse", "--short", "HEAD")
        _, diff, _ = self._run("git", "status", "--porcelain")
        changed = [line for line in diff.splitlines() if line.strip()]
        return {
            "branch": branch or "unknown",
            "commit": commit or "none",
            "is_dirty": len(changed) > 0,
            "changed_files_count": len(changed),
        }

    def checkpoint(self, scope: str = "state(checkpoint)", message: Optional[str] = None) -> Dict[str, Any]:
        self._run("git", "add", "-A")
        ts = datetime.now().strftime("%Y-%m-%dT%H:%M")
        msg = message or f"{scope}: auto-checkpoint {ts}"
        code, out, err = self._run("git", "commit", "-m", msg)
        if code != 0 and "nothing to commit" in (out + err).lower():
            return {
                "committed": False,
                "message": "Nenhuma alteracao detectada para comitar.",
            }

        _, sha, _ = self._run("git", "rev-parse", "--short", "HEAD")
        push_code, _, push_err = self._run("git", "push")
        return {
            "committed": True,
            "sha": sha,
            "message": msg,
            "pushed": push_code == 0,
            "push_error": push_err if push_code != 0 else None,
        }
