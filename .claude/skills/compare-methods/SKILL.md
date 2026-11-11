---
name: compare-methods
description: Compare methodologies, datasets, metrics and findings across a project's analysed papers, consolidate the evidence matrix and identify contradictions. Use after paper analyses are complete, or when the user asks how studies differ or agree.
---

# Compare methodologies

`rlab` = `python3 scripts/rlab.py`. Rules: [docs/research-standards.md](../../../docs/research-standards.md) §1, §5, §6.

Input: project id. Use only analyses with `status: ready` or `complete`; `rlab index <id>` then read `literature-matrix.md` for the overview, and each `papers/*/analysis.md` for detail.

## 1. Evidence matrix
Merge every analysis's evidence table (section 13) into `evidence-matrix.md`, one row per claim, Source as `[@key, p. N]`. Keep the paper's label; downgrade strength for abstract-only and preprint sources.

## 2. Methodology comparison
Write `reports/methodology-comparison.md`:
1. **Overview table** — one row per paper: design, data/sample (N), setup, metrics, baselines, statistical testing, reproducibility (data/code available).
2. **Approach families** — group papers by method; for each group: typical strengths, weaknesses, and which papers [@key].
3. **Comparable results** — compare numbers only between papers sharing dataset, metric and setup; say explicitly when results are not comparable and why.
4. **Contradictions** — copy to `evidence-matrix.md` "Contradictions": claims, sources, differences in data/population/method/metric/time, possible explanation labelled [I].
5. **Methodological weaknesses across the field** — recurring problems (small N, no baselines, no significance tests, leakage risk, no code). These feed gap finding.
6. **What this means for our RQs** — per RQ, current answer with evidence strength; update "Current answer" in `RESEARCH-QUESTIONS.md`.

## 3. Check
`rlab cite-check <id> research/<id>/evidence-matrix.md research/<id>/reports/methodology-comparison.md` passes.

Done when: every ready/complete paper appears in the overview table, every RQ has a current answer with strength, cite-check passes. Tick Synthesis in `STATUS.md`.
