---
key: churilov2026range
status: complete
evidence_basis: full-text
design: Temporal replication of Spracklen et al. with preregistered live-registry revalidation + preregistered natural experiment on registration of hallucinated names
dataset: Spracklen et al. prompt datasets reused unchanged (20,163 Stack Overflow + 19,806 LLM-synthesised prompts = 39,969, Python + JavaScript)
sample_size: 5 frontier LLMs, 199,840 generations, 2,282 unique hallucinated names; natural experiment A=104 vs B4=128 names
metrics: Mention-level and generation-level hallucination rate (Wilson 95% CI); chi-square + Holm, permutation tests; Jaccard overlap; registration share (Fisher, Newcombe CI)
main_finding: 2026 frontier models hallucinate 3.63–5.02% of package mentions; 104 names shared by all five; ~1.1% of hallucinated names registered within six months.
relevance: high
analysed: 2026-11-12
---
<!-- Frontmatter: single-line values; they feed literature-matrix.md via `rlab index`.
     status: draft (in progress) -> ready (analyst self-check passed) -> complete (critical review passed).
     evidence_basis: full-text | abstract-only. abstract-only analyses must not fill methodology detail.
     relevance: high | medium | low. -->

# The Range Shrinks, the Threat Remains: Re-evaluating LLM Package Hallucinations on the 2026 Frontier-Model Cohort

- Authors: Churilov, Aleksandr
- Year / venue: 2026, arXiv preprint (not peer-reviewed). **Source tier 3.**
  - The analysed text is "Version 4 (November 2026)". It replaces all numbers in versions 1–3 and in a SCORED '26 workshop version (p. 1).
  - Single author, "Independent Researcher" (p. 1).
- DOI: 10.48550/arxiv.2605.17062 · URL: https://arxiv.org/abs/2605.17062
- Source text: `fulltext.txt` (page refs = PDF page index)

Labels: **[V]** verified in the paper's own data/tables/results · **[A]** author claim · **[I]** our interpretation.
Every [V]/[A] item ends with a page ref `(p. N)`. Write "not reported" when the paper does not say.

## 1. Research objective
[A] To find out whether package hallucination has changed in the 2026 frontier models compared with Spracklen et al.'s 2024 baseline. Every name is re-checked against the live PyPI and npm registries. The paper also tests whether publishing hallucinated names makes them get registered faster (p. 1–2).

## 2. Research questions / hypotheses
- [A] Measurement question: has package hallucination changed for the frontier models of 2025–26? It is broken down into (p. 1–2):
  - per-model rates, counted per mention and per generation;
  - the "universal" set of names that every model hallucinates, and whether outsiders could register them;
  - whether hallucinated names actually get registered.
- [A] Preregistered hypothesis: if publishing names attracts registrations, published names (group A) should be registered more often than comparable unpublished names (group B4). The main test is Fisher's exact test within groups matched on name frequency and name length (p. 11–12).
- [A] Threat model: taken over from Spracklen, a 6-stage attack chain. The estimated API cost of finding hallucinated names is about $1,160 (p. 3).

## 3. Methodology
- Research design: [V] Three parts:
  - a temporal replication: the same prompts run on newer models (p. 2, p. 4);
  - a re-check of all names against the live registries, following a plan registered in advance on 7 Nov 2026, with a log of 20 deviations from that plan (p. 6);
  - a natural experiment that uses an accidental public exposure of the universal list (p. 11).
- Approach / model / intervention: [V] Five models (Table 1, p. 4):
  - Claude Sonnet 4.6 (`claude-sonnet-4-6`);
  - Claude Haiku 4.5 (`claude-haiku-4-5-20251001`);
  - GPT-5.4-mini (`gpt-5.4-mini-2026-03-17`, reasoning effort set to minimal);
  - Gemini 2.5 Pro (`gemini-2.5-pro`);
  - DeepSeek V3.2 (alias `deepseek-chat`).

  Extended thinking was not used for the Claude models (p. 4–5).
- Package extraction: [V] (p. 5)
  - `pip install` anywhere in the response, first argument only.
  - `npm install` only inside code blocks.
  - Import statements: Python parsed with `ast` (sub-imports reduced to the top-level module); JavaScript parsed with tree-sitter.
  - Scoped npm names (`@scope/name`) kept whole.
  - Not extracted: requirements files, uv, poetry, yarn, pnpm.
- Registry check: [V]
  - Two methods per registry (p. 5):
    - PyPI: the JSON API and the Simple API (PEP 691);
    - npm: the registry document and deps.dev.
  - Status 200 = EXISTS, 404 = ABSENT, anything else = UNKNOWN.
  - A name is ABSENT only if both methods return ABSENT in two rounds at least 12 hours apart (round 1: 7 Nov 2026, 11:53–13:14 UTC; round 2: 8 Nov 2026, 10:16–11:22 UTC).
  - At most 1 request per second per host; 14,821 requests, with no errors.
  - Hallucination is judged as of the moment of generation. The package's creation time (npm `time.created`; on PyPI the earliest upload) is compared with the generation timestamp or the batch window (p. 5).
  - OSV is queried for malicious-package records (p. 5).
- Exclusions: [V] four classes of names are removed (p. 5–6):
  1. extraction noise;
  2. standard-library modules: the union of `sys.stdlib_module_names` for Python 3.10–3.13 plus the built-in modules of Node 18/20/22;
  3. names that break PEP 508 or npm naming rules;
  4. Python import names that pipreqs maps to a package that exists. A name that also appears as an install target stays a candidate.
- Baselines or comparison conditions:
  - [V] Spracklen's 2024 figures: 3.59% for the best model, 5.2% commercial average, 21.7% open-source average (p. 3, p. 6).
  - [I] These baselines are not like-for-like:
    - Spracklen's 3.59% (GPT-4 Turbo) is a Python-only per-test rate [@spracklen2024we, p. 20], but Churilov compares it with pooled Python+JavaScript rates such as Haiku 4.5's 3.63%. Churilov's own Python-only rate for Haiku is 4.38% (Table 2, p. 7).
    - Spracklen's 5.2% and 21.7% are unweighted means of per-test rates, not pooled rates [@spracklen2024we, p. 20].
  - [V] Other comparisons: pairwise between the five models (p. 8), and against earlier versions of this paper (p. 10–11).

## 4. Dataset and sample
- Data source(s): [V] Spracklen's released prompt datasets, used unchanged (p. 4):
  - 20,163 Stack Overflow prompts (SO_AT, SO_LY);
  - 19,806 LLM-written prompts (LLM_AT, LLM_LY);
  - 39,969 prompts in total, split evenly between Python and JavaScript;
  - no new 2026 prompts were added.

  [I] The released corpus size of 39,969 does not match the size Spracklen states. Spracklen gives 19,200 samples per model-language test, i.e. 2×19,200 = 38,400 per model across both languages [@spracklen2024we, p. 6], and elsewhere 19,500 prompts [@spracklen2024we, p. 2].
- Sample size (N) and unit:
  - [V] 39,969 generations per model (39,964 for Sonnet 4.6), 199,840 in total (p. 4).
  - [V] Unique hallucinated names: 1,746 on PyPI and 536 on npm (Table 7, p. 11).
  - [V] Registration groups: A = 104 names, B = 2,178 names (p. 11–12).
- Sampling / selection method: [V] The models were chosen to represent the main commercial and open-weight providers at the frontier tier (p. 4). [A] The author notes that the results depend on this selection (p. 13).
- Data availability (public? link?): [V]
  - Code: GitHub `churik5/slopsquatting-replication-2026` (MIT licence).
  - Re-check code, preregistration and aggregate results: `churik5/slopsquatting-revalidation-2026`.
  - Raw responses: available to verified researchers on request.
  - The universal list is not printed (p. 15).

## 5. Experimental setup
- Procedure, settings, hyper-parameters, tools:
  - [V] Generations collected 22–28 April 2026 (p. 4, p. 14).
  - [V] Provider defaults were used "unless noted". The temperature and top-p values are recorded but not printed (p. 4).
  - [V] Refusal rates range from 1.27% to 31.51% (Table 1, p. 4; p. 6).
  - [V] Estimated cost: $1,160.29 (Table A.1, p. 17).
  - [V] The edit-distance analysis uses names "after normalization", compared against the registries' package lists of 23 July 2026. The normalisation rule is not specified (p. 9).
  - [V] PyPI checks rely on PEP 508 (name rules) and PEP 691 (Simple API). PEP 503 normalisation is not explicitly named (p. 5).
- Funding and conflicts of interest:
  - [V] The author paid for the study personally, apart from a one-time Google Cloud free-credit grant used for Gemini 2.5 Pro (p. 15).
  - [A] "The author has no conflicts of interest with the studied providers" (p. 15).
  - [V] The author used Anthropic's Claude to write analysis code and to draft and edit the text (p. 15).
- Code availability: [V] Available (p. 15). [A] The repository history was rewritten on 7 Nov 2026, so commit references in earlier versions no longer resolve (p. 15).

## 6. Evaluation metrics
- Metric — what it measures — why chosen:
  - [V] **Mention-level rate:** the share of extracted package references that are hallucinated. Chosen to match Spracklen's unit (p. 6). [I] It is pooled over both languages, whereas Spracklen's per-model "overall" figures are per-language rates [@spracklen2024we, p. 20].
  - [V] **Generation-level rate:** the share of generations with at least one hallucinated reference. This is the rate named in the preregistration (p. 6).
  - [V] **Jaccard overlap** between models' sets of hallucinated names (p. 6).
  - [V] **Registration share** (p. 11).
- Statistical testing (tests used, significance, effect sizes, confidence intervals): [V]
  - Wilson confidence intervals for rates.
  - Pearson χ² tests with Holm–Bonferroni correction over the 10 model pairs.
  - Permutation tests (10,000 resamples, seed 42) (p. 6).
  - Newcombe intervals for differences (p. 7, p. 12).
  - Fisher's exact test and Cochran–Mantel–Haenszel test.
  - Minimum detectable effect: 10.5% at a 1% baseline (p. 12).

## 7. Key findings
1. [V] Per-model rates range from 3.63% (Haiku 4.5) to 5.02% (GPT-5.4-mini) of mentions, and from 2.15% (GPT-5.4-mini) to 3.39% (Gemini 2.5 Pro) of generations (p. 6; Table 2, p. 7).
2. [V] Pairwise differences (p. 6; Table 4, p. 8):
   - 7 of 10 model pairs differ significantly at the mention level, and 8 of 10 at the generation level.
   - Gemini 2.5 Pro, DeepSeek V3.2 and GPT-5.4-mini do not differ significantly from each other at the mention level only. At the generation level all three of their pairs differ significantly.
3. [V] Python rates are higher than JavaScript rates for every model, by 2.34 to 3.47 percentage points per mention (Table 2, p. 7). [A] The author calls this the reverse of Spracklen's 2024 result (p. 7, p. 13).
4. [V] LLM-written prompts give higher rates than Stack Overflow prompts for every model. Pooled: 4.79% (LLM_AT) and 5.44% (LLM_LY) vs 2.28% (SO_AT) and 3.10% (SO_LY) (Table 3, p. 7). [I] This reverses Spracklen's ordering on the same corpus, where Stack Overflow prompts gave higher rates than LLM-generated prompts for almost every model [@spracklen2024we, p. 20]. Recorded as a contradiction.
5. [V] Overlap between models: mean Jaccard 0.219 (range 0.173–0.342). DeepSeek and GPT-5.4-mini overlap most, at 0.342 (p. 8).
6. [V] The universal set (Table 5, p. 9):
   - 104 names (88 PyPI, 16 npm) are hallucinated by all five models, giving 2,699 mentions;
   - 54 of them are one character edit away from a registered package;
   - 4 are in npm scopes owned by an organisation, so outsiders cannot register them.
7. [V] Haiku 4.5 hallucinates less than Sonnet 4.6 (3.63% vs 4.09%, Holm-corrected p = 0.012) (p. 9). [A] The author has withdrawn an earlier explanation and offers no mechanism (p. 9).
8. [V] Re-checking against the live registries lowered every model's rate by about a fifth. The biggest correction was import names of real packages, 144–207 mentions per model. The universal set shrank from 127 to 104 names (p. 10–11, Tables 6–7).
9. [V] Registration (p. 12):
   - 25 of 2,282 hallucinated names (1.1%) were registered within about six months;
   - publishing names had no detectable effect: 0 of 87 published names vs 2 of 101 comparable unpublished names were registered, a difference of −2.0 percentage points (95% CI −6.9 to +2.5), p = 0.50.
10. [V] What the 24 registrations in group B were (p. 12):
    - 22 published packages, whose content was not inspected;
    - 1 npm security-holding placeholder carrying a malicious-package record published after the runs, i.e. a name registered with malware and later taken over by npm;
    - 1 name-reservation placeholder.
11. [V] At least 23 names the models suggest had previously hosted malware that the registries later removed (p. 12).

## 8. Limitations stated by the authors
- [A] **Scope:** smaller, fine-tuned and quantized local models, and agentic setups, are not studied (p. 14).
- [A] **Timing:** the results describe one point in time (p. 14).
- [A] **Leakage:** the Spracklen prompts may be in 2026 training data, and no new held-out prompts were used (p. 14).
- [A] **GPT-5.4-mini:** run at minimal reasoning effort, with a 31.51% refusal rate (p. 14).
- [A] **DeepSeek:** the alias returned `deepseek-v4-flash` in its metadata, so the model behind it may have changed (p. 14).
- [A] **Extraction:** some install forms are missed, so rates may be underestimated. The pipreqs mapping covers about 1,157 import names (p. 14).
- [A] **Creation dates:** PyPI creation dates can be late, and removed packages have no date (p. 14).
- [A] **Registrability:** whether names can be registered was not re-estimated (p. 14).
- [A] **Natural experiment:** small, can detect only large effects, and cannot tell defensive from malicious registrations without looking at content (p. 14).
- [A] **Preregistration:** the timestamps are self-attested (p. 6, p. 14).

## 9. Limitations we identified
- [I] **Extraction differs from Spracklen.** The paper says "We follow Spracklen's extraction approach" (p. 5), but it parses import statements. Spracklen explicitly rejects import parsing and instead asks the model for package lists [@spracklen2024we, p. 6–7].
- [I] **Unit mismatch with the 2024 baseline.** The statement "practically level with the best 2024 model" (p. 6) compares Haiku 4.5's pooled Python+JavaScript rate (3.63%) with Spracklen's Python-only 3.59% for GPT-4 Turbo [@spracklen2024we, p. 20]. Churilov's own Python-only rate for Haiku is 4.38% (Table 2, p. 7), which is above 3.59%. Spracklen's 5.2% and 21.7% are unweighted means of per-test rates [@spracklen2024we, p. 20]. So the headline "2026 frontier at 2024's commercial level" (p. 1) mixes extraction methods, units and ways of averaging.
- [I] **Two attributions to Spracklen were not found.** The paper says Spracklen explained higher JavaScript rates by npm "fragmentation" (p. 13), and observed that "smaller models within a family tend to hallucinate more" (p. 9). We searched the spracklen2024we text and found neither statement.
- [I] **Python rates may still be inflated.** pipreqs covers only about 1,157 names (p. 14). Python modules whose import name differs from the package name and are not in that list would still count as hallucinations, which could partly explain the Python > JavaScript result. The author argues against this on p. 13.
- [I] **Long gap between generation and checking.** About 6 months passed between generation (April) and the registry checks (November). Packages deleted in between could be misclassified as hallucinations.
- [I] **Temperatures not printed** (p. 4).
- [I] **Reliability record.** This is version 4 of a fast-revised, single-author paper, and several earlier numbers could not be reproduced (p. 10–11, p. 17). The text was drafted with AI help (p. 15).
- [I] **Refusals change the rankings.** Model rankings at the generation level depend on how refusals are handled (p. 6).

## 10. Threats to validity
- Internal (confounds, leakage, selection):
  - [A] The prompts may be in the models' training data (p. 14).
  - [I] Refusal rates differ between models, which distorts generation-level comparisons (p. 6).
  - [I] Model aliases and settings may have drifted during the run (p. 14).
- External (generalisability of sample/context):
  - [A] Results apply only to frontier API models (p. 13–14).
  - [I] No agentic setting was tested.
- Construct (do metrics measure the concept?):
  - [I] Import-based extraction counts names that may never be installed (p. 5–6).
  - [V] The dated check with two methods per registry is more robust than the static lists used before (p. 5).
  - [I] Pooled rates are not comparable with Spracklen's per-language rates (section 9).
- Statistical conclusion (power, multiple comparisons, variance):
  - [V] Holm correction is applied, and permutation tests confirm the results (p. 6, p. 8).
  - [V] The natural experiment is underpowered (minimum detectable effect 10.5%) (p. 12).
  - [I] Only one sample was drawn per prompt.
- Reproducibility (data/code/setup reported?):
  - [V] Code, preregistration and aggregate results are public; raw responses are available on request (p. 15).
  - [A] The repository history was rewritten, and an earlier statement about a Zenodo deposit was incorrect (p. 15).
- Funding / conflicts of interest:
  - [V] Self-funded, plus a Google Cloud credit grant (p. 15).
  - [A] The author reports no conflicts of interest with the studied providers (p. 15).
  - [I] The free Google credits went specifically to running one of the evaluated models (Gemini) (p. 15).
  - [V] Claude, one of the evaluated model families, was used to write the analysis code and draft the text (p. 15).

## 11. Future research directions
- Stated by authors [A]:
  - report the overlap across a whole cohort of models as standard (p. 10);
  - monitor registrations of hallucinated names (p. 15);
  - test smaller, quantized and next-tier models (p. 13–14);
  - use held-out prompts and vary the reasoning effort (p. 14);
  - test agentic setups (p. 14).
- Suggested by us [I]:
  - Re-run on open-weight models small enough for a laptop, with the same live-check protocol.
  - Compare import-based and model-queried extraction on the same generations, reporting per-language and pooled rates.
  - Measure persistence with more than one sample per prompt.

## 12. Relevance to our research
- Research questions addressed (RQ ids): RQ1, RQ2, RQ4, RQ5.
- How it informs our work [I]:
  - **Most complete replicable validation protocol in our set** (p. 5–6). It runs on a laptop:
    - two lookup methods per registry, two rounds at least 12 hours apart, at most 1 request per second per host;
    - an append-only log of every response;
    - a check of package creation time against generation time;
    - OSV lookups for known malicious packages;
    - removal of standard-library modules, names that break naming rules, and import names mapped by pipreqs;
    - Wilson confidence intervals and Holm-corrected tests.
  - **The gap a laptop study can fill.** Local quantized models and agentic setups are explicitly out of scope (p. 14).
  - **Comparing with 2024.** A small study should report per-language and pooled rates separately, to avoid the unit mismatch noted in section 9.
  - **Prompt source matters.** The prompt dataset shifts the results, and its effect has reversed since Spracklen's study (finding 4). Stratify results by prompt source.
  - **Existence checks are not enough.** About 1% of hallucinated names were registered, and at least 23 suggested names have a malware history (p. 12). This supports defences that check package age, OSV records and placeholder status rather than only whether the package exists.

## 13. Evidence table (for the evidence matrix)
| RQ | Claim | Page | Label | Strength |
|---|---|---|---|---|
| RQ1 | Five 2026 frontier models hallucinate 3.63–5.02% of package mentions (pooled Py+JS; 2.15–3.39% of generations) | 6–7 | [V] | moderate |
| RQ1 | Python > JavaScript for every frontier model (+2.34 to +3.47 pp per mention) | 7 | [V] | moderate |
| RQ1 | LLM-synthesised prompts give higher rates than Stack Overflow prompts (pooled 4.79/5.44% vs 2.28/3.10%); reverses Spracklen's ordering on the same corpus | 7 | [V] | moderate |
| RQ1 | Refusal rates 1.27–31.51% change model rankings between mention and generation levels | 4, 6 | [V] | moderate |
| RQ1 | "Level with 2024's best model" compares pooled 3.63% with Spracklen's Python-only 3.59%; Churilov's own Python-only Haiku rate is 4.38% | 6–7 | [I] | — |
| RQ2 | 104 names hallucinated by all five models (88 PyPI, 16 npm), 54 one edit from a registered package | 9 | [V] | moderate |
| RQ2 | Mean pairwise Jaccard overlap of hallucinated-name sets 0.219 (0.173–0.342) | 8 | [V] | moderate |
| RQ2 | 25 of 2,282 hallucinated names (1.1%) registered within ~6 months; one registered with malware | 12 | [V] | weak |
| RQ2 | Publishing names had no detectable effect on registration (0/87 vs 2/101; underpowered, MDE ~10.5%) | 12 | [V] | weak |
| RQ2 | At least 23 suggested names previously hosted malware later removed by registries | 12 | [V] | moderate |
| RQ3 | Registry-as-oracle defences face oracle poisoning, whose precondition (pre-registration) occurs rarely (~1%) | 12 | [A] | weak |
| RQ4 | Live two-method, two-round registry validation with time-of-generation rule; static lists miscounted and inflated rates by ~1/5 | 5, 10 | [V] | moderate |
| RQ4 | Import names of real packages were the largest false-positive class (144–207 mentions per model) | 10 | [V] | moderate |
| RQ4 | Claims to follow Spracklen's extraction but parses imports, which Spracklen rejects, so the 2024/2026 comparison is not like-for-like | 5 | [I] | — |
| RQ5 | Local quantized models and agentic configurations explicitly not studied | 14 | [A] | moderate |

## 14. Key quotes
> "A name is finally ABSENT only if both methods return ABSENT in two rounds at least 12 hours apart" (p. 5)

> "A single-model measurement therefore understates the slopsquatting attack surface" (p. 10)

> "We follow Spracklen’s extraction approach and inherit its known false-positive behavior" (p. 5)

## Analyst notes
- Reading coverage: the whole text was read (p. 1–18), including Appendices A–B. Figures 2–3 are plots; only numbers stated in the prose and tables are used.
- Contradiction to record in the evidence matrix:
  - prompt-source ordering: Churilov finds LLM-written > Stack Overflow (p. 7), Spracklen finds Stack Overflow > LLM-written [@spracklen2024we, p. 20], on the same corpus;
  - language ordering: Churilov finds Python > JavaScript (p. 7), Spracklen finds JavaScript > Python [@spracklen2024we, p. 7].
- Uncertainties:
  - The status of the SCORED '26 workshop version is mentioned only on p. 1.
  - The PDF identity is "probable"; the title and author on p. 1 match.
  - The two attributions to Spracklen were checked by text search only.
