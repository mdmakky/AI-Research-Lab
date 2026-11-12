---
key: lu2025webgen
status: complete
evidence_basis: full-text
design: benchmark construction + comparative evaluation of 3 agent frameworks x LLMs; UI-agent (LLM) functional testing validated against 3 human testers; SFT training study
dataset: WebGen-Bench, 101 NL website-generation instructions with 647 GPT-4o-drafted, human-refined UI test cases; WebGen-Instruct 6,667 training instructions
sample_size: 101 instructions / 647 test cases x 16 framework-model settings (single run); human validation on 3 settings
metrics: accuracy = (YES + 0.5 PARTIAL)/total test cases judged by WebVoyager UI agent; appearance score 1-5 (GPT-4o); agent-human alignment rate
main_finding: Best general model setting (Bolt.diy + DeepSeek-R1) reaches 27.8% test-case accuracy on websites built from scratch; UI-agent judge agrees with humans on 86-94% of cases.
relevance: high
analysed: 2026-11-11
---
<!-- Frontmatter: single-line values; they feed literature-matrix.md via `rlab index`.
     status: draft (in progress) -> ready (analyst self-check passed) -> complete (critical review passed).
     evidence_basis: full-text | abstract-only. abstract-only analyses must not fill methodology detail.
     relevance: high | medium | low. -->

# WebGen-Bench: Evaluating LLMs on Generating Interactive and Functional Websites from Scratch

- Authors: Lu, Zimu; Yang, Yunqiao; Ren, Houxing; Hou, Haotian; Xiao, Han; Wang, Ke
- Year / venue: 2025, Advances in Neural Information Processing Systems 38 (published)
- DOI: 10.52202/085713-2419 · URL: https://doi.org/10.52202/085713-2419
- Source text: `fulltext.txt` (page refs = PDF page index)
- Version note: the PDF analysed is arXiv v2, "arXiv:2505.03733v2 [cs.CL] 11 Aug 2025" (p. 1), from arxiv.org/pdf/2505.03733. It is a pre-acceptance version, marked "Preprint. Under review." (p. 1), with the NeurIPS checklist appended (p. 37–43). Metadata records the NeurIPS 38 published version. Page refs refer to this arXiv PDF; the author line in the PDF (p. 1) lists Shi, Zhou, Zhan and Li and does not include "Hou, Haotian", who appears in `metadata.json` — the published author list may differ.

Labels: **[V]** verified in the paper's own data/tables/results · **[A]** author claim · **[I]** our interpretation.
Every [V]/[A] item ends with a page ref `(p. N)`. Write "not reported" when the paper does not say.

## 1. Research objective
[A] To measure how well LLM-based code agents can build complete, multi-file, interactive websites from scratch from natural-language instructions written for non-expert users, and to provide a training set that improves open models on this task (p. 1–3).

## 2. Research questions / hypotheses
No formal RQs or hypotheses. Stated contributions (p. 3):
- [A] A benchmark (WebGen-Bench) of website-generation instructions with test cases for functionality and appearance (p. 3).
- [A] An evaluation of three code-agent frameworks (Bolt.diy, OpenHands, Aider) with several LLMs (p. 3).
- [A] A training set (WebGen-Instruct, 6,667 instructions) and fine-tuned models (WebGen-LM 7B/14B/32B) (p. 3).

## 3. Methodology
- Research design: benchmark construction; comparative evaluation of agent framework x LLM settings; validation of the automated judge against human testers; fine-tuning experiment with a training-size ablation (p. 4–10). [V]
- Approach / model / intervention: agents receive an instruction without technical details ("The agents should autonomously determine the optimal technical approach") and generate a website codebase from scratch (p. 5). [V]
- How functional correctness is tested: for each instruction GPT-4o drafted 5–10 atomic test cases (operation + expected result) covering every functional and appearance requirement; two CS PhD students independently reviewed and refined them and resolved discrepancies by discussion, giving 647 test cases (4–11 per instruction) (p. 5–6, p. 19). [V] Each test case is executed by the WebVoyager web-navigation agent driven by Qwen2.5-VL-32B-Instruct, which interacts with the site (at most 15 interactions), inspects screenshots and answers YES, PARTIAL or NO; if the limit is reached, a follow-up prompt forces a final decision (p. 6, p. 19–20). [V]
- How appearance is tested: GPT-4o grades screenshots 1–5 on rendering, content relevance, layout harmony and modernness (p. 6, p. 21). [V]
- Baselines or comparison conditions: three frameworks on DeepSeek-V3, Claude-3.5-Sonnet and DeepSeek-R1; then Bolt.diy with Claude-3.5-Sonnet, DeepSeek-R1, DeepSeek-V3, GPT-4o, o3-mini, Qwen2.5-Coder-32B, Qwen2.5-72B-Instruct, and the fine-tuned WebGen-LM models (p. 7–8). [V] No human-developer baseline. [V] (p. 7–8)

## 4. Dataset and sample
- Data source(s): authors identified 20 web-application categories from freelance platforms (Upwork, Freelancer, Proginn); 40 CS PhD students brainstormed specific applications and requirements, producing 10,152 project descriptions; GPT-4o converted them into instructions with a one-shot prompt (p. 4–5, p. 15). [V]
- Sample size (N) and unit: test set 101 instructions; 647 test cases (p. 5–6). [V] Instruction categories: Content Presentation 28, User Interaction 49, Data Management 24 (p. 6, Table 2). [V] Test-case categories: Functional Testing 339, Data Display 186, Design Validation 122 (p. 23, Table 8). [V] These sum to 647 (339 + 186 + 122), matching the text (p. 1, p. 6). Table 8's printed "Total 667" is therefore an arithmetic or typographical error in that row (p. 23). [V]
- Sampling / selection method: "two to eight representative examples from each category" sampled for the test set; how representativeness was judged is not reported (p. 5). [V] Training set decontaminated by 5-gram Jaccard (> 0.6 removed) and sentence-embedding cosine similarity (> 0.55 removed), plus manual inspection of top-3 matches (p. 5, p. 14). [V]
- Data availability (public? link?): data, code and model weights released under MIT licence at github.com/mnluzimu/WebGen-Bench (p. 1, p. 14). [A] (link not checked by us)

## 5. Experimental setup
- Procedure, settings, hyper-parameters, tools: Bolt.diy (browser-based WebContainer; model picks frameworks such as Vite/React/Remix), OpenHands with CodeActAgent, Aider with adapted prompts; OpenHands told to use TypeScript/HTML/CSS with `npm install` / `npm run dev`; Aider told to prefer Vite and Node.js (p. 7, p. 21–22). [V] Models smaller than Qwen2.5-Coder-32B were excluded because they often failed the output format (p. 7). [V] Sampling temperature, number of runs and time/step budgets for generation: not reported.
- Training: 2K WebGen-Instruct instructions run through Bolt.diy with DeepSeek-V3; trajectories kept only if the GPT-4o appearance score ≥ 3 (600 trajectories); Qwen2.5-Coder-Instruct 7B/14B/32B fine-tuned for 2 epochs, LR 4e-5, batch 32 (p. 7). [V]
- Code availability: released (p. 1, p. 14). [A]
- Evaluator-reliability design: three human testers independently annotated the full test results of Bolt.diy with Claude-3.5-Sonnet, DeepSeek-R1 and DeepSeek-V3; inconsistent cases went to a fourth tester for a final label; the agent's label was compared with this human label (alignment rate) (p. 8–9). [V] Appearance-score reliability: two extra model graders (o3, Claude-3.5-Sonnet) and manual grading of the same three settings (p. 22–23). [V] Number of human appearance graders: not reported.

## 6. Evaluation metrics
- Accuracy — (N_YES + 0.5 × N_PARTIAL) / N_total × 100% over all test cases; websites that fail to start count as failures (p. 7–8, Table 3). [V]
- Yes / Partial / No / Start-failed rates (p. 8, Table 3). [V]
- Appearance score — GPT-4o grade 1–5 (p. 6). [V]
- Alignment rate — share of test cases where UI-agent label equals the human label (p. 9). [V] Inter-human agreement among the three testers: "we assessed the consistency of their annotations" (p. 8), but no value is reported. No chance-corrected statistic.
- Statistical testing (tests used, significance, effect sizes, confidence intervals): none; NeurIPS checklist answers "No" for error bars "because it would be too computationally expensive" (p. 40). [V]

## 7. Key findings
1. Best general-model setting is Bolt.diy + DeepSeek-R1 at 27.8% accuracy (YES 24.7%), closely followed by Bolt.diy + Claude-3.5-Sonnet at 26.4% (p. 8, Table 3). [V]
2. Framework matters: with DeepSeek-V3, accuracy is 20.8% (Bolt.diy), 9.0% (OpenHands), 14.1% (Aider) (p. 8, Table 3). [V] Start-failure rates reach 38.6% (Bolt.diy + o3-mini) and 32.1% (Aider + Claude-3.5-Sonnet) (p. 8). [V]
3. Fine-tuning Qwen2.5-Coder-32B on 600 filtered trajectories raises accuracy from 9.5% to 38.2% (WebGen-LM-32B), above DeepSeek-R1 (p. 8, Table 3); accuracy rises with training size: 25.1% (150), 31.9% (300), 38.2% (600) (p. 10, Table 6). [V]
4. Functional test cases are hardest: e.g. Bolt.diy + DeepSeek-R1 scores 21.1% on Functional Testing vs 44.3% on Design Validation; Bolt.diy + Claude-3.5-Sonnet 17.1% vs 52.0% (p. 9, Table 4). [V] The authors conclude that "superficial aspects, such as color themes, are easier to implement than deeper internal functionalities" (p. 8). [A]
5. UI-agent vs human labels: alignment rate 90.3% (Claude-3.5-Sonnet), 86.1% (DeepSeek-R1), 94.4% (DeepSeek-V3); aggregate accuracy differs by 0.4–2.3 points (agent 26.4/27.8/20.8 vs manual 26.0/30.1/21.3) (p. 9, Table 5). [V]
6. Best appearance score 3.0 (Bolt.diy + Claude-3.5-Sonnet) (p. 8). [V] GPT-4o, o3, Claude-3.5-Sonnet and human graders give the same ranking of three settings, with GPT-4o scoring highest (p. 23, Table 9). [V]
7. Human manual testing of all 647 cases is estimated at ~10.8 hours and $377.8 per setting (60 s per case), the stated reason for automation (p. 6). [V]

## 8. Limitations stated by the authors
- [A] Websites are generated only with TypeScript, JavaScript, CSS and HTML; Python, Java, Go and other tools were not integrated (p. 14).
- [A] Only supervised fine-tuning was used; RL or DPO not explored (p. 14).
- [A] Training data was not scaled beyond 600 trajectories because of API budget (p. 9).
- [A] No error bars, for cost reasons (p. 40).

## 9. Limitations we identified
- [I] The functional oracle is an LLM-driven UI agent with a 15-interaction cap (p. 19). Human validation covers only 3 of 16 settings, all Bolt.diy (p. 8–9); agreement may differ for OpenHands/Aider outputs or weaker models with many start failures. Alignment is reported as raw percent on a 3-class label without chance correction, and inter-human agreement is not reported (p. 8–9).
- [I] The alignment rate counts test cases; with 58–74% NO labels (p. 9, Table 5), a judge that says NO often gets high agreement by default. Per-class (YES vs NO) agreement is not given, so false-positive "YES" rates are unknown.
- [I] Test cases were drafted by GPT-4o from the same instruction the agent sees, and each checks one atomic requirement (p. 5, p. 19). They test whether a stated feature is visible and responds, not deeper behavioural correctness (data persistence, multi-step workflows, edge cases); "PARTIAL" earning half credit further softens the score (p. 7).
- [I] Minor typo: Table 8 prints "Total 667", but its main categories sum to 647 (339 + 186 + 122), matching the text (p. 1, p. 6, p. 23). This is a typo, not evidence of a different test set.
- [I] Single run per setting and no reported generation hyper-parameters (temperature, budgets) (p. 7–8, p. 40); differences of 1–2 points (e.g. 27.8 vs 26.4) are not separable from noise.
- [I] The models evaluated (Claude-3.5-Sonnet, GPT-4o, o3-mini, DeepSeek-V3/R1) are early-2025 models; absolute numbers are already dated relative to later benchmarks such as Vibe Code Bench (tran2026vibe) [I].
- [I] Fine-tuning trajectories were filtered by GPT-4o appearance score, not by functional tests (p. 7), yet gains are measured on functional accuracy; the training and test instructions share the same GPT-4o generation template and colour-requirement style (p. 15–18), so part of the gain may be format/style adaptation to the benchmark distribution despite n-gram/embedding decontamination.
- [I] No code-quality, security or maintainability measures are taken for the generated codebases.
- [I] Funding and conflicts: not reported in the main text.

## 10. Threats to validity
- Internal (confounds, leakage, selection): framework prompts differ (OpenHands/Aider adapted prompts, p. 21–22), confounding framework comparisons with prompt design [I]. Decontamination of training vs test instructions is reported (p. 14) [V]. GPT-4o wrote instructions and test cases and is also an evaluated model (p. 5, p. 8) [V]; it scored low (12.8%), so no evident self-advantage [I].
- External (generalisability of sample/context): 101 synthetic instructions from student brainstorming, not real client requests (p. 4–5, p. 14) [V]; JS/TS web stack only (p. 14) [V]. Inputs are NL instructions, not screenshots or existing apps [I].
- Construct (do metrics measure the concept?): atomic UI-agent tests capture visible feature presence and simple interactions; appearance score mixes rendering correctness with aesthetics (p. 21) [V/I]. No measure of code quality [I].
- Statistical conclusion (power, multiple comparisons, variance): no error bars or tests (p. 40) [V]; three-setting human validation [V].
- Reproducibility (data/code/setup reported?): prompts for instruction generation, test generation, UI-agent testing, appearance grading and agents printed (p. 15–22) [V]; code, data and weights released (p. 1) [A]; generation sampling settings not reported.

## 11. Future research directions
- Stated by authors [A]: support more languages and tools for website generation; explore RL and DPO post-training (p. 14); add more training data or data augmentation (p. 9).
- Suggested by us [I]: report per-class judge agreement and inter-human agreement; validate the judge on all frameworks; extend test cases from atomic checks to multi-step workflows (as Vibe Code Bench does); add code-quality metrics; for reconstruction, generate test cases from an existing site's observed behaviour rather than from an instruction.

## 12. Relevance to our research
- Research questions addressed (RQ ids): RQ1 (agent frameworks generating whole websites from NL instructions — Bolt.diy, OpenHands, Aider), RQ2 (functional fidelity via UI-agent test cases; headline accuracy), RQ4 (LLM-judge vs human alignment, test-case construction, no error bars), RQ5 (code quality not measured).
- How it informs our work [I]: WebGen-Bench established the pattern now common in this area: LLM-drafted, human-refined requirement-level test cases executed by a vision UI agent, with a human-alignment check. Its numbers show that visual/design requirements are met far more often than functional ones (p. 9), which matters for UI-based reconstruction: a rebuild can look right while behaving wrongly. The judge validation (86–94% alignment on 3 settings) is the main evidence that UI-agent testing is usable, but it is limited in scope and statistics.

## 13. Evidence table (for the evidence matrix)
| RQ | Claim | Page | Label | Strength |
|---|---|---|---|---|
| RQ2 | Best general-LLM agent setting (Bolt.diy + DeepSeek-R1) reaches only 27.8% accuracy on 647 UI test cases for 101 websites built from scratch | 8 | V | moderate |
| RQ2 | Functional test cases are passed far less often than design-validation ones (e.g. 21.1% vs 44.3% for Bolt.diy + DeepSeek-R1; 17.1% vs 52.0% for Claude-3.5-Sonnet) | 9 | V | moderate |
| RQ1 | Agent framework strongly affects outcome: DeepSeek-V3 scores 20.8% in Bolt.diy, 14.1% in Aider, 9.0% in OpenHands | 8 | V | weak |
| RQ1 | Fine-tuning Qwen2.5-Coder-32B on 600 filtered agent trajectories lifts accuracy from 9.5% to 38.2% | 8 | V | weak |
| RQ4 | Functional fidelity is judged by a WebVoyager UI agent (Qwen2.5-VL-32B) on GPT-4o-drafted, human-refined atomic test cases, with YES/PARTIAL/NO and half credit for PARTIAL | 6 | V | moderate |
| RQ4 | UI-agent labels match adjudicated human labels on 86.1–94.4% of test cases (3 Bolt.diy settings); inter-human agreement and chance-corrected agreement not reported | 9 | V | moderate |
| RQ4 | No error bars or significance tests; single run per setting | 40 | V | strong |
| RQ4 | GPT-4o appearance scores give the same ranking as o3, Claude-3.5-Sonnet and human grading on 3 settings | 23 | V | weak |

## 14. Key quotes
> "The best-performing combination, Bolt.diy powered by DeepSeek-R1, achieves only 27.8% accuracy on the test cases" (p. 1)
> "This indicates that superficial aspects, such as color themes, are easier to implement than deeper internal functionalities." (p. 8)
> "Error bars are not reported because it would be too computationally expensive." (p. 40)

## Analyst notes
- Reading coverage: main text p. 1–10, references p. 11–13, appendices A–N p. 14–25 read; UI-agent trajectory examples (p. 26–36) skimmed; NeurIPS checklist (p. 37–43) checked for statistics and human-subject answers. Figures 2, 3, 14–16 are images; only text values used. Section 3.1 paragraph "Web Development Project Descriptions Collection" appears twice on p. 5 (duplicated in the PDF).
- Uncertainties: the published NeurIPS version may differ from this arXiv v2 (e.g. the appendix says "We will add this discussion to the revised paper", p. 23). Author list mismatch with metadata (see version note; escalated to the lead for re-resolution via `rlab`). Table 8's "Total 667" is a typo for 647 (categories sum to 647, p. 23). Number of human appearance graders not reported.
