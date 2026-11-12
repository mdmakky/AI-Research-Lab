---
key: xiong2026propgen
status: complete
evidence_basis: full-text
design: Tool paper with empirical evaluation (4 RQs); LLM-based runtime GUI exploration (plus light static analysis of the APK) and property synthesis for Android, compared with DroidAgent, a naive LLM baseline and 4 functional-bug detectors
dataset: 12 open-source Android apps (8 from prior studies + 4 from Google Play; 57.5k-403.8k LOC)
sample_size: 12 apps, no repeated runs reported; 1,282 inferred functionalities, 985 generated properties, 127 imprecise properties, 25 new bugs; 2 independent human annotators
metrics: Functionality validity and execution correctness (%), property validity (%), refinement success rate, number of new functional bugs, bugs in scope / rediscovered by prior tools, Cohen's kappa, token cost
main_finding: Runtime-grounded LLM exploration yields 912/985 valid properties (naive LLM: 0/240 valid), refines 118/127 imprecise ones and found 25 unknown bugs in 12 apps.
relevance: medium
analysed: 2026-11-11
---
<!-- Frontmatter: single-line values; they feed literature-matrix.md via `rlab index`.
     status: draft (in progress) -> ready (analyst self-check passed) -> complete (critical review passed).
     evidence_basis: full-text | abstract-only. abstract-only analyses must not fill methodology detail.
     relevance: high | medium | low. -->

# PropGen: Automated Property Generation for Property-Based Testing of Mobile Apps

- Authors: Xiong, Yiheng; Song, Shiwen; Ma, Bo; Su, Ting; Xie, Xiaofei
- Year / venue: 2026, Proceedings of the 41st IEEE/ACM International Conference on Automated Software Engineering (published)
- DOI: 10.1145/3832783.3837536 · URL: https://doi.org/10.1145/3832783.3837536
- Source text: `fulltext.txt` (page refs = PDF page index). The PDF is arXiv v2 (8 Oct 2026) carrying the ASE '26 camera-ready header and DOI (p. 1); peer-reviewed (received 2026-03-26, accepted 2026-06-18, p. 13).

Labels: **[V]** verified in the paper's own data/tables/results · **[A]** author claim · **[I]** our interpretation.
Every [V]/[A] item ends with a page ref `(p. N)`. Write "not reported" when the paper does not say.

## 1. Research objective
- [A] Automate the construction of properties for property-based testing (PBT) of mobile apps with LLMs. A *property* here is a rule of the form precondition -> interaction -> expected postcondition that must hold whenever it applies; PBT then generates many GUI event sequences and checks whether the rule is violated (p. 1, p. 3).
- [A] Motivation: non-crashing functional bugs lack explicit test oracles; PBT can expose them, but writing properties by hand is "difficult and expensive", and apps rarely have specifications (p. 1). Asking an LLM directly for properties is unreliable because, without evidence of how the app behaves, "LLMs tend to hallucinate properties that the app never satisfies" (p. 2).

## 2. Research questions / hypotheses
- [V] RQ1: effectiveness in exploring app functionalities and generating valid properties; RQ2: how often properties are imprecise (cause false positives) and how well refinement fixes them; RQ3: whether generated properties find new functional bugs; RQ4: comparison with prior functional-testing techniques in finding new bugs (p. 6).

## 3. Methodology
- Research design: [V] Tool design plus empirical evaluation on 12 Android apps, with human annotation of validity, comparison against baselines, and bug reporting to developers (p. 6-8).
- Approach / model / intervention: [V] PropGen has three stages (p. 3-6): (1) **hypothesis-guided exploration**: an MLLM looks at the screenshot (with numbered widgets from the accessibility tree), app name and the activity names extracted from the AndroidManifest.xml file (p. 4), and proposes candidate functionalities each tied to a triggering widget; PropGen executes them step by step, the MLLM labels each step success/fail/complete, and traces are summarised into "behavioral evidence" (state before, event, state after, state diff, outcome); random exploration is used when no unexplored hypothesis remains (p. 4-5); widget signatures keep only app-defined text, filtered against "a whitelist extracted via static analysis" (p. 5); (2) **property synthesis**: the MLLM first writes a natural-language property (precondition P, interaction I, postcondition Q) from the evidence, then translates it into executable code for the PBT tool Kea (p. 6); (3) **feedback-driven refinement**: for properties whose reported violations are *manually confirmed* false positives, the LLM locates which of P, I or Q is imprecise using the source trace and the failing run, and edits only that part (p. 4, p. 6).
- Baselines or comparison conditions: [V] RQ1: DroidAgent (LLM-based functionality exploration) and a naive LLM baseline that writes 20 properties per app from the app's official description without running the app (p. 7). RQ4: Genie, Odin (automated differential oracles), PBFDroid (PBT for data-manipulation functionalities) and VisionDroid (LLM multi-agent functional bug detection) (p. 7).

## 4. Dataset and sample
- Data source(s): [V] 12 popular open-source Android apps (e.g. OmniNotes, Markor, AnkiDroid, NewPipe), 57,529 to 403,785 LOC; GitHub stars 1.1K-37.5K (p. 7).
- Sample size (N) and unit: [V] 12 apps. Units of analysis: 1,282 functionalities inferred by PropGen (575 by DroidAgent), 985 generated properties, 240 naive-baseline properties, 127 imprecise properties, 25 new bugs (p. 8-10).
- Sampling / selection method: [V] Eight apps adopted from prior functional-bug studies, excluding apps no longer runnable/maintained or functionally similar to already chosen ones; four more popular open-source Google Play apps added "to further improve diversity" (p. 6-7). [I] No power or sample-size reasoning reported.
- Data availability (public? link?): [A] "We have made all the artifacts publicly available" (p. 11), Zenodo artifact doi:10.5281/zenodo.21770804 (p. 13). Not checked by us.

## 5. Experimental setup
- Procedure, settings, hyper-parameters, tools: [V] Ubuntu 22.04, 192 CPU cores (AMD EPYC 9654), official Android 11 Pixel emulators; GPT-5.2 (snapshot gpt-5.2-2025-12-11) as backend MLLM for PropGen and DroidAgent with default decoding (temperature 1.0, top-p 1.0); 3 h per app for evidence construction and property synthesis, then 6 h of Kea PBT per app (p. 7). Built on DroidBot, uiautomator2 and ADB; mainly Python and JavaScript (p. 6). RQ4 time budgets aligned: 9 h per app for Genie, Odin and VisionDroid; 6 h testing for PBFDroid after the authors manually wrote its DMF properties (p. 8). [I] DroidAgent's time budget is not stated explicitly (not reported).
- Human annotation: [V] two graduate students in software engineering (each at least four years of Android experience), not co-authors, labelled independently; Cohen's kappa 0.91 (functionality validity), 0.82 (execution correctness), 0.81 (property validity); disagreements then resolved by discussion (p. 7).
- Code availability: [A] artifacts released on Zenodo (p. 11, p. 13).

## 6. Evaluation metrics
- Metric — what it measures — why chosen:
  - [V] **Functionality validity**: share of inferred functionalities that really exist in the app (human judged from screenshot) (p. 7).
  - [V] **Execution correctness**: share of inferred functionalities whose executed event sequence actually realises them (human judged) (p. 7).
  - [V] **Property validity**: property is valid only if every referenced widget/event appears in its source trace (automated groundedness check) and annotators judge P, I and Q faithful to the intended functionality (p. 7). Chosen because "mobile apps lack ground-truth specifications" (p. 7). Validity does not imply precision (p. 7).
  - [V] **Refinement success**: revised property must (a) still hold on its source trace, (b) no longer raise the spurious violation, and (c) be confirmed valid and intent-preserving by humans (p. 8).
  - [V] **New bugs**: manually confirmed, previously unreported functional bugs, reported to developers (p. 8); for RQ4 also a manual **scope analysis** of whether each prior tool's oracle could in principle detect each bug, partly validated by consulting authors of Genie, Odin and PBFDroid (p. 8). [I] These tools share authors with PropGen (see §9).
  - [V] **Cost**: tokens and USD per LLM call and per app (p. 9).
- Statistical testing (tests used, significance, effect sizes, confidence intervals): [I] None found; results are counts and percentages with no repeated runs reported (checked pp. 7-10). The paper states "This single run" only for the RQ4 prior techniques (p. 8). [V] Only inter-rater agreement (Cohen's kappa) is reported (p. 7).

## 7. Key findings
1. PropGen inferred 1,282 functionalities, 1,210 valid (94.4%) and 977 correctly executed (76.2%), vs DroidAgent 575 inferred, 491 valid (85.4%), 187 correctly executed (32.5%) — [V] (p. 8, p. 9).
2. PropGen generated 985 properties, 912 valid (92.6%; 78.7%-98.8% per app) — [V] (p. 8). The naive LLM baseline (app description only) produced 240 properties, none valid, because it referenced non-existent widgets — [V] (p. 9).
3. 127 properties caused false positives during PBT; 118 (92.9%) were successfully refined, mostly by changing the postcondition (64) or precondition (53), only 1 by changing the interaction; of 9 failures, 5 were misdiagnoses and 4 drifted from the original intent — [V] (p. 9).
4. Properties found 25 previously unknown functional bugs in the latest app versions; 5 fixed by developers at writing time; categories: functionality does not take effect (12), state inconsistency (6), unexpected wrong behaviour (4), navigation failure (3) — [V] (p. 9-10).
5. Of the 25 bugs, only 7 (28%) were in the detection scope of the four prior tools and 3 (12%) were rediscovered; the prior tools together found 13 unknown bugs, of which PropGen missed 10 — [V] (p. 10). [A] The approaches are "complementary rather than substitutable" (p. 10).
6. Cost: about $14.86 and 6,364k tokens per app for PropGen vs $13.01 and 5,109k tokens for DroidAgent; refinement about $0.02 per property — [V] (p. 9).

## 8. Limitations stated by the authors
- [A] Manual inspection of functionalities and properties may introduce subjectivity and bias; mitigated by two independent annotators and consensus (p. 11).
- [A] The 12 apps may not represent the diversity of real-world apps; a larger and broader set is planned (p. 11).
- [A] Open-source apps may be in GPT-5.2's training data; mitigated by checking that none of the 25 bugs was previously reported, and by noting that six of the 12 tested builds were released after the model's training cutoff and still yielded bugs (p. 11).
- [A] Failure modes: the MLLM sometimes proposes non-existent functionalities, executions may not finish within the step budget or are labelled successful too early, and synthesis occasionally hallucinates widgets despite grounding (p. 9). PropGen generates only one property per functionality and lacks the differential oracles of Genie/Odin (p. 10).
- [A] A pre-existing app fault could in principle corrupt generated or refined properties; risk argued to be limited because properties come only from successful traces and refinements are human-confirmed (p. 10-11).

## 9. Limitations we identified
- [I] **Not fully automatic.** Refinement is triggered only after a human confirms a violation is a false positive (p. 4, p. 6), and bug confirmation is manual (p. 8). The cost of this human effort is not reported.
- [I] **No repeated runs with temperature 1.0.** A single run is stated for the RQ4 prior techniques (p. 8). For PropGen's RQ1-RQ3 no repetition is reported. Decoding is stochastic (p. 7), so it is unknown how stable the counts are.
- [I] **Weak naive baseline.** The naive baseline sees only the app's description, never the GUI (p. 7). Its 0/240 result shows that runtime evidence is needed, but does not test simpler runtime-grounded alternatives.
- [I] **Author-tool overlap.** Ting Su (PropGen co-author) co-authored Genie, Odin, PBFDroid, Kea and Kea2. Xiong co-authored Genie, Kea and Kea2, and Bo Ma co-authored Kea2 (refs [29], [51], [52], [63], [71], p. 12-13). So three of the four RQ4 baselines (Genie, Odin, PBFDroid, p. 7) come from the PropGen authors' own group. The scope analysis is manual (p. 8). Its validation by "the authors of Genie, Odin, and PBFDroid" (p. 8) involves the same group. The PBFDroid properties were written by the PropGen authors (p. 8). Only VisionDroid (p. 7) is independent. This is not necessarily bias in PropGen's favour, since the group knows these tools well. But the scope analysis is not independently validated.
- [I] **Annotator blinding and kappa scope not reported.** Whether the annotators were blind to which tool (PropGen or DroidAgent) produced each functionality is not reported (p. 7). The set of items over which Cohen's kappa was computed (PropGen only, or both tools) is not stated (p. 7).
- [I] **Contamination check is partial.** "Not previously reported" bugs (p. 11) do not show that the model lacks prior knowledge of app behaviour; app functionality, not bugs, is what the model may have memorised.
- [I] **Validity is judged against human understanding, not a specification** (p. 7). This is reasonable but means "valid" depends on annotators' familiarisation of at least fifteen minutes per app (p. 7).

## 10. Threats to validity
- Internal (confounds, leakage, selection): [I] Same MLLM backend for PropGen and DroidAgent (p. 7) is a fair control. Budget alignment across tools in RQ4 (p. 8) is reasonable, but tools differ in design scope, which the authors address with the scope analysis (p. 8). Possible training-data exposure of open-source apps (p. 11).
- External (generalisability of sample/context): [I] 12 open-source Android apps on emulators (p. 7); unclear transfer to iOS, web, closed-source or login/network-heavy apps.
- Construct (do metrics measure the concept?): [I] "Valid" properties are grounded and faithful but may still be imprecise (p. 7); bug counts depend on each tool's oracle type, which the authors acknowledge ("Raw bug counts alone are therefore not directly comparable", p. 8).
- Statistical conclusion (power, multiple comparisons, variance): [I] No statistical tests; 12 apps; no repeated runs reported (single run stated for RQ4 baselines, p. 8). High kappa values (0.81-0.91, p. 7) support annotation reliability.
- Reproducibility (data/code/setup reported?): [I] Good: model snapshot, decoding parameters, budgets, hardware and artifacts are reported (p. 7, p. 13). Proprietary model dependence and temperature 1.0 limit exact replication.

## 11. Future research directions
- Stated by authors [A] (p. 9-11): evaluate on a larger and broader set of apps (p. 11); interact-then-infer functionality inference, activity transition graphs for step planning, explicit completion checks, post-synthesis widget checks (p. 9); richer context and an intent-verification step for refinement (p. 9); more properties per functionality and combining PropGen with specialised oracles (p. 10).
- Suggested by us [I]: use properties mined from an original app as a behavioural oracle for an AI-reconstructed version of that app (differential fidelity testing), and measure how many original-app properties the rebuild satisfies.

## 12. Relevance to our research
- Research questions addressed (RQ ids): RQ2, RQ4, RQ5 (indirect); RQ1 only tangentially. Not RQ3.
- How it informs our work [I]: PropGen does not generate or reconstruct applications, so it gives no direct evidence on fidelity or code quality of AI-built apps. Its value is as a method. It recovers behavioural specifications from a running app without source code or written specifications. It does this through runtime observation plus light static analysis of the APK: manifest activity names (p. 4) and a string whitelist (p. 5). So it is grey-box rather than purely observational. The authors call this "exploring a black-box app" [A] (p. 11). This is exactly the kind of oracle a reverse-engineering study needs to check functional fidelity (RQ2, RQ5). Its result that an LLM without runtime observation produces 0 valid properties (p. 9) supports grounding any reconstruction or test generation in observed behaviour. Its evaluation design (independent annotators with kappa, scope analysis for oracle-dependent tools) is a good template for RQ4. Relevance is therefore medium.

## 13. Evidence table (for the evidence matrix)
| RQ | Claim | Page | Label | Strength |
|---|---|---|---|---|
| RQ2 | Behavioural properties can be recovered from a running Android app without source or specs (runtime observation plus manifest activity names and a static string whitelist): 912 of 985 LLM-generated properties judged valid (92.6%) | 4, 5, 8, 9 | V | moderate |
| RQ2 | An LLM given only the app description produced 240 properties, none valid (hallucinated widgets); runtime evidence is required | 9 | V | moderate |
| RQ2 | Generated properties found 25 previously unknown functional bugs in 12 apps; prior tools rediscovered 3 of them, but themselves found 13 unknown bugs, 10 of which PropGen missed; authors call the approaches complementary (A) | 9, 10 | V | moderate |
| RQ4 | Validity judged by 2 independent non-author annotators (kappa 0.91 / 0.82 / 0.81); no ground-truth spec exists for apps | 7 | V | moderate |
| RQ4 | Bug counts across functional-testing tools are oracle-dependent and not directly comparable; scope analysis used instead | 8, 10 | V | moderate |
| RQ4 | No repeated runs reported (single run stated for RQ4 baselines) at temperature 1.0; no variance or statistical tests found (our check) | 7, 8 | I | moderate |
| RQ5 | Imprecise LLM properties are common (127 of 985 caused false positives) but 92.9% could be refined, mainly via pre/postconditions | 9 | V | moderate |

Strength note [I]: moderate = peer-reviewed (ASE 2026) single study with 12 apps and good annotation reliability, but no replication or variance.

## 14. Key quotes
> "none of which is valid" (p. 9)

> "Raw bug counts alone are therefore not directly comparable across" (p. 8)

> "Neither annotator is a co-author" (p. 7)

## Analyst notes
- Reading coverage: sections read / skipped and why: all 13 PDF pages read via `fulltext.txt` (abstract to conclusion, data availability, acknowledgements); reference list (p. 12-13) skimmed for author overlap only. Figures 1-2 (p. 3) are diagrams whose content is described in the text. The two-column layout interleaves lines in `fulltext.txt`; all numbers were taken from tables and checked against the text.
- Uncertainties: (1) DroidAgent's exploration time budget in RQ1 is not stated explicitly; (2) the human effort for confirming false positives and bugs is not quantified; (3) the abstract in metadata.json is truncated, but the full text was available; (4) the 25 bugs' report links/IDs on public trackers are not given in the paper (Table 4 lists IDs 1-25 internal to the paper, p. 10).
- Critical-review fixes X1-X5 of `reports/critical-review-batch-c.md` applied 2026-11-12 after checking pp. 4-5, 7, 8, 10, 11 and 12-13.
- Funding [V]: National Research Foundation Singapore / CyberSG R&D Programme Office and NSFC projects (p. 11). [I] We found no conflict-of-interest statement beyond this.
