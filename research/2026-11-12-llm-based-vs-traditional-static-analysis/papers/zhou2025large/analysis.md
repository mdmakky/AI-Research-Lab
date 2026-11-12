---
key: zhou2025large
status: complete
evidence_basis: full-text
design: Systematic literature review (manual top-venue search + 7-database automated search + snowballing + 5-criterion quality scoring); descriptive mapping, no meta-analysis
dataset: 13 conferences + 4 journals (manual); IEEE Xplore, ACM DL, SpringerLink, Wiley, ScienceDirect, Web of Science, arXiv; Jan 2018 - Mar 2024
sample_size: 58 primary studies (40 detection studies in Table 2, 19 repair studies in Table 3; 1,535 records screened)
metrics: Counts/shares of LLMs used, adaptation techniques, input granularity, data labeling and deployment features across included studies
main_finding: To Mar 2024, LLM vulnerability detection was dominated by fine-tuned small encoder models on function-level, heuristically labelled data; none integrated into developer workflows.
relevance: medium
analysed: 2026-11-12
---
<!-- Frontmatter: single-line values; they feed literature-matrix.md via `rlab index`.
     status: draft (in progress) -> ready (analyst self-check passed) -> complete (critical review passed).
     evidence_basis: full-text | abstract-only. abstract-only analyses must not fill methodology detail.
     relevance: high | medium | low. -->

# Large Language Model for Vulnerability Detection and Repair: Literature Review and the Road Ahead

- Authors: Zhou, Xin; Cao, Sicong; Sun, Xiaobing; Lo, David
- Year / venue: 2025, ACM Transactions on Software Engineering and Methodology (published)
- DOI: 10.1145/3708522 · URL: https://doi.org/10.1145/3708522
- Source text: `fulltext.txt` (page refs = PDF page index)
- **Version analysed:** arXiv:2404.02525v3 (7 Oct 2024) (p. 1), not the typeset TOSEM version. Numbers and wording may differ slightly from the journal version.

Labels: **[V]** verified in the paper's own data/tables/results · **[A]** author claim · **[I]** our interpretation.
Every [V]/[A] item ends with a page ref `(p. N)`. Write "not reported" when the paper does not say.

Convention for this survey: counts about the review's own corpus that appear in its own tables or figures are marked [V]. They are the review's own data, although we cannot re-check the underlying extraction. Anything the survey reports about the results of individual primary studies is second-hand and marked [A], never [V].

## 1. Research objective
- [A] Provide the first systematic literature review focused on how LLMs are used for source-code vulnerability detection **and** repair, identify limitations of existing studies and propose a research roadmap (p. 1, p. 2).
- [A] The authors position it against earlier reviews that covered ML/DL broadly (to 2016, 2020, May 2022) or covered LLMs for SE in general without detailing vulnerability tasks (p. 3).

## 2. Research questions / hypotheses
- RQ1: What LLMs have been used for vulnerability detection and repair? (p. 5)
- RQ2: How are LLMs adapted for vulnerability detection? (p. 5)
- RQ3: How are LLMs adapted for vulnerability repair? (p. 5)
- RQ4: What are the characteristics of datasets and deployment strategies in these studies? (p. 5)
- No hypotheses; descriptive review.

## 3. Methodology
- Research design: SLR "following the guide by Zhang et al." (p. 5). Two search arms: (a) manual search of 13 conferences (ICSE, ESEC/FSE, ASE, ISSTA, CCS, S&P, USENIX Security, NDSS, AAAI, IJCAI, ICML, NIPS, ICLR) and 4 journals (TOSEM, TSE, TDSC, TIFS), yielding 35 papers; (b) automated search of 7 databases yielding 1,500 records, with the search string derived from the manually found papers (p. 5; Fig. 2, p. 4). Then multi-phase screening, quality assessment and forward/backward snowballing (p. 6–7).
- Approach / model / intervention: descriptive classification (taxonomy) of LLMs (encoder-only, encoder-decoder, decoder-only, following Pan et al.) and of adaptation techniques: fine-tuning (data-centric, combination with program analysis, LLM + other DL modules, domain-specific pre-training, causal learning), prompt engineering (zero-/few-shot) and retrieval augmentation (p. 3–4, p. 9–14; Fig. 1, p. 2).
- Baselines or comparison conditions: not applicable (review). The review does **not** compare LLM approaches with SAST tools or non-LLM DL detectors. Studies using only GNN/RNN models were explicitly excluded (p. 6).
- Inclusion criteria [A]: English; full text accessible; peer-reviewed full paper in a conference or journal (arXiv preprints from 2023–2024 kept subject to a quality check); uses LLM techniques for source-code vulnerability detection or repair (p. 5).
- Exclusion criteria [A]: fewer than 5 pages; books, keynotes, technical reports, theses, tool demos, editorials; literature reviews and surveys; duplicates or similar studies by the same authors; no LLM use (e.g. GNN only); LLM mentioned only as future work; not source-code detection/repair (binary code, protocols and network excluded) (p. 5–6).
- Quality assessment [A]: five criteria, QAC1–QAC5 (prestigious venue; contribution; clear workflow/implementation; clear experiment details; findings support the claims). Each is scored 0–3, and studies need a total of at least 12 (80%) to be included. Unpublished preprints score 0 on the venue criterion but are kept if they still reach 12 (p. 6).
- Number of reviewers, independent screening, conflict resolution and inter-rater agreement: not reported.

## 4. Dataset and sample
- Data source(s): manual venue search plus IEEE Xplore (197), ACM DL (285), SpringerLink (266), Wiley (205), Web of Science (237), ScienceDirect (220), arXiv (90) [V] (Fig. 2, p. 4).
- Sample size (N) and unit: 58 primary studies [V] (p. 1, p. 7). Selection flow [V] (Fig. 2, p. 4; p. 6–7):
  - 1,535 records
  - 1,387 after the page filter
  - 1,332 after de-duplication
  - 212 after venue/title/abstract screening
  - 82 after full-text screening
  - 42 after quality assessment (37 published + 5 preprints)
  - 58 final, after adding 16 papers from snowballing (83 snowballing candidates)

  The abstract reports 43 published + 15 preprints (p. 1). Table 2 lists 40 detection studies (p. 10) and Table 3 lists 19 repair studies (p. 16) [V].
- Time window: January 2018 – March 2024 (p. 5). The earliest included study is from 2021, and 2024 accounts for 46.6% of studies [V] (p. 7).
- Sampling / selection method: see section 3. Snowballing is described as "lightweight" (p. 7).
- Data availability: search keywords are in an online appendix (Google Doc) (p. 5, ref [8]). Extraction sheet and per-study QA scores: not reported.

## 5. Experimental setup
- Procedure, settings, tools: the data extraction and analysis section reports only the distribution of studies by year and venue (p. 7). The extraction form is not reported beyond the fields visible in Tables 2–3: LLM size, adaptation technique, input granularity, data labelling, user interaction and workflow integration (p. 10, p. 16).
- Code availability: not applicable; the online appendix covers keywords only (p. 5).

## 6. Evaluation metrics
- Metric — what it measures — why chosen: frequency counts and percentages of LLM usage (92 LLM usages in detection, 45 in repair) and of adaptation techniques (p. 7–9, p. 14, p. 17). The review does not aggregate the precision, recall or F1 reported by primary studies.
- Statistical testing: none (descriptive review); not reported.

## 7. Key findings
1. Encoder-only LLMs dominate detection. CodeBERT accounts for 26.1% (24/92) of LLM usages and GPT-3.5 for 9.8% (9/92). By architecture: encoder-only 47.8% (44/92), decoder-only 23.9% (22/92), encoder-decoder 9.8% (9/92), commercial with undisclosed architecture 18.5% (17/92) — [V] (p. 7–8)
2. Detection adaptation: fine-tuning ≈73%, prompt engineering ≈17%, retrieval augmentation ≈10% of studies — [V] (p. 9, p. 14). Repair: fine-tuning ≈63%, prompting ≈37% — [V] (p. 14, p. 17)
3. Most detection studies work at function level. Only 7 address line level, none address class level, and one works at repo level ([130], which is our `zhou2024comparison`) — [V] (p. 17–18)
4. Detection datasets mostly use heuristic labels: functions changed by vulnerability-fixing commits are labelled vulnerable in their pre-fix version, and other functions are labelled clean. Prior work has shown these labels to be noisy — [A] (p. 18)
5. Repair datasets mostly lack test cases. The two studies that have them evaluate only 42 and 12 samples — [A] (p. 18)
6. None of the reviewed studies is integrated into developer workflows; all are evaluated offline on static historical data. Only one detection study ([113]) produces explanations for developers — [V] (Tables 2–3; p. 19)
7. The only LLM-vs-SAST evidence comes from [130]: SAST tools reach low detection rates with relatively few false positives, while LLMs detect more vulnerabilities but have high false-positive rates. This is second-hand, from a study by the same first and last authors — [A] (p. 22)
8. The best reported state of the art is cited as 67.6% accuracy for detection and 20% for repair (refs [56], [128]) — [A], second-hand (p. 20–21)
9. Cited studies report that LLMs are not robust to data perturbations ([116], [59]). Others report that LLMs struggle with rare CWE types and with inter-procedural or multi-unit vulnerabilities ([51], [84], [128], [129]) — [A] (p. 20–21)

## 8. Limitations stated by the authors
- [A] The only threat to validity discussed is missing relevant studies because of incomplete keywords or varied LLM terminology. It is mitigated by manual venue selection, automated search and snowballing (p. 24).
- [A] Scope: future versions will add vulnerability localisation and assessment (p. 24).

## 9. Limitations we identified
- [I] Dated corpus. The search ends in March 2024 (p. 5), before most agentic, repository-level and LLM + SAST hybrid work. Findings such as "encoder-only dominates" may not hold for 2025–2026: `kaniewski2026systematic` and `sheng2025llms` already report decoder-only dominance. Based on the time window and comparison with the other two surveys in this project.
- [I] Very thin evidence on LLM vs SAST. The single repo-level comparison is the authors' own study ([130], Zhou … Lo, 2024; ref list p. 29). The roadmap's statement about SAST-vs-LLM trade-offs is therefore effectively self-citation, not a synthesis.
- [I] No comparison with non-LLM DL detectors. GNN/RNN-only studies are excluded (p. 6), so the review cannot answer whether LLMs beat DL detectors.
- [I] The quality assessment uses "published in a prestigious venue" (QAC1) as a criterion (p. 6). This mixes venue prestige with methodological quality and structurally penalises preprints.
- [I] Gaps in process transparency: the number of screeners, their agreement and the per-study QA scores are not reported, and the search string is only in an external Google Doc (p. 5).
- [I] Minor internal inconsistencies:
  - The RQ3 answer says "three commonly used techniques" but lists two (p. 17).
  - Limitation 2 opens with "For vulnerability repair" while discussing detection label noise (p. 19).
  - By our count, Tables 2 and 3 contain 57 unique study references (Fu et al. [27] and [29] appear in both), versus 58 stated.

  None of these changes the main conclusions.
- [I] Repair is half of the scope, so detection-specific depth (metrics, benchmarks, CWE coverage) is limited.

## 10. Threats to validity
- Internal (confounds, leakage, selection): selection could be biased by the venue-first strategy and the prestige-weighted QA. Whether one or several people screened each paper is not reported. The review itself flags contamination of LLM pre-training corpora as a concern for primary studies (p. 20).
- External (generalisability of sample/context): the corpus covers Jan 2018–Mar 2024 and source code only, no binaries (p. 5–6). It is dominated by function-level studies (Table 2, p. 10).
- Construct (do metrics measure the concept?): the technique shares (≈73/17/10%) are given without a stated denominator (p. 9). The classification of studies into categories is not validated.
- Statistical conclusion: not applicable (no quantitative synthesis).
- Reproducibility: keywords are in an online appendix (p. 5). Extraction data and QA scores are not released (not reported).

## 11. Future research directions
- Stated by authors [A]:
  - Curate a smaller, manually verified, living high-quality test set for vulnerability detection, e.g. by combining manually checked samples from several studies (p. 22).
  - Repository-level detection and repair using long-context LLMs, extending the initial repo-level SAST-vs-LLM comparison (p. 22).
  - Open-source LLMs customised for vulnerability data (p. 22).
  - LLM usages not yet explored: agents, external tool use, advanced RAG (iterative, recursive, adaptive) (p. 22–23).
  - Deployment-ready features: developer interaction, explanations, IDE/VCS integration (p. 23).
  - Benchmarks with no overlap with LLM pre-training corpora, to avoid data contamination (p. 20).
  - Handling complex vulnerabilities: inter-procedural, rare CWE types, vulnerabilities spanning multiple code units (p. 20).
  - Vision for 2030: line- to repo-level detection and repair, evaluated on an expert-annotated benchmark (p. 23).
- Suggested by us [I]:
  - Check whether the agent, tool-use and repo-level directions proposed here have since been realised. Our corpus contains `guo2025repoaudit`, `li2024iris`, `yildiz2025benchmarking` and `li2026llm`.
  - Check whether the SAST-vs-LLM trade-off reported by `zhou2024comparison` (higher detection for LLMs, but more false positives) replicates in independent studies.

## 12. Relevance to our research
- Research questions addressed (RQ ids): RQ2 (dataset labelling, granularity, contamination) and RQ5 (limitations and roadmap). Marginally RQ1 (one second-hand SAST-vs-LLM statement) and RQ4 (rare CWEs, inter-procedural vulnerabilities).
- How it informs our work [I]: a peer-reviewed (TOSEM) baseline of the field up to March 2024. It mainly shows two things:
  - As of early 2024, head-to-head SAST-vs-LLM evidence was almost absent.
  - Dataset quality, small input granularity and missing workflow integration were already named as key gaps.

  Its LLM-vs-SAST statement should be cited to the primary study `zhou2024comparison`, not to this survey.

## 13. Evidence table (for the evidence matrix)
| RQ | Claim | Page | Label | Strength |
|---|---|---|---|---|
| RQ1 | Only one study in the 58-study corpus compares LLMs with SAST tools (repo level). It reports that SAST tools have low detection rates with few false positives, while LLMs detect more but with high false-positive rates. Second-hand, and the study is the survey authors' own | 18, 22 | A | weak |
| RQ2 | Most LLM detection studies work at function level (7 at line level, 0 at class level, 1 at repo level) | 17–18 | V | moderate |
| RQ2 | Detection datasets mostly use heuristic labels from vulnerability-fixing commits, which prior work has shown to be noisy | 18 | A | moderate |
| RQ2 | Benchmarks may overlap with LLM pre-training corpora (data contamination); contamination-free benchmarks are recommended | 20 | A | moderate |
| RQ4 | LLMs reportedly struggle more with less frequent CWE types and with inter-procedural and multi-unit vulnerabilities | 20 | A | weak |
| RQ5 | Building a high-quality vulnerability detection benchmark remains an open challenge; a curated, living, manually verified test set is proposed | 19, 22 | A | moderate |
| RQ5 | None of the 58 studies is integrated into developer workflows, and almost none supports developer interaction or explanations | 19 | V | moderate |
| RQ5 | Directions still under-explored as of Mar 2024: repo-level detection, LLM agents, external tool use, LLMs customised for vulnerabilities | 22–23 | A | moderate |

## 14. Key quotes
> "Constructing a high-quality vulnerability detection benchmark remains an open challenge to date." (p. 19)

> "all studies in our review are not integrated into developers’ workflows and tools but are evaluated only offline using static and historical data" (p. 19)

> "SAST tools achieve low vulnerability detection rates with relatively low false positives, whereas LLMs can detect more vulnerabilities but tend to suffer from high false positive rates" (p. 22)

## Analyst notes
- Reading coverage: all 24 body pages read (abstract to conclusion, Tables 1–3, Figs. 1–8). The reference list (p. 24–30) was consulted for refs [8], [56], [84] and [128]–[130]. Figures 2–8 are partly garbled in the text layer, so counts were taken from the running text where both exist.
- Version: arXiv v3 (Oct 2024). The published TOSEM version (DOI 10.1145/3708522) was not compared.
- Uncertainties:
  - The denominators of the 73/17/10% technique shares are not stated.
  - The abstract's split of 43 published + 15 preprints is not reconciled with the 37 + 5 papers after QA plus 16 snowballed papers.
- Funding / conflict of interest: funded by the National Research Foundation, Singapore (p. 24). The only SAST-vs-LLM evidence in the survey is the authors' own work ([130]).
