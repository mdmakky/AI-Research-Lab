---
name: find-gaps
description: Identify evidence-backed, novelty-checked research gaps and propose contributions and experiments. Use after methodology comparison, or when the user asks what is missing in the literature or what they could research.
---

# Find research gaps

`rlab` = `python3 scripts/rlab.py`. Rules: [docs/research-standards.md](../../../docs/research-standards.md) §7 (gap and novelty rules) is binding.

Delegate to the `gap-analyst` agent with the project id (it follows these steps); review its report before showing the user.

## 1. Collect candidate gaps
Sources, all in the project: future-work sections (analysis §11), recurring limitations (§8–9), validity threats (§10), contradictions in `evidence-matrix.md`, field-wide weaknesses in `reports/methodology-comparison.md`, RQs with weak or no answer in `RESEARCH-QUESTIONS.md`. Classify each: evidence, methodological, population/context, theoretical, practical, contradiction.

## 2. Evidence test
Keep a candidate only if at least one analysed paper supports it with `[@key, p. N]`; a gap stated by ≥2 independent papers is stronger.

## 3. Novelty check (per surviving candidate)
- ≥3 targeted `rlab search` queries across ≥2 sources, including the last 2 years (`--from`).
- One WebSearch for very recent preprints/work.
- Read titles/abstracts of the closest hits. If a hit fills the gap, drop or narrow the gap. If it is highly relevant, recommend adding it to the project.
Record date, queries and closest hits in the gap entry.

## 4. Contributions and experiments
For each gap: potential contribution, a concrete study design (data, sample, method, baseline, metrics, analysis, expected validity threats), and beginner feasibility (easy/moderate/hard and why).

## 5. Write and check
Fill `gap-report.md` using its template, ranked by evidence strength × feasibility. `rlab cite-check <id> research/<id>/gap-report.md` passes.

Done when: every listed gap has evidence, a recorded novelty check and a confidence rating. Tick Gaps in `STATUS.md`. Tell the user the top 3 gaps in plain language.
