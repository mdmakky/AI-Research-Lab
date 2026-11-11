---
key: {{KEY}}
status: draft
evidence_basis: {{BASIS}}
design: 
dataset: 
sample_size: 
metrics: 
main_finding: 
relevance: 
analysed: {{DATE}}
---
<!-- Frontmatter: single-line values; they feed literature-matrix.md via `rlab index`.
     status: draft (in progress) -> ready (analyst self-check passed) -> complete (critical review passed).
     evidence_basis: full-text | abstract-only. abstract-only analyses must not fill methodology detail.
     relevance: high | medium | low. -->

# {{TITLE}}

- Authors: {{AUTHORS}}
- Year / venue: {{YEAR}}, {{VENUE}} ({{VENUE_KIND}})
- DOI: {{DOI}} · URL: {{URL}}
- Source text: `fulltext.txt` (page refs = PDF page index)

Labels: **[V]** verified in the paper's own data/tables/results · **[A]** author claim · **[I]** our interpretation.
Every [V]/[A] item ends with a page ref `(p. N)`. Write "not reported" when the paper does not say.

## 1. Research objective

## 2. Research questions / hypotheses

## 3. Methodology
- Research design:
- Approach / model / intervention:
- Baselines or comparison conditions:

## 4. Dataset and sample
- Data source(s):
- Sample size (N) and unit:
- Sampling / selection method:
- Data availability (public? link?):

## 5. Experimental setup
- Procedure, settings, hyper-parameters, tools:
- Code availability:

## 6. Evaluation metrics
- Metric — what it measures — why chosen:
- Statistical testing (tests used, significance, effect sizes, confidence intervals):

## 7. Key findings
1. finding — numbers — [V]/[A] (p. N)

## 8. Limitations stated by the authors
- [A] (p. N)

## 9. Limitations we identified
- [I] limitation — why it matters

## 10. Threats to validity
- Internal (confounds, leakage, selection):
- External (generalisability of sample/context):
- Construct (do metrics measure the concept?):
- Statistical conclusion (power, multiple comparisons, variance):
- Reproducibility (data/code/setup reported?):

## 11. Future research directions
- Stated by authors [A] (p. N):
- Suggested by us [I]:

## 12. Relevance to our research
- Research questions addressed (RQ ids):
- How it informs our work [I]:

## 13. Evidence table (for the evidence matrix)
| RQ | Claim | Page | Label | Strength |
|---|---|---|---|---|

## 14. Key quotes
> "short verbatim quote" (p. N)

## Analyst notes
- Reading coverage: sections read / skipped and why:
- Uncertainties:
