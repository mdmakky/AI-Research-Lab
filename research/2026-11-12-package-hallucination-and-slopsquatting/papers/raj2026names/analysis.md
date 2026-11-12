---
key: raj2026names
status: complete
evidence_basis: full-text
design: System design + small empirical evaluation (agent pipeline run on hand-written prompts; offline classifier transfer matrix; convenience-sample user survey)
dataset: 300 hand-written single-line Python prompts in 18 tiers; per-LLM package-verdict dataset (464 unique package names, 7 LLMs) for classifier training
sample_size: 300 prompts (385 runs, 823 package verdicts) on llama-3.1-8b/llama-3.3-70b; 24 survey participants
metrics: primary give-up rate, intra/cross-model rescue rate, end-to-end clean rate, classifier F1 (bootstrap 95% CI), feature importance, Likert ratings
main_finding: PyPI 404 check plus 10-feature metadata classifier; about half of 179 flagged names already exist on PyPI; a two-feature OR rule matches the Random Forest.
relevance: high
analysed: 2026-11-12
---
<!-- Frontmatter: single-line values; they feed literature-matrix.md via `rlab index`.
     status: draft (in progress) -> ready (analyst self-check passed) -> complete (critical review passed).
     evidence_basis: full-text | abstract-only. abstract-only analyses must not fill methodology detail.
     relevance: high | medium | low. -->

# Names Can Hurt: Spotting Slopsquatting Risks Caused by Package Name Hallucinations in Local Coding LLMs

- Authors: Raj, Akash; Sahu, Sargam
- Year / venue: 2026, arXiv (Cornell University) (preprint)
- DOI: 10.5281/zenodo.22087562 · URL: https://arxiv.org/abs/2608.23897
- Source text: `fulltext.txt` (page refs = PDF page index)

Labels: **[V]** verified in the paper's own data/tables/results · **[A]** author claim · **[I]** our interpretation.
Every [V]/[A] item ends with a page ref `(p. N)`. Write "not reported" when the paper does not say.

**Source tier:**
- arXiv preprint, v1, August 2026 (p. 1); not peer-reviewed.
- The authors are an M.Tech student and a B.Tech intern; much of the work was done during an internship (pp. 1, 15).
- The metadata DOI is a Zenodo DOI. `metadata.json` verification is "single-source (openalex)".
- Per the critical review (2026-11-12), `rlab validate` returns MISMATCH: arXiv and OpenAlex agree, but the Zenodo DOI is not in Crossref.
- PDF identity is only "probable": the PDF prints just "Version: v1, arXiv, August 2026" and no arXiv id (p. 1).

## 1. Research objective
- [A] Build and evaluate a client-side guard that stops a coding LLM's hallucinated Python package names from turning into slopsquatting installs. The guard targets "small, open-weight, locally runnable LLMs in the 7B to 70B range" (p. 2).
- [A] The authors say local models matter for three reasons (p. 2):
  - developers outside large companies run them;
  - they "tend to hallucinate more often than frontier systems";
  - local deployment rules out asking a hosted model to verify the output.

  No evidence is given for the second point.

## 2. Research questions / hypotheses
- No formal RQs or hypotheses. The paper lists five contributions instead (p. 2):
  1. a two-layer detector (PyPI existence check plus a per-LLM Random Forest);
  2. an import-name reconciler;
  3. a LangGraph retry/fallback agent;
  4. an evaluation on 300 prompts;
  5. a user acceptance study.
- §6 implicitly answers six questions (pp. 6–12):
  - how often the pipeline gives up;
  - how much retries and fallback recover;
  - how give-up varies by prompt tier;
  - how many flagged names already exist on PyPI;
  - whether per-LLM classifiers transfer across models;
  - whether a hand-written rule matches the Random Forest.

## 3. Methodology
- Research design: [V] A system-building paper with a single-configuration evaluation (one primary/fallback model pair), an offline classifier analysis and a convenience-sample survey (pp. 6–12). There is no control condition without the detector, apart from earlier buggy system versions (p. 7).
- Approach / model / intervention:
  - [V] **Extractor.**
    - Parses the syntax tree (AST) of Python code blocks and keeps only the top-level module name.
    - A regex fallback runs only inside code fences and ignores keywords and shell tokens.
    - `pip install` lines are read only inside code fences (pp. 3, 5).
  - [V] **Layer 1, deterministic check.** One PyPI JSON API lookup per name. A 404 means the name is fake; a 200 sends the package metadata to the classifier (p. 5).
  - [V] **Layer 2, Random Forest.** 400 trees, 10 features (p. 5):
    - 8 name features: length, number of parts, digits, a letter repeated three times, hype words (`super`, `pro`, `ai`, `magic`), generic words (`helper`, `tools`), a `py-`/`python-` prefix, and Levenshtein distance to a list of the top 15,000 PyPI names;
    - 2 metadata features: maintainer count and whether a GitHub URL is present.
  - [V] **Import-name reconciler.**
    - A 24-entry YAML table (e.g. `cv2` → `opencv-python`, `PIL` → `Pillow`).
    - It is consulted only after a PyPI 404, and a mapped name is accepted only if the install name passes both layers.
    - The authors' security argument: an attacker-registered `cv2` returns 200, so the reconciler never runs and the classifier must catch it (pp. 5–6).
  - [V] **Agent.**
    - A LangGraph state machine with six nodes.
    - Retry budget is 1 per model ("up to 2 attempts"), with rising temperature (0.7 → 1.0 → 1.2).
    - After the budget is spent, the task goes to a fallback model with its own matched classifier.
    - Every attempt is logged to JSONL (pp. 3, 6).
- Baselines or comparison conditions:
  - [V] Earlier system versions v0/v1 (broken regex, no reconciler) are used as an ablation (p. 7).
  - [V] Three hand-written rules are compared with the Random Forest on the same package-disjoint split (p. 12).
  - [V] LLM self-verification is described as a "baseline" in related work but is **not run** (p. 3).
  - [V] There is no comparison with any published detector or with Spracklen et al.'s method; the reference list has only three entries (p. 15).

## 4. Dataset and sample
- Data source(s):
  - [V] 300 single-line Python coding prompts, written by hand (p. 6).
  - [V] Classifier data: "Sargam's dataset" (`raw_master_dataset.csv`) of package names generated by seven LLMs (pp. 9, 14). How it was generated (prompts, hosting, dates) is not reported.
- Sample size (N) and unit:
  - [V] Prompts: 300 in 18 tiers of 5–30 prompts each (pp. 6–8):
    - about 140 routine tasks (data engineering, security/DevOps, standard workflows);
    - about 55 obscure-dependency tasks;
    - about 105 adversarial prompts.
  - [V] Runs and verdicts: 385 runs (300 primary + 85 fallback) gave 823 package verdicts (p. 8).
  - [V] Classifier data (pp. 9–10):
    - 464 unique package names across 7 LLMs; 210 occur in at least two models and 42 in all seven;
    - each model has 68–108 hallucinated rows, which leaves 2–12 positive examples per test slice.
  - [V] Survey: n = 24 CS undergraduates (p. 11).
- Sampling / selection method:
  - [V] The researchers wrote the prompts themselves. Adversarial prompts name packages or use "tricky wording" such as asking for "the newest and most capable library for X" (p. 6).
  - [V] Survey participants were "Sargam's CS undergraduate peers" / "the intern's friends" (pp. 2, 11).
  - Not reported: the tier construction criteria, and the classifier labelling procedure (who or what decided "hallucinated" in the training data).
- Data availability: [A] Code, mapping table, the 300 prompts, seven classifiers, the 385-record run log and the leakage-safe matrix are released at a GitHub repository (p. 15). We did not check the repository.

## 5. Experimental setup
- Procedure, settings, hyper-parameters, tools:
  - [V] **Models.**
    - Classifiers were trained for `gpt-5`, `gpt-oss-120b`, `llama-3.1-8b`, `llama-3.3-70b`, `llama-4-scout`, `qwen3-27b` and `qwen3-32b` (p. 2).
    - The agent evaluation uses two **Groq-hosted** models chosen to fit "our free-tier budget": primary `llama-3.1-8b`, fallback `llama-3.3-70b` (p. 2).
    - Not reported: exact model versions/checkpoints and quantization.
  - [V] **Classifier.** Random Forest with 400 trees; scikit-learn 1.8 in v2 (pp. 5, 7). Other hyper-parameters and the decision threshold on P(fake) are not reported.
  - [V] **Split.** The original split was a per-model 75/25 row split with `random_state=42`. It was replaced by a package-disjoint 75/25 split over the 464 unique names (p. 9).
  - [V] **Uncertainty.** Bootstrap 95% CIs with 1,000 resamples, for F1 only (p. 10).
  - **Standard-library handling: not reported.** The extractor keeps every top-level import name (p. 5), and every 404 counts as "fake" (p. 5). [I] Whether stdlib modules are filtered before the PyPI lookup is never stated. Any unfiltered stdlib name that returns 404 would be flagged and trigger a retry, which directly affects the give-up rates.
  - **Hardware: not reported.** All generation ran through Groq's hosted API, and the classifier analysis was "computed offline" (pp. 2, 6). [I] Despite the title, no model was run on local hardware. "Local" describes the model class (open-weight, 7–70B), not the deployment. The classifier training set also includes `gpt-5`, which is not a local model.
  - [V] **Run budget.**
    - One fallback run was lost to a mid-batch Groq rate-limit event (p. 7).
    - A cross-family fallback was not run because it "would have required 5 times the Groq token budget beyond the free tier" (p. 11).
  - [V] **Survey.** Standalone Streamlit tool; seven dimensions on a 1–5 Likert scale (p. 11).
- Code availability: [A] A GitHub repository is stated, and twelve extractor regression tests are said to pass (p. 15).

## 6. Evaluation metrics
- Metric — what it measures — why chosen:
  - [V] **Primary give-up rate:** share of prompts where the primary model exhausts its retry budget (p. 6).
  - [V] **Fallback rescue rate:** share of give-ups that the fallback recovers (p. 6).
  - [V] **End-to-end clean rate:** share of prompts that finish with no hallucinated recommendation (p. 6).
  - [V] **Per-tier and per-name breakdowns** (p. 6).
  - [V] **Classifier F1** in a 7×7 train-LLM × test-LLM matrix (p. 9).
  - [V] **Random Forest split importance** per feature (p. 10).
  - [V] **Likert means/medians** from the survey (p. 11).
  - [I] Why these metrics were chosen is not justified.
  - [I] Retries are triggered both by non-code answers and by flagged names (p. 4). The give-up rate is therefore a pipeline outcome, not a pure hallucination rate, and it also absorbs detector false positives (see §9).
  - Not reported: detector precision/recall against a manually checked ground truth on the 300-prompt run.
- Statistical testing:
  - [V] Bootstrap CIs are reported for the F1 matrix only (p. 10).
  - There are no CIs or tests for give-up, rescue or tier rates, and no significance testing.

## 7. Key findings
1. **Pipeline outcome on `llama-3.1-8b`.** [V]
   - 186/300 prompts (62%) produced code on the first try (p. 7).
   - 114 triggered a retry, and 28 of those were fixed by the retry, a 24.6% intra-model rescue (p. 7).
   - 86/300 (28.7%) exhausted the budget (p. 7).
   - The fallback ran on 85 of those 86 and recovered 14 (16.5%) (p. 7).
   - End to end, 228/300 (76%) finished clean; the remaining 72 would get a "do not pip install" warning (p. 7).
2. **Most of the give-up reduction came from preprocessing fixes, not the classifier.** [V] Primary give-up rates by version (p. 7):
   - v0: 79% (55/70), broken regex on the full text;
   - v1: 57% (33/58), AST plus code-only regex;
   - v2: 30% (18/60) on 60 prompts and 28.7% (86/300) on 300 prompts, after the reconciler was added.

   These are different, overlapping prompt sets, not one fixed set (p. 7). The reconciler fired 29 times over 4 distinct alias pairs in the 300-prompt run (p. 7). [A] The extractor and reconciler fixes together "caused a 49-point drop"; "Changing the classifier itself did not help much" (p. 12).
3. **Give-up rate rises with prompt tier.** [V]
   - Low tiers: Data Engineering 0% (n=20); Security & DevOps 5% (n=20); Level 1 and Level 2 10% each (n=10 each) (pp. 7–8).
   - High tiers: Hallucination Bait 55% (n=20); Adversarial (Realistic Hallucination Bait) 73.3% (n=30) (p. 8).
   - Direct Slopsquatting Stress Tests: 30% (n=30) (p. 8). This is below the abstract's "40 to 73% on slopsquat baits" (p. 1).

   [I] Table 2 is sorted by rate, not by any independent measure of how adversarial a prompt is. The "Level N" tiers are not in order of rate (Level 8 = 0%, Level 4 = 60%; pp. 7–8). The abstract's claim that the rate "scales almost linearly with prompt adversariality" (p. 1) is therefore an author claim with no defined adversariality scale.
4. **"Already-registered lookalike" finding (the paper's headline).**
   - [V] 385 runs produced 823 verdicts: 644 `real` (78.3%) and 179 `hallucinated` (21.7%) (p. 8).
   - [V] Of the 179 flags, "Half were true 404s". The other half returned PyPI status 200 and were flagged by the classifier because of suspicious metadata. The paper later gives 90 `status=200` flags (pp. 8–9).
   - [V] Table 3, "Wild caught PyPI registered squats and lookalikes" (pp. 8–9):

     | Name | Canonical project (per Table 3) | P(fake) | Flags |
     |---|---|---|---|
     | `pil` | Pillow | 0.89 | 36 |
     | `faiss` | faiss-cpu/-gpu | 0.57 | 10 |
     | `tabula` | tabula-py | 0.57 | 4 |
     | `haystack` | now haystack-ai | 0.56 | 2 |
     | `camelot` | camelot-py | 0.95 | 1 |
     | `skimage` | scikit-image | 0.58 | 1 |
     | `fastyaml` | none identified | 0.99 | 1 |
     | `fastvector` | none identified | 0.82 | 1 |
     | `graphbrain` | ambiguous | 0.92 | 2 |

     Further rows include `aiworkflow`, `taskgraph`, `promptstudio`, `flowgraph-ai`, `embeddinghub`, and "22 more" names with one or more flags each.
   - [A] "Approximately half of the hallucinated recommendations produced by the LLM were already present on PyPI as squats or low-quality lookalikes", so a deterministic-only check "would have caught only the other half" (p. 9).
   - [V] Security invariant: for all 90 `status=200` flags, the reconciler was never called (p. 9).
   - [A] The reconciler "correctly refused to help every single time" against an attacker suite; the attacker suite is not described (p. 6).
   - [V] **The paper's own evidence that import names are being flagged:**
     - The reconciler table maps `pil` → `Pillow` (p. 7). It can only fire after a 404, and `pil` returns 200 (p. 5), so it never fires for `pil`. As a result `pil` was flagged 36 times as a registered squat (Table 3, p. 8).
     - `pkg-resources` is listed among the true-404 "inventions" (p. 8).
     - In the bait test, the model's plain `faiss` is counted as a hallucinatory variant because the name is "metadata suspicious" (p. 11).
   - [I] **This finding needs caution.**
     - In Table 3, 36 + 10 = 46 of the 90 status-200 flags (≈51%) come from `pil` and `faiss`. Both are the normal *import* names of real projects (`import PIL` for Pillow, `import faiss` for faiss-cpu), as the paper's own "Canonical project" column shows (p. 8).
     - `skimage`, `camelot`, `tabula` and `haystack` are also import or legacy names of legitimate projects. `pkg_resources` is a module shipped with setuptools (general Python knowledge).
     - So a large share of the "already registered" half is probably correct `import` statements whose import name happens to be a separate, low-quality PyPI project. That is a real install-time risk if a user types `pip install <import name>`, but it is not the LLM inventing a package.
     - The reconciler's 404-only rule (p. 5) produces these flags by design. The authors admit they have not audited the ≥30 registered names (pp. 13–14).
5. **Classifier transfer.** [V]
   - The first per-model row split leaked: 72.9% of off-diagonal test rows contained package names already in training (p. 9).
   - On the corrected package-disjoint split, F1 ranges from 0.833 to 1.000 (pp. 9–10).
   - Two test columns (llama-4-scout, qwen3-27b) have only 2 positives each, giving CIs of [0.00, 1.00]. The llama columns have 5 positives each (CI [0.67, 1.00]) (p. 10).
   - [A] One classifier trained on `gpt-oss-120b` (~410 rows) "works well across all seven models", so matched-pair training "is not needed" (p. 10).
6. **The classifier is in effect a two-feature metadata rule.** [V]
   - `log_maintainers` provides 57.6% of the split importance and `github_url_present` another 24.5%, 82% together (p. 10).
   - Rule C (OR over the two features) reaches a mean F1 of 0.99, against 0.98 for the Random Forest. The strict-AND rules reach 0.53–0.55 (p. 12).
   - [A] "the 400-tree Random Forest does not really give us more help than the simple OR baseline" (p. 12).
   - [I] The prose then states the rule as "zero PyPI maintainers AND no GitHub URL", which contradicts the table, where the OR rule wins (p. 12). The exact rule is ambiguous.
7. **Same-family fallback mostly fails.** [V] 71 of 85 give-ups (83.5%) failed again on `llama-3.3-70b`. The same invented names recurred in both models' outputs, e.g. `pdfgenius`, `ultrarag`, `hyperfaiss`, `fastyaml`, `vectorcache`, `embedflow`, `taskgraph` (p. 10). [A] A cross-family fallback should work better, but was not tested (pp. 11, 13).
8. **Bait refusal.** [V] The Bonus Stress Test has 10 prompts that name fabricated packages (p. 11):
   - 1 bait was used verbatim (`ultrarag`) and caught by the detector;
   - 3 became nearby variants (`fastvector`, `fastyaml`, `faiss`);
   - 6 were "refused outright", and real packages were substituted;
   - the pipeline finished clean on 6/10.

   [I] The paper reports this inconsistently: the abstract says the model "refused 6 of 10 direct baits unaided" (p. 1), while §6.8 says "The LLM refused the bait name on 9 of 10 prompts" (p. 11).
9. **User acceptance.** [V] Mean ratings 4.21–4.58, overall 4.42/5. 21/24 participants would use the tool and 23/24 would recommend it (p. 11). [A] The authors acknowledge possible desirability bias (pp. 2, 11).

## 8. Limitations stated by the authors
- [A] Only one model pair was evaluated (llama-3.1-8b → llama-3.3-70b). A cross-family test was not affordable on the Groq budget (p. 13).
- [A] The `pypi_maintainers_count` feature "is basically 0" because the PyPI JSON API only shows maintainers to admins, which "might cause false positives for small legitimate packages" (p. 13).
- [A] Transferability cells rest on 2–12 hallucinated test examples, so two columns are uninformative. More runs or pooled cross-validation are needed (pp. 10, 13).
- [A] About 82% of the classifier's signal comes from two metadata features, so attackers could evade it by registering squats with realistic-looking metadata. This was not tested (p. 13).
- [A] The ≥30 registered names flagged as suspicious were not individually audited (pp. 13–14).
- [A] The user study participants were the intern's friends (p. 14).
- [A] Drift (p. 14):
  - brand-new legitimate packages will be mis-flagged (zero maintainers, no GitHub link, not in the 15k list);
  - the reference list goes stale;
  - packages can be renamed or taken over (`haystack` → `haystack-ai`).

  None of the proposed mitigations is implemented: monthly snapshot refresh, quarterly retraining, a 24 h metadata cache, false-positive monitoring (p. 14).

## 9. Limitations we identified
- [I] **No ground truth for the 300-prompt run.** Detector precision and recall are never measured against manually labelled package names; "hallucinated" means "flagged by the detector". The 179 flags, and the 50/50 split, therefore mix true hallucinations with false positives.
- [I] **Construct problem in the "already registered" finding.**
  - As shown in §7 finding 4, about half of the status-200 flags are `pil` and `faiss`, which are standard import names. The paper itself lists their canonical projects (p. 8) and even maps `pil` → `Pillow` in its reconciler table (p. 7).
  - The 404-only reconciler rule turns correct imports into "hallucinations" whenever someone else has registered the import name.
  - The headline "half of hallucinations are registered lookalikes" (pp. 1, 9, 15) probably overstates LLM invention and understates the ambiguity between import names and install names.
- [I] **Standard-library handling not reported.** Unfiltered stdlib imports that return 404 would be counted as fake (p. 5). That would inflate both give-up and hallucination counts by an unknown amount.
- [I] **Mismatch between training data and live use for the top feature.** At inference, `log_maintainers` (57.6% of importance) is near zero for most packages via the JSON API (p. 13). The training data were "pulled" another way ("Sargam's dataset helps a little by pulling metadata", p. 13). The live classifier therefore probably flags legitimate status-200 packages on that feature alone, which would inflate the registered-lookalike count.
- [I] **Possibly circular training labels.** How the training labels were assigned is not reported. If "hallucinated" was derived from PyPI non-existence, then "no maintainers" and "no GitHub URL" are trivially true for 404 names. That would explain both the near-perfect F1 and the dominance of the metadata features.
- [I] **Overstated baseline comparison.** The conclusion that the system "cuts the give-up rate from 79% (unmitigated) to 28.7%" (p. 15) compares against v0, a version with a broken extractor, run on a different 70-prompt set (p. 7). That is a bug-fix comparison, not an unmitigated baseline.
- [I] **Unsupported term attribution.** The paper says Spracklen et al. (2024) "termed this attack pattern slopsquatting" (p. 2), without a page or quote. twist2026library attributes the term to Park (2025) [@twist2026library, p. 1; @twist2026library, p. 3]. The reference list has three items (p. 15).
- [I] **Internal inconsistencies:**
  - bait refusal 6/10 vs 9/10 (pp. 1, 11);
  - "40 to 73%" vs a 30% bait tier (pp. 1, 8);
  - a retry budget of "up to 2 attempts" vs a three-step temperature schedule (pp. 3, 6);
  - "AND" vs "OR" rule wording (p. 12).
- [I] **Unverifiable model identifier.** `qwen3-27b` is given without provider or version (p. 2); we could not confirm it from the paper.
- [I] **Weak survey.** The user study tests the standalone UI, not the detector's accuracy. With a friends-and-peers sample it says little about effectiveness.

## 10. Threats to validity
- Internal:
  - The authors wrote the prompt set, and the tiers are defined post hoc.
  - Detector false positives are counted as hallucinations.
  - Same-family names recur across primary and fallback, so the two runs are not independent.
  - Leakage in the first classifier split was found and fixed (p. 9).
  - The labelling procedure and stdlib filtering are not reported.
- External:
  - One small model (llama-3.1-8b) through one API provider (Groq), Python/PyPI only.
  - No genuinely local inference; hardware, quantization and runtime are not reported.
  - Single-line prompts, not agentic multi-file tasks.
- Construct:
  - "Give-up" mixes non-code answers, true hallucinations and detector false positives.
  - "Hallucination" is defined by the detector itself.
  - Squat or lookalike status was not audited (pp. 13–14).
- Statistical conclusion:
  - Only F1 has CIs, and those are very wide (p. 10).
  - Tier rates rest on n = 5–30 prompts each, with no CIs (pp. 7–8).
  - One run per prompt; nothing on seed variation.
  - The version ablation uses different, overlapping prompt sets (70, 58, 60, 300; p. 7).
- Reproducibility:
  - [A] Artefacts are said to be on GitHub (p. 15).
  - Not reported: model versions, Groq dates, classifier threshold, training-data construction. Groq-hosted models change over time.

## 11. Future research directions
- Stated by authors [A]:
  - cross-family fallback pairing, e.g. Llama → Qwen or GPT-OSS (pp. 11, 14);
  - richer features (first-upload age, release cadence, owner-network overlap, README quality, repository activity), which must beat the two-feature rule (p. 14);
  - about 3× more hallucinated examples per model, or pooled cross-validation (pp. 10, 14);
  - drift handling: monthly top-N refresh and quarterly retraining (p. 14);
  - adversarial squats with realistic metadata are named as untested (p. 13).
- Suggested by us [I]:
  1. Manually audit every flagged name, and keep three cases apart:
     - (a) a correct import name whose PyPI namesake is a different project;
     - (b) a hallucinated name that is registered;
     - (c) a hallucinated name that is unregistered.

     Filter stdlib names explicitly before the lookup.
  2. Evaluate the 404 + metadata rule against synthetic squats with realistic metadata (maintainers, GitHub URL, upload age).
  3. Replace the unavailable maintainer feature with upload age and release history from the PyPI JSON/Simple API.
  4. Run the models truly locally (e.g. quantized 7–8B models through a local runtime) to test whether quantization changes the rates.

## 12. Relevance to our research
- Research questions addressed (RQ ids):
  - RQ3 (primary): tool-side defence.
  - RQ2: registered lookalikes; names recurring across same-family models.
  - RQ1: rates by prompt tier for one small model.
  - RQ4: pitfalls (extractor scope, import-name reconciliation, stdlib handling, split leakage).
  - RQ5: untested settings (cross-family fallback, realistic-metadata squats, local inference).
- How it informs our work [I]:
  - **Laptop-scale feasibility.**
    - The defence is cheap: a PyPI JSON lookup plus a two-feature rule that the authors say fits in "one line of Python" (p. 12). It needs no GPU and runs on any laptop.
    - It is a natural baseline for our defence study.
    - The authors' own evaluation ran on a free API tier, not locally, so a truly local replication (Ollama or llama.cpp with quantized models) would add something new.
  - **What a measurement study should do better.** The paper shows the pitfalls a laptop-scale measurement must handle:
    - extract only from code fences, with AST parsing;
    - filter stdlib modules explicitly;
    - keep a separate map from import name to distribution name, and record PyPI status separately from "hallucinated";
    - snapshot PyPI responses with timestamps;
    - hand-label a sample to estimate precision.
  - **Open question worth testing.** How many LLM-suggested names are already registered on PyPI, and by whom. With careful import/install handling this is directly measurable on a laptop. This paper's ~50% is the number to check, and we have reason to think import-name collisions inflate it.
  - **Weight.** Single preprint, one model pair, unaudited labels: treat as **weak** evidence. Use it for design ideas and pitfalls, not for effect sizes.

## 13. Evidence table (for the evidence matrix)
| RQ | Claim | Page | Label | Strength |
|---|---|---|---|---|
| RQ3 | Two-layer guard (PyPI 404 check + metadata Random Forest + import-name reconciler + retry/fallback) finishes clean on 228/300 prompts (76%) with llama-3.1-8b → llama-3.3-70b | 7 | V | weak |
| RQ3 | Random Forest signal is 82% from two metadata features (maintainers 57.6%, GitHub URL 24.5%); a two-feature OR rule matches it (mean F1 0.99 vs 0.98) | 10, 12 | V | weak |
| RQ2 | 90 of 179 flagged names returned PyPI 200 (registered), but 46 of these 90 flags are `pil` and `faiss`, which the paper itself maps to Pillow and faiss-cpu/-gpu; registered-lookalike share is likely inflated by import-name collisions | 7, 8, 9 | V (counts) / I (interpretation) | weak |
| RQ2 | Same-family fallback (Llama 8B → 70B) fails again on 83.5% of give-ups; invented names (pdfgenius, ultrarag, vectorcache, ...) recur across both models | 10 | V | weak |
| RQ1 | Primary give-up rate (llama-3.1-8b) is 0–10% on routine tiers and 55–73% on hallucination-bait tiers (n = 5–30 per tier) | 7, 8 | V | weak |
| RQ4 | Most early "hallucinations" were extractor false positives (aliases, submodules, prose tokens); fixing extraction and adding the reconciler cut give-up from 79% to ~29%, measured on different, overlapping prompt sets (70, 58, 60, 300) | 7, 12 | V | weak |
| RQ4 | A per-model random row split leaked package names (72.9% of off-diagonal test rows); a package-disjoint split is needed | 9 | V | moderate |
| RQ4 | Stdlib handling not reported: all top-level imports are checked and every 404 counts as fake | 5 | V (absence) / I (impact) | weak |
| RQ3 | PyPI JSON API does not expose maintainers for non-admins, so the top classifier feature is ≈0 in practice and risks false positives on small or new legitimate packages | 13, 14 | A | weak |
| RQ5 | Untested: cross-family fallback, squats with realistic metadata, drift handling, local (non-API) inference | 11, 13, 14 | A | weak |

## 14. Key quotes
> "half of the flagged hallucinations are packages already registered on PyPI, as low quality lookalikes of well known projects, caught by the classifier rather than the deterministic layer" (p. 1)

> "The classifier was therefore memorizing names, instead of learning to generalize." (p. 9)

> "You can write that rule in one line of Python." (p. 12)

> "the PyPI JSON API only shows maintainers if you are an admin" (p. 13)

## Analyst notes
- Reading coverage: all 16 PDF pages of `fulltext.txt`, from the abstract through Appendix C. Figure 1 (p. 4) is a pipeline diagram; we relied on its caption. Tables 1–6 extracted cleanly.
- Uncertainties:
  - The metadata DOI is a Zenodo DOI, while the paper presents itself as arXiv v1 (p. 1). The review reports `rlab validate` MISMATCH; we did not re-run it.
  - The model identifier `qwen3-27b` could not be confirmed.
  - We did not inspect the GitHub artefacts.
  - Whether exactly 89 or 90 of the 179 flags were 404s is not stated ("Half", p. 8; "90 `status=200` flags", p. 9).
- Critical-review fixes applied (2026-11-12):
  - validate/identity note;
  - stdlib not reported (§5, §9, §10, §13);
  - the paper's own `pil`/`pkg-resources`/`faiss` evidence (§7.4);
  - RQ4 ablation row downgraded to weak (different prompt sets);
  - unsupported "slopsquatting" attribution (§9).
