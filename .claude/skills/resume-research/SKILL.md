---
name: resume-research
description: Resume or continue an existing research project from its saved state. Use when the user says "resume", "continue", "where were we", names an earlier project, or asks which research projects exist.
---

# Resume research

`rlab` = `python3 scripts/rlab.py`.

## 1. Find the project
`rlab list`. If the user named a project, match it (`rlab status <part-of-id>` accepts any unique fragment). If several match or none was named and more than one is active, ask which one (show id + topic + phase).

## 2. Load state
- `rlab status <id>` — phase, stats, next actions, blocked items, papers needing work, last log entries.
- Read `STATUS.md`, `RESEARCH-QUESTIONS.md`, the last ~20 lines of `research-log.md`.
- Check what changed while away: PDFs the user dropped in for papers with fulltext `unavailable` (look in the project folder and ask if they mentioned files) → `rlab attach`; then re-analyse those papers from abstract-only to full-text (new revision section if the analysis was complete — ask first).

Done when: you can state the current phase, the next 1–3 actions and any blocker.

## 3. Brief the user
≤6 lines: topic, phase, what is done, what is next, what you need from them (if anything).

## 4. Continue
Proceed with the first next action using the matching skill (`discover-papers`, `analyze-paper`, `compare-methods`, `find-gaps`, `write-literature-review`, `research-report`), following the phase order in `start-research`. Log `rlab log <id> resume "<what was resumed>"`.
