---
key: okwor2026hallucination
status: complete
evidence_basis: full-text
design: Registration-status measurement of hallucinated names (self-generated corpus + public anchor set) with static content triage and an offline install-time demo
dataset: 6,800 generations from 5 local open-weight code models via Ollama (Python + JS); 149 anchor names from Trend Micro and DepScope public datasets
sample_size: 1,641 confirmed hallucinated names; 149 anchor names (22 registered)
metrics: Distinct confirmed hallucinated names; new names per generation; share registered with rule-of-three 95% upper bound; intent taxonomy of registered names
main_finding: None of 1,641 self-generated hallucinated names were registered four days later; 22 of 149 public names registered, none malicious, most reported as one placeholder operator.
relevance: medium
analysed: 2026-11-12
---
<!-- Frontmatter: single-line values; they feed literature-matrix.md via `rlab index`.
     status: draft (in progress) -> ready (analyst self-check passed) -> complete (critical review passed).
     evidence_basis: full-text | abstract-only. abstract-only analyses must not fill methodology detail.
     relevance: high | medium | low. -->

# From Hallucination to Registration: Do the Package Names That LLMs Invent Actually Get Claimed?

- Authors: Okwor, Daniel
- Year / venue: 2026, Zenodo preprint ("Preprint, July 2026", p. 1). Single author, affiliated with Orygn LLC (p. 1).
- **Source tier: 4 (grey literature).** Reasons:
  - The paper calls itself a "Preprint" (p. 1).
  - It is a self-deposit on Zenodo, not on a moderated preprint server, and has no peer review.
  - Single author with a company affiliation, and no funding or conflict-of-interest statement.

  It is used as background and corroborating evidence only.
- DOI: 10.5281/zenodo.21199426 (concept DOI, used in metadata). The PDF prints 10.5281/zenodo.21199427 (p. 1), which is the version DOI of the same Zenodo deposit. The orchestrator resolved this via the Zenodo API on 2026-11-12. `rlab validate` reports MISMATCH only because Crossref has no record of this DataCite DOI; OpenAlex matches.
- Source text: `fulltext.txt` (page refs = PDF page index); user-supplied PDF.

Labels: **[V]** verified in the paper's own data/tables/results · **[A]** author claim · **[I]** our interpretation.
Every [V]/[A] item ends with a page ref `(p. N)`. Write "not reported" when the paper does not say.

## 1. Research objective
[A] Earlier studies measure exposure: how often models invent package names. This paper measures the next step, harm: how many invented names are actually registered on the package index, by whom, and with what intent (p. 1–2). [A] The author claims no earlier work checks the true registration dates of hallucinated names or judges the intent behind the registrations (p. 2).

## 2. Research questions / hypotheses
- [A] Of the names models invent, how many are registered today? When a hallucinated name is registered, what is the registrant doing with it (p. 2)? No formal hypotheses are stated.

## 3. Methodology
- Research design: [V] Three parts (p. 2):
  - (a) a self-generated corpus of hallucinated names, re-checked live;
  - (b) a public "anchor set" of previously reported hallucinated names, judged by registration date and static content inspection;
  - (c) an offline demonstration of code running at install time.
- Approach / model / intervention: [V] Five open-weight models served locally through Ollama: qwen2.5-coder:7b, deepseek-coder:6.7b, codellama:13b, codestral:22b and gpt-oss:20b (p. 3). Prompts ask for Python and JavaScript solutions across a "fixed task set", at temperatures 0.7 and 1.0, with fixed seeds (p. 3).
- Hallucination check ("two oracles"): [V] (p. 3)
  - Check A: the name is absent from a frozen snapshot taken at t0 = 2026-06-30. The snapshot has 839,365 normalised PyPI names (from the simple index) and 4,194,421 lowercased npm names (from a public mirror). Both lists are SHA-256 hashed.
  - Check B: the live registry returns 404 for the name.
  - A name counts as a confirmed hallucination only if it passes both checks.
  - When the checks disagree:

    | Snapshot at t0 | Live now | Classified as |
    |---|---|---|
    | absent | exists | candidate registration after t0 |
    | present | 404 | yanked package |
    | — | network error | unknown |

- Extraction: [V] (p. 3)
  - Python is parsed with `ast`; JavaScript with an acorn-based parser, falling back to lenient parsing.
  - Import names are mapped to distribution names where they differ (example: sklearn → scikit-learn). Where the mapping comes from is not reported.
  - Names are normalised per PEP 503.
  - Standard-library and built-in modules are excluded.
  - Scoped and subpath names are resolved.
  - Tokens that break registry naming rules are dropped.
- Anchor-set judgement: [V] (p. 4)
  - True registration time: npm `time.created`; for PyPI, the earliest release upload.
  - Static inspection only: `setup.py`, `PKG-INFO` and manifests are read as text.
  - A fixed rubric sorts each registered name into one of four classes: malicious, defensive placeholder, organic (an unrelated real package), or individual reservation.
- Baselines or comparison conditions: none. [V] A negative control is reported (p. 7; see section 7, finding 5).

## 4. Dataset and sample
- Data source(s):
  - [V] The self-generated corpus (p. 3–4).
  - [V] The anchor set: 149 previously published hallucinated names, taken from the Trend Micro slopsquatting dataset and the DepScope corpus (p. 2–4).
  - The selection rule for the anchor set is not reported beyond "circulated long enough to attract registration" (p. 1, p. 5).
- Sample size (N) and unit:
  - [V] 4,800 generations plus 2,000 more, 6,800 in total. These produced 1,186 + 455 = 1,641 distinct confirmed hallucinated names (p. 4).
  - [V] Of the 149 anchor names, 22 are registered (p. 5).
- Sampling / selection method: [V] Generations rotate evenly across the five models (p. 5). Not reported: the size of the task set, the prompt texts, and the split between languages.
- Data availability (public? link?): [A] Code, configuration and snapshot hashes "will be deposited" with a DOI. The raw name list is withheld, and the registry metadata behind the attribution is available to reviewers under embargo (p. 8–9). We did not check whether any deposit exists.

## 5. Experimental setup
- Procedure, settings, hyper-parameters, tools:
  - [V] Temperatures 0.7 and 1.0, fixed seeds, Ollama runtime (p. 3).
  - Not reported: seed values, maximum tokens, quantization level, hardware.
  - [V] All 1,641 names were re-checked live on 2026-07-04 (p. 5). The date of the anchor-set check is not reported.
  - [V] The check was validated on 17 known-real names and 8 synthetic fake names; precision and recall were both 1.000 (p. 4).
  - [A] The author says every headline count was recomputed independently (p. 4); the procedure is not described.
- Funding and conflicts of interest: not reported.
- Code availability: [A] promised for later deposit (p. 8). We did not check whether the deposit exists.

## 6. Evaluation metrics
- Metric — what it measures — why chosen:
  - [V] The number of distinct confirmed hallucinated names, and new names per generation, used to judge whether the name space runs out (p. 4).
  - [V] The share of names that are registered, with a rule-of-three 95% upper bound (p. 5–6). (Rule of three: when 0 of n cases are observed, the 95% upper bound is about 3/n.)
  - [V] An intent classification of registered names (p. 5–6).
  - No hallucination rate is reported.
- Statistical testing (tests used, significance, effect sizes, confidence intervals): [V] Only rule-of-three upper bounds: below 0.2% (1,641 names), about 14% (22 names), about 2% (149 names) (p. 5–6).

## 7. Key findings
1. [V] **No saturation.** New hallucinated names keep appearing at almost the same rate: 0.228 new names per generation in the extra run vs 0.247 in the first (p. 4).
   - 450 of the 455 new names came from a single model.
   - 82 of the first 1,186 names came from two or more models (p. 4).
2. [V] **Self-generated names are unregistered.** All 1,641 were still unregistered on 2026-07-04; the 95% upper bound is below 0.2% (p. 5).
3. [V] **Public names that are registered.** 22 of the 149 anchor names are registered (p. 5–6):
   - 19 defensive placeholders;
   - 1 organic name collision;
   - 1 individual reservation;
   - 1 typosquat from 2019;
   - 0 malicious (95% upper bound about 14%).
4. [V] **The 19 placeholders.** They all carry the same summary, "Benign slopsquatting research package" (p. 5). [A] The author attributes all 19 to one anonymous operator using numbered account aliases, based on blank identity fields, account names and upload bursts. This evidence sits in withheld registry metadata and can be verified only under embargo (p. 6).
5. [V] **Negative control.** In the 2,000 extra generations, 11 names were absent from the snapshot but live at check time. All were registered years before t0 (2014–2023), so they are names the npm mirror missed, not new registrations after t0 (p. 7). [A] The author calls this negative control "essentially uninformative" about future registrations, because the window is only a few days (p. 7).
6. [V] **Install-time execution.** In an offline lab, a harmless package ran code at install time under both pip (`setup.py` during the build) and npm (`postinstall`), before it was imported (p. 7).
7. [A] **npm mirror reliability.** The author describes the public npm name mirror as unreliable: it lists more names than npm's own total yet misses real packages (p. 3). [V] This is partly supported by the 11 negative-control names that existed before t0 but were missing from the mirror (p. 7).
8. [A] **Secondary claims from grey sources**, not verified by this paper (p. 2):
   - a hallucinated name, `huggingface-cli`, registered by Lanyado, drew more than 30,000 downloads in three months;
   - a hallucinated npm name spread to 237 GitHub repositories before it was defensively claimed.

## 8. Limitations stated by the authors
- [A] "Zero malicious" does not mean zero risk. "Benign now" applies only to the current version, since a placeholder can be weaponised in a later release (p. 8).
- [A] The registered sample is small (22 of 149) and biased towards names claimed by defenders. One person assigned the intent labels (p. 6, p. 8).
- [A] The corpus is a lower bound, because false inclusions in the npm mirror hide some real hallucinations (p. 3, p. 8).
- [A] The corpus is self-generated, not real production traffic (p. 8).
- [A] The time window is short (p. 7–8).

## 9. Limitations we identified
- [I] **The "zero claimed" result is close to certain by design.** The names were generated privately and re-checked only 4 days after the snapshot (p. 3, p. 5). The 0 of 1,641 result therefore says almost nothing about attacker behaviour.
- [I] **No hallucination rate is reported.** The paper gives neither a per-mention nor a per-generation rate, so it cannot contribute rates to RQ1. The task set, prompts and quantization are unknown.
- [I] **Cited numbers are misreported.**
  - It describes Spracklen's 21.7% as a share "of generations" (p. 1). Spracklen measures per recommended package, and 21.7% is an average over tests [@spracklen2024we, p. 7; @spracklen2024we, p. 20].
  - It quotes Churilov's 4.62–6.10% "per generation", 127 universal names and 53 registrable names (p. 1–2). These are Churilov's version 1–3 figures, superseded in version 4 [@churilov2026range, p. 10–11], and they were per-mention rates.
- [I] **The anchor-set selection is unclear** (p. 4–5). The date of the anchor check is missing.
- [I] **Static inspection may miss payloads.** Reading only setup and manifest files can miss malicious code inside modules or code that runs at import time. Wheel-only packages are not discussed (p. 4).
- [I] **The attribution cannot be checked.** The single-operator attribution rests on withheld metadata (p. 6).
- [I] **The grey-source exploitation figures** (p. 2) are not verified by this paper. Use them only through their original sources, which would be tier 5 (vendor and researcher blogs).
- [I] **No funding or conflict-of-interest statement**, despite the company affiliation (p. 1).

## 10. Threats to validity
- Internal (confounds, leakage, selection):
  - [A] The anchor set over-represents names claimed by defenders (p. 6).
  - [I] A single adjudicator assigned the labels (p. 8).
- External (generalisability of sample/context):
  - [A] Only small local open-weight models, and no agent traffic (p. 8).
  - [I] Only PyPI and npm, with one snapshot.
- Construct (do metrics measure the concept?):
  - [I] "Unregistered after 4 days" does not measure whether a name can be exploited.
  - [V] The two-check definition is sound as of t0 (p. 3).
  - [I] It ignores packages registered after the model's training cutoff (compare krishna2025importing).
- Statistical conclusion (power, multiple comparisons, variance): [V] Only rule-of-three bounds are given (p. 5–6). [I] The bound on the malicious share, about 14%, is wide (p. 6).
- Reproducibility (data/code/setup reported?):
  - [A] Code and snapshot hashes are promised but not yet deposited (p. 3, p. 8).
  - [I] Prompts, seeds and the task set are not given.

## 11. Future research directions
- Stated by authors [A] (p. 8):
  - keep watching the 1,641 names over time;
  - move from self-generated output to live coding-agent traffic;
  - use larger gated corpora that are not pre-filtered by public visibility.
- Suggested by us [I]:
  - report hallucination rates with their denominators;
  - publish the prompt set;
  - re-check registrations at 3, 6 and 12 months;
  - inspect wheel contents as well;
  - combine with Churilov's six-month registration data.

## 12. Relevance to our research
- Research questions addressed (RQ ids): RQ2, RQ4, RQ5.
- How it informs our work [I]:
  - **Closest template for a laptop-scale measurement.** It runs local Ollama models (p. 3) and uses a pipeline we can reuse:
    - a frozen, hashed registry snapshot (PyPI simple index, PEP 503-normalised; npm names lowercased) as an offline first filter;
    - a live 404 check to confirm;
    - `ast` and acorn parsers;
    - an import-to-package mapping;
    - standard-library exclusion (p. 3).
  - **Pitfall to avoid.** The author reports that the npm name mirror is unreliable (p. 3, p. 7), so the live registry should be the ground truth.
  - **Reproduction gaps.** The task set, prompts, seeds and hardware are missing.
  - **Weight in synthesis.** Its registration results agree with churilov2026range (about 1% registered within six months, one with malware): weaponised slopsquatting looks rare so far. As tier-4 evidence, it can only corroborate RQ2 claims, not carry them.

## 13. Evidence table (for the evidence matrix)
| RQ | Claim | Page | Label | Strength |
|---|---|---|---|---|
| RQ1 | Five local open-weight models keep inventing new names (0.228 vs 0.247 new names per generation; no saturation over 6,800 generations) | 4 | [V] | weak |
| RQ2 | 0 of 1,641 self-generated hallucinated names registered 4 days after the snapshot (95% upper bound below 0.2%) | 5 | [V] | weak |
| RQ2 | 22 of 149 publicly listed hallucinated names registered; 0 malicious (95% UB ~14%); 19 share a "Benign slopsquatting research package" summary | 5–6 | [V] | weak |
| RQ2 | The 19 placeholders come from one anonymous operator (evidence in withheld metadata) | 6 | [A] | weak |
| RQ2 | Most newly found names are single-model (450 of 455), while the cross-model set is captured early | 4 | [V] | weak |
| RQ2 | Install-time code execution confirmed offline for pip (setup.py) and npm (postinstall) | 7 | [V] | weak |
| RQ2 | Grey-source reports: huggingface-cli >30,000 downloads in 3 months; an npm hallucinated name in 237 GitHub repos (not verified here) | 2 | [A] | weak |
| RQ4 | Two-oracle gate (frozen hashed t0 snapshot + live 404) | 3 | [V] | weak |
| RQ4 | Public npm name mirror unreliable; partly supported by 11 pre-t0 names missed by the mirror | 3, 7 | [A] | weak |
| RQ5 | Measurement on live coding-agent traffic proposed as future work | 8 | [A] | weak |

## 14. Key quotes
> "Every one is still unregistered." (p. 5)

> "A generated name is admitted as a confirmed hallucination only if it passes both oracles" (p. 3)

> "The npm name mirror we snapshot is unreliable" (p. 3)

## Analyst notes
- Reading coverage: the whole paper was read (p. 1–9), including the references.
- DOI: …426 is the Zenodo concept DOI and …427 the version DOI of the same deposit. The orchestrator resolved this via the Zenodo API on 2026-11-12. `rlab validate` reports MISMATCH only because Crossref has no record of DataCite DOIs; OpenAlex matches.
- Tier: 4. Reasoning is in the header.
- The rule-of-three bounds were recomputed: 3/1,641 = 0.18%, 3/22 = 13.6%, 3/149 = 2.0%. All are consistent with the paper.
