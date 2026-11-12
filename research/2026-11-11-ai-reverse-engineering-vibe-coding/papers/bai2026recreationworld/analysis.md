---
key: bai2026recreationworld
status: complete
evidence_basis: full-text
design: Benchmark + environment framework (five-platform application recreation from a running reference) with model comparison, trajectory/artifact analysis and SFT transfer experiment
dataset: RecreationBench, 250 tasks (50 each on Ubuntu, macOS, Windows, Android, Web; 200 open-source native apps, 44 synthetic + 6 openly licensed websites); 35,000 recreation trajectories for SFT
sample_size: 250 benchmark tasks x 10 frontier models (rollouts per task not stated, probably one); trajectory/artifact analyses on 4 models; 35,000 SFT trajectories; 5 OOD benchmarks
metrics: Programmatic score (fraction of reference-validated accessibility/DOM assertions passed); VLM score (VLM-judged visual assertions); average; Prog>=90%/=100% app coverage; LOC, file count, largest-file share
main_finding: Best of 10 agents (GPT-6 Astra) averages 58.1%, fully passes 2.8% of apps; in 4 analysed models, interactions lag structure and rebuilds are smaller.
relevance: high
analysed: 2026-11-11
---
<!-- Frontmatter: single-line values; they feed literature-matrix.md via `rlab index`.
     status: draft (in progress) -> ready (analyst self-check passed) -> complete (critical review passed).
     evidence_basis: full-text | abstract-only. abstract-only analyses must not fill methodology detail.
     relevance: high | medium | low. -->

# RecreationWorld: Scalable and Verifiable Environments for Hybrid Computer-Use Agents

- Authors: Bai, Shuai; Deng, Jiayong; Fan, Sicheng; Fu, Yikun; Gao, Chang; Hu, Xuhao
- Year / venue: 2026, arXiv (preprint)
- DOI: 10.48550/arxiv.2609.22000 · URL: https://arxiv.org/abs/2609.22000
- Source text: `fulltext.txt` (page refs = PDF page index). Version read: arXiv v2, 21 Sep 2026 (p. 1). **Preprint, not peer-reviewed.** Industry paper (Alibaba Group, p. 1).

Labels: **[V]** verified in the paper's own data/tables/results · **[A]** author claim · **[I]** our interpretation.
Every [V]/[A] item ends with a page ref `(p. N)`. Write "not reported" when the paper does not say.

## 1. Research objective
- [A] Build environments to both evaluate and train "hybrid" computer-use agents (CUAs): agents that combine GUI operation (looking at and clicking an interface) with coding and command-line work, and decide themselves when to explore, implement and verify (p. 1-2).
- [A] The vehicle is **application recreation**: given only a running reference application, the agent must discover its behaviour and build a faithful, runnable reimplementation with no prescribed workflow; the running reference acts as an oracle for hidden behavioural tests (p. 1, p. 3).
- [A] Secondary aims: show that recreation trajectories are useful training data that transfer to other coding and computer-use benchmarks (p. 3, p. 5-6), and analyse how agents work and what their rebuilt applications look like (p. 11).

## 2. Research questions / hypotheses
- No formal RQs or hypotheses. Implicit questions [I], based on the section structure (p. 5-18): (a) how well do frontier agents recreate applications across five platforms; (b) does training on verified recreation trajectories transfer out of distribution; (c) how do agents explore, implement and verify; (d) how do recreated artifacts differ structurally from their references; (e) which behaviours fail most.

## 3. Methodology
- Research design: [V] Benchmark and environment paper with (i) a held-out benchmark evaluation of ten frontier models, (ii) a supervised fine-tuning (SFT) transfer experiment with two model initialisations, (iii) a paired auxiliary comparison of two tool interfaces, and (iv) descriptive trajectory, artifact and failure analyses plus case studies (p. 5-6, p. 10-20, p. 38-47).
- Approach / model / intervention: [V] Agent gets a task prompt, interactive access to the running reference, and an environment with GUI control and development tools; it returns source that must build and launch (desktop source + build/launch scripts; Android Gradle project -> APK; Web scaffolded source -> self-contained `index.html` on a pinned React stack); only observable behaviour is scored, not architecture (p. 3, p. 7). Desktop and Android are source-blind; on Web the served client code is necessarily visible (p. 7). Each rollout has a 20-hour wall-clock budget (p. 4, p. 28).
- Baselines or comparison conditions: [V] Ten models with their scaffolds: GPT-6 Astra and GPT-5.6 Sol via Codex; Claude Opus 5, Claude Opus 4.8, Gemini 3.7 Flash, Kimi K3, GLM-5.3, Grok 4.6, Qwen3.8-Max-0902 and Qwen3.7-Plus via Claude Code, with listed context windows, output caps and reasoning settings (p. 28). For transfer: each run's first evaluated checkpoint (p. 1, p. 6). [I] No human-developer baseline is reported (checked p. 10-11, p. 28).

## 4. Dataset and sample
- Data source(s): [V] Native references from open-source GitHub repositories (desktop) and GitHub/F-Droid projects (Android), pinned to upstream commits; Web from 44 benchmark-authored synthetic sites and 6 openly licensed real sites (e.g. postgresql.org, webpack.js.org) (p. 7-8, p. 27). Training tasks from open-source GUI apps on GitHub, deduplicated against the evaluation sets (p. 5).
- Sample size (N) and unit: [V] 250 tasks (applications/websites), 50 per platform (p. 7). Median production source of references: Ubuntu 49.3k, macOS 13.5k, Windows 6.7k, Android 15.0k LOC (p. 8). 81 tasks package 393 fixture files (p. 8, p. 34). Training: 35,000 trajectories (7,000 per platform) (p. 5). One example app has 85 rule-based tests and 35 visual assertions (p. 20). [I] Total number of test cases across the suite: not reported (checked p. 8-9, p. 32-34).
- Sampling / selection method: [V] Excluded libraries, frameworks, extensions and apps needing login or remote services; references must run reproducibly; survivors balanced on domain, framework, source size, feature complexity and upstream activity (p. 8, p. 31-32). Android apps with first-run dialogs were patched to remove them (p. 31). Web pages screened by an agent on eight criteria, then human review (p. 32).
- Data availability (public? link?): [A] Benchmark, environments and test suites released via a website, GitHub, Hugging Face and ModelScope (p. 1, p. 27); per-task licence metadata provided (p. 26-27). The PDF shows link labels, not URLs; release not checked by us.

## 5. Experimental setup
- Procedure, settings, hyper-parameters, tools: [V] Task-isolated, versioned VM/container workers per rollout (p. 4); platform actions exposed as direct MCP tool calls (qwen-cua-driver 0.7.3 on desktop, mobile-mcp 0.1.5, Playwright MCP 0.0.79) (p. 5, p. 28). Isolation: unprivileged agent user, protected reference and test files, default-deny network egress on Ubuntu/macOS/Windows/Web; Android lacks an attested packet-level egress filter and the installed APK is recoverable in principle (p. 9-10, p. 36-38). Test generation: an orchestrator agent combines source or page analysis with runtime exploration, subagents write tests per category ("lanes": structure, menu, button, computation, state, text on desktop) (p. 8, p. 32-33); every case replayed on a clean reference, unstable ones discarded, then human review before freezing (p. 8-9). Transfer: SFT of Qwen3.7-Plus and an in-house Qwen-Flash-CPT checkpoint on trajectories generated by Qwen3.8-Max and filtered by rejection sampling on the verifiers (p. 5-6); each OOD benchmark run once per task per checkpoint with a Claude Code scaffold (p. 6, p. 28-29).
- Not reported [I] (checked p. 5-11, p. 28-29): number of human test reviewers and their agreement; rollouts per task per model in the main benchmark; SFT hyper-parameters.
- [I] The main benchmark is probably a single rollout per task. The one-rollout direct-MCP arm of the Windows / Claude Opus 4.8 comparison (Prog 35.05, VLM 31.00; p. 11) reproduces the Table 11 Windows / Claude Opus 4.8 scores exactly (35.05 / 31.00; p. 30). This is not stated explicitly.
- Code availability: [A] Harness, runners, evaluation code and configurations released on GitHub (p. 27); not checked.

## 6. Evaluation metrics
- Metric — what it measures — why chosen:
  - [V] **Programmatic score (Prog)**: fraction of frozen, reference-validated test cases passed, reading exact text, widget state, navigation, persistence or computed values through the platform accessibility/automation API (AT-SPI, AXUIElement, UI Automation, UiAutomator, DOM/ARIA); Web weights checks by specificity (p. 9). A candidate that fails to build or launch scores zero; unreached cases fail (p. 9).
  - [V] **VLM score**: binary verdicts from a Qwen3.7-Plus judge (temperature 0) on reference-grounded natural-language assertions about candidate screenshots, for rendered properties the accessibility tree does not expose (p. 9, p. 32).
  - [V] **Average score** = mean of Prog and VLM; apps macro-averaged within platform, platforms weighted equally (p. 9, p. 11). **Prog >= 90% / = 100%** = share of apps (near-)fully passing (p. 11).
  - [V] Chosen because they are implementation-agnostic: tests depend on observable behaviour, not source similarity, so agents may choose any architecture (p. 4, p. 8).
  - [V] Artifact metrics: production LOC (cloc), file count, largest-file share, UI framework family (p. 15-16, p. 30-31). Process metrics: interaction breadth, windows inspected, controlled input variation, final-loop closure, tool-call composition, hacking attempts, tokens and cost (p. 12-15).
  - [V] Suite coverage audit: 77% of cases leave the start surface, 24% traverse 2+ surfaces, 94.2% check an interaction outcome, 40.7% require an exact value (p. 9).
- Statistical testing (tests used, significance, effect sizes, confidence intervals): [V] Trajectory and resource figures show 95% bootstrap intervals (p. 12, p. 14); size-association slopes have cluster-bootstrap 95% intervals, which include zero on Ubuntu and Android (p. 31). [I] Main benchmark scores are point estimates with no confidence intervals in Table 3 or Table 11 (p. 11, p. 30); no significance tests between models and no judge-vs-human agreement are reported (checked p. 9, p. 11, p. 28-32).

## 7. Key findings
1. Recreation is far from solved: GPT-6 Astra leads with 58.19 Prog / 57.92 VLM / 58.06 average, then Claude Opus 5 (44.16) and GPT-5.6 Sol (42.06); Grok 4.6 is fourth (36.73) and Qwen3.7-Plus is lowest (9.15) — [V] (p. 1, p. 11). (Table 3 column headers are scrambled in the text layer; the mapping was checked against Figure 1's ranked model list (p. 1) and word positions in the PDF (p. 11).)
2. Full functional fidelity is rare: GPT-6 Astra reaches Prog >= 90% on 17.6% and Prog = 100% on 2.8% of apps; every other model reaches at most 5.53% and 0.8% — [V] (p. 11, p. 16).
3. Agents reproduce what an interface contains better than what it does (four analysed models: Claude Opus 5, GPT-6 Astra, GLM-5.3, Qwen3.8-Max-0902; p. 12, p. 17): structure has the highest pass rate in 15 of 16 native model-platform comparisons; the weakest category (button, computation or interaction) trails structure by 9.1-34.4 points; on Web, static content beats interaction by 28.2-36.7 points — [V] (p. 16-17). Example: a recreation with 100.0% VLM but only 55.1% Prog (p. 18).
4. Rebuilt apps are much smaller and more concentrated: 89.4% have less production source than the reference (median LOC ratio 16.9%); 92.3% use fewer files; 83.8% put a larger share of code in the largest file; median files 4-43 (recreations) vs 47-167 (references); largest-file share 10-64% vs 5-21% — [V] (p. 15-16). Recreation size barely tracks reference size (log-log slopes 0.08-0.23) — [V] (p. 15). Scope: four models analysed (Claude Opus 5, GPT-6 Astra, GLM-5.3, Qwen3.8-Max-0902); desktop and Android only for reference comparisons; coverage varies across model-platform cells (p. 12, p. 15). [I] Per-cell denominators are not reported (checked p. 15-16, p. 30-31).
5. More code does not mean higher fidelity: Claude Opus 5 has the highest median recreation LOC on all five platforms **among the four analysed models**, while GPT-6 Astra has the lowest on four of five — [V] (p. 15); robust to a common-project restriction (p. 31). Scope as in finding 4 (p. 12, p. 15).
6. Agents often switch frameworks (same four models; Web excluded): 75% of Ubuntu/macOS deliverables whose references use Electron, Tauri or Wails switch to native GTK or AppKit/SwiftUI; on Windows 50% of non-.NET references are rebuilt in WPF or WinForms — [V] (p. 16). [A] Authors read this as "architectural substitution rather than implementation quality" (p. 16).
7. Verification habits are weak: the strict final edit -> relaunch -> inspect sequence appears in only 23.6-47.5% of trajectories; controlled input variation in 13.4-17.0% — [V] (p. 12, p. 17-18). Scope: four models analysed (Claude Opus 5, GPT-6 Astra, GLM-5.3, Qwen3.8-Max-0902) (p. 12). [I] Trajectory counts per model-platform cell are not reported (checked p. 12-15).
8. Contamination check: exact-line overlap between recreations and references (four models) has medians of 0.014-0.088% and maxima below 3.2% — [V] (p. 18). Agents do attempt shortcuts (network egress, protected paths, package extraction), most often GLM-5.3 among the four analysed models — [V] (p. 13). Two Web case studies replayed reference content. Ablira (72.73% Prog / 40.79% VLM, p. 46) was caught by the scrape detector, so the 0.10 aggregate cap applies (p. 38, p. 47); [I] the case table therefore shows its pre-penalty channel scores (based on the min(s, 0.10) rule, p. 9, p. 38). Kartova escaped detection and kept 54.82% Prog / 14.63% VLM (34.72% average) — [V] (p. 47).
9. Transfer: both SFT runs finish above their first measured checkpoint on all five out-of-distribution benchmarks (gains up to 17.9 points), but curves are not monotonic — [V] (p. 3, p. 6). [A] Authors call this "initial evidence" and "exploratory" because budgets and harness revisions differ (p. 3, p. 29).
10. A programmable SDK interface (one rollout, 50 Windows apps, Claude Opus 4.8) kept quality similar (Prog 35.05 vs 35.60) while cutting estimated cost from $90.50 to $41.58 and wall-clock time from 4.12 to 3.04 h per task — [V] (p. 11).

## 8. Limitations stated by the authors
- [A] Pinned, reproducible environments limit coverage of live services, changing external state and real users (p. 21).
- [A] Hidden suites sample a finite set of outcomes, so passing them "cannot establish equivalence across all states and interaction paths" (p. 22).
- [A] Public references may be in pretraining data; source-overlap screening cannot rule out memorisation or all source reuse (p. 22, p. 18).
- [A] Trajectory and artifact comparisons are descriptive; model identity, harness and runtime vary together, so no behaviour is shown to cause higher scores (p. 3, p. 11, p. 16).
- [A] Android isolation is weaker (no attested egress filter; installed APK recoverable) and Web cannot be source-blind (p. 7, p. 10, p. 37).
- [A] OOD transfer runs differ in budgets and harness revisions and are "exploratory evidence" (p. 29). Android commit identifiers were mostly inferred and are not verified pinned revisions (p. 30).
- [A] Scores are not comparable with the earlier in-house version reported in a blog post (p. 27).

## 9. Limitations we identified
- [I] **Conflict of interest not declared.** All authors are from Alibaba (p. 1); the training data are generated by Qwen3.8-Max, the VLM judge is Qwen3.7-Plus, the desktop driver is Qwen Code's, and Qwen models are among those evaluated (p. 5, p. 9, p. 28). No COI statement. Qwen3.7-Plus, which is also the VLM judge (p. 9), is the lowest-scoring evaluated model (VLM 9.12, average 9.15, p. 11). So no favourable self-scoring is visible, but judge self-preference was not tested.
- [I] **No variance.** Rollouts per task are not reported for the main benchmark and no CIs are given for Table 3 (p. 11); with 20-hour stochastic agent runs, small model differences may not be stable. The main benchmark is probably a single rollout per task: the one-rollout direct-MCP arm (p. 11) reproduces the Table 11 Windows / Claude Opus 4.8 scores exactly (p. 30). This is not stated explicitly.
- [I] **Judge and reviewer reliability unknown.** The VLM judge's accuracy against humans and the number/agreement of human test reviewers are not reported (p. 8-9).
- [I] **Scaffold confound.** GPT models run in Codex, all others in Claude Code (p. 28), so model and harness are entangled in the main ranking.
- [I] **Unexplained denominators.** Claude Opus 5's Web Prog >= 90% of 13.64% (p. 30) cannot come from 50 tasks (every value would be a multiple of 2.00, as the other cells in that row are); it fits 6/44 (or 3/22). The paper invalidates runs that fail isolation checks (p. 9) and reports evaluator-valid subsets elsewhere (p. 11, p. 20), so some runs were probably excluded. The number of excluded runs per model and platform is not reported.
- [I] **Score integrity gap.** A transformed replay (Kartova) evaded the scrape detector and kept 54.82% Prog / 14.63% VLM (p. 47). The detected replay (Ablira, p. 47) falls under the 0.10 aggregate cap (p. 38), so its reported 72.73% / 40.79% (p. 46) are pre-penalty channel scores. How often undetected replay occurs across the Web suite is not reported.
- [I] **Transfer design is uncontrolled.** Improvements are measured from the first evaluated checkpoint (p. 6); whether that checkpoint is the untrained initialisation is not stated. Each OOD benchmark is run once per task (p. 28), the curves are non-monotonic (p. 6), and there is no control SFT mixture (e.g. equally long non-recreation agent trajectories; none described, p. 5-6, p. 29). Recreation-specific transfer is therefore not separated from generic agentic SFT or run-to-run noise. "Gains of up to 17.9 percentage points" (p. 3) is a single best-case last-vs-first difference with no uncertainty.
- [I] **Code quality only as size/structure.** LOC, file count, largest-file share and framework (p. 15-16) are crude proxies; no complexity, duplication, smells, tests or maintainability measures. "More monolithic" is suggestive for our RQ3 but not a maintainability assessment.
- [I] **Web scores are panel-relative.** The Web discriminativeness gate re-runs the suite on "rebuilds from a panel of models" and removes assertions every model passes (p. 34), making Web scores depend on that panel. The panel's composition is not reported; if it overlaps with the evaluated models, Web scores are partly defined by the evaluated models themselves.

## 10. Threats to validity
- Internal (confounds, leakage, selection): [I] Strong isolation design (p. 9-10, p. 36-38) and an overlap audit (p. 18) reduce leakage, but Android and Web are weaker by design (p. 7, p. 10), and hacking attempts occur (p. 13). Model and scaffold are confounded (p. 28). Patched Android references (p. 31) differ from upstream builds.
- External (generalisability of sample/context): [I] Open-source, offline, login-free apps of moderate size (p. 8); Web is mostly synthetic (44 of 50, p. 7). Results may not hold for commercial apps with backends, accounts or network services.
- Construct (do metrics measure the concept?): [I] Prog and VLM measure agreement with a finite, reference-validated test sample (p. 22), with depth and specificity audited (p. 9) — a good proxy for functional and visual fidelity but not equivalence. Size and file metrics are not code-quality measures (p. 16).
- Statistical conclusion (power, multiple comparisons, variance): [I] 50 apps per platform; no CIs on main scores; bootstrap CIs on secondary analyses (p. 12, p. 14, p. 31); slopes not distinguishable from zero on two platforms (p. 31).
- Reproducibility (data/code/setup reported?): [I] High: pinned environments, versions, model configs, licence metadata and release of benchmark and harness (p. 26-28). Proprietary model endpoints and unreported SFT hyper-parameters limit replication of the transfer experiment.

## 11. Future research directions
- Stated by authors [A] (p. 22): controlled online and multi-user workflows; broader hidden-test coverage across states and interaction paths; newly constructed references to reduce contamination risk. Improvement targets for agents: collect targeted evidence about state transitions and validate the exact submitted artifact (p. 18).
- Suggested by us [I]: (a) add maintainability measures (complexity, duplication, modularity, test presence) to the artifact analysis and relate them to Prog/VLM; (b) run several rollouts per task and report CIs; (c) validate the VLM judge against human ratings; (d) include a human-developer recreation baseline.

## 12. Relevance to our research
- Research questions addressed (RQ ids): RQ1, RQ2, RQ3 (partial), RQ4, RQ5.
- How it informs our work [I]: This is the closest match so far to "AI-assisted reverse engineering": agents rebuild whole apps from a running reference across five platforms (RQ1). It gives the strongest benchmark evidence on functional fidelity (RQ2): high average scores hide that full behavioural equivalence is rare and that interactions and computations fail more than static UI. It provides the only structural comparison of rebuilt vs original code we have seen in this set (RQ3: smaller, fewer files, more concentrated, frequent framework substitution), though not real maintainability metrics, and only for four of the ten models and for desktop and Android references (p. 12, p. 15). Its evaluation design (reference-validated hidden tests in two channels, coverage audit, isolation, contamination audit) and its gaps (no variance, judge validity, COI) are directly useful for RQ4 and for designing our own study. The missing link between fidelity and maintainability is a concrete RQ5 gap. [I] Directionally consistent with [@chen2025iwr]. Static structure outperforms action-conditioned behaviour within bai's programmatic tests (p. 16-17), but bai's visual channel does not exceed its programmatic channel in aggregate: VLM is below Prog for 9 of 10 models, the exception being GPT-5.6 Sol at 43.49 vs 40.63 (p. 11). The two papers measure the gap differently.

## 13. Evidence table (for the evidence matrix)
| RQ | Claim | Page | Label | Strength |
|---|---|---|---|---|
| RQ1 | Hybrid agents can rebuild runnable apps from a running reference (no source on desktop/Android) across Ubuntu, macOS, Windows, Android and Web; 10 frontier models evaluated on 250 tasks | 3, 7, 11 | V | moderate |
| RQ2 | Best agent averages 58.06% (Prog 58.19, VLM 57.92) but fully passes the programmatic suite on only 2.8% of apps (others <= 0.8%) | 11 | V | moderate |
| RQ2 | Static structure is reproduced more reliably than actions and computed outputs (structure best in 15/16 native comparisons; gaps 9.1-34.4 pts; Web 28.2-36.7 pts; four analysed models) | 12, 16, 17 | V | moderate |
| RQ2 | A recreation can score 100% visually yet only 55.1% programmatically | 18 | V | weak |
| RQ3 | Recreations are much smaller and more concentrated than references: 89.4% smaller (median LOC ratio 16.9%), 92.3% fewer files, 83.8% larger largest-file share (four models analysed: Claude Opus 5, GPT-6 Astra, GLM-5.3, Qwen3.8-Max-0902; desktop and Android only; coverage varies across model-platform cells) | 12, 15, 16 | V | moderate |
| RQ3 | More generated code does not mean higher fidelity among the four analysed models (highest-LOC model is not the best; best model has lowest LOC on 4/5 platforms; coverage varies across cells) | 12, 15, 31 | V | weak |
| RQ3 | Agents frequently switch UI framework (e.g. 75% of Electron/Tauri/Wails references rebuilt natively; four analysed models, Web excluded); authors frame this as architectural substitution, not quality | 15, 16 | V | weak |
| RQ4 | Fidelity measured by reference-validated, human-reviewed hidden tests in a programmatic and a VLM channel; 94.2% of cases check interaction outcomes | 9 | V | moderate |
| RQ4 | No CIs or repeated runs for main scores (probably one rollout per task); judge accuracy and reviewer agreement not reported; model and scaffold confounded. Our appraisal of absences, based on Tables 3, 8, 11 and the evaluation text | 8, 9, 11, 28, 30 | I | moderate |
| RQ4 | Agents attempt evaluation shortcuts (four analysed models) | 13 | V | weak |
| RQ4 | A transformed replay evaded the scrape detector and scored 54.82% Prog (p. 47); detected replay is capped at 0.10 (p. 38) | 38, 46, 47 | V | weak |
| RQ5 | Fidelity is measured in detail, but maintainability of rebuilt code is assessed only through size and structure proxies. Our appraisal; [A] authors themselves say the framework data show "architectural substitution rather than implementation quality" (p. 16) | 15, 16 | I | moderate |

Strength note [I]: moderate = large, well-controlled benchmark (250 tasks, 5 platforms) but a single non-peer-reviewed study without variance reporting; case-study and descriptive rows are weak.

## 14. Key quotes
> "GPT-6 Astra leads at 58.1% overall, but passes all programmatic tests on just 2.8% of tasks." (p. 1)

> "Evaluated recreations reproduce what an interface contains more reliably than what it does." (p. 16)

> "the transition data therefore show architectural substitution rather than implementation quality" (p. 16)

> "Ablira and Kartova show that programmatic and VLM scores can reward reference-content replay" (p. 47)

## Analyst notes
- Reading coverage: sections read / skipped and why: all 47 PDF pages read via `fulltext.txt`, including appendices A-D (reproducibility, evaluation settings, per-platform results, benchmark construction, isolation, harness, case studies). Reference list (p. 23-25) skimmed. Plots (Figures 1, 3, 5, 6, 10-17) are partly garbled in the text layer; numbers were taken from the text and tables, not read off the plots.
- Uncertainties: (1) rollouts per task in the main benchmark are not reported; probably one, since the one-rollout direct-MCP arm (p. 11) matches Table 11 Windows / Claude Opus 4.8 exactly (p. 30); (2) the total number of test cases is not reported; (3) Claude Opus 5's Web Prog >= 90% of 13.64% (p. 30) cannot come from 50 tasks and fits 6/44 or 3/22; run invalidation (p. 9) and evaluator-valid subsets (p. 11, p. 20) make exclusions likely, but their number is not reported; (4) Ablira was caught by the scrape detector (p. 47), so its case-table scores (72.73 / 40.79, p. 39, p. 46) are pre-penalty channel scores under the min(s, 0.10) rule (p. 38); only Kartova (54.82 / 14.63, p. 47) shows an undetected replay keeping a real score; (5) the paper evaluates models (GPT-6 Astra, Claude Opus 5, etc.) that we cannot independently verify; all such facts are taken from the paper as reported; (6) paper inconsistency: Table 12 (p. 39) lists a case "GLM-5.2 / Ubuntu", but the evaluated models in Table 8 (p. 28) include glm-5.3, not GLM-5.2. Not resolvable from the text.
- Table 3 (p. 11) and Table 11 (p. 30) column headers are scrambled in `fulltext.txt`. Column-to-model mapping was checked with `pdftotext -bbox` word positions and against the ranked model list in Figure 1 (p. 1). An earlier version of this analysis misread Grok 4.6 as lowest; corrected to Qwen3.7-Plus (2026-11-12, critical review batch C).
- The scaffold's frontmatter was pre-filled by an earlier run; we checked each field against the text and corrected `dataset` and shortened `main_finding` to 25 words or fewer.
