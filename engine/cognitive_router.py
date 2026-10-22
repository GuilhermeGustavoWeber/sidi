"""
Roteador Cognitivo Central do SIDI.
Integra ativacao sinaptica, portao pre-frontal de seguranca e memoria de trabalho.
"""
from typing import Any, Dict

from .config import setup_logger
from .prefrontal_cortex import PrefrontalCortex
from .synaptic_engine import SynapticEngine

logger = setup_logger("cognitive_router")


class CognitiveRouter:
    def __init__(self):
        self.synaptic = SynapticEngine()
        self.prefrontal = PrefrontalCortex()

    def process(self, prompt: str) -> Dict[str, Any]:
        # 1. Auditoria pre-frontal de seguranca e guardrails
        audit = self.prefrontal.audit_execution(prompt)
        if not audit.is_safe:
            logger.warning("Bloqueio pre-frontal ativado por violacao de guardrail.")
            return {
                "allowed": False,
                "reason": "Bloqueado pelo Cortex Pre-Frontal",
                "violations": audit.violations,
                "warnings": audit.warnings,
            }

        # 2. Ativacao neural de contexto e restricoes
        neural_state = self.synaptic.activate(prompt)

        return {
            "allowed": True,
            "neural_context": neural_state.get("top_activated", []),
            "constraints": neural_state.get("inviolable_constraints", []),
            "warnings": audit.warnings,
        }
