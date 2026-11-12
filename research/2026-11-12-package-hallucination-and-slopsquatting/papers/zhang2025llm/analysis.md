---
key: zhang2025llm
status: complete
evidence_basis: full-text
design: Empirical study: manual open-coding taxonomy of repository-level code hallucinations + pilot RAG mitigation evaluated by Pass@1
dataset: CoderEval Python (230 repository-level tasks from real projects); 6 LLMs (GPT-3.5-Turbo, CodeGen-350M, PanGu-alpha-2.6B, DeepSeekCoder-6.7B, CodeLlama-7B-Python, StarCoder2-7B), 10 samples per task
sample_size: 230 tasks x 6 models x 10 samples (13,800 snippets by our computation; total not stated); taxonomy seeded on 1,380 snippets
metrics: Share of hallucination instances per taxonomy category; Pass@1 for the mitigation
main_finding: Repository-level code hallucinations fall into 3 categories/8 types, mostly task-requirement conflicts (43.53%); environment conflicts, incl. missing packages, are only 0.94%.
relevance: low
analysed: 2026-11-12
---
<!-- Frontmatter: single-line values; they feed literature-matrix.md via `rlab index`.
     status: draft (in progress) -> ready (analyst self-check passed) -> complete (critical review passed).
     evidence_basis: full-text | abstract-only. abstract-only analyses must not fill methodology detail.
     relevance: high | medium | low. -->

# LLM Hallucinations in Practical Code Generation: Phenomena, Mechanism, and Mitigation

- Authors: Zhang, Ziyao; Wang, Chong; Wang, Yanlin; Shi, Ensheng; Ma, Yuchi; Zhong, Wanjun; Chen, Jiachi; Mao, Mingzhi; Zheng, Zibin
- Year / venue: 2025, Proceedings of the ACM on Software Engineering (published) — vol. 2, ISSTA issue, pp. 481–503 as cited in [@zheng2026when, p. 11]; also cited as ISSTA 2025 in [@dasu2026refusing, p. 11]. Not FSE.
- DOI: 10.1145/3728894 · URL: https://doi.org/10.1145/3728894
- Source text: `fulltext.txt` (page refs = PDF page index). The text is the arXiv copy (2409.20550v2, 17 Jan 2025), not the published version; its author list has five authors (Zhang, Wang Y., Wang C., Chen, Zheng) (p. 1) versus nine in the published metadata, so content may differ from the PACMSE version.

Labels: **[V]** verified in the paper's own data/tables/results · **[A]** author claim · **[I]** our interpretation.
Every [V]/[A] item ends with a page ref `(p. N)`. Write "not reported" when the paper does not say.

## 1. Research objective
[A] Study the phenomena, mechanism and mitigation of LLM hallucinations in practical, repository-level code generation, going beyond standalone-function benchmarks (p. 1).

## 2. Research questions / hypotheses
- [A] RQ1 (Taxonomy): What are the manifestations of hallucinations in practical code generation, and how are they distributed? (p. 1)
- [A] RQ2 (LLM comparison): How do LLMs compare in hallucination occurrences and patterns? (p. 1)
- [A] RQ3 (Root causes): What are the root causes? (p. 1)
- [A] Plus an exploratory RAG-based mitigation (p. 2, p. 9). No hypotheses.

## 3. Methodology
- Research design: [V] Qualitative open coding of generated code to build a taxonomy, followed by descriptive distribution analysis and a pilot mitigation experiment (p. 3, p. 9).
- Approach / model / intervention: [V] Open coding: 10% of the 230 CoderEval Python tasks (23 tasks) x 6 models x 10 samples = 1,380 snippets; each snippet tested in the task's real environment; two authors compare with the ground truth and record hallucinations; a preliminary taxonomy is formed; remaining snippets annotated independently by three volunteers (two with >10 years, one with 4 years of Python experience), with new types discussed (p. 3). Model outputs were mixed before annotation and one author reviewed all labels (p. 10). Mitigation: RepoCoder-style retrieval corpus per repository using a sliding window of 20 lines and step 2, excluding ground-truth lines to prevent leakage; sparse bag-of-words with Jaccard similarity; top-10 snippets added to the prompt (p. 9).
- Baselines or comparison conditions: [V] "Raw" prompting with docstring and function signature only (p. 9).

## 4. Dataset and sample
- Data source(s): [V] CoderEval Python: 230 tasks from real repositories, each with description, ground-truth code, tests and project environment (p. 3).
- Sample size (N) and unit: [V] 6 models x 10 snippets per task (p. 3); 13,800 snippets in total by our computation (230 x 6 x 10) — the paper does not state the total or the number of hallucination instances in the text (Fig. 2 and Fig. 11 show distributions, p. 4, p. 8).
- Sampling / selection method: [V] Random selection of the 23 seed tasks (p. 3); all models generate for all tasks.
- Data availability (public? link?): [A] Code, data and results at https://github.com/DeepSoftwareAnalytics/LLMCodingHallucination (p. 1, p. 2).

## 5. Experimental setup
- Procedure, settings, hyper-parameters, tools: [V] Models: GPT-3.5-Turbo, CodeGen-350M-Mono, PanGu-alpha-2.6B, DeepSeekCoder-6.7B base, CodeLlama-7b-Python-hf, StarCoder2-7B (p. 3). Nucleus sampling, temperature 0.6, 10 samples per task, following CoderEval (p. 3). Hardware, max tokens and exact prompt templates are not reported.
- Code availability: [A] Yes (p. 1).

## 6. Evaluation metrics
- [V] Percentage of hallucination instances per category/type (p. 4–p. 7); a snippet can contain several hallucinations (p. 3).
- [V] Pass@1 on CoderEval tests for the mitigation (p. 9).
- Statistical testing: [V] none; no inter-rater reliability statistic (p. 10).

## 7. Key findings
1. [V] Taxonomy of 3 categories and 8 types, Fig. 1 (p. 4): Task Requirement Conflicts 43.53% (functional 36.66%, non-functional 6.86%) (p. 4, p. 5); Factual Knowledge Conflicts 31.91% (background 8.82%, library 2.68%, API 20.41%) (p. 5, p. 6); Project Context Conflicts 24.56% (environment 0.94%, dependency 11.26%, non-code resource 12.36%) (p. 6, p. 7).
2. [V] The package-existence case appears under Environment Conflicts: CodeGen imports `_lfu_cache`, a package that does not exist in the current environment (p. 6, p. 7). Environment Conflicts also cover version mismatches of platforms, languages and libraries (p. 6). [I] `_lfu_cache` is not a valid PyPI distribution name under PEP 508 (names must start with a letter or digit), so it is most likely a missing internal module, not a slopsquatting target; the 0.94% Environment Conflicts share is therefore an upper bound on invented-package cases.
3. [V] Dependency Conflicts are mostly non-existent project-internal functions/attributes (e.g. a similar-but-wrong function name) (p. 6, p. 7); API Knowledge Conflicts include non-existent parameters of real APIs (e.g. `timedelta(year=1)`) (p. 6).
4. [V] Security-relevant non-functional example: generated code uses `yaml.load` instead of `safe_load` (p. 5).
5. [V] Task Requirement Conflicts are the most frequent category for all six models; CodeGen and StarCoder2 have notably more, DeepSeekCoder and CodeLlama fewer; PanGu-alpha has the most factual-knowledge conflicts (p. 8).
6. [A] Four root causes: training-data quality, intention understanding, knowledge acquisition, repository-level context awareness (p. 8, p. 9).
7. [V] RAG mitigation raises Pass@1 for all models: CodeGen 1.30% -> 2.61%, PanGu-alpha 0.04% -> 1.74%, DeepSeekCoder 3.04% -> 3.91%, CodeLlama 2.17% -> 5.22%, StarCoder2 0.04% -> 2.61%, ChatGPT 10.40% -> 12.61%, Table I (p. 9). [A] The improvement is modest and the study is a pilot (p. 9).

## 8. Limitations stated by the authors
- [A] Python only; CoderEval has only 230 tasks (mitigated by 6 models x 10 samples) (p. 10).
- [A] No formal inter-rater reliability measure; disagreements resolved in meetings; one author reviewed all labels (p. 10).
- [A] Possible model bias in annotation, mitigated by mixing outputs (p. 10).
- [A] Mitigation evaluated with CoderEval test cases (p. 10); retrieval corpus limited to the current repository, insufficient for background-knowledge conflicts (p. 10).

## 9. Limitations we identified
- [I] The mitigation is evaluated by Pass@1, not by hallucination counts (p. 9), so the paper gives no direct evidence that RAG reduces hallucinations, and none for package hallucination specifically.
- [I] No registry (PyPI) check: "non-existent package" means not available in the task's environment (p. 6), so invented PyPI names cannot be separated from real but uninstalled packages.
- [I] Category shares are shares of hallucination instances with no stated totals or per-model denominators in the text (p. 4), so per-sample rates cannot be derived.
- [I] Models are dated and small (CodeGen-350M, PanGu-alpha-2.6B, GPT-3.5) (p. 3); Pass@1 values as low as 0.04% (p. 9) suggest near-total failure of some base models in this setting.
- [I] Version mismatch: we analysed the arXiv v2 text, which lists five authors (p. 1) while the published metadata lists nine; other project papers cite it as the ISSTA 2025 issue of PACMSE [@zheng2026when, p. 11; @dasu2026refusing, p. 11], not FSE.

## 10. Threats to validity
- Internal: annotation without IRR (p. 10); taxonomy built from the same data it is applied to — [I].
- External: Python, one benchmark, 2023-era models (p. 3, p. 10) — [I].
- Construct: Pass@1 as a proxy for hallucination mitigation (p. 9) — [I].
- Statistical conclusion: no tests or uncertainty (p. 9) — [I].
- Reproducibility: replication package available (p. 1); prompts and hardware not in the paper — [I].

## 11. Future research directions
- Stated by authors [A]: hallucination identification and localisation techniques; richer RAG sources (search engines, API documentation, Stack Overflow); input query refinement; multi-agent systems with tools (search, static analysis); fine-tuning (p. 9, p. 10); taxonomies for other languages (p. 10).
- Suggested by us [I]: re-annotate with a registry check to measure how many environment/library conflicts are invented PyPI names.

## 12. Relevance to our research
- Research questions addressed (RQ ids): RQ1 (marginal), RQ3 (background), RQ4 (background).
- How it informs our work [I]:
  - Mainly background: places package hallucination inside a broader taxonomy of code hallucination (Project Context / Environment and Factual Knowledge / Library-API conflicts) (p. 4).
  - RQ1: In repository-level Python completion with these models, missing-package/environment problems are a very small share (0.94%) of all hallucination instances (p. 6) — a different setting from prompt-to-code studies that ask for whole programs.
  - RQ3: Repository-context RAG is a cheap baseline but was not shown to reduce hallucinations directly (p. 9).
  - Laptop-scale implication: all open models used are <=7B and runnable locally, and CoderEval is small; but the study gives little for a package-hallucination measurement or defence. Cite as related-work context only.
  - Replication checklist: CoderEval Python (230 tasks), 10 samples, nucleus sampling temperature 0.6; RAG window 20 lines, step 2, BOW-Jaccard, top-10 snippets; Pass@1 (p. 3, p. 9).

## 13. Evidence table (for the evidence matrix)
| RQ | Claim | Page | Label | Strength |
|---|---|---|---|---|
| RQ1 | In repository-level Python generation (CoderEval, 6 LLMs <=7B + GPT-3.5), Environment Conflicts (incl. importing a non-existent package) are 0.94% of hallucination instances, vs 20.41% API Knowledge Conflicts. [I] The only example (`_lfu_cache`) is not a valid PyPI name (PEP 508), so 0.94% is an upper bound on invented-package cases | 6 | [V] | weak |
| RQ3 | Repository-context RAG (BOW-Jaccard, top-10 snippets) raises Pass@1 for all 6 models by 0.87–3.05 points; effect on hallucination counts not measured | 9 | [V] | weak |
| RQ4 | Taxonomy: 3 categories / 8 types; package-related errors fall under Environment (Project Context) and Library/API (Factual Knowledge) conflicts | 4 | [V] | moderate |
| RQ4 | Manual annotation without a formal inter-rater reliability measure | 10 | [A] | weak |

## 14. Key quotes
> "attempts to use the package _lfu_cache, which does not exist in the current environment" (p. 6)
> "A key issue is the absence of formal inter-rater reliability measure for annotating hallucinations." (p. 10)
> "Note that the performance improvement in our experiments is modest" (p. 9)

## Analyst notes
- Reading coverage: whole paper read (pp. 1–10 text; pp. 11–13 references skimmed). Figures 2 and 11 are charts without numeric labels in the text layer; shares taken from section text.
- Uncertainties: We analysed arXiv v2 (5 authors). An OA published version (9 authors) exists via the metadata oa_pdf_url (https://dl.acm.org/doi/pdf/10.1145/3728894) but was not analysed and may differ. Total number of hallucination instances not reported in the text.
