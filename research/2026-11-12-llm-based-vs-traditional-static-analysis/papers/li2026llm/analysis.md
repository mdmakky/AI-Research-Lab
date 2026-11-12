---
key: li2026llm
status: complete
evidence_basis: full-text
design: comparative empirical study; 5 specialized LLM detectors + 2 general coding agents vs 4 SAST tools, controlled benchmark + real-world projects, FP root-cause taxonomy, cost measurement
dataset: controlled set of 265 known vulns (ReposVul C/C++; CWE-Bench-Java; JLeaks) across 8 CWEs; 24 real-world C/C++ and Java projects/modules
sample_size: 265 known vulnerabilities (110 C/C++, 155 Java); 24 projects/modules; 6,442 sampled warnings; 5,896 FPs classified; 355 manually coded reports
metrics: recall, precision (controlled); #warnings, sampled false discovery rate SFDR (real-world); tokens, USD, minutes per project and per warning
main_finding: General agents (Codex, Claude Code) reach highest recall; specialized LLM detectors and SAST tools have near-zero recall on some CWEs and 75-100% SFDR; LLM cost up to $1,248/project.
relevance: high
analysed: 2026-11-12
---
<!-- Frontmatter: single-line values; they feed literature-matrix.md via `rlab index`.
     status: draft (in progress) -> ready (analyst self-check passed) -> complete (critical review passed).
     evidence_basis: full-text | abstract-only. abstract-only analyses must not fill methodology detail.
     relevance: high | medium | low. -->

# LLM-based Vulnerability Detection at Project Scale: An Empirical Study

- Authors: Li, Fengjie; Jiang, Jiajun; Chen, Dongchi; Xiong, Yingfei
- Year / venue: 2026, IEEE Transactions on Software Engineering (published)
- DOI: 10.1109/tse.2026.3742453 · URL: https://doi.org/10.1109/tse.2026.3742453
- Source text: `fulltext.txt` (page refs = PDF page index). Our PDF is arXiv:2601.19239v2 (25 Sep 2026, stamp on p. 1), not the IEEE version of record; page numbers and possibly some numbers may differ from the TSE copy.

Labels: **[V]** verified in the paper's own data/tables/results · **[A]** author claim · **[I]** our interpretation.
Every [V]/[A] item ends with a page ref `(p. N)`. Write "not reported" when the paper does not say.

## 1. Research objective
Systematically evaluate specialized project-scale LLM-based vulnerability detectors against general-purpose coding agents and traditional static analyzers on (a) known vulnerabilities and (b) current real-world projects, explaining their false positives and measuring their cost [A] (p. 1, p. 2).

## 2. Research questions / hypotheses
- RQ1: How effective are LLM-based methods at detecting known vulnerabilities in a controlled benchmark? [V] (p. 3)
- RQ2: How reliable are they on real-world projects/modules, in terms of false discovery rates? [V] (p. 3)
- RQ3: What are the root causes of false positives? [V] (p. 4)
- RQ4: What is the overhead (tokens, money, time) of project-scale LLM detection? [V] (p. 4)
- No formal hypotheses.

## 3. Methodology
- Research design: comparative empirical benchmark study, plus qualitative FP root-cause taxonomy (open coding, double coding) and LLM-assisted (Codex) labelling with stratified manual validation [V] (p. 6, p. 11, p. 13).
- Approach / model / intervention (Table I, p. 4) [V]:
  - Specialized LLM-based: RepoAudit (multi-agent; Claude Sonnet 3.5 / GPT-5.4; C/C++; CWE-401/416/476), KNighter (LLM-synthesised Clang Static Analyzer checkers; o3-mini / GPT-5.4; C/C++), IRIS (LLM-inferred sources/sinks + CodeQL; GPT-4 / GPT-5.4; Java; CWE-022/078/079/094), LLMDFA (multi-agent dataflow; GPT-4 / GPT-5.4; Java; CWE-078/079), INFERROI (LLM intent inference + CFG; GPT-4 / GPT-5.4; Java; CWE-772) (p. 4, p. 5).
  - General agents: Codex (GPT-5.4) and Claude Code (Claude Sonnet 4.6), all CWEs, internet search disabled (p. 4, p. 7).
  - Each specialized method run with its original backbone and with GPT-5.4 to separate model from workflow effects (p. 4).
- Baselines or comparison conditions: traditional SAST — CodeQL (48 selected rules, C/C++ and Java), Semgrep (59 rules, C/C++ and Java), SpotBugs + Find Security Bugs (21 patterns, Java), Clang Static Analyzer CSA (12 checkers, C/C++) [V] (p. 4, p. 7). Rules were manually curated to the target CWEs; all severities treated equally [V] (p. 7). No deep-learning (fine-tuned/GNN) detectors and no prompt-only/RAG function-level methods (excluded because they do not produce repository-level warnings) [V] (p. 4). LLMxCPG excluded (needs local fine-tuning) [V] (p. 4).

## 4. Dataset and sample
- Data source(s): controlled dataset from ReposVul (C/C++), CWE-Bench-Java (Maven projects only) and JLeaks (50 randomly sampled resource leaks); all cases manually checked for validity and successful compilation [V] (p. 5). Real-world dataset: 24 actively maintained projects/modules with historical vulnerabilities in the studied CWEs (e.g. Linux subsystems, ImageMagick, Vim, gpac, bitlbee; OpenOLAT, Spark, DSpace, XStream, Jenkins, Keycloak, Tika, xwiki, ActiveMQ, RxJava, jsoup) [V] (p. 5, p. 6).
- Sample size (N) and unit: 265 known vulnerabilities — C/C++: CWE-401 50, CWE-416 25, CWE-476 35; Java: CWE-022 49, CWE-078 11, CWE-079 28, CWE-094 17, CWE-772 50 [V] (p. 6). 24 projects/modules sized 1,715 to 6,033,855 LOC [V] (p. 6). Up to 300 warnings sampled per tool per project → 6,442 warnings; 5,896 FPs classified; 355 warnings manually coded to build the taxonomy (>150 person-hours) [V] (p. 6, p. 11, p. 13).
- Sampling / selection method: for ReposVul, the three repositories with most cases per CWE (to limit build effort); 8 CWEs chosen by tool support and benchmark availability [V] (p. 5). 21 of 24 real-world commits postdate the August 2025 knowledge cutoff of GPT-5.4 and Claude Sonnet 4.6 [V] (p. 5). Several C/C++ modules come from the same Linux commit [A] (p. 18). No power analysis.
- Data availability (public? link?): artifacts (scripts, prompts, taxonomy labels, statistics) at https://github.com/Feng-Jay/LLM4Security [V] (p. 2).

## 5. Experimental setup
- Procedure, settings, hyper-parameters, tools: released replication packages of each specialized tool with hyper-parameters from the original papers; no extra timeouts or token/money budgets [V] (p. 6). Default RepoAudit configuration; IRIS/LLMDFA/INFERROI use their own LLM-generated API lists; KNighter checkers generated from 18 bug-fixing patches from its original study [V] (p. 7). General agents via official CLIs with built-in tools/skills, internet off [V] (p. 7). Official OpenAI/Anthropic APIs; local server with dual Xeon 6388, 512 GB RAM, Ubuntu 20.04.6 [V] (p. 7). Each LLM configuration run once [A] (p. 18).
- Controlled-dataset TP rule: a vulnerability counts as detected if the tool reports the labelled vulnerable program point; FPs are warnings in known vulnerable files that do not match the known data-flow pattern (IRIS protocol) [V] (p. 5, p. 6).
- Real-world labelling: Codex labels each sampled warning TP/FP with access to the repository; validation on up to 5 TPs + 5 FPs per tool per repo (197 TPs, 424 FPs) [V] (p. 11).
- Code availability: yes, project homepage above [V] (p. 2). Appendices A–C (FP examples, rule lists, detailed cost statistics) are referenced but are not in our 20-page PDF (p. 7, p. 13, p. 15).

## 6. Evaluation metrics
- Metric — what it measures — why chosen:
  - Recall = TP/(TP+FN) and Precision = TP/(TP+FP) on the controlled set, following prior studies [V] (p. 5, p. 6).
  - #Reports, #Files, #Sampled FPs and SFDR = #Sampled FPs / #Sampled Reports on real-world projects, because ground truth is unknown there [V] (p. 6).
  - Input/output tokens, USD and end-to-end minutes per project/module; cost and minutes per warning [V] (p. 6, p. 15, p. 16).
- Statistical testing (tests used, significance, effect sizes, confidence intervals): no significance tests between tools. Labelling accuracy estimated with stratified sampling, normal approximation and finite-population correction at the 95% level [V] (p. 11, p. 13); the intervals themselves are not printed in the text we have.

## 7. Key findings
1. C/C++ controlled set: general agents average recall 59.55% (131/220) and precision 32.19% (131/407); KNighter detects 0 vulnerabilities in all three CWEs; RepoAudit with its original backbone (Claude Sonnet 3.5) detects 0 of 110 (0 TPs among 40 warnings: 0 warnings on CWE-401, 33 on CWE-416, 7 on CWE-476), and RepoAudit (GPT-5.4) detects 2 (CWE-476 recall 5.71%) — [V] (p. 7, Table IV).
   - Table XII lists a minimum of 0.00K input tokens and $0.00 for both RepoAudit variants on the real-world projects — [V] (p. 16). [I] So on at least one project RepoAudit made no LLM call at all; this fits the authors' finding that incomplete API modelling explains all 108/108 RepoAudit (GPT-5.4) misses (p. 7), i.e. sources/sinks were never matched. Relevant to the guo2025repoaudit tension (§9).
2. C/C++ per CWE (Table IV): CWE-401 Codex R 68.00% / P 41.98%, Claude Code R 80.00% / P 40.00%, CodeQL R 6.00% / P 14.29%, Semgrep and CSA 0%; CWE-416 Codex R 40.00%, Claude Code R 36.00%, CodeQL/Semgrep/CSA 0%; CWE-476 Codex R 62.86%, Claude Code R 45.71%, CodeQL R 34.29% with 1,110 warnings (P 1.08%) — [V] (p. 7).
3. Java controlled set: Codex average recall 63.87% (99/155), Claude Code 81.94% (127/155); CodeQL 14.19%, Semgrep 6.67%, SpotBugs 14.84%; LLMDFA (GPT-5.4) finds 1 vulnerability; INFERROI (GPT-5.4) reaches 66.00% recall on CWE-772 vs CodeQL 10.00% and SpotBugs 6.00% — [V] (p. 9, Table VI p. 10).
4. Java precision is low for most tools (e.g. CWE-022: IRIS GPT-4 6.30%, Semgrep 0.29% from 2,075 warnings, SpotBugs 1.76%, Codex 58.73%, Claude Code 37.29%) — [V] (p. 10, Table VI).
5. Swapping in GPT-5.4 barely changes recall of specialized methods but raises some precision (IRIS CWE-078 6.06% → 20.00%; INFERROI 15.74% → 20.50%) — [V] (p. 9). The authors conclude that the workflow, not the model, limits recall (e.g. RepoAudit GPT-5.4 vs Codex on the same model) — [A] (p. 9).
6. Incomplete API modelling and incomplete candidate exploration explain 108/108 (RepoAudit GPT-5.4), 97/110 (KNighter GPT-5.4), 40/44 (Codex) and 40/45 (Claude Code) missed C/C++ vulnerabilities — [V] (p. 7). With perfect allocation/deallocation API specs on CWE-401, recall rises: RepoAudit 0 → 48%, Codex 68 → 90%, Claude Code 80 → 96%, CodeQL 6 → 56% — [V] (p. 8, Table V).
7. Vulnerabilities missed by general agents sit in larger files than detected ones (Fig. 4 C/C++, Fig. 6 Java) — [V] (p. 9, p. 10). The authors attribute this to file size and complexity, and say IRIS and INFERROI are largely unaffected because they reason over compact representations such as CFGs — [A] (p. 8, p. 10).
8. LLM-based tools contribute most unique detections; traditional tools add few unique ones (CodeQL at most 3 unique on CWE-022) — [V] (p. 9, p. 10, Fig. 5).
9. Real-world C/C++ (Table VII): overall SFDR RepoAudit (Sonnet 3.5) 92.77%, KNighter (o3-mini) 81.25%, Codex 9.09% (2.44 warnings/project), Claude Code 74.07%, CodeQL 86.01% (752.67 warnings/project; 6,345 on gpac), Semgrep 100.00%, CSA 85.51% — [V] (p. 11). GPT-5.4 versions: RepoAudit 95.41%, KNighter 95.56% (Table VIII) — [V] (p. 11).
10. Real-world Java (Table IX): IRIS (GPT-4) 97.80% SFDR with 232.42 warnings/project, LLMDFA 100.00%, INFERROI 96.40%, Codex 31.82% (1.47 warnings/project), Claude Code 81.82%, CodeQL 77.00%, Semgrep 92.71%, SpotBugs 86.21%; traditional tools emit warnings in only about half of projects — [V] (p. 12). IRIS with GPT-5.4 drops to 78.73% (Table X) — [V] (p. 12).
11. Codex labels were 94.36% accurate on 621 manually validated warnings (population-weighted 98.16%); Codex FP-reason labels 87.76% accurate on 425 cases (weighted 92.52%) — [V] (p. 11, p. 13).
12. FP root causes: incorrect program-point classification B1 = 63.33% (3,734/5,896) and truncated interprocedural context A1 = 14.60% (861/5,896); LLM tools additionally show incorrect control flow (A2), missed sanitizers/guards (D1, >15% in 7 of 12 LLM settings) and prompt deviations (C1) — [V] (p. 15, Table XI p. 14). CodeQL's largest FP causes are A1 35.80% and path-insensitivity D3 20.17% — [V] (p. 14).
13. Cost (Table XII): RepoAudit (Sonnet 3.5) up to 225,493.97K input and 38,078.26K output tokens and $1,247.66 for one project, average $172.77; LLMDFA (GPT-4) average $61.60 and 2,000 min per Java project (max 4,638 min); IRIS (GPT-4) average $2.59, 213.44 min; INFERROI average $11.62–$12.99; KNighter $0.34–$2.36; Codex $5.38 / 14.80 min; Claude Code $9.67 / 13.19 min per project. SAST average runtimes 0.64 (Semgrep) to 60.92 (CSA) minutes, no token cost — [V] (p. 16).
14. Per warning: Codex $2.93 and 8.1 min, Claude Code $1.77 and 2.4 min; LLMDFA >$24 and >800 min per warning — [V] (p. 15, p. 16).

## 8. Limitations stated by the authors
- [A] Controlled evaluation counts warnings about other, unlabelled genuine vulnerabilities as FPs (p. 18).
- [A] Each LLM configuration run once; nondeterminism may affect results (p. 18).
- [A] Taxonomy and labels involve expert judgement; large-scale labels partly come from Codex and may contain model bias (p. 18).
- [A] Pretraining contamination possible for both datasets; post-cutoff commits may retain older code; sessions showed no explicit reliance on CVE data (p. 18).
- [A] Tool selection, two languages (C/C++, Java), 8 CWEs; several Linux modules share one repository/commit; no concurrency or type-confusion bugs; may not generalise to Rust, Go, TypeScript or multi-language projects (p. 18).

## 9. Limitations we identified
- [I] Codex (GPT-5.4) is both an evaluated detector and the main TP/FP labeller and FP-reason classifier. Codex has by far the lowest SFDR (9.09% C/C++, 31.82% Java). Validation was stratified (≤5 TPs + ≤5 FPs per tool per repo), so a judge that favours its own reports is only partly ruled out; per-tool labelling accuracy is not reported. Based on p. 11 and Tables VII/IX.
- [I] The low SFDRs of general agents rest on very few warnings (Codex: 2.44 × 9 ≈ 22 C/C++ and 1.47 × 15 ≈ 22 Java warnings), so they are imprecise; no per-tool confidence intervals are shown. Based on Tables VII and IX (p. 11, p. 12).
- [I] Controlled-set precision only counts FPs inside known vulnerable files, so it is not project-wide precision and is not comparable with SFDR or with precision in other papers. Based on p. 6.
- [I] SAST rule sets were curated by the authors (48/59/21/12 rules); other rule choices could change SAST recall and FP counts. Based on p. 7.
- [I] The controlled benchmark uses public CVEs that likely predate model training; general agents' high controlled recall may partly reflect memorisation even without explicit lookup. The post-cutoff real-world set gives no recall, so recall on unseen code is not measured. Based on p. 5, p. 18.
- [I] No deep-learning (fine-tuned) detectors are compared: informs LLM vs SAST, not LLM vs DL. Based on p. 4.
- [I] Backbones differ across tools (Claude Sonnet 4.6 vs GPT-5.4 vs GPT-4), so agent-vs-specialized comparisons mix workflow and model effects, partly controlled by the GPT-5.4 re-runs. Based on Table I (p. 4).
- [I] Documented tension with guo2025repoaudit (RepoAudit's own evaluation); both sides are confirmed in the texts and neither is a replication of the other. Based on the pages cited below.
  - Effectiveness. guo: RepoAudit (Claude 3.5 Sonnet) reproduces all 21 previously reported bugs and finds 19 new ones, 40 TPs / 11 FPs, precision 78.43%, on 15 C/C++ projects [@guo2025repoaudit, p. 7, p. 8]. li: RepoAudit (Sonnet 3.5) detects 0/110 and RepoAudit (GPT-5.4) 2/110 known C/C++ vulnerabilities (p. 7); real-world SFDR 92.77% as a 9-project average (p. 11).
  - Cost. guo: average $2.54 and 0.44 h per project, maximum $18.15 (icu) [@guo2025repoaudit, p. 7, p. 8]. li: average $172.77, maximum $1,247.66 per project, and over 800 min maximum runtime (p. 15, p. 16). The project behind the $1,247.66 maximum is not named in the main text; details are deferred to Appendix C (p. 15), which our PDF lacks.
  - Dataset. guo's targets are bug reports of prior tools [@guo2025repoaudit, p. 7]. li's controlled set is ReposVul CVEs from "the three repositories with the most cases" per CWE, and li does not name those repositories (p. 5). The targets overlap only with li's *real-world* set, where recall is not measured: linux/sound, linux/mm, linux/drivers/net, linux/drivers/peci and ImageMagick (Table III, p. 6; [@guo2025repoaudit, p. 7]). For 3 of these 5 the bug type differs: ImageMagick is NPD in guo but CWE-401 in li, linux/driver(s)/net is MLK vs CWE-416, and peci is UAF vs CWE-476. Sizes differ at every shared target. For example, linux/sound is 1,378,262 LoC in guo vs 1,253,234 in li, and guo analyses ImageMagick/MagickCore (242,555) while li analyses the whole ImageMagick repository (680,878). guo's "linux/driver/net" (914,025) is closer in size to li's linux/net (962,143) than to li's linux/drivers/net (3,924,621), so the module mapping is unclear. On li's linux/net, RepoAudit emits 3 warnings with an SFDR of 66.67% (Table VII, p. 11). On the other shared projects li's RepoAudit (Sonnet 3.5) emits 0 warnings (linux/sound, linux/mm, ImageMagick), 1 FP (linux/drivers/net) and 3 FPs (peci) (Table VII, p. 11).
  - Commit. guo analyses the versions used by the earlier works, and its new bugs are "in historic versions" [@guo2025repoaudit, p. 7, p. 8]. li uses recent commits 6093a68 (Linux) and 3bf1076 (ImageMagick) (p. 6). guo's 4 Linux known bugs are all intra-procedural [@guo2025repoaudit, p. 8], and li notes that RepoAudit was evaluated on only 4 intra-function Linux cases (p. 7).
  - Metric. guo reports precision on the tool's own reports and reproduction of 21 known bugs. li reports recall on CVEs (controlled set) and SFDR (real-world set).
  - Labeller. guo does not describe how RepoAudit's own reports were judged TP/FP; only the Infer/CodeGuru reports are said to be labelled manually [@guo2025repoaudit, p. 14]. li used Codex labels with stratified manual validation (p. 11).
  - Scale. guo's projects average 251 KLoC, and its 4 Linux modules took only 1–35 prompts and $0.03–$0.86 each [@guo2025repoaudit, p. 7, p. 8]. li runs RepoAudit with no time or money budgets (p. 6) on modules up to 3,924,621 LOC; it emits 77 warnings on gpac and 374 on bitlbee (Tables III and VII, p. 6, p. 11). guo itself says cost depends on the number of source elements [@guo2025repoaudit, p. 9].
  - Explanation (ours). Target selection, code version, bug-type mapping, project scale and metric all differ, so the results are not directly comparable. RepoAudit made no LLM call on at least one project in li (0.00 tokens, Table XII, p. 16), and guo's Linux runs used very few prompts. Together with li's API-modelling analysis (p. 7), this points to source/sink coverage as one plausible mechanism for both the low recall and the cost spread.

## 10. Threats to validity
- Internal (confounds, leakage, selection): LLM self-labelling (see 9); pretraining contamination acknowledged (p. 18); single runs (p. 18); different backbones per tool (p. 4).
- External (generalisability of sample/context): C/C++ and Java only, 8 CWEs, 24 projects with several from one Linux commit (p. 18); tools limited to publicly available, runnable ones (p. 4).
- Construct (do metrics measure the concept?): SFDR measures false alarms among sampled warnings, not missed vulnerabilities; controlled precision is file-restricted (p. 6); all SAST severities counted equally (p. 7).
- Statistical conclusion (power, multiple comparisons, variance): no significance tests between tools; small warning counts for some tools; no run-to-run variance.
- Reproducibility (data/code/setup reported?): good — artifacts, prompts and rule lists released (p. 2, p. 7); API model versions may change.

## 11. Future research directions
- Stated by authors [A]: combine flexible agents with program-analysis support such as path constraints, IRs and validators (p. 17); integrate LLMs with formal analysis/symbolic execution (p. 17); evidence-grounded API-role/specification inference with iterative validation (p. 17); explicit modelling of ownership, sanitizers, error paths and resource lifecycles (p. 17); structured multi-agent or self-verification for prompt compliance (p. 17); cost-aware designs — hierarchical/incremental analysis, caching, adaptive LLM invocation, cheaper models (p. 18); broader languages and CWE classes (p. 18).
- Suggested by us [I]: an independent (non-evaluated) judge or full manual labelling for warning triage; repeated runs with variance; LLM vs DL vs SAST on the same post-cutoff projects with recall measured via newly disclosed vulnerabilities.

## 12. Relevance to our research
- Research questions addressed (RQ ids): RQ1, RQ2, RQ3, RQ4, RQ5.
- How it informs our work [I]: one of the few head-to-head project-scale comparisons of LLM detectors and SAST (CodeQL, Semgrep, SpotBugs, CSA) on the same targets, with recall, precision/SFDR and cost. It shows "LLM vs SAST" depends heavily on the LLM workflow: general agents beat SAST on recall, specialized hybrids (IRIS, INFERROI, KNighter) often do not. Gives concrete cost data for RQ3 and an FP taxonomy shared by both families for RQ5.

## 13. Evidence table (for the evidence matrix)
| RQ | Claim | Page | Label | Strength |
|---|---|---|---|---|
| RQ1 | On 110 known C/C++ vulns, Codex/Claude Code average recall 59.55% vs CodeQL 6.00–34.29%, Semgrep and CSA 0%; KNighter 0, RepoAudit (Sonnet 3.5) 0 and RepoAudit (GPT-5.4) 2 detections | p. 7 | V | moderate |
| RQ1 | On 155 known Java vulns, Claude Code recall 81.94% and Codex 63.87% vs CodeQL 14.19%, Semgrep 6.67%, SpotBugs 14.84% | p. 9 | V | moderate |
| RQ1 | On 24 real-world projects, SFDR is high for most tools: IRIS 97.80%, INFERROI 96.40%, RepoAudit 92.77%, CodeQL 77.00–86.01%, Semgrep 92.71–100%, CSA 85.51%, SpotBugs 86.21%; Codex lowest at 9.09%/31.82% but on ~22 warnings each | p. 11, p. 12 | V | moderate |
| RQ2 | Specialized LLM detectors show much lower recall than in their original papers; authors attribute this to narrow original evaluations (e.g. RepoAudit on 4 intra-function Linux cases) | p. 7 | A | moderate |
| RQ2 | Real-world TP/FP labels come from Codex (94.36% accuracy on 621 validated warnings), a tool that is also evaluated | p. 11 | V | moderate |
| RQ3 | On real-world SFDR, IRIS (GPT-4, LLM+CodeQL) is worse than plain CodeQL on Java (97.80% vs 77.00%; IRIS GPT-5.4 78.73%) and KNighter (GPT-5.4) is worse than CSA/CodeQL (95.56% vs 85.51%/86.01%); KNighter (o3-mini) is lower at 81.25% but from 48 warnings on one module (linux/drivers/net). INFERROI beats CodeQL/SpotBugs on CWE-772 recall (66% vs 10%/6%) | p. 9, p. 11, p. 12 | V | moderate |
| RQ3 | LLM cost per project: RepoAudit up to $1,247.66 and 225M input tokens; LLMDFA avg $61.60 and 2,000 min; Codex $5.38/14.8 min; SAST runs in minutes with no token cost | p. 16 | V | moderate |
| RQ2 | Tension with guo2025repoaudit: RepoAudit 40 TP / 11 FP and $2.54 avg per project there vs 0/110 known C/C++ vulns, 92.77% SFDR and $172.77 avg ($1,247.66 max) here; targets, commits, bug-type mapping, scale, metric and labeller differ (see §9) | p. 7, p. 11, p. 15, p. 16 | I | weak |
| RQ4 | Vulnerabilities missed by general agents involve larger files; IRIS/INFERROI less affected by file size | p. 9, p. 10 | V | weak |
| RQ4 | Project-specific API modelling drives misses in both families; perfect API specs raise CWE-401 recall of CodeQL 6→56% and RepoAudit 0→48% | p. 8 | V | moderate |
| RQ5 | 63.33% of 5,896 FPs come from incorrect program-point classification and 14.60% from truncated interprocedural context, across LLM and SAST tools | p. 15 | V | moderate |
| RQ5 | Scalability (tokens, hours to days per project) remains a bottleneck for CI use of project-scale LLM detection | p. 17, p. 18 | A | moderate |

## 14. Key quotes
> "the two general agent methods achieve an average recall of 59.55% (131/220) and an average precision of 32.19% (131/407)" (p. 7)

> "Codex is the most conservative, with only 2.44 warnings on average and the lowest overall SFDR of 9.09%" (p. 12)

> "we utilize Codex to automatically label whether each reported warning is a true vulnerability or not" (p. 6)

## Analyst notes
- Reading coverage: all 20 PDF pages read. Appendices A (extra FP examples), B (rule/checker lists) and C (detailed cost statistics) are referenced but not included in the arXiv v2 PDF; not read.
- Version: arXiv v2 (25 Sep 2026); metadata records the TSE version (DOI 10.1109/tse.2026.3742453). Numbers in the published version may differ; check before quoting in the final report.
- Uncertainties: Fig. 5 Venn diagrams are garbled in extraction; per-CWE unique-detection counts not extracted. "First comprehensive empirical study" is a novelty claim [A] (p. 1). Finding 1 calls general agents highest in recall and precision, but on Java CWE-772 SpotBugs (75.00%) and CodeQL (50.00%) have precision close to or above Codex (52.00%) on very few warnings (p. 10).
