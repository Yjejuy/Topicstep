---
name: jj-discuss-step-by-step
description: Maintain a persistent, dossier-backed discussion that first organizes a topic comprehensively and then reveals it naturally step by step. Use when the user explicitly invokes $jj-discuss-step-by-step or clearly asks to first整理/全面思考/检索并写下来, then discuss one point at a time. Do not trigger merely because a question is long.
---

# Step-by-step discussion

Use a temporary dossier as durable working memory while keeping the conversation cognitively light.

## Activation

Activate only when either condition is true:

- The user explicitly invokes `$jj-discuss-step-by-step`.
- The user clearly asks for a complete bounded analysis to be prepared first and then discussed gradually.

Do not activate for an ordinary long or difficult question. Each harness session may have at most one active topic.

1. Resolve the current harness session ID from its environment. For Codex, prefer `CODEX_SESSION_ID`, then `CODEX_THREAD_ID`.
2. Check the hook state or use `status --harness codex`. If already active, continue the existing discussion without creating or replacing its dossier. Otherwise create the state with:

   ```bash
   python3 "$HOME/.codex/skills/jj-discuss-step-by-step/scripts/discussion_state.py" start --harness codex --topic "<topic>" --goal "<goal>"
   ```

3. Read the available conversation and local context. Research externally only when the question needs current, niche, uncertain, or source-backed facts. Keep the research bounded to what is needed for the stated goal.
4. Replace the dossier skeleton in one complete, non-overlapping edit. Do not send multiple patch operations against the same initial dossier content. Write a concise but complete topic map containing:
   - scope and objective;
   - concepts and relationships;
   - full analysis and supporting evidence;
   - disagreements or competing interpretations;
   - uncertainties and open questions;
   - user corrections and confirmed decisions.
5. Record conclusions and evidence, not private chain-of-thought or a transcript of hidden reasoning.
6. In the first reply, briefly acknowledge that the dossier is ready, give one sentence orienting the discussion, then explain exactly one foundational or high-leverage point. Stop once that point is understandable. Keep the rest of the topic map in the dossier: do not preview every branch, compress the whole analysis into a mini-overview, or introduce an adjacent concept in this first reply. Include only the context, evidence, and qualifications needed to understand that one point accurately. If the user already asks a focused question, use that as the point rather than imposing a different starting topic.

For a broad opening question, completeness belongs in the dossier, not in the first chat reply. Gradual discussion takes precedence over covering every part of the opening request at once. A user explicitly requesting a full overview or the whole analysis overrides this pacing rule. Do not force a follow-up question.

The state root is:

```text
${XDG_STATE_HOME:-$HOME/.local/state}/jj-discuss-step-by-step/<harness>/<session_id>/
```

`active.md` contains only Topic, Goal, and Dossier. Its presence indicates active mode. Legacy files may contain extra fields; ignore them without migrating or rewriting the file on each turn.

The dossier is temporary external working memory. Do not copy it into Obsidian or project documentation unless the user explicitly requests that.

## Every active turn

Use the short state injected by the hook when it suffices; do not reread `active.md` redundantly. Read it only when state is missing or uncertain. Read relevant dossier sections only to recover context, verify something, or expand material not already available in context. Do not reread files mechanically every turn.

Keep the topic and goal stable. Infer the current focus from the conversation; do not maintain a persistent conversation cursor.

Begin every active response with exactly this shape:

```text
【逐步讨论中｜主题：<topic>｜当前：<focus>】
```

For a focused follow-up, answer the current question completely but compactly, revealing only necessary detail and at most one adjacent concept. For a broad question, select one useful point to discuss rather than compressing every branch into one answer, unless the user explicitly requests an overview. The stricter first-reply rule above still applies on activation. Do not force a question at the end of every turn.

Ordinary explanations, follow-ups, and expansion of existing material require no state or dossier writes. Update only the relevant dossier section when the user corrects important facts, changes the goal, or the discussion produces an important new conclusion worth retaining. Do not keep a per-turn discussion log or duplicate conclusions in `active.md`.

If the goal changes within the same topic, also update the short state:

```bash
python3 "$HOME/.codex/skills/jj-discuss-step-by-step/scripts/discussion_state.py" update --harness codex --goal "<revised goal>"
```

If the harness provides a reliable pre-compaction opportunity, optionally save one short resume hint in the dossier. Do not add routine writes to anticipate compaction. After context loss, recover from the dossier and available conversation; briefly clarify the last point if necessary. Preserving understanding matters more than preserving the exact discussion position.

## Topic changes and cancellation

- Repeated explicit or inferred activation while active is a no-op. It cannot replace, clear, or retitle the dossier. A new topic requires explicitly ending the current discussion before starting another; do not implement a silent clear-and-start transition.
- If a substantial tangent could be a new topic but the user did not explicitly switch, ask whether to switch and leave the current state unchanged.
- Requests to discuss or edit this Skill, and mode-control requests, are outside the stored topic. Answer normally without the unrelated topic label and do not record them in its dossier. Mentioning or invoking the Skill for these requests does not start a discussion dossier.
- If the user explicitly says to end or cancel the current discussion, run:

  ```bash
  python3 "$HOME/.codex/skills/jj-discuss-step-by-step/scripts/discussion_state.py" clear --harness codex
  ```

  Confirm cancellation without the active-discussion label.
- Closing, leaving, resuming, clearing, or compacting the harness session does not delete state.

## Harness adapters

- Codex: `adapters/codex-hooks.json`
- Claude Code template: `adapters/claude-settings.json`
- DeepSeek Harness Codex-compatible hooks: `adapters/deepseek-hooks.json`
- DeepSeek Harness plugin template: `adapters/deepseek-cordis.yml`

Claude Code and DeepSeek files are reference adapters. Do not install or modify those harnesses unless explicitly requested.
