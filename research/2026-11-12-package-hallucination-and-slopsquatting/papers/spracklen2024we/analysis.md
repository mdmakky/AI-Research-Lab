---
key: spracklen2024we
status: complete
evidence_basis: full-text
design: Large-scale measurement study + mitigation experiment (prompt LLMs, extract package names, check against registry master list)
dataset: 2 own prompt sets (Stack Overflow questions; Llama-2-generated prompts from top-5,000 PyPI/npm package descriptions), Python + JavaScript
sample_size: 16 LLMs, 30 model-language tests, 576,000 code samples, 2.23M package mentions
metrics: Package hallucination rate = hallucinated packages / all recommended packages (mention level); HumanEval pass@1 for code quality
main_finding: 19.7% of 2.23M package mentions hallucinated; commercial 5.2% vs open-source 21.7% (per-test means); 43% of hallucinations repeat 10/10; RAG/self-refinement/fine-tuning reduce rates.
relevance: high
analysed: 2026-11-12
---
<!-- Frontmatter: single-line values; they feed literature-matrix.md via `rlab index`.
     status: draft (in progress) -> ready (analyst self-check passed) -> complete (critical review passed).
     evidence_basis: full-text | abstract-only. abstract-only analyses must not fill methodology detail.
     relevance: high | medium | low. -->

# We Have a Package for You! A Comprehensive Analysis of Package Hallucinations by Code Generating LLMs

- Authors: Spracklen, Joseph; Wijewickrama, Raveen; Sakib, A H M Nazmus; Maiti, Anindya; Viswanath, Bimal; Jadliwala, Murtuza
- Year / venue: Published at USENIX Security 2025. **Source tier 1** (peer-reviewed full conference paper).
  - This analysis uses the arXiv v3 text (arXiv:2406.10279v3, 2 Mar 2025, p. 1).
  - The venue is not printed in the arXiv text. It is supported by [@churilov2026range, p. 1; @churilov2026range, p. 16] and [@okwor2026hallucination, p. 9].
  - Differences between the arXiv text and the proceedings version cannot be ruled out.
- DOI: 10.48550/arxiv.2406.10279 · URL: https://arxiv.org/abs/2406.10279
- Source text: `fulltext.txt` (page refs = PDF page index)

Labels: **[V]** verified in the paper's own data/tables/results · **[A]** author claim · **[I]** our interpretation.
Every [V]/[A] item ends with a page ref `(p. N)`. Write "not reported" when the paper does not say.

## 1. Research objective
[A] The paper sets out to measure how common package hallucinations are in Python and JavaScript code produced by commercial and open-source code LLMs. It also studies how model settings affect them, what the hallucinated names look like, and whether mitigation can reduce them without hurting code quality (p. 2, p. 4). The authors call it "the first systematic study" of how often package hallucinations occur and what they are like (p. 2).

## 2. Research questions / hypotheses
- [A] RQ1: how common are package hallucinations in LLM-generated Python and JavaScript code? (p. 4)
- [A] RQ2: how do model settings (training-data recency, temperature, decoding strategy) affect them? (p. 4)
- [A] RQ3: which model behaviours are observed: repetition within a model, repetition across models, verbosity, and whether models can detect their own hallucinations? (p. 4)
- [A] RQ4: what properties do hallucinated names have: similarity to popular packages, mix-ups between languages, recently deleted packages? (p. 4)
- [A] RQ5: can RAG, self-refinement, decoding strategies or supervised fine-tuning reduce hallucinations? (p. 4–5)
- [A] Explicit hypothesis on deleted packages: the authors expected a sizeable share of hallucinations to come from packages removed from PyPI. The data did not support this (p. 11).
- [A] Adversary model (p. 4):
  - the attacker can query the same LLMs but cannot modify them;
  - the attacker finds hallucinated names by checking them against the registry, then registers them;
  - victims install suggested packages without checking them.

## 3. Methodology
- Research design: [V] A three-phase pipeline: (i) build the prompt datasets, (ii) generate code, (iii) detect hallucinations (p. 5). This is followed by targeted sub-experiments for RQ2–RQ4 and a mitigation experiment for RQ5 (p. 7–13).
- Approach / model / intervention: [V] 16 models (Table 1, p. 6):
  - GPT-4, GPT-4 Turbo, GPT-3.5 Turbo;
  - CodeLlama 7B/13B/34B;
  - DeepSeek Coder 1.3B/6.7B/33B;
  - Magicoder 6.7B, WizardCoder 34B, Mistral 7B, Mixtral 8x7B, OpenChat 7B;
  - WizardCoder-Python 7B and CodeLlama-Python 33B (Python only).

  Models were picked from the top of the EvalPlus leaderboard as of 20 January 2024, plus the GPT models (p. 5). The two Python-only models were not tested on JavaScript, which gives 30 tests (p. 6).
- Package-name extraction: [V] Three heuristics (p. 6–7):
  - **H1:** parse `pip install` / `npm install` commands that the model wrote on its own (they appear in 7% of outputs).
  - **H2:** give the generated code back to the same model and ask which packages are needed to run it.
  - **H3:** give the original prompt back to the same model and ask which packages would solve the task.

  Parsing `import` / `require` statements is explicitly rejected, because module names do not map one-to-one onto package names (p. 6; Appendix G, p. 19).
- Hallucination decision: [V] A name counts as hallucinated if it is absent from a master list of PyPI or npm package names taken on 10 January 2024 (p. 7). [A] The master list may already contain names that attackers have squatted, so the authors present their rates as a lower bound (p. 7).
- Mitigation: [V] Tested on DeepSeek Coder 6.7B and CodeLlama 7B, each method alone and all combined (p. 12–13):
  - **RAG:** 65,000 statements of the form "Package [x] could answer questions about [y]", generated with LlaMA-2 from the top 20,000 PyPI packages and stored in a vector database. The 5 closest statements are added to the prompt.
  - **Self-refinement:** the model is asked whether its packages are valid and regenerates up to 5 times.
  - **Supervised fine-tuning:** 560,000 response pairs that contain only valid packages. The paper calls these "code/package list (Heuristic 1) and prompt/package list (Heuristic 2)" pairs (p. 12–13).
  - [I] By the definitions on p. 6–7, these pairs are actually H2 (code→packages) and H3 (prompt→packages); H1 is install-command parsing. Appendix B uses the same shifted numbering: Figure 11 "Heuristic 1" is code→packages and Figure 12 "Heuristic 2" is prompt→packages (p. 18). So the heuristic numbers in the main text and the appendix do not match.
- Baselines or comparison conditions: [V]
  - Commercial vs open-source models; Python vs JavaScript.
  - "Recent" (2023) vs "all-time" (before 2023) prompt subsets (p. 5, p. 7–8).
  - Temperature sweep, and top-p / top-k / min-p settings (p. 8).
  - Unmitigated baseline vs each mitigation (p. 13).
  - Comparison with Lanyado's blog estimate: GPT-3.5 24.2%, GPT-4 22.2% (p. 7).

## 4. Dataset and sample
- Data source(s):
  - [V] **Stack Overflow set** (p. 5):
    - 240 manually chosen tags, each with more than 5,000 questions and relevant to Python or JavaScript;
    - the 20 most-upvoted questions per tag give 4,800 prompts per language;
    - this was done once for 2023 ("recent") and once for before 2023 ("all-time"), so 9,600 prompts per language.
  - [V] **LLM-generated set** (p. 5):
    - Llama-2 70B turned the descriptions of the 5,000 most-downloaded PyPI and npm packages into one-sentence coding prompts (prompt template in Figure 13, p. 19);
    - about 4,800 prompts per language;
    - also split into recent and all-time halves, with overlap removed.
- Sample size (N) and unit:
  - [V] 19,200 code samples per test, 30 tests, 576,000 code samples in total (p. 6).
  - [V] Two package prompts per code sample, so 1,152,000 package prompts (p. 7).
  - [V] These produced 2.23 million package mentions; 440,445 were hallucinated, covering 205,474 unique hallucinated names (p. 7).
  - [V] The contributions list instead says 19,500 prompts and 586,000 samples (p. 2), which does not match the 576,000 elsewhere (p. 1, p. 6). The paper does not explain the difference.
- Sampling / selection method:
  - [A] The authors say RQ2–RQ4 use only Python, 4 models (GPT-4 Turbo, GPT-3.5, CodeLlama 7B, DeepSeek 6.7B) and "randomly sampled subsets" of the datasets (p. 7).
  - [V] Some RQ2–RQ4 analyses nonetheless use all 16 Python models: the recency comparison ("all 16 Python models", p. 8) and the cross-model analysis (Figure 8 and the family comparison, p. 10).
  - The size of the subsets is not reported, except for the 500 prompts in the persistence test (p. 9).
  - The size of the self-detection sample is not reported (p. 9–10).
- Data availability (public? link?):
  - [A] The authors promise to release code, both prompt datasets, generated code, the RAG database and the fine-tuned models via Zenodo record 14676377 and GitHub Spracks/PackageHallucination (p. 2, p. 14).
  - The release of the prompt datasets, package lists and validation code is confirmed by a later replication [@churilov2026range, p. 15; @churilov2026range, p. 17].
  - [V] The master list of hallucinated names and the detailed per-test results are withheld and shared "by request to verified researchers" (p. 14).

## 5. Experimental setup
- Procedure, settings, hyper-parameters, tools:
  - [V] Open-source models were run with Hugging Face transformers, using GPTQ-quantized weights (p. 6).
  - [V] Hardware: a 40-node Debian cluster with A100/V100 GPUs, and an Ubuntu machine with 3 RTX 6000 GPUs (p. 18).
  - [V] RQ1 settings (Table 6, p. 19):

    | Setting | Code generation | Package prompts |
    |---|---|---|
    | Temperature | 0.7 | 0.01 |
    | Max tokens | 2048 | 64 |
    | Top-p / top-k / repetition penalty | 0.9 / 20 / 1 | 0.9 / 20 / 1 |

  - [V] System messages and prompts are given word for word in Figures 10–13 (p. 18–19).
  - [V] Temperature sweep: up to 2 for GPT models and up to 5 for open models (p. 8).
  - [V] Decoding sweep: top-p 0.4/0.6/0.8, top-k 5/10/15, min-p 0.1/0.2/0.3, plus one combined setting. Top-k and min-p were "only tested for DeepSeek and CodeLlama", because the OpenAI API does not expose them (p. 8).
  - [V] Ground truth: PyPI and npm master lists as of 10 January 2024 (p. 7).
  - [V] Deleted packages were found from Google BigQuery PyPI download counts from 2022 and earlier (p. 11).
  - [V] The cross-language check used libraries.io package lists for 9 registries (p. 11).
  - **Name normalisation** (case folding, PEP 503 equivalence of `-`, `_` and `.`, npm scopes): not reported.
  - **Standard-library exclusion:** not reported.
  - **Deduplication:** rates count mentions, and "unique" means distinct strings (p. 7). The exact rule is not reported.
- Funding and conflicts of interest:
  - [V] Partly funded by the UTSA Faculty Development Leave programme and NSF award 2231002 (p. 14).
  - No conflict-of-interest statement.
  - [V] Findings were disclosed to OpenAI, Meta, DeepSeek and Mistral AI (p. 14).
- Code availability: [A] Promised (p. 14); confirmed as released, see section 4.

## 6. Evaluation metrics
- Metric — what it measures — why chosen:
  - [V] **Package hallucination rate** = number of hallucinated packages / total recommended packages (p. 7). This is counted per mention. It pools names from H1 (install commands inside the code) with names from H2/H3 (the model's answer to a direct "which packages" question).
  - [I] **Pooled vs averaged.** Our recomputation from Tables 7–8 (p. 20) shows that only the 19.7% figure is pooled over all mentions (440,445 / 2.23M, p. 7). The other headline figures are unweighted means of per-test rates:

    | Headline figure | Recomputed unweighted mean |
    |---|---|
    | 5.2% commercial | 5.22% (6 GPT tests) |
    | 21.7% open-source | 21.74% (24 open tests) |
    | 15.8% Python | 15.87% (16 tests) |
    | 21.3% JavaScript | 21.38% (14 tests) |

  - [V] **Persistence:** how many of 10 repeated queries regenerate the same hallucinated name (p. 9).
  - [V] **Cross-model count:** the number of models that produce each unique name (p. 10).
  - [V] **Levenshtein distance** (number of character edits) to the nearest valid package (p. 10–11).
  - [V] **Self-detection:** accuracy, precision and recall (p. 10).
  - [V] **HumanEval pass@1**, used to measure code quality after fine-tuning (p. 13).
- Statistical testing (tests used, significance, effect sizes, confidence intervals):
  - Not reported. There are no confidence intervals, no significance tests and no run-to-run variance. "Significantly reduce" is used only in a descriptive sense (p. 1, p. 13).
  - [V] The Python–JavaScript relationship is called "linear" and "positively correlated" from a scatter plot, with no coefficient given (p. 7; Figure 14, p. 19).

## 7. Key findings
1. [V] **Overall rate.** 440,445 of 2.23 million package mentions (19.7%) were hallucinated, including 205,474 unique names that do not exist (p. 7).
2. [V] **Commercial vs open models.**
   - GPT models average 5.2% and open-source models 21.7% (p. 7); these are per-test means (section 6).
   - The paper calls GPT-4 Turbo's 3.59% the "lowest overall" rate and DeepSeek 1B's 13.63% the best open model (p. 7). Both numbers are the Python totals in Table 7 (p. 20). The JavaScript values are GPT-4 Turbo 4.00% and DeepSeek 1B 27.45% (Table 8, p. 20).
   - [I] So the paper's "overall" labels for single models are Python-only.
   - The highest per-test rates are CodeLlama 7B: 26.12% in Python and 35.71% in JavaScript (Tables 7–8, p. 20).
3. [V] **Language and prompt source.**
   - Python is lower than JavaScript (15.8% vs 21.3%, per-test means) (p. 7).
   - Stack Overflow prompts give higher rates than LLM-generated prompts for almost every model, e.g. CodeLlama 7B in Python: 32.53% vs 21.51% (Table 7, p. 20).
4. [V] **Persistence.** 500 prompts were each re-run 10 times (p. 9):
   - 43% of hallucinated names reappeared in all 10 runs;
   - 39% never reappeared;
   - 58% reappeared more than once.
5. [V] **Model-specific names.** 81% of distinct names were produced by only one model (p. 10).
6. [V] **Not simple typos.** Only 13.4% (10,263 of 76,489) of hallucinated names are within 1–2 character edits of a real package; 48.6% are 6 or more edits away (p. 11).
7. [V] **Other sources.** Deleted PyPI packages are a negligible source: 133 names (0.17%). 8.7% (6,705 of 76,489) of hallucinated Python names are valid npm packages (p. 11).
8. [V] **Effect of settings.**
   - Rates rise with temperature, and sharply above 1. At maximum temperature GPT-4 reached 8.9% and GPT-3.5 reached 31.8% (p. 8).
   - Changing top-p, top-k or min-p raised rates slightly (+1.16% on average) and did not help (p. 8).
   - Prompts about recent topics gave about a 10% higher rate (p. 8–9).
9. [V] **Self-detection.** GPT-4 Turbo, GPT-3.5 and DeepSeek recognised their own hallucinations with more than 75% accuracy. CodeLlama tended to label most packages as valid (Figure 7, Table 2, p. 10).
10. [V] **Mitigation results** (Table 4, p. 13):

    | Method | DeepSeek 6.7B | CodeLlama 7B |
    |---|---|---|
    | Baseline | 16.14% | 26.28% |
    | RAG | 12.24% | 13.40% |
    | Self-refinement | 13.04% | 25.51% |
    | Fine-tuning | 2.66% | 10.27% |
    | All combined | 2.40% | 9.32% |

    Fine-tuning lowered HumanEval pass@1 from 51.4% to 25.3% (DeepSeek) and from 19.6% to 16.4% (CodeLlama) (Table 5, p. 13).

## 8. Limitations stated by the authors
- [A] The master list may already contain squatted hallucinated names, so the rates are a lower bound (p. 7).
- [A] RQ2–RQ4 used Python only, 4 models and sampled subsets. The authors argue this does not harm generalisability (p. 7).
- [A] Newer models may behave differently. Few commercial models were tested because of limited funding (p. 13).
- [A] Self-refinement may wrongly flag valid packages as hallucinations (p. 12).
- [A] Fine-tuning lowers code quality (p. 13).
- [A] Registries do not fully disclose which packages they removed (p. 3).
- [A] For ethical reasons the authors did not register any hallucinated names on PyPI, so real exploitation was not demonstrated (p. 14).

## 9. Limitations we identified
- [I] **The rate mixes three name sources.** H2 and H3 ask the model directly for package lists (p. 6–7). Names in those answers are not necessarily names that would be installed from generated code. So the pooled per-mention rate is not the same thing as "hallucinated dependency in code", and it cannot be compared directly with rates from import/install parsing (churilov2026range) or per-prompt rates (krishna2025importing). Based on the heuristic definitions, p. 6–7.
- [I] **Mixed aggregation.** The headline numbers use different aggregations: 19.7% is pooled over mentions, while 5.2%, 21.7%, 15.8% and 21.3% are unweighted means of per-test rates. The "overall" figures for single models are Python-only (p. 7, p. 20). Later studies that compare against "Spracklen's best model 3.59%" are therefore comparing against a Python-only figure.
- [I] **Normalisation and standard library not reported.** If names were matched without PEP 503 normalisation, variants of real names that differ only in case or separators (e.g. `my_pkg` vs `my-pkg`) would count as hallucinations, which would inflate the rates (p. 7).
- [I] **Possible train/test leakage in fine-tuning.** The model was fine-tuned on 560,000 valid responses produced from the same prompt datasets (p. 12–13). The paper does not describe which prompts were used for evaluation, so the 2.66% result may be partly in-distribution.
- [I] **No uncertainty reported.** Each condition was run once, so small differences cannot be judged. For example, self-refinement on CodeLlama moved from 26.28% to 25.51% (p. 13).
- [I] **Internal inconsistencies.** These are probably typos, but they lower confidence in exact numbers:
  - 586,000 vs 576,000 samples (p. 2 vs p. 6);
  - CodeLlama is marked "✗" (not open source) in Table 1 (p. 6) but treated as open-source in the text;
  - Table 7 contains malformed counts "(2,495/41,7)" and "(2,8523/13,329)" (p. 20);
  - in the GPT-4 JavaScript Stack Overflow cell, 3.86% does not equal 1,672/23,416 = 7.1% (p. 20);
  - the recency effect is stated in both directions (p. 8–9);
  - the heuristic numbering differs between the main text and the appendix (section 3).
- [I] **"10%" is ambiguous.** For the recency effect, the paper does not say whether 10% is a relative change or a difference in percentage points (p. 8).
- [I] **No real-world exploitation data.** The registry snapshot (January 2024) is from before the analysis, and the paper does not track whether hallucinated names were registered later (relevant to RQ2).

## 10. Threats to validity
- Internal (confounds, leakage, selection):
  - [I] In H2/H3 the same model generates the code and then names its packages, so its self-consistency becomes part of the measurement.
  - [I] Fine-tuning data comes from the same prompt pool that is used for evaluation (p. 12–13).
  - [I] The LLM-generated prompts were written by Llama-2 70B, from the same family as the CodeLlama models being tested (p. 5).
- External (generalisability of sample/context):
  - [I] The models are from 2023 to early 2024 (p. 5–6). Agentic and IDE settings are not covered.
  - [V] Only Python and JavaScript are studied (p. 6).
  - [I] Open models were run GPTQ-quantized (p. 6), so results may differ for full-precision models.
- Construct (do metrics measure the concept?):
  - [I] "Absent from the 10 Jan 2024 list" stands in for "hallucinated". The authors acknowledge that squatted names in the list would bias rates downward (p. 7).
  - [I] Normalisation, the standard library, and private or scoped names are not addressed (p. 7).
  - [I] Counting mentions gives more weight to verbose models. Mixing pooled and averaged rates can confuse comparisons (p. 7, p. 20).
- Statistical conclusion (power, multiple comparisons, variance): [I] There are no tests, no confidence intervals and no repeated runs, apart from the 10-run persistence check (p. 9).
- Reproducibility (data/code/setup reported?):
  - [V] Prompts and settings are documented (p. 18–19).
  - [A] Data and code release is promised (p. 14) and confirmed by [@churilov2026range, p. 15].
  - [V] The list of hallucinated names is withheld (p. 14).
  - [I] The commercial-model results cannot be reproduced exactly, because those API endpoints have since changed.
- Funding / conflicts of interest:
  - [V] UTSA FDL and NSF 2231002 (p. 14).
  - No conflict-of-interest statement.
  - [V] Findings were disclosed to the model vendors before publication (p. 14).

## 11. Future research directions
- Stated by authors [A] (p. 13):
  - find the root causes (model architecture, tokenizers, training-data composition);
  - develop mitigations tailored to code (prompt engineering, knowledge graphs, refined loss functions, new fine-tuning methods);
  - add real-time feedback;
  - study persistence at the token level;
  - find fine-tuning that preserves code quality.
- Suggested by us [I]:
  - Re-measure with import/install-based extraction and explicit PEP 503 normalisation, reporting both pooled and per-test rates.
  - Evaluate cheap tool-side defences on held-out prompts.
  - Track whether hallucinated names are registered over time.

## 12. Relevance to our research
- Research questions addressed (RQ ids): RQ1, RQ2, RQ3, RQ4.
- How it informs our work [I]:
  - **Baseline and prompt corpus.** This is the baseline paper, and its prompt corpus is publicly available and reusable (p. 14; [@churilov2026range, p. 15]).
  - **Replication details** (p. 5–7, p. 18–19):
    - prompt sources: Stack Overflow (top 20 questions for each of 240 tags, 2023 vs before 2023) and Llama-2-70B prompts from the top 5,000 package descriptions;
    - system prompts: Figures 10–13;
    - temperatures: 0.7 for code, 0.01 for package prompts;
    - registry snapshot: 10 Jan 2024;
    - metric: hallucinated packages / all recommended packages. Report both pooled and per-test means, because the paper mixes them (section 6);
    - normalisation: not reported, so we must define it ourselves (PEP 503 for PyPI, lowercase for npm, scoped names kept whole).
  - **Cheap defences.** RAG and self-refinement need no training and could run on a laptop (p. 13). Self-refinement only helps models that are good at recognising their own hallucinations (p. 10). Fine-tuning is costly and hurt code quality (p. 13).
  - **Persistence.** About 43% of names repeat every time and 39% never repeat (p. 9). A study therefore needs several samples per prompt to separate persistent names from noise.
  - **Existence checks are not enough.** An attacker can register a hallucinated name before the user checks (p. 12). A lightweight defence needs extra signals such as package age, popularity or provenance.

## 13. Evidence table (for the evidence matrix)
| RQ | Claim | Page | Label | Strength |
|---|---|---|---|---|
| RQ1 | 19.7% of 2.23M package mentions hallucinated across 16 LLMs (Python + JS, 2023–24 models), pooled | 7 | [V] | moderate |
| RQ1 | Commercial (GPT) 5.2% vs open-source 21.7% (unweighted per-test means); GPT-4 Turbo lowest in Python 3.59% (JS 4.00%); paper's "overall" single-model labels are Python-only | 7, 20 | [V] | moderate |
| RQ1 | JavaScript higher than Python (21.3% vs 15.8%, per-test means) | 7, 20 | [V] | moderate |
| RQ1 | Stack Overflow prompts give higher rates than LLM-generated prompts for almost every model | 20 | [V] | moderate |
| RQ1 | Hallucination rate rises with temperature, sharply above 1; top-p/top-k/min-p changes do not help (+1.16%) | 8 | [V] | moderate |
| RQ1 | Prompts on recent topics yield about 10% higher rates (direction stated inconsistently) | 8–9 | [V] | weak |
| RQ2 | 43% of hallucinated names recur in 10/10 re-queries; 58% recur more than once; 39% never recur | 9 | [V] | moderate |
| RQ2 | 81% of distinct hallucinated names come from a single model (low cross-model overlap in 2023–24 cohort) | 10 | [V] | moderate |
| RQ2 | Only 13.4% of hallucinated names are within Levenshtein 1–2 of a real package; 48.6% are at distance 6 or more | 11 | [V] | moderate |
| RQ2 | 8.7% of hallucinated Python names are valid npm packages; deleted PyPI packages explain 0.17% | 11 | [V] | moderate |
| RQ3 | RAG cut rates 16.14→12.24% (DeepSeek) and 26.28→13.40% (CodeLlama); self-refinement 13.04% / 25.51% | 13 | [V] | weak |
| RQ3 | Fine-tuning cut rates to 2.66% / 10.27% but HumanEval pass@1 fell 51.4→25.3% / 19.6→16.4% | 13 | [V] | weak |
| RQ3 | Plain registry existence checks are inadequate because attackers can pre-register names | 12 | [A] | weak |
| RQ4 | Ground truth = PyPI/npm name lists of 10 Jan 2024; names from pip/npm install + two model-queried package lists; no normalisation reported | 6–7 | [V] | moderate |
| RQ4 | Parsing import/require is rejected as invalid because module names do not map to package names | 6, 19 | [A] | moderate |

## 14. Key quotes
> "19.7% of the generated packages are fictitious" (p. 13)

> "43% of hallucinated packages were repeated in all 10 queries, while 39% did not repeat at all across the 10 queries" (p. 9)

> "If a package name is not on the master list, it is considered a hallucination." (p. 7)

## Analyst notes
- Reading coverage: the whole text was read (p. 1–20): abstract, sections 1–7, ethics, open science, appendices A–G and Tables 6–8. The reference list was skimmed.
- Venue and metadata:
  - The project metadata stays on the arXiv record (DOI 10.48550/arxiv.2406.10279), because the USENIX Security 2025 version has no DOI that `rlab add` could resolve.
  - The venue is supported by [@churilov2026range, p. 1; @churilov2026range, p. 16] and [@okwor2026hallucination, p. 9]. This analysis is based on the arXiv v3 text.
- Recomputation: the per-test means in section 6 were recomputed from Tables 7–8 (p. 20): Python 15.87%, JS 21.38%, commercial 5.22%, open-source 21.74%.
- Uncertainties:
  - Figures 2, 3 and 5–9 are plots; only numbers stated in the prose are used.
  - The table inconsistencies in section 9 were not checked against the PDF page images.
