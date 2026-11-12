---
key: kaniewski2026systematic
status: complete
evidence_basis: full-text
design: Systematic literature review (Kitchenham guidelines) with taxonomy and dataset analysis; descriptive mapping, no performance meta-analysis
dataset: IEEE Xplore, ACM DL, arXiv (search Dec 2024 + continuous alerts) + snowballing; Jan 2020 - Nov 2025; 20 datasets characterised, 12 re-analysed for CWE coverage
sample_size: 263 primary studies (185 peer-reviewed, 78 arXiv preprints); 4,155 database hits
metrics: Study counts per taxonomy category; dataset size, % vulnerable, #CWEs, CWE-1000 pillar coverage, dataset usage/co-usage frequency
main_finding: LLM vulnerability detection is fragmented: mostly binary function-level C/C++ classification on noisy, leakage-prone, long-tailed datasets with inconsistent splits, so results are hard to compare.
relevance: high
analysed: 2026-11-12
---
<!-- Frontmatter: single-line values; they feed literature-matrix.md via `rlab index`.
     status: draft (in progress) -> ready (analyst self-check passed) -> complete (critical review passed).
     evidence_basis: full-text | abstract-only. abstract-only analyses must not fill methodology detail.
     relevance: high | medium | low. -->

# A Systematic Literature Review on Detecting Software Vulnerabilities with Large Language Models

- Authors: Kaniewski, Sabrina; Schmidt, Fabian; Enzweiler, Markus; Menth, Michael; Heer, Tobias
- Year / venue: 2026, ACM Transactions on Software Engineering and Methodology (published)
- DOI: 10.1145/3815425 · URL: https://doi.org/10.1145/3815425
- Source text: `fulltext.txt` (page refs = PDF page index)
- **Version analysed:** arXiv:2507.22659v2 (19 Dec 2025) (p. 1), the preprint of the TOSEM article (DOI 10.1145/3815425), not the typeset journal version. Study statistics are "as of December 13th 2025" (p. 8).

Labels: **[V]** verified in the paper's own data/tables/results · **[A]** author claim · **[I]** our interpretation.
Every [V]/[A] item ends with a page ref `(p. N)`. Write "not reported" when the paper does not say.

Convention for this survey: two kinds of numbers are marked [V]: counts about the review's own corpus shown in its own tables and figures, and dataset statistics that the authors recomputed from the published datasets (Table 5 states the numbers "are reproduced with the officially published datasets", p. 28). They are the review's own data, although we cannot re-check the extraction. Anything reported about results of individual primary studies is second-hand and marked [A], never [V].

## 1. Research objective
- [A] Map the fragmented field of LLM-based software vulnerability detection. The authors argue that studies are hard to compare because of different system designs, datasets, metrics and splits (p. 1–2).
- [A] Contributions (p. 2–3):
  - an SLR of 263 studies (Jan 2020–Nov 2025)
  - a taxonomy covering task formulation, input representation, system architecture, adaptation/orchestration technique and dataset usage
  - an in-depth dataset analysis (class balance, CWE coverage/diversity)
  - limitations and future directions
  - a living public repository (Awesome-LLM4SVD)
- [A] The term "LLM" is used broadly and includes small pre-trained models such as BERT and CodeBERT (footnote, p. 2).

## 2. Research questions / hypotheses
- RQ1: How is the detection task formulated in LLM-based systems? (p. 6)
- RQ2: How are input and vulnerability semantics represented for LLMs? (p. 6)
- RQ3: What are the predominant techniques for adapting LLMs to detection? (p. 6)
- RQ4: Which datasets are used, and how does dataset selection affect applicability? (p. 6)
- RQ5: How does dataset selection affect comparability across studies? (p. 6)
- No hypotheses.

## 3. Methodology
- Research design: SLR following Kitchenham et al. guidelines (p. 5). It has three phases: literature search, study selection and study analysis (Fig. 1, p. 8).
- Search: automated search of IEEE Xplore, ACM Digital Library and arXiv on titles/abstracts (p. 6–7). The full Boolean search string is printed: LLM/model-family terms AND (vulnerability/CVE/CWE) AND (detect*/identif*/classif*/analy*/discover*/assess*) AND (software/program/code) (p. 7). The initial search ran in December 2024, followed by continuous database alerts and scholar.inbox notifications (p. 7).
- Inclusion criteria [A]: title or abstract matches the search string; the study uses **and evaluates** LLMs for software vulnerability detection and introduces novel techniques or systems (Table 2, p. 8).
- Exclusion criteria [A] (Table 2, p. 8; p. 7):
  - not in English, or full text not accessible
  - reviews, surveys, theses, abstracts, posters, demos, tutorials
  - binary code, smart contracts, network analysis or malware
  - studies that use LLMs **only to work on outputs of other tools (e.g. SAST)**
  - LLMs mentioned only in passing or used merely as baselines
  - duplicates or extended versions
- Quality assessment [A]: a manual check of contribution, workflow/implementation description, evaluation setup (datasets, baselines, metrics) and coherence of findings, motivated by the inclusion of preprints (p. 7). The scoring scheme, threshold and number of excluded studies are not reported.
- Snowballing: backward (reference lists) and forward (Google Scholar citations), with snowballed studies passing the same criteria (p. 7).
- Extraction: task definition, LLMs used, adaptation techniques, input representation, datasets, targeted CWEs and metrics (p. 7–8).
- Number of reviewers, independent double screening and inter-rater agreement: not reported.
- Baselines or comparison conditions: not applicable. The review does **not** synthesise LLM-vs-SAST or LLM-vs-DL performance. Studies that use LLMs only as baselines are excluded (p. 8).

## 4. Dataset and sample
- Data source(s): ACM DL (514 hits), IEEE Xplore (865), arXiv (2,776) [V] (Fig. 1, p. 8). Screening counts per stage (title/abstract, full text, quality, snowballing) are not reported.
- Sample size (N) and unit: 263 primary studies [V] (p. 7–8): 185 peer-reviewed and 78 (29.7%) arXiv preprints [V] (p. 8; Fig. 2, p. 9). The earliest study is from 2020 (p. 8). The A*/A conference and Q1 journal venues are listed in Table 3, e.g. ICSE 13 and TSE 7 [V] (p. 9).
- Time window: January 2020 – November 2025 (p. 1–2).
- Dataset analysis: 20 datasets are characterised (the 15 most used plus 5 selected recent ones; Tables 4–5, p. 26, p. 28). 12 real-world/mixed multi-class datasets are analysed for CWE distribution, with D2A and FormAI excluded (p. 30).
- Data availability: artifacts and the categorised study list are in a public GitHub repository [144] (p. 3, p. 43).

## 5. Experimental setup
- Procedure, settings, tools: full-text review with structured extraction (p. 7–8). The taxonomy categories are refined iteratively and aligned with existing definitions where possible (p. 43). CWE clustering uses the MITRE CWE-1000 Research View pillars (p. 30–32). Dataset usage is analysed over time (Fig. 11, p. 34), by co-usage pairs (Fig. 12, p. 35) and by overlap within use cases (Fig. 13, p. 36).
- Code availability: artifacts released [144] (p. 3).

## 6. Evaluation metrics
- Metric — what it measures — why chosen:
  - Study counts per taxonomy node, used to show prevalence.
  - Dataset size, % vulnerable samples and number of distinct CWEs, as proxies for label diversity and balance (p. 25, p. 28).
  - Share of CWE labels per CWE-1000 pillar and Top-25 CWE concentration, measuring thematic diversity (p. 31–32).
  - Dataset usage frequency and overlap, measuring comparability (p. 34–37).
- The review does not extract or pool the effectiveness metrics (precision/recall/F1) of primary studies, although "evaluation metrics" is listed among the extracted fields (p. 8).
- Statistical testing: none; not reported.

## 7. Key findings
1. Task formulation: binary classification dominates (195 studies). Vulnerability-specific classification: 20; multi-class: 61; multi-label: 23. Only a minority combine classification with generation tasks (description, root-cause reasoning, structured report) — [V] (p. 11; Fig. 4, p. 12)
2. Input: 139 studies feed raw code. Structured inputs (AST/CFG/DFG/PDG/CPG, slices, code gadgets) and auxiliary information (CWE lists, few-shot examples, execution context, SAST tool output) are used less often — [V] (p. 13–14)
3. Architecture and scale: decoder-only LLMs dominate. Tiny/small models (< 8B) are mostly full-parameter fine-tuned, while medium/large models are mostly prompted or PEFT-tuned. Hybrid LLM + GNN/RNN/CNN architectures form a distinct group — [V] (p. 15–16; Fig. 5, p. 16)
4. Advanced techniques are emerging but rare: RAG in 25 studies, LoRA in 27, agentic systems in 10, GNN hybrids in 20 — [V] (p. 36–37)
5. Dataset usage is concentrated on old function-level C/C++ benchmarks. Devign is used in 69 studies, Big-Vul in 63, ReVeal in 40, SARD in 32, DiverseVul and PrimeVul in 27 each — [V] (Table 4, p. 26)
6. Datasets are highly imbalanced. Recomputed vulnerable shares: Big-Vul 4.5%, DiverseVul 5.7%, PrimeVul 2.9%, D2A 1.4%, ReposVul 0.7%, compared with Devign 48.0% — [V] (Table 5, p. 28)
7. Real-world datasets follow a long-tail CWE distribution: the Top-25 CWEs account for about 80% of labels. Memory/resource-lifetime CWEs dominate, and several CWE-1000 pillars are absent from the Top 25 — [V] (p. 30, p. 32; Figs. 8–10)
8. 555 CWEs that are allowed for vulnerability mapping in CWE-1000 appear in none of the analysed datasets. Many dataset labels use discouraged or abstract CWEs (e.g. CWE-119, CWE-399, CWE-20) — [V] (p. 32, p. 34)
9. Fragmentation of evaluation setups:
   - 87 studies use or introduce custom datasets, and only nine datasets are reused in more than ten studies (p. 35).
   - Few datasets have predefined train/validation/test splits: Draper, CodeXGLUE-Devign, Big-Vul, PrimeVul (p. 39).
   - Among agentic studies, only 4 of 10 share PrimeVul (p. 37).

   — [V] for the counts, [A] for the conclusion that cross-study comparison is unreliable
10. Data leakage: widely used static benchmarks (Devign, Big-Vul) are likely in LLM pre-training corpora, so high scores may reflect memorisation rather than generalisation — [A] (p. 30, p. 38–39)
11. Robustness: models rely on superficial textual patterns, and performance degrades under semantics-preserving transformations (renaming, reordering, formatting) — [A] (p. 39)
12. Practical deployment: there are few evaluations in realistic development settings, models often underperform outside curated benchmarks (citing our `chakraborty2024revisiting`), and costs are high — [A] (p. 39–40)
13. LLM–SAST relationship. LLMs are presented as free of the hand-written, language-specific rules that SAST needs (p. 1, p. 12–13). In the corpus, SAST appears as auxiliary input to LLMs: tool output in prompts, or hybrid workflows where the LLM verifies or refines static-analysis findings ([18], [145], [219], [340], [365]) (p. 14, p. 18). The authors see synergy of LLMs with program analysis as "a current pathway for industrial adoption": SAST detects and the LLM filters false positives, or the LLM proposes and static analysis verifies (p. 42). This is qualitative only, with no quantified comparison — [A]

## 8. Limitations stated by the authors
- [A] Paper retrieval omissions (keywords, a static snapshot of a living field), mitigated by a broad search string, snowballing, continuous alerts and a maintained repository (p. 42–43).
- [A] Study selection bias, including the decision not to filter by venue rank and to include preprints. Mitigated by reporting venue tiers and a manual quality assessment (p. 43).
- [A] Subjectivity in data extraction and taxonomy classification (e.g. "reasoning" vs "description"). Mitigated by aligning with existing definitions and releasing the categorised study list (p. 43).

## 9. Limitations we identified
- [I] It is a mapping study, not an effectiveness synthesis. No precision/recall/F1 or false-positive data are pooled or compared, so it cannot answer RQ1 directly. Its value for us is RQ2/RQ5. Based on sections 4–6 and the absence of any results tables.
- [I] Scope excludes much of the hybrid design space we care about. Studies that use LLMs only to post-process SAST output (e.g. false-positive filtering) are excluded (p. 7–8). The very hybrid that the authors recommend for industry (p. 42) is therefore out of the corpus. Our RQ3 needs primary studies such as `du2026reducing`, `xiong2026sifting` and `li2024iris`.
- [I] Only three databases are searched (IEEE, ACM, arXiv) (p. 6). Springer, Elsevier, Wiley and USENIX/NDSS are not searched directly, which partly explains the high arXiv hit count. Snowballing and alerts mitigate this only partly.
- [I] Opaque quality assessment and screening. The QA criteria are listed without a scoring scheme or threshold, and per-stage exclusion counts, number of reviewers and agreement are not reported (p. 7–8). This is weaker than `zhou2025large`'s explicit 0–3 scoring.
- [I] The broad LLM definition (BERT/CodeBERT counted as LLMs, p. 2) and the inclusion of feature-extraction-only uses (p. 17) blur the line between "LLM-based" and "pre-trained-transformer DL" detectors. That line matters for our three-way LLM vs SAST vs DL comparison.
- [I] Minor internal inconsistencies:
  - The Fig. 11 caption says "Jan 2020 to Mar 2025" while the text says Jan 2020 to Nov 2025 (p. 34).
  - SecurityEval is described with "75 CWE types" (p. 29) but 69 CWEs in Table 5 (p. 28) and on p. 30.
  - Ding et al. (PrimeVul) appears twice in the references, as [54] (arXiv) and [55] (ICSE) (p. 46).
  - The statement that large models "achieve state-of-the-art performance on vulnerability detection benchmarks" (p. 15) has no citation.

  None of these affects the main conclusions.
- [I] Preprint-heavy corpus: 29.7% of studies are arXiv preprints (p. 8). Corpus-level counts mix peer-reviewed and non-peer-reviewed work, and the counts are not split by peer-review status.

## 10. Threats to validity
- Internal (confounds, leakage, selection): selection is subjective and the screening reliability is not reported. The exclusion of "LLM on tool output" studies shapes conclusions about hybrids (p. 7). The review itself highlights data leakage as a key threat in primary studies (p. 24, p. 30, p. 38–39).
- External (generalisability of sample/context): source code only, with binaries, smart contracts and malware excluded (p. 8). The corpus is C/C++-heavy because the datasets are (p. 28, p. 37).
- Construct (do metrics measure the concept?): the number of distinct CWEs is used as a proxy for label diversity (p. 25), and pillar mapping depends on the quality of NVD labels (p. 32). Counts of studies per technique measure popularity, not effectiveness.
- Statistical conclusion: not applicable (no inferential analysis).
- Reproducibility: strong for an SLR. The full search string is printed (p. 7), and the artifacts and categorised studies are public [144] (p. 3, p. 43). Screening records and QA scores are not reported.

## 11. Future research directions
- Stated by authors [A] (Table 7, p. 38; p. 40–42):
  - L1 Granularity: project- and repository-level detection; richer code context (callees, types, globals, execution/data flow); languages beyond C/C++ (Python, Java, Rust); multilingual and cross-project benchmarks (p. 40).
  - L2 Labels and quality: manual verification and better VFC labelling tools; reasoning-oriented benchmarks with verified root-cause explanations; datasets built after model knowledge cutoffs to avoid leakage; covering the 555 unused mappable CWEs (p. 40–41).
  - L3 Comparability: datasets with documented splits (or closed test sets); evaluating on multiple datasets (recent PrimeVul/MegaVul plus established Devign/Big-Vul); documenting all preprocessing; open science (p. 41).
  - L4 Up-to-date knowledge: automatically updated datasets (e.g. CVEfixes); RAG and continual learning (p. 41).
  - L5 Representation: structure-aware and language-agnostic inputs; LLM + GNN hybrids; robustness tests on perturbed or LLM-generated code (p. 41).
  - L6 Explainability: metrics for explanation trustworthiness; structured explanations (propagation paths); grounding via CWE hierarchies (p. 42).
  - L7 Integration (p. 42):
    - IDE/CI integration, field studies and evaluation on proprietary code
    - CWE-type classifiers
    - agentic self-assessment
    - SAST + LLM synergy in both directions (SAST then LLM false-positive filter; LLM then static-analysis verification)
    - model compression and on-premise small models
- Suggested by us [I]:
  - No direction asks for controlled, same-benchmark comparisons of LLMs against SAST tools and non-LLM DL detectors. This gap is consistent with `zhou2025large` and `sheng2025llms`, and is a candidate for our RQ5 gap section (requires a novelty check).
  - The recommended SAST + LLM pipelines (p. 42) are, by construction, outside this SLR's corpus. Evidence for them must come from studies this SLR excludes.

## 12. Relevance to our research
- Research questions addressed (RQ ids): RQ2 (strongest: dataset taxonomy, imbalance, CWE coverage, leakage, splits, fragmentation), RQ5 (L1–L7 limitations and directions), RQ4 (C/C++ bias, CWE long tail, missing pillars), RQ3 (qualitative: SAST output as LLM input; recommended hybrids). RQ1 is not answered.
- How it informs our work [I]: the most recent and largest SLR in our corpus (263 studies, to Nov 2025) and peer-reviewed (TOSEM). Its dataset analysis gives concrete, recomputed evidence for why reported numbers disagree across studies. That is the core of our RQ2: different benchmarks, extreme class-balance differences (0.7–100% vulnerable across Table 5; 1.4–50% among the function-level C/C++ benchmarks, p. 28), long-tailed CWE coverage, missing splits, custom datasets and leakage. It supports the claim that head-to-head LLM-vs-SAST/DL evidence must be read benchmark by benchmark.

## 13. Evidence table (for the evidence matrix)
| RQ | Claim | Page | Label | Strength |
|---|---|---|---|---|
| RQ1 | This 263-study SLR does not synthesise effectiveness; it presents SAST tools as rule-dependent with high false-positive rates, and LLMs as rule-free but unproven outside curated benchmarks (no pooled comparison) | 1, 12–13, 40 | A | weak |
| RQ2 | Most-used benchmarks are old function-level C/C++ datasets (Devign 69, Big-Vul 63, ReVeal 40 studies) with vulnerable shares from 0.7% (ReposVul) to 100% (SecurityEval) across Table 5, or 1.4% (D2A) to 50.0% (PairVul) among the function-level C/C++ benchmarks | 26, 28 | V | strong |
| RQ2 | 87 studies use or introduce custom datasets, only nine datasets are reused in more than ten studies, and few datasets have predefined splits, so cross-study comparison is unreliable | 35, 39 | V | strong |
| RQ2 | Widely used benchmarks are likely in LLM pre-training corpora (data leakage), so high scores may reflect memorisation | 30, 38–39 | A | moderate |
| RQ3 | In LLM-based detectors, SAST output is used as auxiliary input, or the LLM verifies/refines static-analysis findings; studies that only post-process tool output are excluded from the SLR | 7–8, 14, 18 | V | moderate |
| RQ3 | Authors recommend SAST + LLM synergy (SAST detects then LLM filters false positives; LLM proposes then static analysis verifies) as a pathway to industrial adoption; not quantified | 42 | A | weak |
| RQ4 | Datasets are C/C++-biased and long-tailed (Top-25 CWEs ≈80% of labels); 555 mappable CWEs are absent from all analysed datasets; logic/interaction pillars are under-represented | 28, 32, 34 | V | strong |
| RQ5 | Seven open limitation themes: granularity, label quality/leakage, comparability, outdated knowledge, representation robustness, explainability, workflow integration/cost | 37–40 | A | moderate |
| RQ5 | Few studies evaluate in realistic development settings; models often underperform outside curated benchmarks | 39–40 | A | moderate |

## 14. Key quotes
> "studies frequently adopt custom datasets, metrics, and data splits, making it difficult to assess progress, reproduce results, or compare models fairly" (p. 2)

> "Only nine datasets are reused in more than ten studies, highlighting the lack of a standardized suite of benchmark datasets" (p. 35)

> "Pipelines where SAST tools detect candidates and LLMs filter false positives can significantly reduce alert fatigue" (p. 42)

## Analyst notes
- Reading coverage:
  - All 43 body pages read: methodology, taxonomy (sections 4.1–4.4), datasets (section 5), limitations and road ahead (section 6), threats, conclusion.
  - Long citation lists inside the taxonomy sections were skimmed, not checked individually.
  - The reference list (p. 44–63) was consulted for refs [29], [42], [54]/[55], [145], [159], [172], [219], [304], [368] and [394].
  - Figures 4, 5 and 8–13 are partly garbled in the text layer, so counts were taken from the running text and from Tables 4–5.
- Version: arXiv v2 (19 Dec 2025). The published TOSEM version was not compared.
- Overlap with our corpus (cited as primary studies): `ahmed2026secvuleval` ([3]), `chakraborty2024revisiting` ([29]), `ding2025vulnerability` ([54]/[55]), `khare2025understanding` ([146]), `li2024iris` ([172]), `yildiz2025benchmarking` ([368]), `zhou2024comparison` ([394]). It also cites a separate LLM-vs-traditional-methods survey (Taghavi Far & Feyzi 2025, [304]) that is not in our project. That survey might be worth screening for RQ1.
- Funding / conflict of interest: DFG project 528745080 (p. 44). The first author's prior survey ([143]) seeded the search terms (p. 7).
- Uncertainties: per-stage screening numbers are unknown, and the quality-assessment threshold is unknown.
