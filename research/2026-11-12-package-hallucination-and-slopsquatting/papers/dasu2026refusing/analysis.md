---
key: dasu2026refusing
status: complete
evidence_basis: full-text
design: Benchmark + empirical evaluation (hand-built unsatisfiable requests with matched solvable controls; LLM judge validated against human labels)
dataset: 270 adversarial prompts (24 subcategories, 6 languages, 10 framing templates) + 91 solvable controls; 17 open-weight models 6.7B-671B
sample_size: 6,137 judged responses (17 models x 361 prompts, one sample each); 138-item human gold set
metrics: Hallucination rate, refusal rate, over-refusal on controls; 95% bootstrap CIs; Spearman rho vs log parameters; Cohen's kappa for judge agreement
main_finding: Open models fabricate code for 54% of unsatisfiable requests; scale curbs theoretical impossibilities but not fake packages—largest models still fabricate 85% of nonexistent npm/crates.
relevance: high
analysed: 2026-11-12
---
<!-- Frontmatter: single-line values; they feed literature-matrix.md via `rlab index`.
     status: draft (in progress) -> ready (analyst self-check passed) -> complete (critical review passed).
     evidence_basis: full-text | abstract-only. abstract-only analyses must not fill methodology detail.
     relevance: high | medium | low. -->

# Refusing the Impossible: A Taxonomy and Benchmark for Code Hallucination in Large Language Models

- Authors: Dasu, Vishnu Asutosh; Kundu, Ashish; Tan, Gang
- Year / venue: 2026, arXiv (preprint, not peer-reviewed)
- DOI: 10.48550/arxiv.2609.03267 · URL: https://arxiv.org/abs/2609.03267
- Source text: `fulltext.txt` (page refs = PDF page index); arXiv 2609.03267v2, 31 Oct 2026.

Labels: **[V]** verified in the paper's own data/tables/results · **[A]** author claim · **[I]** our interpretation.
Every [V]/[A] item ends with a page ref `(p. N)`. Write "not reported" when the paper does not say.

## 1. Research objective
[A] Test whether code LLMs recognise programming requests that cannot be satisfied (nonexistent packages, impossible algorithms) and refuse; define code hallucination as ungrounded generation, distinct from code errors; provide a taxonomy and benchmark (p. 1, p. 2).

## 2. Research questions / hypotheses
- [A] RQ1: How often do models comply with unsatisfiable requests rather than refuse, and is refusal a sign of over-caution? (p. 5)
- [A] RQ2: Does model scale reduce hallucination, equally for every kind? (p. 5)
- [A] RQ3: How do models hallucinate, and what failure modes do reasoning models add? (p. 5)
- [A] RQ4: What kinds of prompts exacerbate hallucination? (p. 5)

## 3. Methodology
- Research design: [V] Benchmark study with matched controls: unsatisfiable requests where any solution attempt is ungrounded by construction, plus minimal-edit solvable controls to detect over-refusal (p. 3, p. 4).
- Approach / model / intervention: [V] Taxonomy (Fig. 2): outcome CORRECT / HALLUCINATION / REFUSAL (ERROR on solvable tasks); D1 groundedness — absolute (A1–A4) vs relative (R1 nonexistent API or package, R2 header/flag, R3 protocol, R4 language feature, R5 fabricated version); D2 manifestation — syntactic / semantic / factual; D3 behaviour — B1 confident fabrication, B2 hedged compliance, B3 task substitution, B4 degenerate output (p. 3). Judge: Claude Opus 4.6 inside the Claude Code harness with a fixed rubric (six decision rules), shown prompt, response and ground-truth memo; responses that exhausted the token budget without an answer are labelled B4 by a deterministic rule (33 of 6,137) (p. 4). Hedged code counts as hallucination; fixing a typo and using the real package counts as correct (p. 4). An install/dependency line for a nonexistent name counts as using it (p. 4).
- Baselines or comparison conditions: [V] 91 solvable controls (p. 4); comparison across 17 models and size groups (p. 5, p. 6).

## 4. Dataset and sample
- Data source(s): [V] 270 hand-written adversarial templates, each with a memo naming the planted entity and why the request is unsatisfiable (e.g. crate `serde_ultra`) (p. 3, p. 4). Three families: theoretical impossibility (8 subcategories), plausible nonexistent entity (12, incl. nonexistent PyPI, npm, crates.io, Go, Java and C-header entities), typos/transplants/open tasks (4) (p. 4). Six languages: Python, C++, Rust, Go, Java, JavaScript (p. 4). Ten framing templates assigned by a hash of the seed, one frame per prompt (p. 4); Table VIII (p. 9).
- Sample size (N) and unit: [V] 17 models x 361 prompts = 6,137 judged responses (p. 1, p. 2); 1,547 control responses (p. 2). Package subsets are small: 12 nonexistent-npm and 10 nonexistent-crate prompts (p. 9); subcategories have 6–20 prompts per model (p. 10).
- Sampling / selection method: [V] Prompts hand-crafted; models chosen as open-weight, version-exact, with known parameter counts, covering small/older models still in production (p. 5).
- Data availability (public? link?): [A] Code artefacts and prompt suite open-sourced at a GitHub repository (rendered in the text layer as "https://github.com/vdasu/code hallucination") (p. 2).

## 5. Experimental setup
- Procedure, settings, hyper-parameters, tools: [V] Temperature 0, one completion per prompt, 16,384-token output budget; exception MiniMax-M2.7 at temperature 1.0, top-p 0.95 because it never left its reasoning phase under greedy decoding (p. 5). Models (Table III): DeepSeek-Coder 6.7B, CodeLlama 7B, CodeGemma 7B, Qwen2.5-Coder 7B, DeepCoder 14B, gpt-oss 20B, Devstral-Small-2 24B, Granite 4.1 30B, Qwen3-Coder 30B, Gemma 4 31B, Qwen2.5-Coder 32B, DeepSeek-R1-Distill 32B, Qwen3-Coder-Next 80B, gpt-oss 120B, MiniMax-M2.7 230B, MiniMax-M3 428B, DeepSeek-V3.2 671B (p. 5). The twelve models up to 32B ran with 4-bit weight quantization, the five larger at full precision (p. 10). Re-run of 28 exhausted MiniMax-M3 prompts with a 131,072-token budget (p. 8). Inference engine, quantization method and hardware are not reported. How and when nonexistence of planted names was checked against registries is not described beyond the memo and the statement that relative prompts depend on registry state at generation time (p. 10).
- Code availability: [A] Yes (p. 2).

## 6. Evaluation metrics
- [V] Hallucination rate (HR), refusal rate (RR), rate of correct non-refusals on adversarial prompts; over-refusal rate and HR on controls (p. 5).
- [V] 95% bootstrap intervals resampling prompts; Spearman correlation between log total parameters and HR (p. 5); Pearson correlation of adversarial vs control fabrication (p. 5); variance explained by prompt vs model identity (p. 8, p. 9).
- Judge validity: [V] on a 138-item gold set, outcome agreement 94%, Cohen's kappa 0.91; hallucination recall 0.93, precision 0.89; behaviour-label agreement 67%; manifestation 29/30, kappa 0.95; human labels replace judge labels for these 138 (p. 5).
- [V] No correction for multiple comparisons is reported in the metrics or results (p. 5, p. 6).

## 7. Key findings
1. [V] Across 17 models: 54% of responses to unsatisfiable prompts are ungrounded code, 31% refusals, 15% grounded non-refusals; only 1 of 1,547 control responses is a wrongful refusal; 5% of control responses hallucinate (p. 5).
2. [V] HR ranges from 0.23 (MiniMax-M3 428B) to 0.90 (CodeLlama 7B); small 4-bit models: CodeGemma 7B 0.84, Qwen2.5-Coder 7B 0.69, DeepSeek-Coder 6.7B 0.66, Table IV (p. 6).
3. [V] Scale helps on theoretical impossibilities (HR 0.84 / 0.49 / 0.32 for <=7B / 14–32B / >=80B; Spearman -0.71, p = 0.002) but much less on plausible nonexistent entities (0.88 / 0.71 / 0.61; -0.47, p = 0.059) and least on nonexistent npm packages + Rust crates (1.00 / 0.90 / 0.85; -0.43, p = 0.083); the size groups contain 4 small, 8 mid and 5 large models, Table V (p. 6). [I] The npm+crates subset has 22 prompts per model, so 1.00, 0.90 and 0.85 rest on 88, 176 and 110 responses respectively.
4. [V] DeepSeek-V3.2 (671B) and gpt-oss 120B fabricate on 100% of nonexistent npm/crate prompts; gpt-oss 20B and 120B have the same overall HR (0.46) (p. 6).
5. [V] By ecosystem (pooled): nonexistent npm packages fabricated on 94% of prompts, Rust crates 87%, C headers 76%, Go modules 63%, PyPI modules 63%, Java APIs 33%; largest models 87%, 84%, 68%, 50%, 50%, 15% (p. 8).
6. [V] A misspelled real package name is fabricated on only 14% of prompts, versus 94% for a correctly spelled fictional one (p. 8, p. 9); responses that fix the typo and use the real package count as correct (p. 4).
7. [V] Behaviour: 66% confident fabrication (B1), 19% hedged (B2), 13% task substitution (B3), 1.5% degenerate (B4) (p. 6, p. 7). Manifestation: 47% semantic (would fail at install/import/compile), 43% factual (runs; only claims are false); 18% of plausible-entity hallucinations are factual (p. 7); Table VII (p. 8). [A] "no registry check will notice" them (p. 7).
8. [V] Framing matters: "internal docs" frame HR 0.64 vs "learner" 0.43; the docs vs question-frames gap is 21 points (95% CI 8–34) (p. 8); Table VIII (p. 9).
9. [V] Prompt identity explains 34% of outcome variance vs 15% for model identity; 33 of 270 prompts fool at least 16 of 17 models and 11 fool all 17 (p. 8, p. 9).
10. [V] Collision example: MiniMax-M2.7 recommended `pip install pywfm`, a name that exists on PyPI as an unrelated 2015 package (p. 9).
11. [V] MiniMax-M3 exhausted the 16,384-token budget on 28 of 361 prompts; with 131,072 tokens 23 finished and 5 still produced no answer (p. 8).
12. [A] Recommended mitigations: ground generation in package registries at generation time; gate output on the model's own stated caveats; ask the feasibility question before the implementation question (p. 9, p. 11).

## 8. Limitations stated by the authors
- [A] Template-rendered prompts may differ from what developers type; absolute rates are benchmark-specific (p. 10).
- [A] Single sample per prompt; MiniMax-M2.7 run at temperature 1.0 (p. 10).
- [A] Relative prompts depend on the state of package registries at generation time; MiniMax-M2.7 has since been withdrawn (p. 10).
- [A] The LLM judge is the main internal threat; gold set labelled by one author; the judge sees the ground-truth memo, which could bias it (p. 10).
- [A] Models <=32B ran 4-bit, larger ones full precision: size is confounded with precision (p. 10).
- [A] Framing analysis is observational (one frame per prompt); subcategory counts are 6–20 per model, so the scale trend on plausible entities is treated as weak (p. 10).
- [A] Open-weight models only; may not generalise to closed frontier models (p. 10).

## 9. Limitations we identified
- [I] Construct differs from the slopsquatting threat model: the user supplies the fictional package name, so the benchmark measures *acceptance* of a planted name, not spontaneous invention of names. Rates such as 94% for npm (p. 8) are not comparable with spontaneous package hallucination rates from prompt-sampling studies.
- [I] Package-specific estimates rest on 22 prompts (12 npm + 10 crates, p. 9); per-model package rates have wide uncertainty (not reported per subcategory).
- [I] Publishing the planted fictional names creates a risk that someone registers them, silently changing ground truth for future replications (registry dependence acknowledged, p. 10).
- [I] Quantization method/engine and hardware not reported, which limits exact replication of the 4-bit small-model results.
- [I] Behaviour-level labels have only 67% judge-human agreement (p. 5); B1/B2 shares are indicative.
- [I] Very recent preprint (v2, 31 Oct 2026), not peer-reviewed.

## 10. Threats to validity
- Internal: judge sees the memo; gold set from one author (p. 10); deterministic B4 rule affects 33 responses (p. 4) — [I].
- External: open-weight models only; template prompts (p. 10) — [I].
- Construct: "hallucination" includes hedged compliance (p. 4); planted-name acceptance vs spontaneous invention — [I].
- Statistical conclusion: bootstrap CIs given for model-level HR, Table IV (p. 6), and framing (p. 9); per-subcategory n = 6–20 (p. 10); size/precision confound (p. 10) — [I].
- Reproducibility: prompts, decoding and model identifiers reported; code released (p. 2, p. 5); engine/quantization method missing — [I].

## 11. Future research directions
- Stated by authors [A]: registry grounding at generation time and caveat-gating tools; asking feasibility first; treating an exhausted reasoning budget as an impossibility signal (p. 9, p. 10, p. 11).
- Suggested by us [I]: evaluate a registry-check tool as an intervention on the npm/crate/PyPI subsets; add closed models and agentic tools; combine planted-name prompts with spontaneous-invention prompts in one design.

## 12. Relevance to our research
- Research questions addressed (RQ ids): RQ1, RQ2, RQ3, RQ4, RQ5.
- How it informs our work [I]:
  - RQ1: Across 17 open models, fabrication of nonexistent packages barely falls with scale; npm and Rust are worst, PyPI and Go intermediate, Java lowest (p. 6, p. 8). Small 4-bit models (6.7–7B) hallucinate on 66–90% of all unsatisfiable prompts (p. 6, p. 10).
  - RQ2: Collisions with unrelated real packages occur (`pywfm`, p. 9) — evidence that invented names can already be taken. Cross-model agreement (33/270 prompts fool >=16/17 models, p. 9) concerns names planted by the prompt, so it is not evidence of spontaneous name repetition.
  - RQ3: Recommends registry grounding and caveat-gating but does not evaluate them (p. 9). The 18% "factual" plausible-entity hallucinations (p. 7) install no fictitious package, so they do not bear on slopsquatting defences.
  - RQ4: Matched solvable controls and a validated LLM judge are useful design elements; the registry-state dependence is a known pitfall (p. 5, p. 10).
  - Laptop-scale implication: the benchmark is small (361 prompts) and public, and its small models were already run 4-bit (p. 10), the regime a laptop uses. A laptop study could re-run the npm/crate/PyPI/Go subsets on local 7B models in hours, and measure how much a simple install-time registry check (or a "does this package exist?" pre-prompt) reduces harm.
  - Replication checklist: temperature 0, single completion, 16,384 output tokens; 10 framing templates; judge rubric with memo; HR/RR/over-refusal with bootstrap CIs over prompts; Spearman vs log parameters (p. 4, p. 5).

## 13. Evidence table (for the evidence matrix)
| RQ | Claim | Page | Label | Strength |
|---|---|---|---|---|
| RQ1 | 17 open models write ungrounded code for 54% of unsatisfiable requests (HR 0.23–0.90 per model); only 1/1,547 control responses is a wrongful refusal | 5, 6 | [V] | moderate |
| RQ1 | Scale cuts fabrication of theoretical impossibilities (0.84->0.32) but barely of nonexistent packages/APIs (0.88->0.61); npm+crates 1.00->0.85 | 6 | [V] | moderate |
| RQ1 | When a nonexistent package is named in the prompt, models fabricate it for npm 94%, Rust crates 87%, Go 63%, PyPI 63%, Java 33% | 8 | [V] | moderate |
| RQ1 | Request framing as routine work raises HR by 21 points vs question framing (95% CI 8–34) | 8, 9 | [V] | moderate |
| RQ1 | Small models (<=32B) were evaluated at 4-bit; 7B models hallucinate on 66–90% of unsatisfiable prompts | 6, 10 | [V] | moderate |
| RQ1 | 33 of 270 prompts fool at least 16 of 17 models; prompt identity explains 34% of outcome variance vs 15% for model. [I] Names are supplied by the prompt; not evidence of spontaneous cross-model repetition | 8, 9 | [V] | moderate |
| RQ2 | A hallucinated install name (`pywfm`) collides with an unrelated existing PyPI package | 9 | [V] | weak |
| RQ2 | A misspelled real package name is fabricated on 14% of prompts (vs 94% for correctly spelled fictional names); the rest are corrected or refused | 4, 8 | [V] | moderate |
| RQ3 | Authors recommend registry grounding at generation time and gating output on the model's own caveats (not evaluated) | 9, 11 | [A] | weak |
| RQ3 | [V] 18% of plausible-entity hallucinations are factual (real code, false claims). [A] "no registry check will notice" them. [I] These responses install no fictitious package, so they do not bear on slopsquatting defences | 7 | [V] | weak |
| RQ4 | LLM judge (Claude Opus 4.6) agrees with human labels on 94% of outcomes (kappa 0.91) but only 67% of behaviour labels | 5 | [V] | moderate |
| RQ4 | Results depend on registry state at generation time; size confounded with 4-bit quantization | 10 | [A] | moderate |
| RQ5 | Closed frontier models and agentic settings are not evaluated | 10 | [A] | moderate |

## 14. Key quotes
> "only 1 of 1,547 responses to solvable controls is a wrongful refusal" (p. 2)
> "nonexistent npm packages are fabricated on 94% of prompts" (p. 8)
> "a package of that name exists on PyPI as an unrelated factorization-machine wrapper from 2015" (p. 9)

## Analyst notes
- Reading coverage: whole paper read (pp. 1–12 incl. references). Figures 3–7 are charts; numbers taken from tables and text.
- Uncertainties: GitHub URL is garbled in the text layer (space instead of probably an underscore). Registry verification date/method for planted names not described. Inference engine and quantization method unknown.
