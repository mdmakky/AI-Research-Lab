---
key: liu2026trust
status: complete
evidence_basis: full-text
design: Attack paper; controlled experiment comparing direct injection, Bayesian-optimisation and LLM-driven optimisation of malicious Skill files, plus a detection test against 8 Skill scanners
dataset: Spracklen et al. package-hallucination prompt benchmark (LLM_AT, LLM_LY, SO_AT, SO_LY), filtered to prompts about one source package (requests, numpy, django)
sample_size: 5 open-weight models (Llama-3.1-8B, Phi-4-mini, Qwen2.5-Coder 7B/14B/32B); 10% held-out test prompts, N=1 completion each; exact prompt counts not reported
metrics: Targeted hallucination rate (THR, share of outputs containing the attacker-chosen package); general hallucination rate (GHR); detected/not detected per scanner
main_finding: A third-party Skill file can steer open-weight coding models to import an attacker-chosen package in up to 100% of test prompts; static Skill scanners missed it.
relevance: high
analysed: 2026-11-12
---
<!-- Frontmatter: single-line values; they feed literature-matrix.md via `rlab index`.
     status: draft (in progress) -> ready (analyst self-check passed) -> complete (critical review passed).
     evidence_basis: full-text | abstract-only. abstract-only analyses must not fill methodology detail.
     relevance: high | medium | low. -->

# Trust Me, Import This: Dependency Steering Attacks via Malicious Agent Skills

- Authors: Liu, Yiyong; Hsu, Chia-Yi; Huang, Chun-Ying; Backes, Michael; Wen, Rui; Yu, Chia-Mu
- Year / venue: 2026, arXiv (preprint)
- DOI: 10.48550/arxiv.2605.09594 · URL: https://arxiv.org/abs/2605.09594
- Source text: `fulltext.txt` (page refs = PDF page index)

Labels: **[V]** verified in the paper's own data/tables/results · **[A]** author claim · **[I]** our interpretation.
Every [V]/[A] item ends with a page ref `(p. N)`. Write "not reported" when the paper does not say.

Analyst note on scope: this is an attack paper. This analysis records what was measured and how well, for threat-model and defence purposes; it does not reproduce the optimisation procedure in operational detail.

## 1. Research objective
[A] Show that package hallucination is not only a passive model error but can be actively induced: a malicious persistent instruction artifact ("Skill", e.g. SKILL.md, Cursor Rules) can bias a coding agent toward an attacker-chosen package during benign coding tasks, without changing model weights, training data or the user's prompt (p. 1). The paper calls this "Dependency Steering" (p. 1, p. 3).

## 2. Research questions / hypotheses
Not stated as numbered RQs. Implicit questions [I]: (a) does a Skill that names a target package raise how often that package appears in generated dependencies; (b) does optimising the Skill text raise it further while keeping the Skill plausible; (c) does the effect transfer across models, prompts and domains; (d) do existing Skill scanners detect such Skills (pp. 2–3, 9–12).

## 3. Methodology
- Research design: controlled black-box experiment on open-weight models; three attack conditions compared against a benign-Skill baseline (pp. 4–7).
- Approach / model / intervention: (1) direct injection — the Skill explicitly recommends the target package (p. 4); (2) Bayesian optimisation over a fixed set of semantic mutation operators, refined by a genetic algorithm (p. 4); (3) the authors' method, adapted from the AutoDAN-Turbo jailbreak framework: an LLM-generated patch appended to an otherwise benign Skill, scored by an LLM judge on target inclusion, stealth and fluency, with a strategy library reused across rounds (p. 5).
- Baselines or comparison conditions: benign Skill (general hallucination rate, Table I, p. 7); direct injection (Table II, p. 7); Bayesian optimisation (Table III, p. 8).

## 4. Dataset and sample
- Data source(s): the four prompt sets from Spracklen et al. — LLM-generated and Stack Overflow prompts, each in all-time and last-year variants (p. 6). This links the paper directly to [@spracklen2024we].
- Sample size (N) and unit: prompts filtered to those about the source package (default `requests`), split 90% optimisation / 10% evaluation (p. 6). The absolute number of test prompts is not reported. [I] The reported percentages are consistent with small, model-dependent denominators (e.g. 78.57% = 11/14, 93.55% = 29/31, 97.30% = 36/37; Table IV, p. 8), so each cell probably rests on about 14–77 outputs (e.g. Phi-4-mini 35.06% = 27/77); some values (9.13%, 56.21%, 63.50%) fit no simple fraction, which suggests unexplained averaging.
- Sampling / selection method: filtering by source package; no further detail (p. 6).
- Data availability (public? link?): not reported. No code or artifact link found in the paper.

## 5. Experimental setup
- Procedure, settings, hyper-parameters, tools: five open-weight models — Llama-3.1-8B, Phi-4-mini, Qwen2.5-Coder 7B/14B/32B (p. 6). Target temperature 0.6, top_p 0.9; proxy LLM temperature 0.7; one completion per test prompt (p. 6). Bayesian optimisation used a 300-iteration budget; the authors' method used 10 iterations per target (p. 6). Main results use the "Unconstrained Mode" (stealth and fluency weights set to 0, veto off), i.e. they maximise inclusion only (p. 6). Only Python tasks (p. 6). The default target package is `awesome_request` (p. 6). The authors state the target packages are benign and were released only to simulate attacks (p. 14); whether they exist on PyPI is unclear.
- Detection test: 3 static scanners, 4 LLM/agent-based auditors and 1 commercial sandbox (SandyClaw) (p. 11); an adaptive variant feeds scanner feedback back into optimisation on Qwen2.5-Coder-7B (p. 12).
- Code availability: not reported.

## 6. Evaluation metrics
- Targeted hallucination rate (THR) — share of benign prompts whose dependency-related output (imports, `pip install`, requirements entries) contains the attacker-chosen package (p. 3, p. 6). It measures attack success at the generation step only.
- General hallucination rate (GHR) — share of outputs containing any non-existent package other than the target (p. 6).
- Detection outcome per scanner: detected / not detected / "low" severity (Table IX, p. 12).
- Statistical testing: none. Repeated-run variability is reported only as a standard deviation not exceeding 6.5% (p. 11). No confidence intervals or significance tests.

## 7. Key findings
1. With a benign Skill, general hallucination rates were 0%–32.37%; Phi-4-mini on LLM_LY was highest; Qwen2.5-Coder 14B/32B were at or near 0% on several sets — [V] (p. 7)
2. Direct injection (Skill openly recommends the package) reached THR of 1.52%–87.50%; Qwen2.5-Coder models were most susceptible (e.g. 32B: 87.50% on LLM_AT) — [V] (p. 7)
3. The optimised attack reached THR of 21.43%–100%; Qwen2.5-Coder-32B: 100% (LLM_AT), 97.30%, 62.07%, 63.50%; Llama-3.1-8B: 78.57% on LLM_AT — [V] (p. 8)
4. Lookalike names close to a real package (e.g. a one-letter typo of `requests`) were often auto-corrected by the model under the baselines (0% on Qwen2.5-Coder-14B) but reached 61%–100% under the optimised attack — [V] (p. 8, p. 9)
5. Optimised Skills transferred across models (many Qwen cells above 80%) and across domains, and test-prompt THR was comparable to training-prompt THR — [A] (p. 9, p. 10)
6. Hiding the package name completely (explicitness levels 4–5) dropped THR to 0%; the name must appear in some form for the attack to work — [V] (p. 10)
7. Longer Skills diluted the effect for most models (e.g. Qwen2.5-Coder-7B 89.66% short vs 27.59% long) — [V] (p. 11)
8. Two static scanners missed the Skills and the third flagged them only as "low" severity; among LLM/agent auditors only Snyk Agent Red Teaming detected them; the sandbox (SandyClaw) detected all five — [V] (p. 12)
9. With scanner feedback in the loop, the Skill evaded Snyk and was downgraded by SandyClaw, at a THR of 65.52% on Qwen2.5-Coder-7B — [A] (p. 12)

## 8. Limitations stated by the authors
- [A] Only open-source models; closed commercial agents were not tested (p. 12).
- [A] The prompt distribution cannot fully represent real software-engineering workflows (p. 12).
- [A] Measures dependency generation, not end-to-end compromise after installation (p. 12).
- [A] Future defences designed for persistent steering may be stronger (p. 12).

## 9. Limitations we identified
- [I] Small and unreported test sets: N=1 completion on a 10% split, with percentages implying about 14–77 outputs per cell (some values unexplained); differences of 5–10 points are within noise.
- [I] Main results use Unconstrained Mode (stealth weight 0). The stealth claims and the detection test may therefore apply to different Skills than the headline THRs; the paper does not state which mode produced the Skills in Table IX.
- [I] The models are 8B–32B open-weight models served directly, not agents with tool use. "Coding agent" in the title is broader than what was tested.
- [I] The judge, attacker and scorer are LLMs; the scoring rubric and proxy models are not fully specified, which limits reproducibility.
- [I] Reference [36] for "Llama-3.1-8B-Instruct" is a security-tuned Llama derivative's technical report (p. 15), so the exact model checkpoint is ambiguous.
- [I] Minor reporting errors: the THR definition is cited as Section IV-C but appears in Section III-A (p. 3, p. 6); one Table I value lacks a % sign (p. 7).
- [I] Detection is reported as binary per model, without false-positive rates of the scanners on benign Skills.

## 10. Threats to validity
- Internal: the same benchmark family is used to optimise and evaluate (90/10 split); the risk of leakage across near-duplicate prompts is not discussed.
- External: Python only; five open-weight models; one placeholder target name by default; no real IDE agent or closed model.
- Construct: THR counts any appearance of the name in dependency outputs (mention, import or install command), not an actual install. That is appropriate for a generation-step attack but overstates installation risk.
- Statistical conclusion: no CIs or tests; small denominators; single completion per prompt (only the stability check repeats runs, p. 11).
- Reproducibility: no code or data link found; hyper-parameters are partly reported (p. 6).

## 11. Future research directions
- Stated by authors [A]: defences designed specifically against persistent behavioural steering (p. 12); the attack is argued to generalise to other persistent instruction artifacts such as Cursor/Windsurf rules and repository instruction files (p. 12).
- Suggested by us [I]: (a) measure whether a pre-install guard (registry existence + metadata checks, as in [@raj2026names]) blocks the steered package at install time, which is independent of how the name was induced; (b) test closed agents with real tool use; (c) report scanner false-positive rates on benign Skills.

## 12. Relevance to our research
- Research questions addressed (RQ ids): RQ1 (baseline hallucination rates for 5 open models), RQ2 (exploitability: an attacker can induce a chosen name rather than wait for one), RQ3 (Skill scanners as a defence and how they fail), RQ5 (agent instruction files as an untested attack surface for client-side guards).
- How it informs our work [I]: this changes the threat model behind G2. If an attacker can make an agent emit a specific package name on demand, defences that only rely on the model not hallucinating are insufficient; an install-time check (does the package exist, is it new, does it have maintainers and a repository) is the layer that still applies. It also shows that static Skill scanners missed these Skills, which supports evaluating guards at the package-install step rather than at the instruction-file step.

## 13. Evidence table (for the evidence matrix)
| RQ | Claim | Page | Label | Strength |
|---|---|---|---|---|
| RQ1 | With a benign Skill, general hallucination rates for 5 open models were 0%–32.37% (highest Phi-4-mini on LLM_LY; Qwen2.5-Coder 14B/32B near 0%) | 7 | V | weak |
| RQ2 | A Skill that openly recommends a non-existent package makes models emit it in 1.52%–87.50% of benign prompts | 7 | V | weak |
| RQ2 | An optimised malicious Skill raised targeted hallucination to 21%–100% (Qwen2.5-Coder-32B: 100% on LLM_AT) | 8 | V | weak |
| RQ2 | Typo-like target names were auto-corrected under the baselines but not under the optimised attack | 8, 9 | V | weak |
| RQ2 | Hiding the package name entirely (explicitness levels 4–5) reduced targeted hallucination to 0% | 10 | V | weak |
| RQ3 | Of three static Skill scanners, two missed the optimised Skills and one flagged them only as low severity; only 1 of 4 LLM/agent auditors and the sandbox detected them | 12 | V | weak |
| RQ3 | Feeding scanner feedback into optimisation evaded Snyk and downgraded the sandbox verdict, with THR 65.52% | 12 | A | weak |
| RQ5 | Experiments used open-source coding LLMs rather than closed-source commercial agents, and measured dependency generation rather than end-to-end compromise after installation | 12 | A | weak |

## 14. Key quotes
> "we show that this risk is not only a passive model failure. It can be actively induced through the persistent Skill artifact." (p. 1)
> "our evaluation mainly measures dependency-generation behavior rather than full end-to-end compromise after malicious package installation." (p. 12)
> "To avoid causing real-world harm, we do not publish or deploy any malicious packages." (p. 14)

## Analyst notes
- Reading coverage: whole paper read (pp. 1–16), including appendix A–C. References skimmed.
- Shared authorship: three authors (Hsu, Huang, Yu) also wrote [@hsu2026harmless], which uses the same benchmark and scanner set; scanner results across the two papers are not independent replications.
- Uncertainties: absolute test-set sizes; which optimisation mode produced the Skills used in the detection test; exact Llama checkpoint.
- Ethics: the authors used benign placeholder packages and did not publish malicious packages (p. 14).
