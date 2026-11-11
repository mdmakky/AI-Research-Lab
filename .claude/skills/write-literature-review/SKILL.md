---
name: write-literature-review
description: Write an academic literature review from a project's analyses, evidence matrix and gap report, with verified citations and BibTeX. Use when the user asks for a literature review, related-work section, or survey write-up.
---

# Write a literature review

`rlab` = `python3 scripts/rlab.py`. Rules: [docs/research-standards.md](../../../docs/research-standards.md). Delegate drafting to the `academic-writer` agent; review the result yourself.

Inputs: `RESEARCH.md`, `RESEARCH-QUESTIONS.md`, `literature-matrix.md`, `evidence-matrix.md`, `reports/methodology-comparison.md`, `gap-report.md`, analyses. Ask the user only for: target length, audience (thesis chapter / paper section / standalone) and citation style if they care; default = standalone review, ~3000 words, author–year.

## 1. Prepare
`rlab bib <id>`; `rlab index <id>`. Count search and screening numbers from `search/search-log.md` and `search/screening.md`.

## 2. Structure
`reports/literature-review-YYYY-MM-DD.md`:
1. Introduction — problem, why it matters, the review's RQs.
2. Method — sources, queries, years, inclusion criteria, numbers (hits → screened → included; full-text vs abstract-only).
3. Thematic synthesis — one section per theme or RQ; synthesise across papers (agreements, differences, strength of evidence), never paper-by-paper summaries.
4. Methodological landscape — from the comparison report.
5. Contradictions and open debates.
6. Research gaps and future directions — from `gap-report.md`, with novelty-check caveats.
7. Limitations of this review — coverage, abstract-only papers, preprints, language, date of search.
8. Conclusion.
9. References — every cited key, from `references.bib`.

## 3. Writing rules
Formal academic register, clear sentences. Cite every factual claim `[@key, p. N]`; hedge to match evidence strength ("suggests" for weak, "shows" for strong and replicated). Flag preprints as such in the text. Only papers in the project are cited.

## 4. Check
`rlab cite-check <id> <review file>` passes; every reference in section 9 is cited in the text and vice versa.

Done when: all sections are written, cite-check passes, references match citations. Tick Writing in `STATUS.md`.
