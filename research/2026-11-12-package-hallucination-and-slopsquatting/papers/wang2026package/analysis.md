---
key: wang2026package
status: complete
evidence_basis: full-text
design: Attack paper; controlled end-to-end simulation with real agent frameworks, a local PyPI mirror hosting benign look-alike packages, 5 baseline prompt-injection attacks, and a detector evaluation
dataset: BigCodeBench (981 victim tasks, 5 packages), DS-1000 (772 tasks, 4 packages), RefactorBench (43 tasks, 5 packages); 200 rule files (100 benign, 100 injected) for detection
sample_size: 8 agent frameworks (incl. Claude Code, Cursor), 13 backbone LLMs (incl. GPT-5.5, Claude Sonnet 4.6); per-cell denominators not stated (inferred about 9-100 tasks)
metrics: SASR (share of tasks importing the look-alike package), DASR (look-alike imported and code executed), attention proportion, detector FNR/FPR
main_finding: An injected prompt in a shared rule file made agents swap a real package for a look-alike in 79% of BigCodeBench tasks on average; Claude Code was most resistant (31-59%).
relevance: high
analysed: 2026-11-12
---
<!-- Frontmatter: single-line values; they feed literature-matrix.md via `rlab index`.
     status: draft (in progress) -> ready (analyst self-check passed) -> complete (critical review passed).
     evidence_basis: full-text | abstract-only. abstract-only analyses must not fill methodology detail.
     relevance: high | medium | low. -->

# Package Hallucination Attacks on Coding Agents through Prompt Injection in Rule Files

- Authors: Wang, Yupu; Jiang, Zhengyuan; Wang, Reachal; Gong, Neil Zhenqiang
- Year / venue: 2026, arXiv (preprint)
- DOI: 10.48550/arxiv.2610.09264 · URL: https://arxiv.org/abs/2610.09264
- Source text: `fulltext.txt` (page refs = PDF page index)

Labels: **[V]** verified in the paper's own data/tables/results · **[A]** author claim · **[I]** our interpretation.
Every [V]/[A] item ends with a page ref `(p. N)`. Write "not reported" when the paper does not say.

Analyst note on scope: this is an attack paper. This analysis records what was measured and how well, for threat-model and defence purposes; it does not reproduce the optimisation procedure in operational detail.

## 1. Research objective
[A] Define a "package hallucination attack" in which an attacker injects a prompt into a community-shared rule file (AGENTS.md, CLAUDE.md, .cursorrules) so that a coding agent replaces a legitimate dependency with an attacker-controlled look-alike package, and propose PackHallu, a black-box optimiser for such injected prompts (p. 1, p. 2). Note: the paper's "package hallucination" is induced substitution of a specific attacker package, not the spontaneous invention of non-existent names studied by most of our corpus (p. 1).

## 2. Research questions / hypotheses
Not stated as numbered RQs. Implicit questions [I]: (a) are existing prompt-injection attacks effective when embedded in long rule files; (b) does an optimised injected prompt work, and does it transfer across LLMs, agent frameworks and task distributions; (c) do existing prompt-injection detectors catch it (pp. 2–3).

## 3. Methodology
- Research design: controlled end-to-end simulation. Agents run in autonomous mode with confirmations disabled; look-alike packages are hosted on a local registry that mirrors PyPI so the agent can `pip install` them on demand (p. 8, p. 10).
- Approach / model / intervention: PackHallu is an evolutionary search that uses a locally run surrogate agent (default: OpenHands + Qwen3-Coder-30B), scores candidates on the agent's full reasoning trajectory rather than only final code, and uses an LLM to critique failed candidates (p. 2, p. 5, p. 8). One prompt is optimised for the numpy pair and reused for other packages by swapping names (p. 12).
- Baselines or comparison conditions: two heuristic attacks (Combined, Repeat) and three optimisation attacks (GCG, ObliInjection — both given white-box access — and TAP) (p. 8, p. 9).

## 4. Dataset and sample
- Data source(s): BigCodeBench (5 third-party packages, 80/20 victim/surrogate split), DS-1000 (pandas, numpy, matplotlib, scipy), RefactorBench (kombu, twisted, urllib3, asgiref, werkzeug) (p. 9, p. 10).
- Sample size (N) and unit: 981, 772 and 43 victim tasks respectively (p. 9); per-package counts e.g. pandas 341, numpy 267 BigCodeBench victim tasks (p. 28). SASR is computed only over tasks where the agent imports the real package under benign conditions (p. 11), and these subset sizes are not reported. [I] Percentages imply much smaller denominators than the task counts (e.g. 98.72% and 1.28% = 77/78 and 1/78 for pandas on Qwen3-Coder-30B, p. 11), so cells rest on about 9–100 tasks (inferred; e.g. 99.00% = 99/100 for Llama-4 matplotlib, p. 14; DASR 11.11% and 33.33% imply about 9 for Qwen2.5-Coder-7B seaborn, p. 11).
- Sampling / selection method: tasks grouped by the package they require; RefactorBench packages chosen by frequency (p. 10).
- Data availability (public? link?): no code or data release link found in the paper (searched for repository links and release statements).

## 5. Experimental setup
- Procedure, settings, hyper-parameters, tools: 8 frameworks — OpenHands, OpenCode, Aider, Pi Coding Agent, Cline, Kilo Code, Claude Code, Cursor (p. 8). 13 backbone LLMs, including GPT-5.5, GPT-5.3-Codex, Claude Sonnet 4.6, DeepSeek-V4-Flash, Llama-4-Maverick (p. 8, p. 14, p. 16). The look-alike package mirrors the real package's interface and only prints a fixed message when invoked; names use a `_hl` suffix (p. 10). Injection at the start of the rule file by default (p. 12). Search settings R=20, N=3, K=5, T=10 (p. 12).
- Detection: 200 rule files (100 public benign files plus 100 injected counterparts) tested against ProtectAI-DeBERTa, PromptGuard, DataSentinel, PromptArmor (GPT-5 judge) and PIShield (p. 18, p. 19).
- Code availability: not reported.

## 6. Evaluation metrics
- SASR (syntactic attack success rate) — share of tasks where the generated code imports the look-alike package, among tasks that import the real package under benign conditions (p. 11).
- DASR (deployable attack success rate) — additionally requires the code to execute and the look-alike's marker behaviour to run (p. 12). This is closer to real harm than import-only metrics.
- Attention proportion — share of model attention on injected tokens (p. 12, p. 13).
- Detector FNR / FPR (p. 19).
- Statistical testing: Pearson correlations (e.g. r = 0.785 capability vs SASR across LLMs, p. 15; r = −0.186 across frameworks, p. 16); mean ± SD across 5 initialisations (p. 18). No confidence intervals or significance tests for SASR/DASR.

## 7. Key findings
1. Averaged over 5 packages and 5 backbone LLMs on BigCodeBench, PackHallu reached 79.29% SASR and 67.68% DASR; the next-best baseline (Combined Attack) reached 14.99% / 11.35% — [V] (p. 12)
2. More popular packages were harder to substitute (median r = −0.69 between success and PyPI downloads); numpy and scipy were hardest, seaborn easiest — [V] (p. 13)
3. Prompts optimised on one LLM transferred to others in the same framework; 8 of 12 victim LLMs exceeded 90% SASR on at least 3 of 5 packages, e.g. GPT-5.5 97.92% on pandas — [V] (p. 14)
4. More capable backbone LLMs were more susceptible (r = 0.785 between task capability and SASR) — [V] (p. 15)
5. Across frameworks with the same LLM, average SASR was 71.55% and DASR 62.99%, with no relation to capability (r = −0.186) — [V] (p. 15, p. 16)
6. On commercial agents: Cursor 69%–98% SASR; Claude Code with Sonnet 4.6 31.03%–58.95% SASR, the most resistant — [V] (p. 16)
7. Effect weakened as context grew: 53.33% SASR on DS-1000 and 18.60% on repository-level RefactorBench — [V] (p. 16)
8. Claude Code case study (87 numpy tasks): 27 successes (31%); 16 suspicion-based refusals (18.4%); in 33 cases (37.9%) the agent first imported the look-alike, the import failed, and it reverted to numpy instead of running `pip install` — [V] (p. 17, p. 27)
9. No detector was usable: FNR/FPR were ProtectAI 100%/3%, PromptGuard 46%/5%, DataSentinel 49%/16%, PromptArmor 20%/34%, PIShield 21%/11% — [V] (p. 19)

## 8. Limitations stated by the authors
- [A] No dedicated limitations section. The authors note that a real-world attack would expose users to compromise and contaminate registries, so they used a controlled local registry and benign marker packages (p. 10).
- [A] Repository-level tasks reduce effectiveness because the injected prompt becomes a smaller share of the input (p. 16).

## 9. Limitations we identified
- [I] Denominators are not reported; the SASR subset (tasks that import the real package under benign conditions) appears much smaller than the task counts in Table 15.
- [I] Loose wording: the Claude Code case study speaks of "the whole 87 victim tasks from the numpy subset" (p. 16), while Table 15 lists 267 numpy victim tasks (p. 28). The 87 is the SASR denominator (tasks where Claude Code imports numpy under benign conditions): 27/87 = 31.03% matches Table 6 (p. 16) and the Table 14 counts sum to 87 (p. 27). Not an error, but it shows how small the SASR subsets are.
- [I] The number of runs per cell is not reported; only the initialisation study reports variability (p. 18).
- [I] The look-alike names follow one pattern (`_hl` suffix). The attack substitutes a specific package and does not measure spontaneous hallucination, so its rates must not be compared with the hallucination rates in [@spracklen2024we] or [@spracklen2026llm].
- [I] Autonomous mode with confirmations disabled is a worst case. The paper does not test the default, confirmation-on configuration that many users run.
- [I] The F2 behaviour (agent reverted instead of installing the missing package) shows that DASR depends on whether the agent installs packages on its own. That install decision is not separately measured across agents.

## 10. Threats to validity
- Internal: surrogate tasks are a disjoint 20% of BigCodeBench (p. 10); in the main experiments the surrogate and victim agent are identical (p. 12), so main-table numbers are a white-box-like upper bound; the transfer tables address this.
- External: Python only; 10 packages; local mirror rather than real PyPI; one injection per rule file.
- Construct: SASR = import of the look-alike; DASR = execution of a benign marker. Neither measures real-world installation from the public registry.
- Statistical conclusion: no CIs; small and unreported per-cell denominators; many comparisons.
- Reproducibility: framework configurations are documented in Table 19 (p. 30); code release not reported.

## 11. Future research directions
- Stated by authors [A]: robust defences for the collaborative rule-file pipeline (p. 20); defences tailored to package hallucination attacks, because general prompt-injection detectors fail (p. 19).
- Suggested by us [I]: (a) an install-time guard that blocks packages that are new, unknown or name-similar to a popular package, which would stop the `_hl`-style substitution regardless of how it was induced; (b) measure how often agents in default mode actually run `pip install` for unknown names (the F2 pattern is evidence they sometimes do not); (c) report denominators and repeated runs.

## 12. Relevance to our research
- Research questions addressed (RQ ids): RQ2 (exploitability: induced substitution with real agents and a working local registry), RQ3 (prompt-injection detectors as a defence), RQ5 (agent install behaviour; commercial agents tested).
- How it informs our work [I]: this is the closest existing work to G1. It runs real agents (including Claude Code and Cursor) end-to-end against a local PyPI mirror, which is the setup our G1 design proposes. The difference is that here the package is induced by an attacker, whereas G1 asks how often agents spontaneously try to install non-existent packages on ordinary tasks. The F2 finding (agents reverted instead of installing in 37.9% of Claude Code cases) is direct evidence that agent install behaviour varies and must be measured, not assumed. For G2, the detector table shows that checking the instruction file is not enough, which supports a guard at the install step.

## 13. Evidence table (for the evidence matrix)
| RQ | Claim | Page | Label | Strength |
|---|---|---|---|---|
| RQ2 | An optimised prompt injected into a shared rule file made agents import an attacker look-alike package in 79.29% of BigCodeBench tasks on average (DASR 67.68%) | 12 | V | weak |
| RQ2 | Popular packages were harder to substitute (median r = −0.69 between attack success and PyPI downloads) | 13 | V | weak |
| RQ2 | More capable backbone LLMs were more susceptible (r = 0.785 between capability and SASR) | 15 | V | weak |
| RQ2 | Commercial agents were affected: Cursor 69%–98% SASR, Claude Code with Sonnet 4.6 31%–59% | 16 | V | weak |
| RQ2 | Effect fell with larger context: 53.33% SASR on DS-1000, 18.60% on repository-level RefactorBench | 16 | V | weak |
| RQ5 | In 37.9% of Claude Code numpy cases the agent imported the look-alike, saw the import fail, and reverted to numpy instead of installing it | 17, 27 | V | weak |
| RQ3 | Five prompt-injection detectors failed on injected rule files: FNR 20%–100%; the lowest-FNR detector had 34% FPR | 19 | V | weak |

## 14. Key quotes
> "a package hallucination attack causes the agent to import a specific package chosen and controlled by the attacker." (p. 1)
> "Rather than attempting to pip install the missing package, the victim agent reverts to numpy and proceeds" (p. 17)
> "no existing detector reliably identifies our attack while maintaining a usable FPR." (p. 19)

## Analyst notes
- Reading coverage: introduction, related work, problem definition, threat model and method overview read (pp. 1–6); optimisation internals (pp. 6–8) read at overview level only; evaluation, detection and conclusion read in full (pp. 8–20); appendix tables 14–17 checked (pp. 27–28). Remaining appendix prompt figures not reproduced on purpose.
- Uncertainties: per-cell denominators (the 87-task Claude Code subset is the SASR denominator, not an error).
- Ethics: controlled local registry and benign marker packages; no public registration (p. 10).
