---
key: zhou2025declarui
status: ready
evidence_basis: full-text
design: technique proposal + controlled comparison vs. raw MLLM baselines + ablation + developer user study
dataset: 50 mobile app UI design sets (250 pages): 25 Figma mockups + 25 Google Play app screenshot sets, 10 categories
sample_size: 50 apps x 5 pages; ablation on 13 apps; user study 5 React Native developers x 12 apps
metrics: CLIP, SSIM, PTG Coverage Rate (manual, vs DroidBot UTG), Compilation Success Rate, ACIC, AMCT; developer ratings of code availability, modification time, readability, maintainability
main_finding: CV segmentation + page-transition graph + compiler-feedback loop raise React Native navigation coverage to 96.8% and compile success to 98% vs 43%/74% for Claude-3.5.
relevance: high
analysed: 2026-11-11
---
<!-- Frontmatter: single-line values; they feed literature-matrix.md via `rlab index`.
     status: draft (in progress) -> ready (analyst self-check passed) -> complete (critical review passed).
     evidence_basis: full-text | abstract-only. abstract-only analyses must not fill methodology detail.
     relevance: high | medium | low. -->

# DeclarUI: Bridging Design and Development with Automated Declarative UI Code Generation

- Authors: Zhou, Ting; Zhao, Yanjie; Hou, Xinyi; Sun, Xiaoyu; Chen, Kai; Wang, Haoyu
- Year / venue: 2025, Proceedings of the ACM on Software Engineering (published)
- DOI: 10.1145/3715726 · URL: https://doi.org/10.1145/3715726
- Source text: `fulltext.txt` (page refs = PDF page index)

Labels: **[V]** verified in the paper's own data/tables/results · **[A]** author claim · **[I]** our interpretation.
Every [V]/[A] item ends with a page ref `(p. N)`. Write "not reported" when the paper does not say.

## 1. Research objective
- Propose DeclarUI, an automated approach that combines computer vision (CV), MLLMs and compiler-driven iterative refinement to generate multi-page declarative mobile UI code (React Native, Flutter, ArkUI) from UI design mockups or app screenshots, improving visual fidelity, navigation completeness and code quality [A] (pp. 1–2).

## 2. Research questions / hypotheses
- RQ1 Effectiveness: how does DeclarUI perform vs. baselines "when operating autonomously without human intervention"? [V] (p. 6)
- RQ2 Ablation: contribution of individual modules [V] (p. 6)
- RQ3 User study and manual repair: how do professional developers rate DeclarUI code vs. the baseline, and how much manual effort repairs compilation failures? [V] (p. 6)

## 3. Methodology
- Research design: technique proposal evaluated by a controlled comparison with two raw-MLLM baselines on a curated dataset, an ablation on a subset, a within-subject developer study, and a manual-repair timing study [V] (pp. 6–11).
- Approach / model / intervention: (1) Page Transition Graph (PTG) construction — Claude-3.5 infers nodes (pages) and edges (transitions with conditions/actions) from the design set as JSON; "designers or developers review the generated PTG, making necessary corrections or additions" [V] (pp. 3–4); (2) UI component extraction — Grounding DINO detection + Segment Anything segmentation + Claude-3.5 classification and functional description of each component [V] (p. 4); (3) prompt synthesis combining PTG, component analysis and the full screenshot [V] (p. 5); (4) iterative refinement — static-analysis check of implemented navigation vs. PTG (up to 3 iterations per page) and compile-error feedback (up to 3 iterations per project) [V] (pp. 5–6).
- Baselines or comparison conditions: GPT-4o and Claude-3.5-Sonnet-20240620 given unprocessed design images with "meticulously designed" prompts following prior image-to-code work, in React Native only [V] (p. 7). DeclarUI is run with GPT-4o and Claude-3.5 as base models; Flutter and ArkUI are run with DeclarUI (Claude-3.5) only, with no baseline [V] (pp. 8–9). No prior UI-to-code tool is used as a baseline [I] (based on p. 7).

## 4. Dataset and sample
- Data source(s): Figma community mockups (selected from 194 designs with >300 followers, ≥5 pages, mobile-specific) and Google Play apps (top 10 by downloads per category, excluding paid apps and complex registration; APKs installed on an emulator and screenshots captured manually) [V] (pp. 6–7).
- Sample size (N) and unit: 50 apps (25 Figma, 25 Google Play), 5 logically connected pages each = 250 pages, 10 functional categories × 5 apps [V] (pp. 6–7). Ablation: 13 apps chosen by CLIP-score distribution across categories [V] (p. 9). User study: 12 apps stratified by CLIP score (3 > 0.85, 6 in 0.8–0.85, 3 < 0.8) [V] (p. 9). RAG experiment: 20 apps (100 pages) [V] (p. 11).
- Sampling / selection method: 3–5 per category per source, random selection of five when more available, "to control experimental costs while ensuring research quality and statistical significance" [A] (p. 7). Sample size limited "due to MLLMs' token cost constraints" [A] (p. 12).
- Data availability (public? link?): not reported in our PDF (no repository link found).

## 5. Experimental setup
- Procedure, settings, hyper-parameters, tools: generated code inserted into an initial project in Android Studio (React Native, Flutter) or DevEco Studio (ArkUI) without manual intervention, built into an APK and run on the built-in emulator [V] (p. 8). Hardware: 2× RTX 3090, 64-core AMD EPYC, 512 GB RAM; custom Python scripts of 2,935 lines [V] (p. 8). UTG for evaluation obtained with DroidBot [V] (p. 7). Temperature, sampling settings and GPT-4o version: not reported. Image assets are excluded from evaluation [V] (p. 2).
- Code availability: not reported in our PDF.

## 6. Evaluation metrics
- CLIP score — semantic visual similarity of generated vs original UI [V] (p. 7).
- SSIM — layout/structural similarity [V] (p. 7).
- PTG Coverage Rate PCR = |PTG edges ∩ UTG edges| / |PTG edges| × 100%, "manually calculated by human evaluators", comparing the predefined PTG with the DroidBot-explored UI Transition Graph of the built app — a navigation/functional-fidelity measure [V] (p. 7).
- Compilation Success Rate (CSR) — share of apps compiling after up to three automated refinement iterations [V] (p. 7).
- Average Compilation Iteration Count (ACIC) — compilation attempts per successfully compiled app (max 3) [V] (p. 7).
- Average Manual Correction Time (AMCT) — human repair time per compilation-failed app [V] (p. 7).
- Developer-rated code quality (user study, following Chen et al. [11]): Code Availability (proportion of generated code kept after modification to meet basic business requirements, tracked with git, mapped from 0.8 in 5% intervals to levels 1–5); Modification Time (5 points ≤5 min down to 1 point >20 min; 20-min cap per app); Readability and Maintainability (five-point Likert ratings) [V] (pp. 7, 9).
- Validation against human judgement: none for CLIP/SSIM; authors acknowledge they "may not fully capture human-perceived UI similarity" and state the user study "confirmed the validity of our evaluations" [A] (p. 12). No correlation between automatic metrics and human ratings is reported.
- Statistical testing (tests used, significance, effect sizes, confidence intervals): Mann-Whitney U test for user-study ratings (p from 9.23E-08 to 2.57E-13) [V] (p. 10). No tests, CIs or run-to-run variance for CLIP/SSIM/PCR/CSR comparisons; no effect sizes — not reported.

## 7. Key findings
1. React Native: DeclarUI (Claude-3.5) CLIP 0.88, SSIM 0.68, PCR 96.8%, CSR 98%; DeclarUI (GPT-4o) 0.87 / 0.58 / 88.6% / 88%; baselines GPT-4o 0.66 / 0.44 / 1.4% / 76% and Claude-3.5 0.65 / 0.41 / 43.3% / 74% [V] (p. 9).
2. Raw MLLMs largely fail to implement multi-page navigation (GPT-4o PCR 1.4%) [V] (p. 9). Baseline compilation failures came from non-existent packages/components, special-character handling and missing imports [A] (p. 8).
3. Generalisation: Flutter PCR 99.4%, CSR 92%; ArkUI PCR 95.9%, CSR 86% (DeclarUI Claude-3.5 only) [V] (p. 9). Knowledge-graph RAG for ArkUI on 20 apps: CSR 86% → 90%, AMCT 183 s → 43.5 s [V] (p. 11).
4. Ablation (13 apps): removing CV extraction drops SSIM 0.72 → 0.57; removing PTG + refinement drops PCR to 23.1% and CSR to 80% [V] (pp. 9–10).
5. User study (5 developers × 12 apps): DeclarUI vs Baseline (Claude-3.5) — availability 4.97 vs 4.15, modification time 4.03 vs 2.45, readability 4.62 vs 3.75, maintainability 4.55 vs 3.37, all p < 0.05 (Mann-Whitney U) [V] (p. 10). 73.3% of DeclarUI code modified within 10 min; 80% of baseline code needed >10 min [V] (p. 10).
6. Manual repair: AMCT 48 s (React Native, Claude-3.5), 43.2 s (GPT-4o), 62 s (Flutter), 183 s (ArkUI) [V] (p. 11).
7. Authors conclude generated code "meets industrial-grade standards" in availability, modification time, readability and maintainability [A] (pp. 1–2) — this rests on Likert ratings from five developers.

## 8. Limitations stated by the authors
- CLIP and SSIM may not capture human-perceived UI similarity; PCR does not reflect navigation fluidity or intuitiveness [A] (p. 12).
- Results depend on prompt design; user-study participant experience may bias results [A] (p. 12).
- Sample of 50 design sets may not represent all mobile UI types; limited by token cost [A] (p. 12).
- Uneven framework performance; ArkUI weaker, attributed to limited MLLM knowledge; RAG implementation limited by time [A] (p. 11).
- PTG construction could not be ablated alone because refinement depends on it [A] (p. 9).

## 9. Limitations we identified
- [I] Human in the loop vs "autonomous" claim: the PTG is reviewed and corrected by designers/developers (p. 4), while RQ1 is framed as operating "without human intervention" (p. 6). How often and how much the PTG was corrected is not reported.
- [I] PCR is partly circular: DeclarUI receives the PTG as input and is checked against it during refinement, then scored against the same PTG (pp. 5–7); baselines never see the PTG. PCR also counts only edges, not correct behaviour on each screen, and is computed manually without reported agreement (p. 7).
- [I] Ablation numbers are internally implausible: on 13 apps, CSR values of 98.0% and 80.0% (p. 10) cannot arise (possible values are k/13, e.g. 76.9%, 84.6%, 92.3%), and the "Full" PCR/CSR equal the 50-app values (pp. 9–10). The Table 2 "Full" row may mix 50-app and 13-app results.
- [I] User-study statistics treat 60 ratings per condition (5 developers × 12 apps) as independent; the tiny p-values (down to 2.57E-13, p. 10) overstate certainty (pseudo-replication). Blinding of participants to condition is not reported. Five participants is a small sample.
- [I] Code quality and maintainability are measured only subjectively (Likert) and by modification time; no static analysis, complexity, duplication or code-smell metrics.
- [I] Minor inconsistencies: Baseline Claude PCR 43.4% (p. 8) vs 43.3% (p. 9); ACIC defined as "number of compilation attempts" (max 3) yet reported as 0.22 (pp. 7, 9), implying it counts only repair iterations.
- [I] Single run per configuration; no variance across runs, though MLLM outputs are stochastic (sampling settings not reported).
- [I] Our PDF is arXiv v1 (18 Sep 2024); the FSE 2025 version may report different numbers.

## 10. Threats to validity
- Internal (confounds, leakage, selection): human PTG correction; PCR scored against the method's own input; ablation subset chosen by CLIP score; possible training-data exposure of popular Google Play apps' UIs not discussed [I].
- External (generalisability of sample/context): 50 apps × 5 pages; only UI and navigation (no back-end, data, business logic); image assets ignored (p. 2) [I].
- Construct (do metrics measure the concept?): CLIP/SSIM unvalidated proxies for visual fidelity (p. 12); PCR measures presence of transitions, not their correctness of state; compilation success is a weak proxy for functional correctness; maintainability is self-reported [I].
- Statistical conclusion (power, multiple comparisons, variance): Mann-Whitney on non-independent ratings; four tests without correction (not critical given p values); no CIs or effect sizes [I].
- Reproducibility (data/code/setup reported?): no code or data link in our PDF; model sampling settings missing; tools (Grounding DINO, SAM, DroidBot) named (pp. 4, 7) [I].

## 11. Future research directions
- Stated by authors [A]: richer knowledge-graph RAG for less common frameworks such as ArkUI, dynamic KG updates, extension to other frameworks (p. 11); larger and more diverse UI samples (p. 12).
- Suggested by us [I]: report PTG correction effort; measure navigation and in-screen behaviour with automated GUI tests rather than manual edge counts; add objective maintainability metrics (static analysis, code smells) alongside developer ratings; use mixed-effects models for user-study ratings.

## 12. Relevance to our research
- Research questions addressed (RQ ids): RQ1, RQ2, RQ3, RQ4, RQ5.
- How it informs our work [I]: DeclarUI is one of few studies that rebuilds multi-screen mobile apps from screenshots of existing Google Play apps — a direct form of reverse engineering from observable UI — and it measures navigation fidelity (PCR via DroidBot exploration), compilability and developer-rated readability/maintainability together. It shows that structuring the observable behaviour (page transition graph) and compiler feedback matter, but its maintainability evidence is subjective and its fidelity metrics have design weaknesses.

## 13. Evidence table (for the evidence matrix)
| RQ | Claim | Page | Label | Strength |
|---|---|---|---|---|
| RQ1 | Pipeline: Grounding DINO + SAM component extraction, MLLM-built page transition graph, compiler/navigation feedback loop for declarative mobile UI code | p. 3–6 | V | moderate |
| RQ1 | PTG is reviewed and corrected by designers/developers (human in the loop) | p. 4 | V | moderate |
| RQ2 | Navigation fidelity via PTG Coverage Rate (manual comparison with DroidBot UTG): DeclarUI 96.8% vs Claude-3.5 43.3% vs GPT-4o 1.4% (React Native, 50 apps) | p. 7, 9 | V | moderate |
| RQ2 | Compilation success 98% (DeclarUI Claude-3.5) vs 74–76% for raw MLLMs; CLIP 0.88 vs 0.65–0.66; SSIM 0.68 vs 0.41–0.44 | p. 9 | V | moderate |
| RQ2 | Without PTG + refinement, PCR falls to 23.1% | p. 10 | V | weak |
| RQ3 | Developer ratings (5 devs × 12 apps): readability 4.62 vs 3.75, maintainability 4.55 vs 3.37, Mann-Whitney p < 1e-11 | p. 10 | V | weak |
| RQ3 | Code quality/maintainability measured only by Likert ratings, code availability and modification time; no static metrics | p. 7, 9 | V | moderate |
| RQ4 | CLIP/SSIM acknowledged not to capture human-perceived similarity; no correlation with human ratings reported | p. 12 | A | moderate |
| RQ4 | Ablation CSR values (98%, 80%) impossible for 13 apps; user-study test ignores rating dependence | p. 9–10 | I | moderate |
| RQ5 | No back-end/business logic, image assets ignored; sample 50 apps limited by token cost | p. 2, 12 | A | moderate |

## 14. Key quotes
> "Finally, designers or developers review the generated PTG, making necessary corrections or additions" (p. 4)
> "This metric, manually calculated by human evaluators, assesses the alignment between the implemented app structure and the intended design." (p. 7)
> "CLIP Score and SSIM, used for UI similarity assessment, may not fully capture human-perceived UI similarity" (p. 12)

## Analyst notes
- Reading coverage: whole PDF read (pp. 1–13); reference list skimmed. Figure 7 heatmaps not inspected in detail (garbled in text; only summary statements used).
- Uncertainties: our PDF is arXiv v1 (Sep 2024), not the PACMSE/FSE 2025 published version; numbers may have changed. Ablation Table 2 numbers look inconsistent with a 13-app subset. Peer-reviewed (Proceedings of the ACM on Software Engineering, tier 1), but our copy is the preprint.
