---
key: kim2026programdistill
status: complete
evidence_basis: full-text
design: automated benchmark construction (LLM mine-craft-patch pipeline) + evaluation of 9 coding agents on partial and 3 agents on full web-app reconstruction from a live reference
dataset: ProgramDistill, 26 interactive web apps (18 OSWorld-derived, 8 open-source clones); 1,975 replay-verified browser behaviours; 4,063 repair tasks
sample_size: partial: 300 tasks x 9 models (runs per task not stated); full: 12 apps x 3 models = 36 runs, 590 atomic + 413 cumulative behaviour tests
metrics: binary score and chain score from deterministic browser-trace replay; atomic behaviour recovery; cumulative workflow recovery; cost per trajectory; failure categories; shortcut-attempt rate
main_finding: Agents rebuild web apps from a live reference only partly: best full-app rebuild passes 49.2% of cumulative workflows; partial-repair success falls sharply as more dependent behaviours must be restored.
relevance: high
analysed: 2026-11-11
---
<!-- Frontmatter: single-line values; they feed literature-matrix.md via `rlab index`.
     status: draft (in progress) -> ready (analyst self-check passed) -> complete (critical review passed).
     evidence_basis: full-text | abstract-only. abstract-only analyses must not fill methodology detail.
     relevance: high | medium | low. -->

# ProgramDistill: From Interactive Web Apps to Verifiable Reference-Guided SWE Tasks

- Authors: Kim, Jeonghye; Kim, Minseon; Kim, Young Jin; Pereira, Matheus; Côté, Marc-Alexandre; Sordoni, Alessandro; Yuan, Xingdi; Shi, Zhengyan
- Year / venue: 2026, arXiv (preprint, not peer-reviewed; v1 dated 16 Sep 2026). Affiliations: KAIST, Microsoft Research Montréal, Microsoft AI (p. 1).
- DOI: 10.48550/arxiv.2609.18805 · URL: https://arxiv.org/abs/2609.18805
- Source text: `fulltext.txt` (page refs = PDF page index)
- PDF version analysed: arXiv v1, "arXiv:2609.18805v1 [cs.SE] 16 Sep 2026" (p. 1), from arxiv.org/pdf/2609.18805. No peer-reviewed version is known.

Labels: **[V]** verified in the paper's own data/tables/results · **[A]** author claim · **[I]** our interpretation.
Every [V]/[A] item ends with a page ref `(p. N)`. Write "not reported" when the paper does not say.

## 1. Research objective
- [A] Evaluate coding agents on "reference-guided" software engineering: inferring intended behaviour by interacting with a working web application, then implementing it in an incomplete or empty application. This differs from benchmarks where behaviour is given as an issue or instruction (p. 1).
- [A] Turn working interactive web apps into a scalable, automatically built source of verifiable tasks ("application-to-task factorization") with controllable difficulty ("restoration depth") (p. 2).

## 2. Research questions / hypotheses
- Not stated as formal RQs. [A] Guiding question: "Can we uncover this latent behavioral structure and use it to turn a working interactive web application into a scalable source of verifiable software-engineering tasks?" (p. 2). [I] Implicit empirical questions: how well agents restore masked features and rebuild whole apps from a live reference, how performance changes with the number of dependent behaviours, and why agents fail.

## 3. Methodology
- Research design: [V] A fully automated LLM pipeline ("mine–craft–patch") builds tasks; two evaluation settings follow, plus trajectory and failure analyses (p. 2; p. 6).
- Approach / model / intervention:
  - [V] *Mine*: LLM agents (Planner, Collector, Relabeler, Reflector), with read access to the source and the live app, propose behaviour goals, drive the app through a Playwright browser helper, and record replayable traces of actions plus expected observable signals (accessible names, visible text, URL, state). A trace is admitted only if it replays deterministically from a reset state (p. 3; p. 4; p. 25).
  - [V] *Craft*: an LLM masks (deletes) the source implementing a behaviour, either logic only or logic plus UI. A mask is accepted only if the app still builds, prerequisite traces still pass, the target trace fails, and an LLM "mask-depth critic" judges the deletion substantive. Masks along a prerequisite lineage are combined into cumulative tasks, and the reversed mask is the gold patch, which must replay the whole lineage (p. 4; p. 5; p. 6).
  - [V] *Patch*, partial-application reconstruction: the agent gets the masked repository, an LLM-written behavioural problem statement, and browser access to the live reference (no reference source, no internet) (p. 6).
  - [V] *Patch*, full-application reconstruction: the agent starts from a minimal scaffold plus a product-level capability description and must rebuild the whole app from the live reference (p. 6; p. 10; p. 11).
  - [V] All construction stages use GPT-5.6 Sol (p. 2; p. 7).
- Baselines or comparison conditions: [V] 9 frontier models compared on partial reconstruction; 3 models (GPT-6 Astra, Claude Opus 5, GPT-5.6 Sol) on full reconstruction. Logic-only vs logic-and-UI masks; restoration depths 1–8 (p. 8; p. 11). No human or non-agent baseline.
- [I] Relation to our topic: full-application reconstruction is very close to our scenario of rebuilding a web application by observing its UI and behaviour, with no access to its source. Partial reconstruction resembles restoring missing features in an existing codebase by consulting a working product.

## 4. Dataset and sample
- Data source(s): [V] 26 self-contained web apps: 18 adapted from the OSWorld web-application suite and 8 real-world open-source projects or SaaS clones (Actual Budget, Reactive Resume, Baserow, two Trello clones, two Jira clones, a Calendly clone), using Django, Angular, React and Next.js with SQL and document back ends. Each is pinned to a commit (p. 19).
- Sample size (N) and unit:
  - [V] Mining: 2,800 candidate goals, 2,350 collected, 2,165 reproduced and 1,975 verified behaviours; maximum lineage depth 17 (mean 3.40) (p. 7).
  - [V] Tasks: 4,063 in total, 2,862 atomic and 1,201 cumulative; 1,997 logic-only and 2,066 logic-and-UI (p. 7).
  - [V] Per-app task counts are very uneven, from 2 (ExpenseFlow) to 372 (Reactive Resume) (p. 19).
  - [V] Evaluation suite ProgramDistill-300: 50 atomic and 250 cumulative tasks covering 269 lineages and all 26 apps (p. 8).
  - [V] Full reconstruction: 12 apps, 590 atomic and 413 cumulative behaviour tests, 36 runs (p. 11; p. 12).
- Sampling / selection method: [V] ProgramDistill-300 is stratified by restoration depth (quotas 50, 45, 45, 40, 35, 30, 30, 25 for depths 1–8) and selected round-robin across apps (p. 8). [I] Why these 26 apps, and why these 12 for full reconstruction ("twelve stateful web applications", p. 11), is not explained beyond "complementary sources" (p. 3).
- Data availability (public? link?): [A] "We are working on a public release of the ProgramDistill benchmark" (p. 1). Not yet released at time of writing; prompts are given in the appendix (p. 25; p. 30; p. 33).

## 5. Experimental setup
- Procedure, settings, hyper-parameters, tools: [V] Modified R2E-Gym harness with tools `execute_bash`, `file_editor`, `search` and `finish`. A browser CLI drives both the reference and the current app (p. 8). Agents see only structured text observations (visible text, element IDs, roles, accessible names, input values); full reconstruction additionally exposes selectors. Screenshots and raw HTML are excluded (p. 3; p. 24).
- [V] Partial reconstruction: reasoning effort high, at most 1,000 steps, 150k-token history cutoff. Full reconstruction: reasoning effort max, at most 10,000 steps, 500k-token cutoff. Per-tool timeout 90 s, no aggregate time limit (p. 24).
- [V] Determinism: application state is reset before each collection and replay, and a shared fake clock (libfaketime plus a browser Date offset) is used (p. 3; p. 19; p. 20).
- [V] Isolation: the reference is reachable only via the browser helper, public egress is blocked, there is no pre-mask git history, and grading traces are private. Submissions are rebuilt and replayed in a fresh verifier (p. 10; p. 23; p. 24).
- [V] The full-reconstruction scaffold requires an `app.js` exporting `async function handle(req, res, context)`, with state kept in `context.state` (p. 37).
- [V] Number of runs, full reconstruction: 36 runs = 12 apps x 3 models (p. 11; p. 12). [I] Partial reconstruction: the number of runs per task is not stated. No variance is reported, so presumably one run each. Repeats or seeds: not reported.
- [V] Cost: tokens x LiteLLM list prices (p. 37). One GPT-6 Astra pass over 300 tasks took about 557 minutes on 4 servers (p. 37).
- Code availability: [A] release in progress (p. 1).

## 6. Evaluation metrics
- Replay verifier V(A, L): returns 1 only if every recorded browser action completes and every expected signal is satisfied, replaying the whole prerequisite lineage without LLM involvement (p. 4).
- Binary score: 1 only if the complete lineage passes after the agent's patch. Chain score: fraction of repair targets passed, giving partial credit (p. 6).
- Full reconstruction: atomic behaviour recovery (fraction of single-behaviour tests passed, with prerequisites replayed) and cumulative workflow recovery (binary and chain) (p. 6; p. 11).
- [V] Source-level matching is not required: function names, variables and structure may differ if behaviour replays (p. 6). [V] In full reconstruction, however, selectors and accessible names must match the reference, because evaluation "replays user interactions using selectors" (p. 35).
- Diagnostics: interaction counts (observation, read/search, edit/write steps), share of unchanged target files and retained stub lines, shortcut-attempt rate, failure categories (p. 9; p. 10; p. 12).
- Statistical testing (tests used, significance, effect sizes, confidence intervals): [V] None; means only. Pearson correlations between prompt size and binary score are reported in the context-length check (p. 40).

## 7. Key findings
1. [V] Partial reconstruction (ProgramDistill-300): mean binary score is 84.3% for GPT-6 Astra, 68.7% for Claude Opus 5 and 60.7% for GPT-5.6 Sol, with a middle tier at 45.3–48.3% and Gemini 3.1 Pro Preview lowest at 22.3%. Mean cost per trajectory is $33.99, $28.86 and $16.01 for the top three (p. 8; p. 38).
2. [V] Success drops with restoration depth: Astra falls from 100% at depth 1 to 64.0% at depth 8, Opus 5 from 96% to 32.0% and Sol from 92% to 32.0%; every other model keeps less than half of its depth-1 performance (p. 8; p. 9).
3. [V] Restoring UI as well as logic is harder. Binary scores for logic-only vs logic-and-UI masks are 92.9% vs 76.9% for Astra and 76.4% vs 46.9% for Sol (p. 38).
4. [V] Full-application reconstruction (12 apps): Astra recovers 58.98% of atomic behaviours and 49.15% of cumulative workflows, Opus 5 42.03% and 28.81%, and Sol 33.39% and 21.07% (p. 11). Per-app results vary widely, e.g. Astra's cumulative recovery ranges from 81.8% (MailHub) to 5.9% (Baserow) (p. 11).
5. [V] Of 977 failed atomic behaviours in full reconstruction, 59.2% were never observed in the reference. Of the rest, 1.8% were observed but not implemented, 11.1% were implemented with the wrong observable form and 27.9% produced the wrong state, route or result (p. 12).
6. [A] Agents' own validation (syntax checks, successful requests, selected text matches) often did not recheck the failing workflow after the last relevant edit, so mismatches went undetected (p. 12; p. 13).
7. [V] From depth 1 to 8, code to restore grows 9.3x and required browser actions 10.7x, but reference-observation steps per target fall from 34.60 to 8.46. Retained mask stub lines rise from 11.1% to 24.6% (p. 9; p. 10).
8. [V] The depth effect persists among runs with similar context lengths; e.g. in the 40–80k band, mean binary score falls from 82.6% at depth 1 to 24.2% at depth 8 (p. 39).
9. [V] At least one shortcut attempt (git history, public source fetch, harness probing, direct reference access) appears in 7.2% of trajectories: 19.0% for Grok 4.6, 17.7% for Gemini 3.1 Pro and 0.3% for Astra. These channels were blocked by design (p. 10).
10. [V] The best model was the most observation-heavy and edit-light: Astra averages 96.3 current-app observation steps and 9.9 edit/write steps per trajectory (p. 9).

## 8. Limitations stated by the authors
- [A] Agents receive structured text observations, not screenshots. Visual fidelity is not evaluated and "would require criteria beyond the current replay-based behavioral checks" (p. 14).
- [A] Only self-contained web apps; external services, nondeterministic state, and desktop/mobile apps are future work (p. 14).
- [A] Benchmark coverage and quality depend on the construction model (GPT-5.6 Sol) (p. 15).
- [A] Results depend on the browser/agent infrastructure (replay-stable selectors, settled observations, harness), and sensitivity to these choices is uncharacterised (p. 15).
- [A] The isolation is not a general-purpose sandbox for hostile code (p. 24).
- [A] Possible misuse for cloning proprietary apps; experiments are limited to public/open-source apps (p. 15).

## 9. Limitations we identified
- [I] Code quality and maintainability of the rebuilt or repaired code are not measured at all. Only behavioural replay is scored (p. 6). The full-reconstruction contract forces a single Node `handle()` entry, with application state kept in `context.state` "so the verifier can reset it" (p. 37), while the originals use Django, Angular, React or Next.js with databases (p. 19). The rebuild's architecture is therefore imposed and not comparable to the original.
- [I] Possible self-preference and family bias:
  - GPT-5.6 Sol builds the traces, masks and problem statements (p. 2) and is also an evaluated model; the top model is from the same vendor (GPT-6 Astra) (p. 8).
  - The full-reconstruction failure analysis is done by GPT-6 Astra (p. 12), which judges its own and its competitors' failures, with no human validation reported.
- [I] No human check anywhere. Tasks are built "without human intervention" (p. 1), mask depth is judged by an LLM critic (p. 5), and 572 cumulative masks were merged by an LLM agent (p. 6). The only quality evidence is the replay checks and the 100% depth-1 solve rate of one model (p. 8). No sample of tasks was manually audited.
- [I] Oracle completeness is not measured. Unlike ProgramBench, no code coverage is reported for the trace suites. Behaviours exist only if the mining LLM found and stably replayed them; 29.5% of goals were lost (p. 7). Behaviours an agent never observes still count as failures (59.2% of failures, p. 12), but the trace bank itself may miss large parts of each app.
- [I] The full-reconstruction oracle checks surface identity (selectors, accessible names, labels) (p. 35), and the agent is shown the reference's selectors (p. 24). This mixes functional fidelity with DOM-level mimicry. A functionally equivalent rebuild with different labels would fail, while visual appearance is not checked at all (p. 14).
- [I] Contamination is not discussed. The 8 real-world apps are public GitHub projects (p. 19), so agents may partly reconstruct masked code from memory, especially for well-known clones.
- [I] The abstract places the full-reconstruction results under "Across nine frontier coding agents" (p. 1; same wording p. 2), but only 3 models were evaluated in that setting (p. 11). Synthesis should not describe 49.2% as best-of-nine.
- [I] Small and uneven samples for headline claims: apparently one run per cell (runs per task not stated for partial reconstruction), full reconstruction on 12 apps x 3 models (36 runs) (p. 12), and per-app task pools from 2 to 372 (p. 19). Differences between close models (e.g. 45.3% vs 45.7%, p. 8) are not interpretable without variance estimates.
- [I] The model names (GPT-6 Astra, Claude Opus 5, GPT-5.6 Sol) were very recent at publication and are cited to system cards (p. 16; p. 17). Results may not be reproducible once these API versions change.

## 10. Threats to validity
- Internal (confounds, leakage, selection): [V] Leakage controls: no pre-mask git history, blocked egress, hidden grading files, browser-only reference access, fresh-verifier rebuild (p. 10; p. 24). [I] Remaining threats: the same model family builds and is evaluated; LLM-only task validation; memorisation of public source.
- External (generalisability of sample/context): [I] 26 mostly small, self-contained CRUD-style web apps, 18 of them from one synthetic suite (OSWorld) (p. 19); a single harness; text-only observation (p. 14). Transfer to large production apps, visual-design fidelity or human-in-the-loop vibe coding is untested.
- Construct (do metrics measure the concept?): [I] Replay of mined traces is a sound behavioural oracle for the traced workflows, but it covers only discovered behaviours and also demands selector-level identity (p. 35). "Reconstruction success" therefore means reproducing specific recorded interactions, not the whole application.
- Statistical conclusion (power, multiple comparisons, variance): [I] No CIs or tests; single runs; stratified 300-task subset. The depth trend is consistent across models and context bands (p. 39), which makes that particular finding more credible.
- Reproducibility (data/code/setup reported?): [V] Prompts, harness settings and pricing are reported in detail (p. 24; p. 25; p. 37). [A] The benchmark is not yet public (p. 1).

## 11. Future research directions
- Stated by authors [A] (p. 14; p. 15):
  - add screenshots and visual-fidelity criteria;
  - extend to external services, nondeterministic state, and desktop and mobile apps;
  - study the quality–cost trade-off of the construction model;
  - characterise sensitivity to infrastructure choices;
  - use the tasks and trajectories for training (distillation, RL, curriculum by restoration depth).
- Suggested by us [I]:
  1. Measure code quality and maintainability of rebuilt apps, with a free architecture rather than a single fixed handler.
  2. Audit a sample of mined traces and masks by hand, and measure oracle coverage.
  3. Use a construction model from a different family than the evaluated models.
  4. Add repeated runs.
  5. Study a human-in-the-loop (vibe-coding) condition in which a developer steers reconstruction.

## 12. Relevance to our research
- Research questions addressed (RQ ids): RQ1, RQ2, RQ4, RQ5 (RQ3 only as a documented gap).
- How it informs our work [I]: This is the closest available study of rebuilding *interactive web applications* from a running reference via its UI, which is our core scenario. It offers a reusable fidelity-testing method: deterministic replay of recorded browser workflows with expected signals and prerequisite lineages. It also gives a failure taxonomy showing that most misses come from not exploring the reference rather than from coding errors (p. 12). It shows that agents' self-validation is unreliable (p. 12). Together with ProgramBench (yang2026programbench), it shows that functional fidelity of whole-app rebuilds remains far from complete. Like ProgramBench, it does not measure the maintainability of the rebuilt code, which supports the joint fidelity-plus-quality gap in RQ5.

## 13. Evidence table (for the evidence matrix)
| RQ | Claim | Page | Label | Strength |
|---|---|---|---|---|
| RQ1 | Reference-guided setting: agent interacts with a live reference web app via a browser CLI (structured text observations, no source, no screenshots) and edits a masked repo or a blank scaffold to reproduce its behaviour. | p. 3; p. 6; p. 24 | V | moderate (design fact) |
| RQ2 | Best full-application rebuild from a live reference recovers 58.98% of atomic behaviours and 49.15% of cumulative workflows (12 apps); other models 21–42%. | p. 11 | V | weak (preprint, 36 single runs) |
| RQ2 | Partial-repair success falls as more dependent behaviours must be restored (best model 100% at depth 1 to 64% at depth 8; others to ≤32%), and the drop persists when context length is controlled. | p. 8; p. 9; p. 39 | V | weak (single runs, but consistent across 9 models) |
| RQ2 | Restoring UI plus logic is harder than logic alone (e.g. 92.9% vs 76.9% binary for the best model). | p. 38 | V | weak |
| RQ2 | 59.2% of failed behaviours in full rebuilds were never observed in the reference; 27.9% had wrong state/result and 11.1% wrong observable form. | p. 12 | V | weak (classified by an LLM that is also an evaluated model) |
| RQ4 | Fidelity oracle: deterministic browser-trace replay with expected signals, admitted only if replayable on the intact app, failing after masking, and passing with the gold patch. | p. 4; p. 5; p. 6 | V | moderate (design fact) |
| RQ4 | Agents' own validation (syntax checks, request success, partial text checks) missed behavioural mismatches with the reference. | p. 12 | A | weak |
| RQ4 | Tasks are built and validated without human intervention by one LLM (GPT-5.6 Sol), which is also evaluated; authors note quality depends on the construction model. | p. 1; p. 2; p. 15 | A | weak |
| RQ5 | Visual fidelity and screenshot-based observation are not evaluated; authors name them, plus desktop/mobile apps, as future work. Code quality of rebuilds is not measured (our observation). | p. 14 | A | weak |

## 14. Key quotes
> "The distinction is thus a shift from specification consumption to specification discovery." (p. 14)

> "the largest failure category is behavior that was not observed in the reference, accounting for 59.2% of failures" (p. 12)

> "Similar text or element structure in observations is not sufficient." (p. 35)

## Analyst notes
- Reading coverage: whole paper read, pp. 1–40, including all appendices and prompts. Figures 1, 6, 8–13 are partly garbled in the text layer, so only numbers stated in the text or tables are used. Figure 11 per-model shortcut rates were cross-checked with the text (p. 10).
- Uncertainties:
  - how the 26 and 12 apps were chosen;
  - whether trace suites cover most app functionality;
  - how much memorisation of public app source contributes.
  
  The future-dated model names (GPT-6 Astra, Claude Opus 5, Gemini 3.7 Flash) are taken as reported; the paper is dated 16 Sep 2026, before our analysis date.
- Strength ratings follow research-standards §5 (preprint without replication = weak). The depth-degradation finding is the most robust internally, because it is consistent across 9 models and context bands.
