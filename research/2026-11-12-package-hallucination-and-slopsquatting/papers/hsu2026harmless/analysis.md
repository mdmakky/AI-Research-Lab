---
key: hsu2026harmless
status: complete
evidence_basis: full-text
design: Attack paper; controlled experiment comparing a benign Skill, a prior hallucination-inducing prompt (IP) and optimised "neutral" Skills (NPA, NPA-Stealth), plus closed-loop agent runs, scanner and runtime-safeguard tests and a 10-person blind rating
dataset: Spracklen et al. package-hallucination benchmark (LLM_AT, LLM_LY, SO_AT, SO_LY); 5% of prompts for optimisation, 95% for evaluation; one public SkillsMP Python Skill as the base
sample_size: 4 main open models (Qwen2.5-Coder 14B/32B, Gemma-3-12B, Nemotron-3-Nano-30B) plus Llama-3.1-8B and GPT-5 for transfer; 3 agents (Claude Code, OpenCode, OpenHands); 10 human raters
metrics: Hallucination ASR (share of responses with at least one non-existent package), Pip Install ASR (share with an install command naming a non-existent package), proposed and executed install rates in agents, scanner detection, Likert ratings
main_finding: Benign-sounding "be imaginative and exhaustive" Skill text raised package hallucination from 3.5% to 57.8% (Qwen2.5-Coder-32B) and agent executed-install rates from about 1-3% to 60-91%.
relevance: high
analysed: 2026-11-12
---
<!-- Frontmatter: single-line values; they feed literature-matrix.md via `rlab index`.
     status: draft (in progress) -> ready (analyst self-check passed) -> complete (critical review passed).
     evidence_basis: full-text | abstract-only. abstract-only analyses must not fill methodology detail.
     relevance: high | medium | low. -->

# Harmless Yet Harmful: Neutral Prompting Attacks for Stealthy Hallucination Steering in Agent Skills

- Authors: Hsu, Chia-Yi; Yu, Chia-Mu; Huang, Chun-Ying; Sakuma, Jun
- Year / venue: 2026, Findings of the Association for Computational Linguistics: EMNLP 2026 (published)
- Source text: `fulltext.txt` (page refs = PDF page index)

Labels: **[V]** verified in the paper's own data/tables/results · **[A]** author claim · **[I]** our interpretation.
Every [V]/[A] item ends with a page ref `(p. N)`. Write "not reported" when the paper does not say.

Analyst note on scope: this is an attack paper. This analysis records what was measured and how well, for threat-model and defence purposes; it does not reproduce the optimisation prompts or example Skills in the appendix.

## 1. Research objective
[A] Show that semantically benign Skill instructions (encouraging imagination, completeness, exhaustive exploration) can raise package hallucination and fake-package install commands in coding agents without any explicit malicious intent or target package. The paper calls this a Neutral Prompting Attack (NPA) (p. 1, p. 2). It positions itself against targeted Dependency Steering [@liu2026trust], which leaves package-specific evidence (p. 1).

## 2. Research questions / hypotheses
Stated by the authors (p. 2):
- RQ1: Can benign prompts amplify package hallucination and installation risk?
- RQ2: Does NPA generalise across models?
- RQ3: How does NPA affect the distribution and exploitability of hallucinated packages?
- RQ4: Can NPA evade existing defences?
- RQ5: Which prompt properties contribute most?

## 3. Methodology
- Research design: controlled experiment on the Spracklen benchmark plus closed-loop agent runs (pp. 4–5).
- Approach / model / intervention: evolutionary search over Skill variants with three LLM-driven edit operators (rewrite a section, inject a section, change framing), scored by the share of hallucinated packages in a shadow model's outputs; NPA-Stealth adds penalties for suspicion and utility loss (pp. 3–4).
- Baselines or comparison conditions: Normal Skill (a public Python-patterns Skill from the SkillsMP marketplace) and IP (Illusionist's Prompt, a prior hallucination-inducing prompt method) (p. 5).

## 4. Dataset and sample
- Data source(s): the four prompt sets of [@spracklen2024we] (p. 4, p. 5).
- Sample size (N) and unit: 5% of prompts for optimisation, 95% for evaluation per dataset (p. 5); absolute prompt counts are not restated. Agent runs use "separate task configurations" whose sizes are not reported (p. 5). Human study: 10 computer-science students (p. 8).
- Sampling / selection method: benchmark reuse; human raters recruited from university labs (p. 8).
- Data availability (public? link?): not reported. The authors deliberately avoid revealing complete fake package names (p. 10).

## 5. Experimental setup
- Procedure, settings, hyper-parameters, tools: decoding and evaluation follow the Spracklen benchmark (p. 5); 50 generations, 20 mutations per generation, beam size 15; about 16–18 minutes per generation on NVIDIA H100/H200 GPUs (p. 5). Package names checked against PyPI; standard-library modules excluded (p. 4, p. 5). One optimisation run per setting (p. 5).
- Agents: Claude Code, OpenCode, OpenHands. Generated hallucination, proposed install and executed install were measured in separate task configurations, not as one pipeline (p. 5).
- Runtime safeguards tested: package existence check, registry lookup, allowlist, environment resolution (p. 8). The implementation of these safeguards is not described in the main text or appendix (Appendix E covers only the Skill scanners, p. 50).
- Code availability: not reported.

## 6. Evaluation metrics
- Hallucination ASR — share of evaluated responses containing at least one package not found on PyPI (p. 5).
- Pip Install ASR — share of responses whose `pip install` commands contain at least one non-existent package (p. 5).
- Agent metrics — generated hallucination, proposed install and executed install rates (p. 6).
- Exploitability audit — unique names, registerable share, persistence across 4 models and 3 prompts, share appearing in install commands, plausibility (p. 7).
- Statistical testing: none reported; single optimisation run per setting (p. 5).

## 7. Key findings
1. With the benign Skill, Hallucination ASR on Qwen2.5-Coder-32B was 3.53% (LLM_AT) and 4.54% (LLM_LY); NPA raised these to 57.76% and 78.99% — [V] (p. 5, p. 6)
2. Effects varied a lot by model: Qwen2.5-Coder-14B rose only from 5.21% to 12.32% on LLM_AT; Nemotron-3-Nano had a high baseline (35.58%–50.20%) — [V] (p. 6)
3. In real agents with a benign marketplace Skill, executed-install rates were 3.33% (Claude Code), 1.05% (OpenCode) and 1.11% (OpenHands); with NPA they were 90.77%, 60.34% and 82.29%; with NPA-Stealth 27.99%–42.52% — [V] (p. 5, p. 6). Caveats: the generated, proposed and executed metrics come from separate task configurations (p. 5), so they are not a funnel (e.g. OpenCode benign: 0.00% proposed but 1.05% executed); "executed install" is not explicitly defined as installing a non-existent package [I]; task counts and the backbone model of each agent are not reported.
4. NPA Skills optimised on Qwen2.5-Coder-32B transferred to GPT-5 (Hallucination ASR 1.28% to 29.29%) but barely to Llama-3.1-8B (16.43% to 17.74%) — [V] (p. 6)
5. NPA concentrated hallucinations onto repeated names: unique-name share fell from 73.7% (Normal) to 54.4%; cross-model persistence across 4 models was 24.17% vs 0%–4.47% for other conditions; over 96% of names were registerable — [V] (p. 6, p. 7)
6. Static Skill scanners did not flag NPA Skills; only Snyk Agent Scan did — [V] (p. 7). The authors state that a variant optimised against Snyk evades detection while keeping high ASR — [A] (p. 7); Table 8 reports only its hallucination and pip rates, not a detection result, and gains are small on some models (Qwen2.5-Coder-14B pip 6.25% vs 3.57%).
7. Package-existence check, registry lookup and environment resolution left Hallucination/Pip ASR near the unprotected level (about 50%–60%; model-level, Qwen2.5-Coder-32B, LLM_AT); only a strict allowlist reduced both to 0% — [V] (p. 8). The authors conclude these checks give "limited mitigation" — [A] (p. 8).
8. In the blind human rating (n=10), NPA scored 5.0/7 suspicion and only 50% would enable it, while NPA-Stealth scored 1.2/7 and 100% would enable it, the same as the benign Skill — [V] (p. 8)
9. "Creativity" wording drove most of the effect (44.60% alone); "exhaustiveness" alone had no effect (3.57%) — [V] (p. 8)

## 8. Limitations stated by the authors
- [A] Python only; JavaScript, Rust and other ecosystems not evaluated (p. 10).
- [A] Output-level evaluation only; no mechanistic analysis (p. 10).
- [A] Not every hallucinated name is immediately exploitable; real risk depends on registration availability, user trust and installation behaviour (p. 10).

## 9. Limitations we identified
- [I] The runtime-safeguard result (finding 7) is hard to interpret. An existence check should, by definition, stop installation of names not on PyPI, yet Pip Install ASR stayed at 51.12%. The metric seems to count fake names in generated commands, not installs that succeed after the check, and the safeguard implementation is not described. Further signs: the "None" row (57.76% / 50.63%) is identical to the model-level Qwen2.5-Coder-32B LLM_AT result in Table 2 (p. 6), so the safeguards were applied to model outputs, not in agents; the existence check even raises Hallucination ASR (59.60%); and environment resolution gives identical 58.56% / 58.56% (p. 8). This finding should not be read as "existence checks do not work".
- [I] One optimisation run per setting and no variance or confidence intervals; agent task-set sizes are not reported.
- [I] Results are sensitive to model choice (finding 2) and to the base Skill; only one marketplace Skill was used as the starting point.
- [I] The human study is small (10 students) and not representative of developers who install Skills.
- [I] Compute (H100/H200, about 15 hours per optimisation) means the attack is expensive to construct, but the resulting Skill is cheap to use.
- [I] Shared authorship with [@liu2026trust] (Hsu, Huang, Yu), with the same benchmark and scanner set; the scanner results are not independent replication.
- [I] Positive: unlike most of our corpus, this paper reports executed installs in real agents under a benign Skill, which gives a baseline rate for unattacked agents.

## 10. Threats to validity
- Internal: shadow model equals victim model in the main results (p. 5), so main numbers are an upper bound; transfer is tested separately (pp. 6–7).
- External: Python/PyPI only; one base Skill; three agents; open models plus GPT-5 for transfer only.
- Construct: Hallucination ASR uses PyPI existence at evaluation time; the date of the PyPI check is not reported, so names registered later (including by squatters) may be misclassified.
- Statistical conclusion: no tests; single runs; small human sample.
- Reproducibility: hyper-parameters are reported (p. 5) and prompt templates are in the appendix; no code or data release is stated.

## 11. Future research directions
- Stated by authors [A]: extend to other ecosystems; mechanistic analysis (p. 10); defences beyond content scanning, such as runtime package verification, registry-aware generation, dependency allowlists, grounded retrieval over package indices, and behavioural auditing of Skills (p. 9, p. 10).
- Suggested by us [I]: (a) test a correctly implemented install-time guard (block non-existent, very new or maintainer-less packages before `pip install` runs) and report blocked installs rather than generated names; (b) measure baseline executed-install rates on larger task sets without any malicious Skill (finding 3 is a first data point); (c) audit agent instruction files for creativity-style wording as a cheap heuristic.

## 12. Relevance to our research
- Research questions addressed (RQ ids): RQ1 (baseline hallucination for 4 models), RQ2 (repeatable, registerable names; cross-model persistence), RQ3 (scanners and runtime safeguards), RQ5 (agent install behaviour measured in Claude Code, OpenCode, OpenHands).
- How it informs our work [I]: this paper narrows G1. It already reports executed-install rates for three real agents under a benign Skill (1.05%–3.33%), although task counts, backbone models and the exact definition of "executed install" are not reported. G1 must therefore be positioned as a larger, more realistic measurement (more tasks, default agent settings, a logging registry proxy, natural rather than benchmark prompts), not as the first measurement. It also matters for G2: its runtime-safeguard table is the only prior evaluation of existence checks in this setting, and its method is unclear. A transparent, reproducible benchmark of install-time guards (G2) would directly resolve that. Finally, because benign-sounding instructions can raise hallucination, model-side defences alone are insufficient, which strengthens the case for the install-time layer.

## 13. Evidence table (for the evidence matrix)
| RQ | Claim | Page | Label | Strength |
|---|---|---|---|---|
| RQ1 | With a benign Skill, Hallucination ASR on the Spracklen benchmark was 3.53%–9.48% for Qwen2.5-Coder-32B and 35.58%–50.20% for Nemotron-3-Nano-30B | 6 | V | moderate |
| RQ5 | With a benign marketplace Skill, executed-install rates in real agents were 1.05% (OpenCode), 1.11% (OpenHands) and 3.33% (Claude Code); task counts, backbone models and the definition of executed install are not reported | 5, 6 | V (numbers) / I (that installs were of non-existent packages) | weak |
| RQ2 | Benign-sounding "imaginative/exhaustive" Skill text raised model-level Hallucination ASR from 3.53% to 57.76% (Qwen2.5-Coder-32B, LLM_AT) and from 4.54% to 78.99% on LLM_LY | 5, 6 | V | moderate |
| RQ2 | Under the same Skill, agent executed-install rates rose from 1%–3% to 60%–91% in Claude Code, OpenCode and OpenHands (task counts not reported) | 5, 6 | V | weak |
| RQ2 | Under NPA, 24.17% of hallucinated names persisted across 4 models (vs 0%–4.47% otherwise) and over 96% of hallucinated names were registerable | 7 | V | weak |
| RQ3 | Static Skill scanners missed NPA Skills; only Snyk Agent Scan flagged them (authors claim a Snyk-aware variant evades it, detection result not tabulated) | 7 | V / A | weak |
| RQ3 | At model level (Qwen2.5-Coder-32B), existence check, registry lookup and environment resolution left Hallucination/Pip ASR near 50%–60%; only a strict allowlist reduced them to 0% (safeguard implementation not described) | 8 | V (numbers) / I (interpretation unclear) | weak |
| RQ4 | Hallucination is checked against PyPI with standard-library modules excluded, but the date of the PyPI check is not reported | 4, 5 | I | weak |

## 14. Key quotes
> "semantically benign instructions, such as encouraging imagination, completeness, or broader exploration, can systematically amplify package hallucination." (p. 1)
> "a strict package allowlist eliminates both attack metrics by restricting dependency selection to a predefined set of trusted packages." (p. 8)
> "We also do not register, publish, or distribute hallucinated package names." (p. 10)

## Analyst notes
- Reading coverage: main paper pp. 1–10 read in full; Appendix E–G (p. 50) read; pp. 11–49 (references, optimisation prompt templates, example Skills) skimmed by search only. The prompt templates were not reproduced on purpose.
- Uncertainties: implementation of the runtime safeguards; agent task-set sizes; PyPI check date.
- Venue: peer-reviewed (EMNLP 2026 Findings). Our copy is the ACL Anthology PDF; identity "probable (title found on first pages)", confirmed by the page-1 header (p. 1).
- Ethics: no names registered; full fake names withheld (p. 10).
