---
name: research-report
description: Generate a plain-language research report summarising a project's findings, evidence strength, gaps and next steps for a beginner researcher. Use at the end of a research run, or when the user asks for a summary, report or "what did we find".
---

# Research report

`rlab` = `python3 scripts/rlab.py`. Rules: [docs/research-standards.md](../../../docs/research-standards.md). The `academic-writer` agent may draft it; you check it.

Write `reports/research-report-YYYY-MM-DD.md` (new file each time; earlier reports stay):

1. **Summary in plain language** — 5–8 sentences a newcomer understands.
2. **What we did** — sources, searches, papers found/included, full-text vs abstract-only counts (from `rlab status <id>`).
3. **Answers to the research questions** — per RQ: answer, evidence strength (strong/moderate/weak), key sources `[@key, p. N]`, and what would change the answer.
4. **Key papers to read first** — 3–5 papers with one line each on why.
5. **Where studies disagree** — contradictions and likely reasons.
6. **Research gaps and possible contributions** — top gaps from `gap-report.md` with confidence, suggested study and beginner feasibility.
7. **Limitations of this review** — coverage, missing full texts, preprints, search date.
8. **Recommended next steps** — concrete actions for the user (papers to obtain, decisions to make, a first experiment).
9. **Glossary** — research terms used, one plain sentence each.

Check: `rlab cite-check <id> <report file>` passes. Update `STATUS.md` Next actions and `rlab log <id> writing "report generated: <file>"`.

Done when: all 9 sections exist, cite-check passes, and the user received a ≤10-line summary with the file path.
