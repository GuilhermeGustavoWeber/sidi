#!/usr/bin/env python3
"""
SIDI CLI - Interface de Linha de Comando Operacional do Copiloto Cognitivo.
"""
import argparse
import sys
from pathlib import Path

from engine.config import settings
from engine.cognitive_router import CognitiveRouter
from engine.memory_manager import MemoryManager
from engine.prefrontal_cortex import PrefrontalCortex
from engine.session_state import HandoffManager, SessionState
from engine.sync_engine import GitSyncEngine
from engine.synaptic_engine import SynapticEngine


def cmd_status(sync: GitSyncEngine, handoff: HandoffManager) -> None:
    stat = sync.get_status()
    active = handoff.load_handoff()
    print("=" * 48)
    print("  SIDI :: STATUS OPERACIONAL DO CEREBRO")
    print("=" * 48)
    print("Operador:           Guilherme Gustavo Weber")
    print(f"Diretorio Base:     {settings.project_root}")
    print(f"Git Branch / SHA:   {stat['branch']} ({stat['commit']})")
    print(f"Estado de Trabalho: {'MODIFICADA (' + str(stat['changed_files_count']) + ' arquivos)' if stat['is_dirty'] else 'LIMPA'}")
    if active:
        print(f"Sessao Ativa:       {active.session_id}")
        print(f"Meta Atual:         {active.current_goal or 'N/D'}")
        print(f"Proxima Acao:       {active.next_action or 'N/D'}")
    else:
        print("Sessao Ativa:       Nenhuma sessao registrada no momento.")
    print("=" * 48)


def cmd_think(query: str) -> None:
    router = CognitiveRouter()
    res = router.process(query)
    print("=" * 48)
    print("  SIDI :: PROCESSAMENTO COGNITIVO")
    print("=" * 48)
    print(f"Consulta: {query}")
    if not res.get("allowed"):
        print("\n[BLOQUEIO PRE-FRONTAL]")
        for v in res.get("violations", []):
            print(f"  X {v}")
        return

    print("\nNeuronios e Lobos Ativados:")
    for n in res.get("neural_context", [])[:6]:
        print(f"  - [{n['node']}] (Energia: {n['energy']} | Lobo: {n['lobe']})")

    if res.get("constraints"):
        print("\nRestricoes e Guardrails Relevantes:")
        for c in res.get("constraints"):
            print(f"  ! {c}")

    if res.get("warnings"):
        print("\nAlertas de Engenharia:")
        for w in res.get("warnings"):
            print(f"  * {w}")
    print("=" * 48)


def cmd_checkpoint(message: str, sync: GitSyncEngine) -> None:
    res = sync.checkpoint("state(checkpoint)", message)
    if res.get("committed"):
        print(f"[OK] Checkpoint registrado: {res.get('sha')} - {res.get('message')}")
        print(f"[OK] Git Push: {'Sincronizado com sucesso' if res.get('pushed') else 'Falha: ' + str(res.get('push_error'))}")
    else:
        print(f"[INFO] {res.get('message')}")


def cmd_bootstrap(handoff: HandoffManager, goal: str, project: str) -> None:
    state = SessionState(
        current_project=project or "geral",
        current_goal=goal or "Definicao inicial de arquitetura",
        next_action="Execucao dos modulos centrais",
    )
    handoff.save_session(state)
    mem = MemoryManager()
    mem.record_episodic(
        title=f"boot_{state.session_id[:8]}",
        content=f"Sessao iniciada com a meta: {state.current_goal}. Projeto alvo: {state.current_project}.",
        projects=[state.current_project],
    )
    print(f"[OK] Sessao SIDI inicializada com sucesso: {state.session_id}")
    print(f"Projeto: {state.current_project} | Meta: {state.current_goal}")


def main() -> None:
    parser = argparse.ArgumentParser(description="SIDI - Copiloto Cognitivo Pessoal")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("status", help="Exibe o status do cerebro, memoria e Git")

    think_p = sub.add_parser("think", help="Ativa a rede neural e audita com o pre-frontal")
    think_p.add_argument("query", help="Instrucao ou consulta a avaliar")

    ckpt_p = sub.add_parser("checkpoint", help="Registra commit semantico e sincroniza via push")
    ckpt_p.add_argument("message", help="Mensagem descritiva do checkpoint")

    boot_p = sub.add_parser("boot", help="Inicializa uma nova sessao de trabalho")
    boot_p.add_argument("--goal", default="Desenvolvimento de projetos proprios", help="Meta da sessao")
    boot_p.add_argument("--project", default="core", help="Nome do projeto em foco")

    args = parser.parse_args()
    sync = GitSyncEngine()
    handoff = HandoffManager()

    if args.command == "status" or not args.command:
        cmd_status(sync, handoff)
    elif args.command == "think":
        cmd_think(args.query)
    elif args.command == "checkpoint":
        cmd_checkpoint(args.message, sync)
    elif args.command == "boot":
        cmd_bootstrap(handoff, args.goal, args.project)


if __name__ == "__main__":
    main()
