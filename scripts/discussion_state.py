#!/usr/bin/env python3
"""Persistent session state and hook adapter for step-by-step discussions."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any


STATE_NAME = "jj-discuss-step-by-step"
MAX_ACTIVE_BYTES = 12_000
MAX_CONTEXT_CHARS = 4_800
COMPONENT_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,199}$")
FIELD_NAMES = {
    "Topic": "topic",
    "Goal": "goal",
    "Dossier": "dossier",
}


@dataclass
class ActiveState:
    topic: str
    goal: str
    dossier: str


def state_root() -> Path:
    base = os.environ.get("XDG_STATE_HOME")
    if base:
        return Path(base).expanduser().resolve() / STATE_NAME
    return (Path.home() / ".local" / "state" / STATE_NAME).resolve()


def validate_component(value: str, label: str) -> str:
    if not COMPONENT_RE.fullmatch(value) or value in {".", ".."}:
        raise ValueError(f"invalid {label}: {value!r}")
    return value


def clean_line(value: str, label: str) -> str:
    cleaned = " ".join(value.split())
    if not cleaned:
        raise ValueError(f"{label} must not be empty")
    if len(cleaned) > 1_000:
        raise ValueError(f"{label} is too long")
    return cleaned


def resolve_session_id(explicit: str | None = None) -> str:
    candidates = (
        explicit,
        os.environ.get("CODEX_SESSION_ID"),
        os.environ.get("CODEX_THREAD_ID"),
        os.environ.get("CLAUDE_SESSION_ID"),
        os.environ.get("DSH_SESSION_ID"),
    )
    for candidate in candidates:
        if candidate:
            return validate_component(candidate, "session_id")
    raise ValueError("session_id is required; pass --session-id or set the harness session environment")


def session_dir(harness: str, session_id: str) -> Path:
    safe_harness = validate_component(harness, "harness")
    safe_session = validate_component(session_id, "session_id")
    root = state_root()
    harness_dir = root / safe_harness
    result = harness_dir / safe_session
    if harness_dir.is_symlink() or result.is_symlink():
        raise ValueError("refusing a symlinked harness or session directory")
    harness_dir = harness_dir.resolve()
    result = result.resolve()
    if result.parent != harness_dir:
        raise ValueError("session path escaped state root")
    return result


def atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(content)
        os.replace(temporary_name, path)
    finally:
        if os.path.exists(temporary_name):
            os.unlink(temporary_name)


def render_active(state: ActiveState) -> str:
    return (
        "# Active step-by-step discussion\n\n"
        f"- Topic: {state.topic}\n"
        f"- Goal: {state.goal}\n"
        f"- Dossier: {state.dossier}\n"
    )


def parse_active(path: Path) -> ActiveState:
    if path.stat().st_size > MAX_ACTIVE_BYTES:
        raise ValueError("active.md exceeds the size limit")
    values: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("- ") or ": " not in line:
            continue
        label, value = line[2:].split(": ", 1)
        field = FIELD_NAMES.get(label)
        if field:
            values[field] = value
    missing = [field for field in FIELD_NAMES.values() if field not in values]
    if missing:
        raise ValueError(f"active.md is missing fields: {', '.join(missing)}")
    state = ActiveState(**values)
    expected_dossier = path.with_name("dossier.md").resolve()
    if Path(state.dossier).expanduser().resolve() != expected_dossier:
        raise ValueError("active.md dossier path does not match its session directory")
    if not expected_dossier.is_file():
        raise ValueError("dossier.md is missing")
    return state


def dossier_skeleton(topic: str, goal: str) -> str:
    return (
        f"# {topic}\n\n"
        "## Scope and objective\n\n"
        f"{goal}\n\n"
        "## Stable orientation\n\n"
        "Replace this initialization note with the durable one-paragraph orientation before the first reply.\n\n"
        "## Concept map\n\n"
        "## Full analysis\n\n"
        "## Evidence and sources\n\n"
        "## Uncertainties and competing views\n\n"
        "## User corrections and confirmed decisions\n"
    )


def start_state(
    harness: str,
    session_id: str,
    topic: str,
    goal: str,
) -> dict[str, str]:
    topic = clean_line(topic, "topic")
    goal = clean_line(goal, "goal")
    directory = session_dir(harness, session_id)
    active_path = directory / "active.md"
    dossier_path = directory / "dossier.md"
    if directory.exists():
        parse_active(active_path)
        return {"active": str(active_path.resolve()), "dossier": str(dossier_path.resolve())}
    directory.mkdir(parents=True)
    state = ActiveState(
        topic=clean_line(topic, "topic"),
        goal=clean_line(goal, "goal"),
        dossier=str(dossier_path.resolve()),
    )
    atomic_write(dossier_path, dossier_skeleton(state.topic, state.goal))
    atomic_write(active_path, render_active(state))
    return {"active": str(active_path.resolve()), "dossier": str(dossier_path.resolve())}


def update_state(
    harness: str,
    session_id: str,
    goal: str,
) -> ActiveState:
    active_path = session_dir(harness, session_id) / "active.md"
    state = parse_active(active_path)
    new_goal = clean_line(goal, "goal")
    if state.goal == new_goal:
        return state
    state.goal = new_goal
    atomic_write(active_path, render_active(state))
    return state


def clear_state(harness: str, session_id: str) -> bool:
    directory = session_dir(harness, session_id)
    if not directory.exists():
        return False
    if directory.is_symlink():
        raise ValueError("refusing to clear a symlinked session directory")
    shutil.rmtree(directory)
    harness_dir = directory.parent
    if harness_dir.exists() and not any(harness_dir.iterdir()):
        harness_dir.rmdir()
    return True


def hook_context(state: ActiveState) -> str:
    context = (
        "A jj-discuss-step-by-step discussion is active.\n"
        f"Topic: {state.topic}\n"
        f"Goal: {state.goal}\n"
        f"Dossier: {state.dossier}\n"
        "This is the short state; do not reread active.md when this context suffices. "
        "Read relevant dossier sections only when needed for recall, verification, or new material. "
        "Start the response with 【逐步讨论中｜主题：<topic>｜当前：<focus>】, answer the current question "
        "without dumping the dossier. On the first reply, acknowledge readiness, give one orienting sentence, "
        "then explain exactly one point and stop; no branch previews or adjacent concept. Broad questions "
        "do not require a complete overview unless explicitly requested. Focused follow-ups may include "
        "at most one adjacent concept. Infer focus from the conversation; "
        "do not persist a per-turn cursor or log. Ordinary follow-ups require no writes. "
        "Update the dossier only for durable corrections, changed goals, or important new conclusions. "
        "Repeated skill invocation does not replace the active topic. Skill-design or control requests are "
        "outside the topic: answer normally without the topic label or updating its dossier. "
        "If the user explicitly ends or cancels this discussion, clear only this session state and omit the label."
    )
    return context[:MAX_CONTEXT_CHARS]


def diagnostic_output(event_name: str, message: str) -> dict[str, Any]:
    result: dict[str, Any] = {
        "continue": True,
        "systemMessage": f"jj-discuss-step-by-step state was ignored: {message}",
    }
    if event_name in {"UserPromptSubmit", "SessionStart"}:
        result["hookSpecificOutput"] = {"hookEventName": event_name}
    return result


def handle_hook(payload: dict[str, Any], harness: str) -> dict[str, Any] | None:
    event_name = str(payload.get("hook_event_name", ""))
    if event_name not in {"UserPromptSubmit", "SessionStart"}:
        return None
    raw_session_id = payload.get("session_id")
    if not isinstance(raw_session_id, str) or not raw_session_id:
        return diagnostic_output(event_name, "hook input has no valid session_id")
    try:
        active_path = session_dir(harness, raw_session_id) / "active.md"
    except ValueError as exc:
        return diagnostic_output(event_name, str(exc))
    if not active_path.exists():
        return None
    try:
        state = parse_active(active_path)
    except (OSError, UnicodeError, ValueError) as exc:
        return diagnostic_output(event_name, str(exc))
    return {
        "hookSpecificOutput": {
            "hookEventName": event_name,
            "additionalContext": hook_context(state),
        }
    }


def print_json(value: Any) -> None:
    print(json.dumps(value, ensure_ascii=False, sort_keys=True))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    hook = subparsers.add_parser("hook", help="handle a harness hook event from stdin")
    hook.add_argument("--harness", required=True)

    start = subparsers.add_parser("start", help="create state for the current session")
    start.add_argument("--harness", required=True)
    start.add_argument("--session-id")
    start.add_argument("--topic", required=True)
    start.add_argument("--goal", required=True)

    update = subparsers.add_parser("update", help="minimally update active session state")
    update.add_argument("--harness", required=True)
    update.add_argument("--session-id")
    update.add_argument("--goal", required=True)

    status = subparsers.add_parser("status", help="show current session state")
    status.add_argument("--harness", required=True)
    status.add_argument("--session-id")

    clear = subparsers.add_parser("clear", help="delete only the current session state")
    clear.add_argument("--harness", required=True)
    clear.add_argument("--session-id")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    if args.command == "hook":
        try:
            payload = json.load(sys.stdin)
            if not isinstance(payload, dict):
                raise ValueError("hook input must be a JSON object")
            result = handle_hook(payload, args.harness)
        except (json.JSONDecodeError, OSError, ValueError) as exc:
            result = diagnostic_output("Unknown", str(exc))
        if result is not None:
            print_json(result)
        return 0

    session_id = resolve_session_id(args.session_id)
    if args.command == "start":
        print_json(start_state(args.harness, session_id, args.topic, args.goal))
    elif args.command == "update":
        state = update_state(
            args.harness,
            session_id,
            args.goal,
        )
        print_json({"goal": state.goal, "active": True})
    elif args.command == "status":
        active_path = session_dir(args.harness, session_id) / "active.md"
        if not active_path.exists():
            print_json({"active": False})
        else:
            state = parse_active(active_path)
            print_json({"active": True, "topic": state.topic, "goal": state.goal, "dossier": state.dossier})
    elif args.command == "clear":
        print_json({"cleared": clear_state(args.harness, session_id)})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
