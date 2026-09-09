from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


SCRIPT = Path(__file__).parents[1] / "scripts" / "discussion_state.py"
sys.path.insert(0, str(SCRIPT.parent))

import discussion_state as state  # noqa: E402


class DiscussionStateTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.environment = patch.dict(os.environ, {"XDG_STATE_HOME": self.temporary.name}, clear=False)
        self.environment.start()

    def tearDown(self) -> None:
        self.environment.stop()
        self.temporary.cleanup()

    def payload(self, session_id: str, event: str = "UserPromptSubmit") -> dict[str, str]:
        return {"session_id": session_id, "hook_event_name": event}

    def test_no_state_hook_is_silent(self) -> None:
        self.assertIsNone(state.handle_hook(self.payload("session-a"), "codex"))

    def test_create_and_restore_short_context(self) -> None:
        paths = state.start_state("codex", "session-a", "Model choice", "Choose by tradeoffs")
        output = state.handle_hook(self.payload("session-a"), "codex")
        self.assertTrue(Path(paths["active"]).is_file())
        self.assertTrue(Path(paths["dossier"]).is_file())
        context = output["hookSpecificOutput"]["additionalContext"]
        self.assertIn("Topic: Model choice", context)
        self.assertIn("Goal: Choose by tradeoffs", context)
        self.assertNotIn("Current focus:", context)
        self.assertLessEqual(len(context), state.MAX_CONTEXT_CHARS)
        self.assertNotIn("## Full analysis", context)

    def test_session_start_variants_restore_state(self) -> None:
        state.start_state("codex", "session-a", "Topic", "Goal")
        for source in ("startup", "resume", "clear", "compact"):
            payload = self.payload("session-a", "SessionStart")
            payload["source"] = source
            output = state.handle_hook(payload, "codex")
            self.assertEqual(output["hookSpecificOutput"]["hookEventName"], "SessionStart")

    def test_update_goal_preserves_dossier(self) -> None:
        paths = state.start_state("codex", "session-a", "Topic", "Goal")
        dossier = Path(paths["dossier"])
        before = dossier.read_bytes()
        updated = state.update_state("codex", "session-a", "New goal")
        self.assertEqual(updated.goal, "New goal")
        parsed = state.parse_active(state.session_dir("codex", "session-a") / "active.md")
        self.assertEqual(parsed.topic, "Topic")
        self.assertEqual(parsed.goal, "New goal")
        self.assertEqual(dossier.read_bytes(), before)
        with patch.object(state, "atomic_write") as write:
            state.update_state("codex", "session-a", "New goal")
        write.assert_not_called()

    def test_sessions_and_harnesses_are_isolated(self) -> None:
        state.start_state("codex", "session-a", "A", "Goal A")
        state.start_state("codex", "session-b", "B", "Goal B")
        state.start_state("claude-code", "session-a", "C", "Goal C")
        self.assertIn("Topic: A", state.handle_hook(self.payload("session-a"), "codex")["hookSpecificOutput"]["additionalContext"])
        self.assertIn("Topic: B", state.handle_hook(self.payload("session-b"), "codex")["hookSpecificOutput"]["additionalContext"])
        self.assertIn("Topic: C", state.handle_hook(self.payload("session-a"), "claude-code")["hookSpecificOutput"]["additionalContext"])

    def test_existing_topic_is_not_overwritten(self) -> None:
        paths = state.start_state("codex", "session-a", "A", "Goal")
        original = {key: Path(path).read_bytes() for key, path in paths.items()}
        with patch.object(state, "atomic_write") as write:
            repeated = state.start_state("codex", "session-a", "B", "Different goal")
        write.assert_not_called()
        self.assertEqual(repeated, paths)
        self.assertEqual(original, {key: Path(path).read_bytes() for key, path in paths.items()})

    def test_clear_removes_only_exact_session(self) -> None:
        state.start_state("codex", "session-a", "A", "Goal A")
        state.start_state("codex", "session-b", "B", "Goal B")
        self.assertTrue(state.clear_state("codex", "session-a"))
        self.assertIsNone(state.handle_hook(self.payload("session-a"), "codex"))
        self.assertIsNotNone(state.handle_hook(self.payload("session-b"), "codex"))

    def test_corrupt_state_fails_open_with_diagnostic(self) -> None:
        directory = state.session_dir("codex", "session-a")
        directory.mkdir(parents=True)
        (directory / "active.md").write_text("broken", encoding="utf-8")
        (directory / "dossier.md").write_text("# Dossier\n", encoding="utf-8")
        output = state.handle_hook(self.payload("session-a"), "codex")
        self.assertTrue(output["continue"])
        self.assertIn("was ignored", output["systemMessage"])

    def test_path_traversal_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            state.session_dir("codex", "../outside")

    def test_symlink_cannot_redirect_clear(self) -> None:
        paths = state.start_state("codex", "session-b", "B", "Goal")
        target = Path(paths["active"]).parent
        (target.parent / "session-a").symlink_to(target, target_is_directory=True)
        with self.assertRaises(ValueError):
            state.clear_state("codex", "session-a")
        self.assertTrue(Path(paths["active"]).exists())
        (state.state_root() / "other").symlink_to(target.parent, target_is_directory=True)
        with self.assertRaises(ValueError):
            state.clear_state("other", "session-b")
        self.assertTrue(Path(paths["active"]).exists())

    def test_invalid_start_does_not_leave_partial_state(self) -> None:
        with self.assertRaises(ValueError):
            state.start_state("codex", "session-a", " ", "Goal")
        self.assertFalse(state.session_dir("codex", "session-a").exists())

    def test_hook_cli_emits_zero_bytes_without_state(self) -> None:
        environment = os.environ.copy()
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "hook", "--harness", "codex"],
            input=json.dumps(self.payload("session-a")),
            text=True,
            capture_output=True,
            check=True,
            env=environment,
        )
        self.assertEqual(result.stdout, "")
        self.assertEqual(result.stderr, "")


if __name__ == "__main__":
    unittest.main()
