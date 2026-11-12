---
name: reading-guide-doc-preference
description: User wants every research project to end with a plain-English reading guide published as a public (anyone-with-link view) Google Doc
metadata:
  node_type: memory
  type: feedback
  originSessionId: 81569eae-88cd-4742-96e0-e233fc4afe44
  modified: 2026-11-11T23:12:24.877Z
---

At the end of each research project, produce a Reading Guide (overview, detailed 1–2 page plain-English brief per paper, gaps + opportunities, glossary) and publish it as a styled Google Doc shared "anyone with link: view" (`reading-guide` skill + `scripts/md2gdoc.py`).

**Why:** the user is a beginner who does not read the full papers; the technical analysis.md files and reports are too dense and scattered. They want one nicely presented doc per topic they can keep and share (2026-11-12).

**How to apply:** run the `reading-guide` skill after `research-report` without asking; doc language English (simple), user chats in romanized Bangla. Use `--share none` only if they ask for private.
