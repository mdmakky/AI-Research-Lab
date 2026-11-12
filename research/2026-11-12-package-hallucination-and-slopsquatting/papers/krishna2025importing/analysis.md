---
key: krishna2025importing
status: complete
evidence_basis: full-text
design: Measurement study using garak probes across 11 LLMs and 3 languages, plus correlational analysis with model size and coding benchmarks
dataset: Prompt grid of 7 request stubs x 13 task descriptions x 3 languages (JS, Python, Rust); registry name+release-date lists (npm, PyPI, crates.io) as of 30 Jan 2025
sample_size: 11 LLMs x 3 languages; N per cell not reported, inferred 455 prompts per model-language cell (1,365 per model)
metrics: Package Hallucination Rate (PHR) = share of prompts with >=1 hallucinated package; Pearson correlation with size, HumanEval, MBPP; t-test coding vs general
main_finding: All 11 models hallucinate packages (PHR 0.22–46.15%); JavaScript lowest; larger models and higher HumanEval scores correlate with lower PHR.
relevance: high
analysed: 2026-11-12
---
<!-- Frontmatter: single-line values; they feed literature-matrix.md via `rlab index`.
     status: draft (in progress) -> ready (analyst self-check passed) -> complete (critical review passed).
     evidence_basis: full-text | abstract-only. abstract-only analyses must not fill methodology detail.
     relevance: high | medium | low. -->

# Importing Phantoms: Measuring LLM Package Hallucination Vulnerabilities

- Authors: Krishna, Arjun; Galinkin, Erick; Derczynski, Leon; Martin, Jeffrey (University of Waterloo; NVIDIA) (p. 1)
- Year / venue: 2025, arXiv preprint (not peer-reviewed). **Source tier 3.** arXiv:2501.19012v1, 31 Jan 2025 (p. 1).
  - Page 1 carries the footer "Proceedings of the 41st International Conference on Machine Learning, Vienna, Austria. PMLR 235, 2024" (p. 1).
  - [I] This is most likely left over from the conference template, since v1 was posted after ICML 2024 took place. We treat the venue as unverified.
- DOI: 10.48550/arxiv.2501.19012 · URL: https://arxiv.org/abs/2501.19012
- Source text: `fulltext.txt` (page refs = PDF page index). PDF pages 13–23 are figure-placeholder pages only.

Labels: **[V]** verified in the paper's own data/tables/results · **[A]** author claim · **[I]** our interpretation.
Every [V]/[A] item ends with a page ref `(p. N)`. Write "not reported" when the paper does not say.

## 1. Research objective
[A] The paper aims to measure package hallucination across Python, JavaScript and Rust and across types of LLMs, to find links between model characteristics and hallucination, and to develop defences (p. 1–2).

## 2. Research questions / hypotheses
- [A] RQ1: How often does package hallucination happen? (p. 2)
- [A] RQ2: What effect does the programming language have? (p. 2)
- [A] RQ3: How does model size affect it? (p. 2)
- [A] RQ4: Does it differ between coding-specialised and general-purpose LLMs? (p. 2)
- [A] Also studied: "induced" vs "natural" hallucination (p. 3, p. 5). Induced means the prompt explicitly asks for a package or API that does not exist; natural means the model invents one unprompted.

## 3. Methodology
- Research design: [V] Black-box probing with garak, an open-source tool for probing LLMs: send prompts, extract the imported packages from the output, and compare them with registry lists (p. 3).
- Definition: [V] A package counts as hallucinated if it meets any of these conditions (p. 3):
  - it is not registered on the relevant registry (npm, PyPI or crates.io);
  - it was first registered after the model's knowledge cutoff;
  - if the cutoff is unknown, it was first registered less than 90 days before the model's first publication.

  How the knowledge cutoffs were obtained is not reported.
- Approach / model / intervention: [V] 11 models (Table 1, p. 3):
  - CodeGemma 7B;
  - Dracarys-Llama-3.1-70B;
  - GPT-4o (gpt-4o-2024-08-06; listed as about 200B parameters, an estimate from a third-party source);
  - Granite-3.0 8B;
  - Llama-3.1 8B and 70B;
  - Mamba-Codestral 7B;
  - Mistral-NeMo-Minitron-8B;
  - Llama-3.1-Nemotron-70B;
  - Qwen2.5-Coder 7B;
  - StarCoder2-15B.

  Six are classed as code-specialised and five as general-purpose (p. 6).
- Prompts: [V] Every combination of 7 request stubs and 13 coding tasks, for each language (p. 4; Tables 6–7, p. 12). Each request is repeated five times (p. 4).
  - Some stubs use personas ("As a woman, I need example...", "What <language> module would a Black person use...") (p. 12). Their purpose is not explained.
  - Which prompts count as induced is not stated.
- Extraction: [V] Regular expressions per language (p. 12):
  - Python: `import x`, `from x import`, `import x as`;
  - JavaScript: ES6 `import ... from`, CommonJS `require()`;
  - Rust: `use x`, `extern crate x`, and `x::` path references.

  Not reported: mapping from import name to package name, name normalisation, and standard-library exclusion.
- Baselines or comparison conditions: [V] Comparisons across languages, code-specialised vs general models, model size, and HumanEval/MBPP scores (p. 4–7). No mitigation baseline.

## 4. Dataset and sample
- Data source(s): [V] Package names and release dates scraped from each registry, as of 30 January 2025 (Table 2, p. 4):
  - npm: 3,391,235 packages;
  - PyPI: 604,814;
  - crates.io: 169,823.

  How the scraping was done is not reported.
- Sample size (N) and unit:
  - The number of generations is not reported.
  - [I] Every PHR value in Table 3 (p. 4) is an exact multiple of 1/455; we checked all 33 values. For example, 0.22% = 1/455, 2.42% = 11/455 and 46.15% = 210/455. This supports N = 455 prompts per model-language cell, which matches 7 stubs × 13 tasks × 5 repeats (p. 4, p. 12).
  - [I] That gives 1,365 prompts per model and about 15,000 in total.
  - [I] Nemotron's 0.22% (JavaScript and Rust) is therefore a single hallucinating prompt.
  - [V] 11 models (p. 6).
- Sampling / selection method: [V] Models were chosen to vary in size, provider and purpose (p. 3). The 13 tasks were hand-picked and include obscure or possibly fictional targets such as "StrombergDB", "Tektronics 4051" and "Query/400" (p. 12).
- Data availability (public? link?): [V] Only a general statement that the study used open-source software and openly available models (p. 10). No link is given.

## 5. Experimental setup
- Procedure, settings, hyper-parameters, tools: [V] Experiments were run through garak (p. 3), with 5 repeats per request (p. 4). Not reported: temperature, decoding settings, maximum tokens, hardware, inference provider, quantization.
- Funding and conflicts of interest: not reported. [V] Three of the four authors are affiliated with NVIDIA (p. 1).
- Code availability: no repository is linked (p. 10). [I] garak itself is open source.

## 6. Evaluation metrics
- Metric — what it measures — why chosen: [V] Package Hallucination Rate (PHR) is the share of prompts that produced at least one hallucinated package (p. 4). It is a per-generation rate, not a per-package rate.
- Statistical testing (tests used, significance, effect sizes, confidence intervals): [V]
  - Pearson correlation of model size with PHR: r = −0.542, p = 0.00114; using log(size): r = −0.593, p = 0.00028 (p. 6–7).
  - HumanEval vs PHR: r = −0.7887. MBPP vs PHR: r = −0.2919. No p-values are given for these (p. 7).
  - t-test, code-specialised vs general models: significant only for JavaScript, and not significant once GPT-4o is removed (p. 6).
  - No confidence intervals and no correction for multiple comparisons.

## 7. Key findings
1. [V] All models hallucinated packages in every language. PHR ranged from 0.22% (Nemotron-70B, JavaScript and Rust) to 46.15% (Granite-3.0, Python) (Table 3, p. 4; p. 8).
2. [V] Mean PHR by language: JavaScript 14.73%, Python 23.14%, Rust 24.74% (p. 8; Figure 1, p. 5). Spread across models (standard deviation): Python 16.03, Rust 14.37, JavaScript 8.43 (p. 4).
3. [V] Best values per language (Table 3, p. 4; p. 5):

   | Model | JavaScript | Rust | Python |
   |---|---|---|---|
   | GPT-4o | 1.76% | 10.99% | 3.52% |
   | Nemotron-70B | 0.22% | 0.22% | 4.84% |
   | Dracarys-70B | — | — | 2.42% (lowest Python value) |

4. [V] Larger models hallucinate less: r = −0.542, p = 0.00114 (p. 6).
   - [I] These p-values match n = 33 exactly, i.e. 11 models × 3 languages treated as independent points. With n = 11 models, p ≈ 0.085 (raw size) and ≈ 0.055 (log size), so the effect is not significant at the model level. Based on our own recomputation.
5. [V] Higher HumanEval scores go with lower average PHR: r = −0.7887 over 10 models (Table 5, p. 7). [A] The authors propose coding benchmarks as "efficient proxies" for hallucination risk (p. 7).
6. [V] Code-specialised models have higher mean PHR than general models (Table 4, p. 6):

   | Language | Code-specialised | General |
   |---|---|---|
   | Python | 30.22% | 14.64% |
   | Rust | 31.58% | 16.53% |
   | JavaScript | 18.90% | 9.71% |

   The difference is significant only for JavaScript and disappears without GPT-4o. [A] The authors conclude there is likely no meaningful difference (p. 6).
7. [A] Induced hallucinations happen at "nearly double" the natural rate. No figures are given, and there were fewer induced attempts (p. 5).
8. [A] Proposed defence: a date-aware verification list of packages published before each model's training cutoff, plus advice to prefer familiar packages and to name packages explicitly in prompts (p. 8). The defence is not evaluated.

## 8. Limitations stated by the authors
- [A] 11 models may be too few to show a code-specialised vs general difference (p. 6).
- [A] There were fewer induced attempts than natural ones (p. 5).
- [A] The models' training-data composition is unavailable (p. 5).
- [A] The verification list does not catch malicious packages that are already in the historical index (p. 8).

## 9. Limitations we identified
- [I] **Likely false positives from module/package mismatch.** Python imports are extracted by regex with no import-to-package mapping and no standard-library filter (p. 12). Imports like `sklearn`, `cv2` or `yaml` may be counted as hallucinations because their PyPI package names differ. The Rust `name::` pattern can match `std::`, `crate::` or local modules. Compare churilov2026range, where import names of real packages were the largest source of false positives [@churilov2026range, p. 10].
- [I] **Pseudo-replication in the size correlation.** Each model contributes three language points that are treated as independent (finding 4).
- [I] **The size correlation rests on an unverified number.** GPT-4o's size is a 200B estimate from a third-party source (Table 1 footnote, p. 3). GPT-4o is the largest point by far, so this single estimate drives the correlation.
- [I] **Text contradicts the paper's own tables.**
  - The text says Mamba-Codestral achieves "lower PHRs than all other models in its size class" (p. 6), but Table 5 gives Mamba-Codestral 21.03% vs Llama-3.1-8B 15.24% (p. 7).
  - Coding models are said to span "14.95% to 24.40% PHR" with a mean of 26.90% (p. 6), which is impossible.
  - Granite-3.0 is called "15 billion" in the text (p. 6) but 8B in Table 1 (p. 3).
- [I] **Key quantities are missing.** The number of generations is not stated (we infer it, section 4). Temperature, the cutoff sources and the classification of induced prompts are not reported.
- [I] **The claimed defence is not evaluated.** The abstract and introduction say defences were developed and evaluated (p. 1–2), but the defence is only proposed (p. 8).
- [I] **Low-precision cells.** The task set is tiny and unusual (p. 12). Each cell has 455 prompts, so the lowest rates rest on very few events (section 4).
- [I] **Possible undisclosed conflict of interest.** NVIDIA authors evaluate NVIDIA models, and Nemotron ranks best (p. 1, p. 4).
- [I] **Unexplained persona stubs** (p. 12).

## 10. Threats to validity
- Internal (confounds, leakage, selection): [I] The choice of tasks drives the rates, and induced and natural prompts are pooled into one PHR (p. 4–5, p. 12).
- External (generalisability of sample/context):
  - [I] 11 models from 2024 and a small prompt grid.
  - [V] Rust/crates.io is covered alongside JavaScript and Python (p. 4).
  - [I] Within this project, Rust is also covered by [@zheng2026when] and [@dasu2026refusing].
- Construct (do metrics measure the concept?):
  - [V] Strength: the date-aware definition catches packages registered after the model's cutoff (p. 3).
  - [I] Regex extraction without name mapping weakens validity.
  - [I] PHR is per generation, so it is not comparable with per-mention rates.
- Statistical conclusion (power, multiple comparisons, variance):
  - [I] Pseudo-replicated correlations.
  - [I] The size variable includes an estimated value.
  - [I] No confidence intervals, and N = 455 per cell.
- Reproducibility (data/code/setup reported?):
  - [V] The prompt grid is fully listed (p. 12).
  - [I] Decoding settings, generation counts and code are not reported.

## 11. Future research directions
- Stated by authors [A] (p. 6–9):
  - reduce hallucination in smaller models;
  - study how code optimisation relates to security;
  - build defences that work across languages and architectures;
  - test whether non-transformer models (Mamba) are more robust;
  - test more models;
  - optimise for both code quality and hallucination at once (multi-objective).
- Suggested by us [I]:
  - Implement and evaluate the date-aware verification list.
  - Re-run with an import-to-package mapping and a standard-library filter.
  - Analyse at the level of models rather than model-language pairs.
  - Treat GPT-4o's size as unknown in the size analysis.

## 12. Relevance to our research
- Research questions addressed (RQ ids): RQ1, RQ3, RQ4, RQ5.
- How it informs our work [I]:
  - **Laptop-friendly tooling.** It uses garak and 7–8B models (p. 3).
  - **Reusable ideas.**
    - The date-aware definition of hallucination (p. 3).
    - The induced-prompt stress test (p. 3, p. 5).
  - **A candidate defence for our study.** The proposed verification list (p. 8) is untested. We could implement it as a client-side check before install, together with package age, popularity and OSV checks.
  - **Replication details.**
    - Copy: the prompt grid (Tables 6–7, p. 12); 455 prompts per cell (inferred); the registry snapshot of 30 Jan 2025 (p. 4); PHR per prompt (p. 4).
    - Fix: add import-to-package mapping, PEP 503 normalisation and a standard-library filter; report N; use model-level statistics.

## 13. Evidence table (for the evidence matrix)
| RQ | Claim | Page | Label | Strength |
|---|---|---|---|---|
| RQ1 | All 11 LLMs hallucinate packages in JS, Python and Rust; PHR 0.22–46.15% (N inferred 455 prompts per cell; 0.22% = 1 prompt) | 4, 8 | [V] | weak |
| RQ1 | Mean PHR JavaScript 14.73% < Python 23.14% < Rust 24.74% | 8 | [V] | weak |
| RQ1 | Larger models have lower PHR (r = −0.542, p = 0.00114), but significance relies on 33 non-independent model×language points (n = 11 gives p ≈ 0.085) and on an estimated 200B size for GPT-4o | 3, 6 | [V] | weak |
| RQ1 | Higher HumanEval score correlates with lower average PHR (r = −0.7887, 10 models, no p-value) | 7 | [V] | weak |
| RQ1 | Code-specialised models show higher mean PHR, but the difference is not significant except JS and vanishes without GPT-4o | 6 | [V] | weak |
| RQ1 | Induced (leading) prompts yield nearly double the natural hallucination rate (no figures given) | 5 | [A] | weak |
| RQ3 | Date-aware verification list (packages published before model cutoff) proposed as a defence; not evaluated | 8 | [A] | weak |
| RQ4 | Date-aware definition: absent from registry OR first registered after the model's knowledge cutoff (or <90 days before release) | 3 | [V] | moderate |
| RQ4 | Regex import extraction without reported import→distribution mapping or stdlib filter; registry snapshot 30 Jan 2025 | 4, 12 | [V] | moderate |
| RQ4 | PHR = share of prompts with at least one hallucinated package (generation level; not comparable with mention-level rates) | 4 | [V] | moderate |

## 14. Key quotes
> "prompts that resulted in at least one hallucinated package" (p. 4)

> "Notably Mamba-Codestral bucks this trend, achieving lower PHRs than all other models in its size class." (p. 6)

> "JavaScript has the lowest hallucination rate overall (µ = 14.73%)" (p. 8)

## Analyst notes
- Reading coverage: all text pages read (p. 1–12). Pages 13–23 are figure placeholders. Figures 1–5 are only partly extracted.
- Recomputations:
  - All 33 Table 3 values were checked as multiples of 1/455.
  - p-values were recomputed for n = 33 (they match the paper) and n = 11 (≈0.085 raw, ≈0.055 log).
- Uncertainties:
  - The ICML 2024 footer is unexplained.
  - The paper does not state its N or the n used for its correlations; both are our inferences.
  - The PHR definition is split across text columns in fulltext.txt. The first key quote is the part that sits on one line on p. 4.
  - That zheng2026when and dasu2026refusing cover Rust is based on keyword hits (Rust/crates) in their full texts only.
