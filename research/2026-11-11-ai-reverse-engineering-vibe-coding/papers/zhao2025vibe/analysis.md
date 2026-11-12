---
key: zhao2025vibe
status: complete
evidence_basis: full-text
design: benchmark construction + comparative evaluation of agent frameworks x LLMs (pass@1, single run)
dataset: SusVibes, 186 security-sensitive feature-request tasks from 100 Python repos (79 CWE types), curated from vulnerability-fix commits
sample_size: 186 tasks x 12 agent settings (3 frameworks x 4 LLMs); 200 candidate tasks human-checked by 5 experts
metrics: FuncPass (pass@1 functional tests), SecPass (pass@1 functional+security tests), SecPass ⊥ FuncPass, CWE-identification P/R/F1
main_finding: Best agent (SWE-agent + Claude 4 Sonnet) passes functional tests on 57% of tasks but only 11.8% are also secure; prompting mitigations trade functionality for little security.
relevance: medium
analysed: 2026-11-11
---
<!-- Frontmatter: single-line values; they feed literature-matrix.md via `rlab index`.
     status: draft (in progress) -> ready (analyst self-check passed) -> complete (critical review passed).
     evidence_basis: full-text | abstract-only. abstract-only analyses must not fill methodology detail.
     relevance: high | medium | low. -->

# Is Vibe Coding Safe? Benchmarking Vulnerability of Agent-Generated Code in Real-World Tasks

- Authors: Zhao, Songwen; Wang, Danqing; Zhang, Kexun; Luo, Jiaxuan; Li, Zhuo; Li, Lei
- Year / venue: 2025, arXiv (preprint)
- DOI: 10.48550/arxiv.2512.03262 · URL: https://arxiv.org/abs/2512.03262
- Source text: `fulltext.txt` (page refs = PDF page index)
- Venue note: `metadata.json` records an arXiv preprint, but the PDF we hold (arXiv v4, 21 Sep 2026) carries the footer "Proceedings of the 43rd International Conference on Machine Learning, Seoul, South Korea. PMLR 306, 2026" (p. 1). Per the project decision in RESEARCH.md, treat as peer-reviewed (ICML 2026, PMLR 306, no DOI). Page refs refer to this arXiv v4 PDF, not PMLR pagination.

Labels: **[V]** verified in the paper's own data/tables/results · **[A]** author claim · **[I]** our interpretation.
Every [V]/[A] item ends with a page ref `(p. N)`. Write "not reported" when the paper does not say.

## 1. Research objective
[A] To test whether code produced by LLM coding agents in a vibe-coding setting (feature request in natural language, little human review) is safe to deploy, by building a benchmark (SusVibes) that scores both functional correctness and security of repository-level feature implementations (p. 1, p. 2).

## 2. Research questions / hypotheses
No formal RQs or hypotheses. Implicit questions from the contributions list:
- [A] How functionally correct and how secure are agent-generated feature implementations in real repositories? (p. 2)
- [A] Do models and agent frameworks differ by weakness (CWE) category? (p. 2, p. 6)
- [A] Can simple prompting strategies (CWE self-selection, oracle CWE hint) reduce security risk without hurting functionality? (p. 2, p. 8)

## 3. Methodology
- Research design: benchmark construction followed by a comparative evaluation of 12 agentic settings (3 agent frameworks x 4 backbone LLMs), plus a mitigation experiment on one setting (p. 2, p. 6, p. 8). [V]
- Approach / model / intervention:
  - Task construction: pick a vulnerability-fix commit C0 that fixes feature F; revert to the preceding vulnerable commit C−1; take the security tests added by the fix (Tsecure) and existing functional tests (Tfunc); an LLM agent (SWE-agent) masks out the feature code in C−1 and a second SWE-agent instance writes an issue-style feature request; a third instance links each line of the canonical secure implementation to a requirement in the request, and the mask is enlarged until the request covers the secure implementation (p. 3–4, p. 15). [V]
  - The task description must state the wanted functionality without implementation or security hints ("Do NOT mention security-related considerations") (p. 16). [V]
  - Masks are generated on the vulnerable commit, not the fixed commit, so that no information from the fix leaks into the task input (p. 4). [A]
  - Execution environments: Docker images built automatically by a SWE-agent variant with Claude 4 Sonnet; test-log parsers synthesised with OpenAI o3 (p. 17, p. 18). [V]
- Baselines or comparison conditions: the 12 framework x LLM combinations compared against each other (p. 6–7); in the mitigation study, "generic" security reminder vs. self-selection vs. oracle CWE hint (p. 8). [V] There is no human-developer baseline other than the historical vulnerable human implementation that defines each task [I] (based on p. 3–5).

## 4. Dataset and sample
- Data source(s): vulnerability-fix commits from ReposVul and MoreFixes (over 20,000 records, last 10 years), restricted to Python ≥ 3.7 projects and commits that modify tests (p. 3, p. 14). [V]
- Sample size (N) and unit: 186 tasks (feature requests) from 100 Python GitHub repositories, 10 application domains, 79 CWE types (p. 2, p. 13). [V] Mean context 236K lines / 1,186 files; mean target patch 175.0 lines / 1.8 files; mean 66.9 functional and 3.5 security tests per task (p. 5, Table 2). [V] 130 single-file, 23 two-file and 33 multi-file tasks (p. 14). [V]
- Sampling / selection method: funnel ~20,000 records → ~2,000 Python → ~450 candidate commits → ~420 after task construction/verification → 200 after environment and execution validation → 186 after human test-quality verification (p. 14, Table 10). [V] Counts before the final stage are stated as approximate (p. 14). [V]
- Data availability (public? link?): code and dataset at github.com/LeiLiLab/susvibes; public leaderboard (p. 1). [A] (link not checked by us)

## 5. Experimental setup
- Procedure, settings, hyper-parameters, tools: agent frameworks SWE-agent, OpenHands, Claude Code; backbones Claude 4 Sonnet, Kimi K2, Gemini 2.5 Pro, Gemini 3 Pro; default recommended system prompt of each framework; maximum 200 steps; agents may run their code and use runtime feedback (p. 6). [V] Main experiments include a short generic security reminder in the prompt (p. 7, p. 20). [V] Temperature, sampling settings, number of runs per task, cost and exact model versions: not reported (only pass@1 stated, p. 6).
- Code availability: GitHub repository stated (p. 1). [A]
- How functional correctness is tested: the human-written functional tests already in the upstream repository (Tfunc) are run on the agent's patch inside the Docker environment (p. 2, p. 4). [V] Task validity is checked by execution: the masked repo must fail both test sets, the vulnerable commit must pass functional and fail security tests, and the fixed commit must pass both (p. 5, p. 19). [V] No LLM judge is used for scoring (p. 6). [V]
- How security is tested: security unit tests added by the historical fix commit (Tsecure), mean 3.5 per task (p. 5). [V] Five software-engineering experts independently rated the security tests of the 200 candidate tasks on a Pass / Conditional Pass / Fail rubric for coupling to the reference implementation: 6.5% were coupled to the ground-truth implementation; 93.5% checked the intended property (49.5% full coverage, 44.0% might miss some edge-case secure implementations; 92.1% of these partial tests were refinable). Conditional Pass and Fail tests were rewritten and cross-checked in a second round (p. 19). [V] Inter-annotator agreement: not reported.

## 6. Evaluation metrics
- FuncPass — pass@1 on the functional tests (p. 6, p. 7). [V] Chosen because pass@1 reflects a vibe-coding user who wants correct code at once (p. 6). [A]
- SecPass — pass@1 on functional plus security tests, i.e. share of all tasks solved correctly and securely (p. 6). [V] Rationale: a solution with no meaningful feature is trivially "secure", so security only counts for functionally correct solutions (p. 6). [A]
- SecPass ⊥ FuncPass — secure ratio computed on the intersection of tasks solved correctly by all compared settings, to separate security from functional skill (p. 6). [V]
- Precision / recall / F1 of agent-selected CWE types vs. ground truth (self-selection setting) (p. 9, Table 6). [V]
- Statistical testing (tests used, significance, effect sizes, confidence intervals): none reported. Results are single pass@1 numbers without confidence intervals or repeated runs; Table 5 uses ▲/▼ markers without a stated test (p. 8). [V]

## 7. Key findings
1. Best functional setting SWE-agent + Claude 4 Sonnet: FuncPass 57.0%, SecPass 11.8% (p. 7, Table 3); 79.3% of its functionally correct solutions are insecure (p. 6). [V] (11.8/57.0 = 20.7% secure, arithmetic consistent.)
2. Across all 12 settings FuncPass ranges 12.9–57.0% and SecPass 3.8–12.9% (p. 7, Table 3); the authors summarise average SecPass as "only around 10%" (p. 6). [V]
3. SecPass ⊥ FuncPass by backbone (averaged over frameworks): Claude 4 Sonnet 18.3%, Kimi K2 22.0%, Gemini 2.5 Pro 30.4%, Gemini 3 Pro 21.4%; by framework: SWE-agent 23.3%, OpenHands 20.1%, Claude Code 17.4% (p. 6). [V] The functionally weakest model (Gemini 2.5 Pro) is the most secure on the shared subset (p. 6–7). [V] The authors note one exception to the ranking: Gemini 3 Pro is best on SWE-agent (36.4%) but not on the other frameworks (p. 6). [V] The shared subset is the intersection of tasks solved by all four LLMs within a framework (p. 6), so it cannot exceed the weakest model's FuncPass: Gemini 2.5 Pro solved 18.3% / 19.9% / 12.9% (SWE-agent / OpenHands / Claude Code), i.e. at most ~34 / 37 / 24 of 186 tasks (p. 7, Table 3). [V] The actual subset size is not reported; the secure-ratio comparison therefore rests on a small, unreported subset that is likely biased towards the easiest tasks [I] (based on the definition on p. 6 and Table 3, p. 7).
4. Gemini 3 Pro more than doubles FuncPass over Gemini 2.5 Pro under SWE-agent, while SecPass ⊥ FuncPass improves only 1.3x (p. 6–7). [V]
5. Performance falls with the number of files the reference patch touches: Claude 4 Sonnet FuncPass 66.9% (1 file) → 39.1% (2 files) → 30.3% (>2 files); SecPass 15.4% → 4.3% → 3.0% (p. 14, Table 9). [V]
6. Mitigation (SWE-agent + Claude 4 Sonnet): generic 57.0 / 11.8; self-selection 50.0 / 14.5; oracle CWE hint 55.4 / 15.1 (FuncPass / SecPass) (p. 8, Table 5). [V] The authors read this as small security gains at the cost of functionality (p. 8). [A]
7. In self-selection the agent picks 7.2 CWE types per task on average against 1.1 ground-truth types; precision 0.086–0.114, recall 0.561–0.667 (p. 8–9, Table 6). [V]
8. Model and framework strengths differ by CWE category and application domain (p. 6–7, Figure 4, Table 4). [V] Per-domain subset sizes behind Table 4 are not reported, so these cells may rest on very few tasks [I] (based on p. 7).

## 8. Limitations stated by the authors
- [A] Benchmark is Python-only; test outcomes are a practical proxy for security; CWE annotations and tests may be insufficient; no claim to cover all exploit modalities (p. 24).
- [A] Security tests from fix commits can be tied to the original implementation and reject secure alternatives; addressed by human verification and rewriting (p. 5, p. 19).
- [A] Fix commits may contain unrelated refactoring; addressed by ReposVul filtering, a Prospector score ≥ 65 for MoreFixes, and the verification loop (p. 15).
- [A] The automatic environment-building agent created operational risks (uncleaned images, over-exposed database containers), handled with command filtering (p. 18).
- [A] Mitigation prompts were kept deliberately simple; prompt engineering for security was not optimised (p. 19).

## 9. Limitations we identified
- [I] No repeated runs, seeds or confidence intervals. With 186 tasks one task is ~0.54 pp, so many between-setting SecPass differences (e.g. 11.8 vs 12.9) are within plausible run-to-run noise. Based on the single pass@1 numbers (p. 6–7).
- [I] The human verification of security tests by five experts reports no inter-annotator agreement and no disagreement-resolution rule beyond "a second round of cross-checking" (p. 19). The reliability of the security oracle cannot be judged from the paper.
- [I] Task masks and descriptions were generated and verified by LLM agents; no human check of description quality (under-specification, hidden requirements) is reported (p. 4, p. 15–16). Some functional failures may reflect description gaps rather than agent skill.
- [I] Possible data contamination: tasks reconstruct historical public code and fixes in popular repositories such as django, flask and numpy (p. 13); models may have seen the secure versions. The paper does not discuss contamination of its own tasks.
- [I] Claude 4 Sonnet powers the environment-building agent (p. 17) and SWE-agent drives task construction (p. 4); the best-scoring setting is SWE-agent + Claude 4 Sonnet. A construction–evaluation affinity bias is possible but untested.
- [I] The "generic" condition already contains a security reminder (p. 7, p. 20), so the main results are not a pure no-guidance vibe-coding condition; insecurity without any reminder could be higher.
- [I] Security is checked by few tests per task (mean 3.5, p. 5) that target only the historical vulnerability; other vulnerabilities an agent introduces are not detected (no static analysis), so SecPass is an upper bound on "secure".
- [I] The "most secure LLM / framework" ranking (SecPass ⊥ FuncPass, p. 6) is computed on the intersection of tasks solved by all compared settings (p. 6). Its size is never reported and is bounded by the weakest model's FuncPass (≤ ~24–37 tasks per framework, Table 3, p. 7), and solved-by-all tasks are likely the easiest. Differences such as 30.4% vs 18.3% may therefore rest on a handful of tasks.
- [I] Funding/conflicts: work partly supported by HydroX AI (an author affiliation) with compute/credits from Modal and Google (p. 9); Gemini models are evaluated. No visible bias (Gemini 2.5 Pro scores lowest functionally), noted per the appraisal checklist.

## 10. Threats to validity
- Internal (confounds, leakage, selection): masks built on the vulnerable commit to avoid leaking the fix (p. 4); `.git` history removed to avoid reward hacking (p. 17) [V]. Contamination of public historical code not addressed [I]. Generic security reminder present in all main runs (p. 7) [V].
- External (generalisability of sample/context): Python only, 100 open-source repositories, tasks restricted to features that once had a fixed vulnerability (p. 3, p. 13, p. 24) [V]. Results describe security-sensitive feature additions to existing repositories, not whole-application generation or reconstruction from UI [I].
- Construct (do metrics measure the concept?): FuncPass uses pre-existing upstream functional tests (mean 66.9 per task, p. 5), a fairly strong functional oracle [I]; SecPass covers only the historically known vulnerability through a few tests (p. 5, p. 24) [V]. Human-revised tests improve validity for alternative secure implementations (p. 19) [V].
- Statistical conclusion (power, multiple comparisons, variance): no variance, CIs or tests; per-CWE and per-domain breakdowns on small subsets (p. 7) [V]; many comparisons without correction [I].
- Reproducibility (data/code/setup reported?): data, code, prompts (Appendix B–C) and step limit reported (p. 1, p. 6, p. 15–20) [V]; model versions and sampling parameters not reported.

## 11. Future research directions
- Stated by authors [A]: broaden language and domain coverage; property-based and adversarial test synthesis; static/semantic program analysis; security-aware training rewards; tool use such as fuzzers, taint analysis and secret scanners (p. 24). Find strategies that improve security without disrupting functional task completion (p. 9).
- Suggested by us [I]: apply the same "mask and re-implement" construction to whole applications or UI-observable features, so that an original implementation and its test suite serve as a fidelity oracle for reconstruction; add static analysis to catch vulnerabilities beyond the targeted CWE; report repeated runs and annotator agreement.

## 12. Relevance to our research
- Research questions addressed (RQ ids): RQ2 (functional correctness measured with human-written tests), RQ3 (security as a quality dimension of agent/vibe-coded code), RQ4 (test-oracle design, human verification of tests, single-run pass@1), RQ5 (functional–quality divergence; no maintainability measure).
- How it informs our work [I]: SusVibes shows that passing functional tests says little about a second quality dimension (security): ~80% of functionally correct patches failed the security tests (p. 6). This is direct evidence that fidelity and code quality must be measured separately. Its task design (mask an existing implementation, describe it in natural language, ask an agent to re-implement it, test against the original's tests) is structurally a reconstruction-from-specification setup that could be adapted to behaviour-based reconstruction. It does not measure maintainability, UI behaviour or whole-application rebuilds, so relevance is medium.

## 13. Evidence table (for the evidence matrix)
| RQ | Claim | Page | Label | Strength |
|---|---|---|---|---|
| RQ2 | Best agent setting (SWE-agent + Claude 4 Sonnet) passes upstream human-written functional tests on 57.0% of 186 repository-level feature tasks; the 12 settings range 12.9–57.0% FuncPass | 7 | V | moderate |
| RQ3 | 79.3% of the functionally correct solutions of the best setting fail the security tests; SecPass is 3.8–12.9% across settings | 6 | V | moderate |
| RQ3 | Functional and security skill diverge: the functionally weakest model (Gemini 2.5 Pro) has the highest secure ratio on commonly solved tasks (30.4% vs 18.3% for Claude 4 Sonnet); exception: Gemini 3 Pro best on SWE-agent (36.4%); the commonly solved subset is unreported and at most ~24–37 tasks per framework (p. 7) | 6 | V | weak |
| RQ3 | Simple security prompting (self-selection / oracle CWE) raises SecPass by 2.7–3.3 pp but lowers FuncPass by 1.6–7.0 pp (single setting, single run) | 8 | V | weak |
| RQ2 | Functional success drops as the reference patch spans more files (Claude 4 Sonnet: 66.9% single-file vs 30.3% for >2 files) | 14 | V | moderate |
| RQ4 | Functional and security oracles are human-written upstream tests, validated by execution on masked, vulnerable and fixed commits; no LLM judge is used | 5 | V | moderate |
| RQ4 | Five experts reviewed security tests: 6.5% were coupled to the reference implementation, 44.0% might miss edge-case secure alternatives; tests were rewritten; no inter-annotator agreement reported | 19 | V | moderate |
| RQ4 | Results are single-run pass@1 with no confidence intervals or significance tests | 6 | V | n/a (design fact) |
| RQ5 | Authors call for property-based/adversarial tests and static analysis to complement test-based security evaluation | 24 | A | weak |

## 14. Key quotes
> "Although 57% of the solutions from SWE-Agent with Claude 4 Sonnet are functionally correct, only 11.8% are secure." (p. 1)
> "We find that 6.5% of the security unit tests are coupled to the ground-truth implementation." (p. 19)
> "uses test outcomes as a practical proxy for security; however, CWE annotations and tests may be insufficient" (p. 24)

## Analyst notes
- Reading coverage: whole paper read: main text p. 1–9, references skimmed p. 9–12, appendices A–E p. 13–24 read in full. Figure 4 bar values cannot be extracted from text; only the authors' verbal summary is used.
- Uncertainties: the LLM behind the SWE-agent instances used for masking, description writing and verification is not stated (only the environment-building agent is named as Claude 4 Sonnet, p. 17). Exact model versions and sampling parameters are not reported. Venue: ICML 2026 per the PDF footer (p. 1), while `metadata.json` still says arXiv preprint; metadata left unchanged.
- Scope fit: not a UI/behaviour reconstruction paper; included for the vibe-coding security/quality dimension and its evaluation design.
