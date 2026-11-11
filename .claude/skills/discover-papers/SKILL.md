---
name: discover-papers
description: Search academic sources, screen candidates and add relevant papers to a research project. Use when a project needs (more) literature, when the user asks to find papers, or for snowballing from key papers.
---

# Discover papers

`rlab` = `python3 scripts/rlab.py`. Rules: [docs/research-standards.md](../../../docs/research-standards.md) §3 (source tiers) and §8 (access).

## 1. Plan queries
Read the project's `RESEARCH.md` (scope, criteria, search strategy) and `RESEARCH-QUESTIONS.md`. Write 3–6 facet queries: core concept + each RQ's angle, with field synonyms. Add `--from <year>` per the scope. Add `pubmed` to `--sources` for biomedical/health topics.

## 2. Search (fan out)
Dispatch one `paper-scout` agent per facet (in parallel, one message). Give each: project id, its facet query/queries, inclusion/exclusion criteria, year window, and the number of papers wanted. Scouts search, screen and **return** recommendations; they never run `rlab add`.

Without subagents: run `rlab search <id> "<query>" [--sources ...] [--from Y] [--limit N]` yourself and screen as in step 3.

## 3. Screen
For each candidate decide include / exclude on title + abstract (read the abstract from the saved JSON in `search/`). Prefer published peer-reviewed work; prefer a published version over its preprint; exclude RETRACTED; treat citation counts as a weak signal (recent papers have few). Keep a balance: seminal papers, recent work (last 2–3 years), and at least one review/survey if one exists.

Record every included paper and every notable exclusion in `search/screening.md` (results file, idx, short title, decision, reason).

## 4. Snowball
For the 3–5 most central included papers, look at references and citing works via OpenAlex (WebFetch):
- cited by: `https://api.openalex.org/works?filter=cites:<openalex_id>&sort=cited_by_count:desc&per-page=25`
- references: `referenced_works` in `https://api.openalex.org/works/<openalex_id>`
Use WebSearch for very recent work (current and previous year). Screen these the same way.

## 5. Add
One call for all included ids (DOIs preferred; else arXiv id, OpenAlex W-id, `pmid:N`):
`rlab add <id> <ids...> --reason "<why included>" --query "<query that found it>"`
Use one call per distinct reason. Then handle output:
- `DUPLICATE` → fine, already present.
- `WARNING: RETRACTED` → remove from consideration and tell the user why.
- `WARNING: metadata MISMATCH` or `single-source` → run `rlab validate <id> <key>` and inspect `metadata.json`; if the record is wrong, tell the user.
- `FAIL` → identifier wrong or not indexed; find the correct DOI from the publisher page, never guess.

Finally `rlab dedup <id>` must report 0 pairs (resolve any pair by keeping the published version; ask the user before removing a folder).

Done when: the target number of papers is reached or new searches return mostly IN-PROJECT/irrelevant hits (saturation), every included paper is in `screening.md`, and dedup is clean. Tick Discovery and Screening in `STATUS.md`.
