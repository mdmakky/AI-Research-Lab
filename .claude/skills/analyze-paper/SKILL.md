---
name: analyze-paper
description: Analyse one research paper in depth (objective, method, data, setup, metrics, findings, limitations, validity threats, future work, relevance) with page-cited evidence. Use when a project paper needs its analysis.md written or completed.
---

# Analyse a paper

`rlab` = `python3 scripts/rlab.py`. Rules: [docs/research-standards.md](../../../docs/research-standards.md) — labels §1, never invent §2, reading depth §4, appraisal checklist §5.

Input: project id + paper key. Files live in `research/<id>/papers/<key>/`.

## 1. Prepare
- `rlab scaffold <id> <key>` (creates `analysis.md`; never overwrites an existing one).
- Read `metadata.json`. Note `venue_kind`, `is_retracted`, `fulltext.status`, `fulltext.identity`, `fulltext.text_layer`.
- `identity` UNCONFIRMED → read PDF page 1 and confirm it is this paper; if not, stop and report.
- `text_layer` POOR → read pages from `paper.pdf` with the Read tool (`pages` parameter) instead of `fulltext.txt`.
- No full text → `evidence_basis: abstract-only`; fill objective and headline claims as [A] from the abstract in `metadata.json`, write "full text not available" in sections 3–6, 8 and 10, and stop at step 4.

## 2. Read the whole paper
Read `fulltext.txt` in chunks (Read with offset/limit) from start to end: abstract, introduction, method, results, tables, discussion, limitations, conclusion. Use Grep for `limitation|threat|future work|we did not|sample|dataset|N =` to make sure nothing is missed. For tables or figures garbled by text extraction, read that PDF page directly. Page numbers come from the nearest preceding `=== [PDF page N] ===` marker.

## 3. Write the analysis
Fill every section of `analysis.md`. Each [V]/[A] item ends with `(p. N)`. Use "not reported" when the paper is silent — that absence is itself useful information (e.g. no sample size reported). Separate author-stated limitations (section 8, [A]) from limitations you identify (section 9, [I]). Apply the appraisal checklist to section 10. Fill the evidence table (section 13) with rows linked to project RQ ids from `RESEARCH-QUESTIONS.md`.

## 4. Frontmatter
Fill the single-line frontmatter fields: `design`, `dataset`, `sample_size`, `metrics`, `main_finding` (≤25 words), `relevance` (high/medium/low). These feed the literature matrix.

## 5. Self-check
- Every [V]/[A] has a page ref; `rlab cite-check <id> research/<id>/papers/<key>/analysis.md` passes.
- Grep `fulltext.txt` for 3 of your quotes/numbers: each is found on the cited page.
- No template placeholder or empty required section remains.
Then set `status: ready` and run `rlab index <id>`.

Done when: `status: ready` and the self-check passed — or `status: draft` with the blocking reason written in "Analyst notes".

## 6. Return
Report: key, 2-line summary, evidence-table rows, anything surprising (contradicts other work, suspicious results, missing data).
