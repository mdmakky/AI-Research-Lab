---
name: start-research
description: Start a new research project from a topic and run the full literature workflow end to end. Use when the user says "start a new research on X", "research X for me", or gives a new research topic.
---

# Start research

Run from the workspace root. `rlab` means `python3 scripts/rlab.py`. Rules: [docs/research-standards.md](../../../docs/research-standards.md). You are the orchestrator: follow [.claude/agents/research-orchestrator.md](../../agents/research-orchestrator.md) for delegation and state ownership.

After every phase: tick it in `STATUS.md`, rewrite "Next actions", `rlab log <id> <phase> "<what happened>"`, and give the user a 1–3 line progress update in plain language.

## 1. Scope
Judge whether the topic is researchable as stated. It is **too broad or ambiguous** when it spans several fields, has no clear population/context/outcome, or would plausibly return hundreds of relevant papers.
- Too broad/ambiguous: ask up to 3 multiple-choice questions (AskUserQuestion), each option explained in one plain sentence, with your recommended option first.
- Otherwise: choose sensible defaults (last ~10 years, peer-reviewed first, ≤20 included papers) and record them as assumptions.

Done when: scope, time window and target size are fixed.

## 2. Create the project
`rlab new "<topic>"` → note the project id it prints.

## 3. Objectives and research questions
1. Pilot search to learn the field's vocabulary: `rlab search <id> "<topic keywords>" --limit 10`.
2. Fill `RESEARCH.md`: plain-language topic, scope, 2–4 objectives, inclusion/exclusion criteria, 3–6 facet queries in the search strategy, assumptions under "Key decisions".
3. Fill `RESEARCH-QUESTIONS.md`: 3–5 questions, each answerable from literature, linked to an objective.
4. Show the user the objectives and questions (≤10 lines) and invite corrections. Continue unless they object.

Done when: both files have no empty required fields and Scoping is ticked.

## 4. Discover and screen
Follow the `discover-papers` skill.

## 5. Acquire full texts
`rlab fetch <id>`. For each `NONE` result, list the paper in STATUS "Blocked / needs user" and tell the user once, in one message: which papers lack open access, and that they can download them via their library and run `rlab attach <id> <key> <file.pdf>` (or give you the files). Continue: those papers are analysed abstract-only until a PDF arrives.

Done when: every paper has fulltext status `downloaded`, `user-supplied` or `unavailable`.

## 6. Analyse
Follow the `analyze-paper` skill for every paper, delegated to `paper-analyst` agents in parallel (3–4 papers per agent).

Done when: every paper's analysis is `ready`.

## 7. Critical review
Delegate to the `critical-reviewer` agent. Send each analysis with problems back to a `paper-analyst` with the review findings; repeat until clean. Then set each passed analysis to `status: complete`.

## 8. Synthesis, gaps, report
Follow `compare-methods`, then `find-gaps`, then `research-report`, in that order.

## 9. Close the run
`rlab bib <id>`, `rlab index <id>`, `rlab validate <id>`. Final message to the user: what was found (3–5 bullets), strongest gaps, what is blocked on them, the report path, and how to resume ("Resume research <id>").
