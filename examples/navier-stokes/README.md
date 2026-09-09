# A curious student explores a complex claim

Three independent tutor/student conversations, using GPT-5.6 Luna with xhigh reasoning. The student has first-year university mathematics knowledge and is particularly curious about details. Its goals are to understand the proof's reliability and the dispute involving other researchers.

Every tutor receives the same opening:

> I've heard that OpenAI found a solution to the Navier–Stokes equations and that there's some controversy about it. Tell me about that.

No background syllabus, source URLs, evidence pack or coordinator-written follow-up questions were supplied. Tutors researched independently. The students could ask natural continuations and chose when to stop; there was no turn limit.

## Read the full exchanges

| Condition | Tutor replies | First reply words | Median reply words | Total reply words |
| --- | ---: | ---: | ---: | ---: |
| [Default](default.md) | 14 | 542 | 643.5 | 8,966 |
| [Simple step-by-step prompt](simple-prompt.md) | 12 | 197 | 348 | 4,215 |
| [TopicStep](topicstep.md) | 20 | 105 | 315 | 5,927 |

[Read TopicStep's dossier](dossier.md), the external material behind the conversation. The three conversation exports are unabridged; they include each student's final explanation and remaining uncertainties.

Counts are word-like sequences, excluding status labels and link destinations but including mathematical/code identifiers. They exclude student replies, tools and dossier content; they are not API token or cost counts.

## What this example can and cannot show

TopicStep presents smaller portions than default in this sample. Its median reply is only modestly shorter than the simple prompt, and it produces more total text than that prompt. More turns or fewer words alone do not establish a better discussion.

There was one actual compaction in the TopicStep tutor during Turn 19; the other five participants had none. Its conversation continued through Turn 20. This does not isolate a dossier benefit: native compaction summaries and other retained context may explain continuity. Installed hooks were not used.

This is one simulation per condition, not a human study or a factual audit. Some late questions become more technical than a typical first-year student might independently ask. Sources differ because tutors researched independently. Claims and allegations in the transcripts remain attributed source claims, not verified conclusions of this example.

## Provenance and integrity

Experiment date: September 9, 2026. The [exact prompts](prompts.md) and [skill snapshot](skill-snapshot.md) accompany this exploratory run. The skill was not edited during the experiment; its source had uncommitted changes, so the included snapshot records the version used.

All 46 tutor replies and subsequent student handoffs were checked against original final messages. Five transport-only reissues corrected reply keys across four TopicStep answers; every body was unchanged. An unfinished simple-prompt answer was resumed after a user interruption, without resampling completed turns. Runtime and overhead comparisons are therefore inappropriate.

The agent wrote its dossier under an unintended relative directory. After completion, it was relocated for packaging without changing its content. Session IDs, private paths, transport keys and raw internal logs are not included in this export.
