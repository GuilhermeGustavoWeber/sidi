"""
Auditor Pre-Frontal de Seguranca, Guardrails e Anti-Sicofancia do SIDI.
Intercepta e valida propostas, comandos e codigo antes da execucao.
"""
from dataclasses import dataclass
import json
from pathlib import Path
import re
from typing import List, Tuple

from .config import settings, setup_logger

logger = setup_logger("prefrontal_cortex")


@dataclass
class AuditResult:
    is_safe: bool
    violations: List[str]
    warnings: List[str]


class PrefrontalCortex:
    def __init__(self):
        self.directives = self._load_directives()

    def _load_directives(self) -> dict:
        directives_file = settings.brain.directives_path
        if directives_file.exists():
            try:
                return json.loads(directives_file.read_text(encoding="utf-8"))
            except Exception as e:
                logger.error(f"Erro ao carregar diretivas pre-frontais: {e}")
        return {}

    def audit_execution(self, command_or_intent: str) -> AuditResult:
        violations: List[str] = []
        warnings: List[str] = []
        lowered = command_or_intent.lower()

        # Checagem de acoes destrutivas que exigem confirmacao explicita
        destructive_patterns = [
            r"rm\s+-rf",
            r"del\s+/[s|q]",
            r"drop\s+database",
            r"drop\s+table",
            r"format\s+[c-z]:",
            r"git\s+reset\s+--hard",
            r"git\s+push\s+.*--force",
        ]
        for pattern in destructive_patterns:
            if re.search(pattern, lowered):
                violations.append(
                    f"Acao critica/destrutiva detectada ('{pattern}'). Requer autorizacao explicita de Guilherme."
                )

        # Checagem de vazamento de credenciais e seguranca
        credential_leak_patterns = [
            r"api[_-]?key\s*=\s*['\"][a-zA-Z0-9_\-]{8,}['\"]",
            r"password\s*=\s*['\"][^'\"]+['\"]",
            r"secret\s*=\s*['\"][^'\"]+['\"]",
        ]
        for pattern in credential_leak_patterns:
            if re.search(pattern, command_or_intent):
                violations.append("Exposicao direta de segredo/credencial no texto/codigo detectada.")

        # Checagem de execucao oculta/disfarcada
        if "-windowstyle hidden" in lowered or "start-process -nonewwindow" in lowered:
            violations.append("Violacao de transparencia: tentativa de execucao de processo oculto.")

        # Alertas de tipagem estrita
        if "type: ignore" in command_or_intent or "any" in lowered.split():
            warnings.append("Alerta de tipagem: uso de Any ou supressao de tipos detectado.")

        return AuditResult(
            is_safe=len(violations) == 0,
            violations=violations,
            warnings=warnings,
        )
