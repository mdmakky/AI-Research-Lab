# Research gap report — Package Hallucination and Slopsquatting in LLM Coding Assistants: Measuring Hallucinated Dependencies, Their Exploitability on PyPI/npm, and Lightweight Defences

A gap is listed only when the analysed papers provide evidence for it AND a novelty check found no paper that already fills it.

- Date of all novelty checks: **2026-11-12**. Evidence originally came from the 17 analyses with `status: complete`. The three agent-attack papers were analysed later the same day and are now complete; see the revision section below for how they change G1 and G2.
- Sources used: `rlab search` on **Crossref + arXiv**. OpenAlex failed again with HTTP 429 (free daily budget used up) on the first novelty query (`20261112-053531-…json`), so the remaining queries ran on Crossref + arXiv only. Long multi-word queries often return 0 arXiv hits, so short arXiv-friendly queries were added. WebSearch was used for very recent and grey work. Every query is logged in `search/search-log.md`, with raw results in `search/20261112-05*.json`.
- Shared arXiv/Crossref sweeps used for every gap (2025–): `package hallucination` (arXiv 41 / Crossref 44 hits), `hallucinated packages` (41 / 49), `slopsquatting` (5 / 5).
- Ranking is by novelty × laptop feasibility × impact, given the user's constraints (beginner, laptop only, no GPU, short project).
- Labels: [V] verified in the paper's data, [A] author claim, [I] our interpretation.

## Revision 2026-11-12 (after analysing the three agent-attack papers)

The three attack papers [@wang2026package], [@hsu2026harmless] and [@liu2026trust] were analysed in full and passed critical review (`reports/critical-review-attack-papers.md`). They change two gaps.

- **G1 narrowed; confidence lowered from medium to medium-low.**
  - [V] [@hsu2026harmless, p. 6] already reports executed-install rates for three real agents (Claude Code, OpenCode, OpenHands) under a benign marketplace Skill: 3.33%, 1.05% and 1.11%. Caveats: benchmark prompts designed to elicit packages, separate task configurations per metric, task counts and backbone models not reported, and "executed install" not defined as installing a non-existent package [@hsu2026harmless, p. 5].
  - [V] [@wang2026package, p. 17; @wang2026package, p. 27] characterises post-failure behaviour in Claude Code, but only under attack: in 37.9% of numpy cases the agent reverted to the real package after the import failed instead of running `pip install`.
  - So the old claim "we found no study that measures executed installs" no longer holds. What remains open [I]: a transparent, adequately sized base rate (reported N and CIs) on ordinary developer tasks, in default (confirmation-on) agent settings, against a logged live-registry proxy; and a post-failure taxonomy in the *non-adversarial* setting. The G1 study design below already fits this narrower gap; position it as a larger, reproducible measurement, not as the first one.
- **G2 strengthened.**
  - [V] The only prior test of existence checks and registry lookups in this setting reports "limited mitigation" [@hsu2026harmless, p. 8], but it was run on model outputs (its no-safeguard row equals the model-level result, [@hsu2026harmless, p. 6]) and the safeguard implementation is not described. [I] A transparent install-time guard benchmark would directly resolve this.
  - [V] Content-level defences failed on instruction-file attacks: prompt-injection detectors had FNR 20%–100% (the best FNR came with 34% FPR) [@wang2026package, p. 19], and static Skill scanners missed or under-rated malicious Skills [@liu2026trust, p. 12]; [@hsu2026harmless, p. 7]. [I] An install-time check is independent of how a name was induced, which strengthens the case for G2.
- The recommended order (G3 → G1 → G2) is unchanged, but the G1 write-up must cite these papers as the closest prior work.

## Summary ranking

| Rank | Gap | Type | Confidence | Feasibility | Est. cost / time |
|---|---|---|---|---|---|
| G1 | How often coding agents *actually attempt to install* non-existent or suspicious packages in ordinary, non-adversarial tasks, and what they do after the install fails | population/context, evidence | medium-low (narrowed 2026-11-12, see revision) | moderate | ≤ $100 API + 20–50 h unattended local runs; 4–6 weeks |
| G2 | No independent, shared-benchmark evaluation of laptop-runnable client-side pre-install guards on the hard cases (import≠distribution names, registered lookalikes, new legitimate packages, post-cutoff registrations) | practical, methodological | medium | easy–moderate | $0 API; 2–3 weeks |
| G3 | No validated, shared measurement protocol; the papers' decision rules disagree, so their rates and contradictions cannot be compared | methodological, contradiction | medium-high | easy | $5–30 API; 3–4 weeks incl. annotation |
| G4 | The effect of quantization *as deployed in local runtimes* (GGUF levels via Ollama) on spontaneous PyPI/npm package hallucination | population/context | medium-low | moderate (CPU time) | $0; 40–80 h unattended |
| G5 | Independent long-horizon (≥12-month) re-check of published hallucinated-name corpora for registration and weaponisation | evidence | low (largely narrowed by a new TOSEM paper) | easy | $0; 1 day + monthly cron |

---

## G1: We found no study that measures how often autonomous coding agents *actually run* `pip`/`npm install` on non-existent or suspicious package names during ordinary, non-adversarial tasks, or what they do after the install fails

- **Gap type:** population/context (agentic setting untested) + evidence (no base rate).

- **Evidence that the gap exists:**
  - The agentic setting is explicitly out of scope or named as future work in five independent analysed papers:
    - [A] Churilov states that agentic setups are not studied [@churilov2026range, p. 14].
    - [A] Dasu does not evaluate closed frontier models or agentic settings [@dasu2026refusing, p. 10].
    - [A] Twist names agentic coding workflows as future work [@twist2026library, p. 9].
    - [A] PackMonitor does not cover coding-agent workflows, `requirements.txt`, Dockerfiles or CI [@liu2026packmonitor, p. 19].
    - [A] Okwor proposes moving from self-generated output to live coding-agent traffic [@okwor2026hallucination, p. 8].
  - Installation itself is the harmful event, so measuring generated text alone misses the point:
    - [V] 56% of real malicious packages execute at install time, PyPI 96% [@ohm2020backstabbers, p. 11].
    - [V] Install-time execution through `setup.py` and npm `postinstall` was confirmed offline [@okwor2026hallucination, p. 7].
  - No paper reports actual installs. Measurement stops at generated text or is proxied by HTTP reachability:
    - [A] Haque calls for verifying by executing `go get` [@haque2025secure, p. 7].
    - [A] Zheng did not measure Cargo-level installation [@zheng2026when, p. 10].
  - Agent-like behaviours are suggestive but untested in agents:
    - [V] Models emit install commands even for names their own comments mark as placeholders [@zhao2025hfuzzer, p. 9].
    - [V] An optional PyPI-existence tool is rarely called by GPT-5-mini (7.89%), and invalid libraries remain in up to 38.79% of cases [@twist2026library, p. 8].
    - [V] Retry with a same-family fallback fails again on 83.5% of give-ups, and invented names recur across both models [@raj2026names, p. 10].
    - [I] What an agent does after a 404 (repeat, substitute a lookalike, or write its own code) is therefore an open and security-relevant question.
  - Persistence makes predictable agent installs plausible: [V] 43% of hallucinated names recur in 10 of 10 re-queries [@spracklen2024we, p. 9].
  - Independent support: five analysed papers from different groups list the agentic setting as untested, which makes this the most frequently stated gap in the set.

- **Novelty check (2026-11-12):**
  - `rlab search` queries (Crossref + arXiv, 2024– or 2025–):
    1. `coding agent installs hallucinated package pip npm` — OpenAlex failed (429); Crossref 25 hits; arXiv 0.
    2. `coding agent hallucinated package` — Crossref 24, arXiv 13.
    3. `slopsquatting agent` — Crossref 25, arXiv 1.
    4. `agent trajectories pip install dependency` — Crossref 24.
    5. `AI coding agent supply chain security dependencies` — Crossref 24, arXiv 8.
    6. `software engineering agent package installation security` — Crossref 24, arXiv 7.
    7. `hallucinated tool calls coding agents` — Crossref 24, arXiv 20.
    8. Plus the shared sweeps listed above.
  - WebSearch (2 queries) covered agent install measurement and SWE-agent/OpenHands trajectories. Two pages were also fetched with WebFetch (TrendAI report; DepScope post).
  - Closest hits and why they do not fill the gap:
    - **Bagmar & Saraf, "Setup Complete, Now You Are Compromised…" (arXiv 2607.15143).** [abstract] An *adversarial* evaluation: the attacker edits README, requirements or Makefile files, and the study tests production agent harnesses on 12 scenarios. It reports that a deterministic pre-install check closes most of the gap. Not a natural base rate with ordinary tasks and no attacker. Highly relevant: recommend for inclusion.
    - **Shan et al., "StateMirror…" (arXiv 2610.32648).** [abstract] A preliminary study of 4,398 agent trajectories finds "hallucinated tool use" to be pervasive, including actions on "missing packages". The mismatch is with the *local environment* (path or package not installed), not with the public registry. Slopsquatting exposure is not measured. Closest natural-trajectory evidence. Recommend for inclusion; read the full text to check whether registry-level non-existence is separable.
    - **TrendAI / Trend Micro report (S. Park, 2025-06-05, grey).** 100 web-dev tasks on foundation models. The 10 worst tasks were run manually on coding agents and Cursor with MCP. It reports counts of fabricated names (agents "approximately half"), does not say whether installs were executed, and gives no per-agent rates. Grey and small; not peer-reviewed.
    - **DepScope post (dev.to, grey, vendor).** Uses *induced* names supplied in the prompt and chat output only. "Installed" means "emitted an install command"; nothing was executed.
    - **SetupBench (arXiv 2507.09063)** and **Milliken et al., "Beyond pip Install" (SANER 2025, 10.1109/saner64311.2025.00009).** Agents bootstrapping environments; capability-focused, not slopsquatting. Useful as task sources.
    - **"Beyond Final Code" (arXiv 2503.12374, WebSearch only).** ModuleNotFoundError is common in SWE-bench agent logs. Environment errors, not registry checks.
    - Agent-attack papers in the project, not analysed (abstract-level only): arXiv 2610.09264 studies package-hallucination attacks on coding agents injected through rule files; arXiv 2605.29354 studies prompting attacks that steer hallucination through agent skills; arXiv 2605.09594 studies dependency steering through malicious agent skills. All three are *induced/adversarial* settings, not natural base rates.
  - Result: we found no study that measures executed package installs by coding agents on ordinary tasks against a live registry, or that characterises agent behaviour after a failed install (searches on 2026-11-12). The gap is narrowed from the scout version: adversarial agent installs and environment-level hallucinated tool calls are already studied.

- **Confidence: medium.**
  - For: five analysed papers state the gap, and two databases plus web search found only adversarial or environment-level neighbours.
  - Against: StateMirror's full text may contain registry-relevant counts. Vendor telemetry (e.g., Socket, Aikido) may exist unpublished. The field moves monthly.

- **Potential contribution:**
  1. The first natural base rate (with CIs) of agents attempting to install non-existent, post-cutoff or lookalike packages.
  2. A taxonomy of post-failure behaviour (correct fix / lookalike substitution / own implementation / give up / repeat).
  3. A direct agent-vs-chat comparison on the same tasks and model, testing whether the agent loop reduces or amplifies exposure.
  4. A reusable, *safe* measurement harness: a logging registry proxy that never executes unknown packages.

- **Suggested study (laptop-scale; benign tasks only):**
  - **Safety design (non-negotiable):**
    - Every run happens in a disposable Docker container or VM whose only network route is a **local logging package proxy**: devpi or a small PEP 503 simple-index proxy for PyPI, Verdaccio for npm.
    - The proxy forwards only names that exist and whose first release predates a fixed cutoff (e.g., 2026-01-01). Everything else gets a genuine 404 and is logged as "would-have-installed".
    - So no unknown or newly registered package code ever runs.
    - Never register any name. Report found names to PyPI/npm security through coordinated disclosure instead of publishing lists of unregistered names. [I] Churilov's publishing experiment was underpowered and cannot show that publishing is harmless [@churilov2026range, p. 12].
  - **Phase 0 (free, 1 week):**
    - Mine public agent-trajectory releases for `pip|uv|poetry|npm|yarn|pnpm add/install` commands. Example: SWE-bench submission trajectories; verify availability and licence first.
    - Score the names with the G3 protocol.
    - Gives an existing-data base rate. Caveat: SWE-bench environments are mostly pre-installed.
  - **Phase 1 (controlled runs):**
    - Agents:
      - Aider (open-source CLI; works with API models and Ollama);
      - mini-SWE-agent or OpenHands;
      - optionally Claude Code in headless mode, if the user has access.
    - Models:
      - one cheap frontier API model from Churilov's cohort (e.g., Claude Haiku 4.5 or GPT-5.4-mini);
      - one local model (qwen2.5-coder:7b, Ollama default quantization).
    - Tasks:
      - 200 Python tasks (optionally 100 JavaScript tasks) phrased neutrally ("Write and run a script that … Install whatever you need.");
      - converted from the public prompt corpus released with Spracklen/Churilov (39,969 prompts, [@churilov2026range, p. 4]);
      - stratified by Stack Overflow vs LLM-generated source and by topic recency, because both shift rates [@churilov2026range, p. 7; @spracklen2024we, pp. 8–9].
      - No fake names and no adversarial text in prompts.
    - 3 runs per task × agent × model (persistence).
    - **Baseline:** the same model in single-turn chat on the same task, scored with the same protocol.
  - **Metrics:**
    1. Per-task install-attempt hallucination rate: at least one install request for a name absent from the registry at run time. Report Wilson 95% CIs. With 0 events, use the rule-of-three upper bound.
    2. Per-install-command rate.
    3. Category shares: non-existent / import-name used as install name (e.g., `pip install cv2`) / registered lookalike / registered after model cutoff / correct.
    4. Post-404 behaviour distribution, including whether a substitute name is itself a low-reputation lookalike.
    5. Run-to-run persistence and Jaccard overlap of names across agents.
  - **Analysis:**
    - Paired agent-vs-chat comparison per task (McNemar);
    - logistic mixed model with a task random effect (agent, model, ecosystem, prompt source as fixed effects);
    - pre-register hypotheses and stopping rules.
  - **Sample-size reasoning:** if the true per-task rate is about 3%, 600 runs per configuration give about 18 events, a CI of roughly ±1.4 pp. Zero events bounds the rate below 0.5%, which is itself a publishable result.
  - **Cost and time:**
    - API agent runs use about 20k–100k tokens each, roughly $0.05–0.50 per run with a small model. Cap the API arm at 100 tasks × 3 runs, about ≤ $100.
    - Local Ollama arm: free, about 2–5 min per run on Apple Silicon, so about 20–50 h unattended.
    - Total 4–6 weeks.
  - **Expected threats to validity:**
    - low base rate (power);
    - proxy blocking alters downstream behaviour (mitigate: return a byte-identical registry 404);
    - agent and model version drift (log versions and dates);
    - task-selection bias towards install-heavy tasks [I], the same bias noted for Haque's GPT-4o filtering;
    - import-name ambiguity (handled by G3).

- **Feasibility for a beginner: moderate.**
  - Docker, a proxy and agent CLIs are well documented, and all scoring is offline Python.
  - The hard part is safe sandboxing and enough runs to get events. Phase 0 gives a no-risk start.

---

## G2: We found no independent evaluation, on a shared labelled benchmark, of laptop-runnable client-side pre-install guards on the cases that defeat a plain existence check

- **Gap type:** practical + methodological.

- **Evidence that the gap exists:**
  - Existence checks are necessary but not sufficient (stated by several papers):
    - [A] Plain registry checks are inadequate because attackers can pre-register names [@spracklen2024we, p. 12].
    - [I] Any registry-present name passes PackMonitor's mask, and vetted allowlists are not evaluated [@liu2026packmonitor, p. 6; @liu2026packmonitor, p. 19].
    - [A] If attackers pre-register hallucinated names, a registry oracle labels them valid (oracle poisoning) [@spracklen2026llm, p. 12].
  - The hard cases are real:
    - [V] 25 of 2,282 hallucinated names were registered within about six months, and at least 23 suggested names previously hosted malware [@churilov2026range, p. 12].
    - [V] 19 of 22 registered public names are placeholders [@okwor2026hallucination, pp. 5–6], and [A] a placeholder can be weaponised in a later release [@okwor2026hallucination, p. 8].
    - [V] Import names of real packages were the largest false-positive class (144–207 mentions per model) [@churilov2026range, p. 10].
  - Proposed but **not evaluated** defences:
    - [A] a date-aware verification list [@krishna2025importing, p. 8];
    - [A] registry grounding at generation time [@dasu2026refusing, p. 9];
    - [A] guided decoding plus lightweight registry verification [@djire2026evaluating, p. 11];
    - [A] a namespace- and near-miss-aware Rust guardrail [@zheng2026when, p. 9].
  - The only black-box guard in the set has known false-positive and drift problems:
    - [A] Its top feature (maintainers) is about 0 through the PyPI JSON API, risking false positives on small or new legitimate packages [@raj2026names, p. 13].
    - [A] Drift handling is not implemented [@raj2026names, p. 14].
    - [V] Half of its "registered lookalike" flags are the import names `pil`/`faiss` [@raj2026names, p. 8].
  - Forced versus optional checks: [V] a model-callable existence tool is rarely called by GPT-5-mini [@twist2026library, p. 8]. [I] This supports a *forced* client-side check over a tool the model may skip.
  - Hardware: [V] white-box defences need weights or logits and GPU servers [@liu2026packmonitor, p. 12; @liu2026mitigating, p. 6; @spracklen2026llm, p. 8]. Only static analysis ran on a laptop-class machine [@mirandapena2026empirical, p. 17].
  - Background support: [A] user-side countermeasures (pinning, disabling install scripts) are recommended [@ohm2020backstabbers, p. 16].

- **Novelty check (2026-11-12):**
  - `rlab search` queries (Crossref + arXiv, 2024–):
    1. `pre-install check malicious dependency verification` — Crossref 24, arXiv 1.
    2. `dependency confusion typosquatting detection tool evaluation false positives` — Crossref 24.
    3. `package name squatting detection PyPI npm 2025` — Crossref 24.
    4. `hallucinated imports registry` — arXiv 3.
    5. Plus G1 queries 2 and 7 (which surfaced SlopsGuard) and the shared sweeps.
  - WebSearch: one query on slopsquatting pre-install guard evaluation and false positives.
  - Closest hits and why they do not fill the gap:
    - **Kurnaz et al., "SlopsGuard" (NOMS 2026 demo, 10.1109/noms69089.2026.11668187).** [abstract] Multi-ecosystem pre-install tool (Levenshtein similarity, SBOM, CVE scan, cross-registry validation, CI exit codes). It is a demo paper; the abstract reports no false-positive/false-negative evaluation, and Levenshtein checks miss most hallucinations: 48.6% of hallucinated names are at edit distance ≥ 6 [@spracklen2024we, p. 11]. Recommend for inclusion (medium).
    - **Hillah et al., "Bayesian-Calibrated Detection of Hallucinated Package Imports…" (arXiv 2606.13918).** [abstract] Adds PyPI metadata (age, release count, author, summary) to surface registered-but-suspicious packages, evaluated on 1,734 Python snippets from 6 models. It evaluates *calibration* against a re-implemented binary baseline that shares the oracle, not a cross-tool comparison. Python only; import→distribution handling is not stated in the abstract. Closest academic work: recommend for inclusion (high) and use as a baseline.
    - **Huang et al., TOSEM 2026 (10.1145/3830237).** Proposes NymGuard (detection plus preemptive registration plus a public warning registry). Its focus is the registry side, not client-side false-positive and false-negative evaluation.
    - **Bagmar & Saraf (arXiv 2607.15143).** A deterministic pre-install check closes most of the gap in *adversarial setup-doc* scenarios. It does not benchmark existing guards or the hallucination-specific hard cases.
    - **Hal-Detector (Cyber-AI 2026, 10.1109/cyber-ai70573.2026.11755213).** An explainable classifier of JavaScript package names; not a deployable guard benchmark.
    - **ConfuScope (TSE 2026, 10.1109/tse.2026.3721700).** Package-confusion detection; no abstract retrieved. Check before finalising.
    - **PyPIGuard (SSRN 2026).** A malicious-*code* classifier, not hallucinated-name handling.
    - Grey tools: SlopGuard, pkgguard, ghostpkg, Socket Firewall. They report self-measured false-positive figures on different, incomparable sets, and the web search summary found "no independent head-to-head evaluation … on a shared corpus".
  - Result: we found no study that compares client-side guards on a shared labelled set covering import≠distribution names, registered hallucinated names and placeholders, new legitimate long-tail packages and known-malicious names, reporting per-class false-positive and false-negative rates and laptop latency (searches on 2026-11-12).

- **Confidence: medium.**
  - For: the evidence is strong and multi-paper. The novelty is narrowed because individual guards exist (SlopsGuard, the Bayesian layer, grey tools); the gap is the *independent comparative evaluation on hard cases*, not "a guard".
  - Against: the Bayesian-calibration paper's full text may include more comparisons than the abstract shows.

- **Potential contribution:**
  - An open benchmark ("GuardBench-lite") of labelled install requests;
  - the first independent false-positive/false-negative comparison of existing guards;
  - a minimal reference guard (pip/npm wrapper plus an agent pre-command hook) with ablations showing which signals matter;
  - practical guidance for developers using AI agents.

- **Suggested study:**
  - **Data:** 1,000–2,000 labelled install requests (PyPI first; npm optional) in six classes:
    - C1: popular legitimate packages (about 300; top downloads).
    - C2: legitimate long-tail and *recently created* legitimate packages (about 300; first release < 90 days). This is the false-positive stress class, following the drift problem in [@raj2026names, p. 14].
    - C3: import-name-as-install-name requests (about 100; e.g., cv2, sklearn, PIL, yaml, bs4, dateutil, faiss), labelled with the correct distribution.
    - C4: hallucinated unregistered names (about 300; from G1/G3 generations and published lists such as Okwor's public anchors).
    - C5: hallucinated names that *are* registered: placeholders and squats (about 50; drawn from the names reported by Churilov and Okwor and re-checked live).
    - C6: known-malicious names from the OSV malicious-packages data (about 200). Use names and metadata only; never download.
  - **Guards compared:**
    - plain 404 check;
    - PyPA-normalised check;
    - Raj's two-feature rule, re-implemented [@raj2026names, p. 12];
    - date-aware rule [@krishna2025importing, p. 3];
    - top-N allowlist;
    - open-source community guards run as black boxes;
    - SlopsGuard and the Bayesian layer if their code is released;
    - **reference guard:** stdlib filter + import→distribution map + live registry + first-release date vs model cutoff + OSV malicious lookup + download/maintainer/repository signals + placeholder detection.
  - **Metrics:**
    - per-class false-negative rate (C3–C6) and false-positive rate (C1–C2), with Wilson CIs;
    - balanced accuracy;
    - "warn" vs "block" counts;
    - median and 95th-percentile latency per check on the laptop;
    - offline-mode behaviour.
  - **Analysis:**
    - signal ablation;
    - temporal re-test at T0 + 4 weeks to measure drift;
    - end-to-end: plug the best guard into the G1 harness as an agent hook and measure the drop in would-have-installed events and the false-block rate on correct installs.
  - **Cost and time:** $0 API. Use the registry and OSV APIs at ≤1 request/s per host, as in Churilov's protocol [@churilov2026range, p. 5]. 2–3 weeks.
  - **Threats:**
    - label circularity (the registry oracle is used for both label and guard; mitigate with manual audit of C3/C5);
    - tool-version drift;
    - attackers can fake metadata, untested as noted in [@raj2026names, p. 13] (add a small synthetic "realistic-metadata" class, built from metadata records only, never published);
    - class proportions are not real-world prevalence (report per class).

- **Feasibility for a beginner: easy–moderate.** Pure Python plus HTTP APIs. No models are needed except to generate C4 names.

---

## G3: There is no validated, shared protocol for deciding whether an LLM-mentioned package is hallucinated, and the analysed papers' rules disagree enough to change conclusions

- **Gap type:** methodological + contradiction.

- **Evidence that the gap exists:**
  - **Import names (contradiction 5 in the evidence matrix):**
    - [V] Twist counts any registered import name as valid, with PyPA normalisation only [@twist2026library, p. 4; @twist2026library, p. 15].
    - [V] Raj flags registered import names (`pil`, `faiss`) as squats [@raj2026names, p. 8].
    - [I] Djire validates code-generation imports against the registry without a reported mapping, so `cv2`-type names probably count as hallucinations [@djire2026evaluating, p. 6].
  - **Extraction:**
    - [A] Spracklen rejects import parsing because module names do not map to package names [@spracklen2024we, p. 6].
    - [I] Churilov claims to follow Spracklen yet parses imports [@churilov2026range, p. 5].
    - [V] 34 of 46 GPT-4o hallucinations in HFuzzer are install-name errors with a correct import [@zhao2025hfuzzer, p. 9].
  - **Stdlib:** [V] treating stdlib modules as hallucinations inflates Python PHR by +7.6 to +9.4 pp [@djire2026evaluating, p. 5]. [V] Raj does not report stdlib handling [@raj2026names, p. 5].
  - **Snapshots and time:**
    - [V] Static lists miscounted and inflated rates by about 1/5 compared with live two-round validation [@churilov2026range, p. 10].
    - [V] Only two papers apply a release-date or cutoff rule [@krishna2025importing, p. 3; @liu2026mitigating, p. 5].
    - [A] The public npm name mirror is unreliable [@okwor2026hallucination, p. 3].
  - **Units:** [V] per-prompt [@krishna2025importing, p. 4] vs per-mention [@spracklen2024we, p. 7] vs per-string including file paths [@haque2025secure, p. 8] vs per source-level crate reference, including std-module confusions [@zheng2026when, p. 4].
  - **Extractor errors dominate small studies:** [V] most early "hallucinations" were extractor false positives [@raj2026names, p. 7].
  - **The contradictions may be method artefacts:**
    - [V] Language direction: JS > Py in Spracklen [@spracklen2024we, p. 7] vs Py > JS in Krishna and Churilov [@krishna2025importing, p. 8; @churilov2026range, p. 7].
    - [V] Prompt-source ordering reverses on the *same* corpus [@spracklen2024we, p. 20; @churilov2026range, p. 7].
    - [I] Both are plausibly driven by extraction and import-name handling. Untested.
  - Independent support: six or more papers from different groups use incompatible rules, and the critical reviews flagged it as the field's main comparability problem.

- **Novelty check (2026-11-12):**
  - `rlab search` queries (Crossref + arXiv, 2024–):
    1. `import name distribution name mapping Python package` — Crossref 24; nothing relevant.
    2. `package hallucination measurement methodology registry snapshot` — Crossref 24; only djire2026evaluating (in project).
    3. `package hallucination benchmark standardized evaluation` — Crossref 17, arXiv 1; general hallucination benchmarks only.
    4. `hallucinated imports registry` — arXiv 3.
    5. Plus the shared sweeps.
  - WebSearch: one query on an import vs install name measurement protocol. It found "no standardized protocol", only per-paper reconcilers and tool alias tables (e.g., pkghall's ~180-alias table, Socket's glossary examples).
  - Closest:
    - churilov2026range's live two-round protocol (in project; the most complete, but its pipreqs map covers only about 1,157 import names, [@churilov2026range, p. 14], and it is unvalidated against human labels);
    - Hillah et al. (arXiv 2606.13918; calibration of one detector, not a cross-rule protocol);
    - Al-Zofi systematic review (Research Square 2025, 10.21203/rs.3.rs-8007192/v1; synthesises definitions, no protocol validation).
  - Result: we found no study that re-scores the same generations under the different published decision rules, validates them against human labels, and tests whether the documented contradictions survive (searches on 2026-11-12).

- **Confidence: medium-high.**
  - For: the evidence is direct and multi-paper, and no protocol-validation study was found.
  - Against: the risk is that a methodology note gets less attention than an attack or defence paper.

- **Potential contribution:**
  - A short, versioned protocol checklist (extraction scope, stdlib, import→distribution map, normalisation, live registry plus time-of-generation rule, registered-lookalike class, units);
  - an open reference scorer (a small pip-installable library);
  - a human-labelled gold set;
  - a sensitivity analysis quantifying how far the rule choice moves rates and whether contradictions 1 and 2 flip.
  - [I] It is also the scoring engine that G1, G2 and G4 need, so it is reused rather than wasted.

- **Suggested study:**
  - **Data:**
    - 1,000 prompts from the released Spracklen/Churilov corpus [@churilov2026range, p. 4], balanced by Stack Overflow vs LLM-generated source and Python vs JS;
    - 2 cheap API models plus 1 local Ollama model, 1 sample each (3 samples for a 200-prompt subset): about 3,600 generations.
  - **Method:**
    - Implement seven scorers: six reproducing the analysed papers' rules (Spracklen static list; Churilov live + time-of-generation + pipreqs; Krishna regex + date-aware; Twist PyPA-normalised imports; Raj top-level-import 404; Djire registry ∪ stdlib) plus the proposed protocol.
    - Gold set: a stratified sample of 400 extracted names, labelled by two annotators (the user plus a peer), with Cohen's κ.
  - **Metrics:**
    - rate per rule (per mention and per generation, with Wilson CIs);
    - precision and recall of each rule against gold;
    - rank changes across models;
    - whether the Py-vs-JS and prompt-source orderings flip.
  - **Baseline:** Churilov's protocol as the strongest existing rule.
  - **Cost and time:** about 3M output tokens on small models, about $5–30. Local arm free. 3–4 weeks, including annotation.
  - **Threats:**
    - gold-label subjectivity for borderline names (e.g., deprecated aliases, cross-ecosystem names);
    - corpus leakage into 2026 training data [@churilov2026range, p. 14];
    - re-implementations may not match the originals exactly (validate on any published examples).

- **Feasibility for a beginner: easy.** Deterministic Python, small API spend, and a clear deliverable. A good first project or a first work package.

---

## G4: We found no study of how quantization levels *as shipped by local runtimes* (GGUF via Ollama/llama.cpp) affect spontaneous package hallucination on PyPI/npm

- **Gap type:** population/context.

- **Evidence that the gap exists:**
  - [A] Local quantized models are explicitly excluded by Churilov [@churilov2026range, p. 14].
  - [V] The only quantization study is Go-only, uses bitsandbytes, and finds that 4-bit Qwen 0.5B hallucinates 96–99% of Go package strings vs 41–54% at full precision [@haque2025secure, p. 6]. [V] Its 8-bit effects are inconsistent [@haque2025secure, p. 6]. [V] Its oracle counts file paths [@haque2025secure, p. 8].
  - Quantization is a hidden confound elsewhere:
    - [V] Spracklen ran all open models GPTQ-quantized [@spracklen2024we, p. 6].
    - [A] Dasu confounds size with 4-bit quantization [@dasu2026refusing, p. 10].
    - [I] Contradiction 3 (model size) in the evidence matrix may partly be a quantization effect.
  - Small open models are covered, but without varying quantization or reporting rates under local runtimes:
    - [V] Djire: 8 open 1–8B models, 4 ecosystems, "single GPU", quantization not reported [@djire2026evaluating, p. 4].
    - [V] Okwor runs five models through Ollama but reports no rate [@okwor2026hallucination, p. 3].
    - [A] Raj lists local (non-API) inference as untested [@raj2026names, p. 14].

- **Novelty check (2026-11-12):**
  - `rlab search` queries:
    1. `quantized local LLM package hallucination` (Crossref + arXiv, 2024–) — Crossref 20.
    2. `Ollama code generation security` — Crossref 21, arXiv 5.
    3. `small language models hallucinated dependencies quantization` — Crossref 23, arXiv 1.
    4. `quantization package hallucination` (arXiv) — 1 hit, haque2025secure (in project).
    5. `quantized code models hallucination` (arXiv) — 19.
  - WebSearch: one query on package hallucination with quantized local models, Ollama and GGUF.
  - Closest:
    - **Afrin et al., "Quantize with Confidence?" (arXiv 2607.14181).** [abstract] Six quantization methods including GGUF on Qwen2.5-Coder/CodeLlama; measures correctness, maintainability and security of code, *not* package hallucination. Recommend for inclusion (medium).
    - **DepScope post (grey).** Three Ollama models, *induced* names, chat only.
    - The in-project papers above (haque2025secure, djire2026evaluating, okwor2026hallucination).
  - Result: we found no study that varies GGUF quantization level for the same models and measures spontaneous PyPI/npm hallucination with registry-correct scoring (searches on 2026-11-12). Narrowed from the scout version ("local models at scale across ecosystems"), because small models across four ecosystems are already covered by djire2026evaluating.

- **Confidence: medium-low.**
  - For: an increment over Haque (Go to PyPI/npm, bitsandbytes to GGUF).
  - Against: Djire or Okwor artefacts may contain quantized runs, and the result may be "small effect", which is lower impact.

- **Potential contribution:** practical guidance for laptop developers ("is Q4 riskier than Q8 for dependencies?"), and resolution of the quantization confound behind contradiction 3.

- **Suggested study:**
  - qwen2.5-coder 1.5B and 7B plus llama3.2 3B at Q4_K_M, Q8_0 and F16 in Ollama. Use F16 for 7B only if RAM ≥ 32 GB.
  - 400 prompts (Python + JS) from the Churilov corpus, 3 samples at temperature 0.7, scored with the G3 protocol.
  - **Metrics:**
    - per-mention and per-generation rates (Wilson CIs);
    - number of mentions, since the denominator shifts under 4-bit [@haque2025secure, p. 5];
    - refusals;
    - persistence;
    - Jaccard overlap across quantization levels.
  - **Analysis:** logistic mixed model (prompt random effect; quantization × ecosystem interaction).
  - **Cost and time:** $0. About 7,200 generations at about 20–40 s each, about 40–80 h unattended. 3–4 weeks.
  - **Threats:**
    - Ollama default tags and chat templates change over time (pin digests);
    - Metal/CPU nondeterminism;
    - small models' low mention counts.

- **Feasibility for a beginner: moderate.** The code is simple, but compute time and model management need care.

---

## G5: Evidence on whether hallucinated names actually get claimed and weaponised over long horizons is thin and short-window (narrowed after the novelty check)

- **Gap type:** evidence.

- **Evidence that the gap exists:**
  - [V] 25 of 2,282 names were registered within about six months, one with malware; the natural experiment is underpowered (MDE about 10.5%) [@churilov2026range, p. 12].
  - [A] Churilov proposes monitoring registrations [@churilov2026range, p. 15].
  - [V] 0 of 1,641 private names were registered after only 4 days [@okwor2026hallucination, p. 5].
  - [A] Okwor proposes to keep watching the names [@okwor2026hallucination, p. 8].
  - [A] Spracklen did not register names and withheld the list [@spracklen2024we, p. 14].
  - [V] Pre-LLM malicious packages stayed available for 209 days on average [@ohm2020backstabbers, p. 11], so windows of six months or less can miss them.

- **Novelty check (2026-11-12):**
  - `rlab search` queries:
    1. `hallucinated package names registered registry monitoring` — Crossref 23.
    2. `longitudinal registration hallucinated package names` — Crossref 20.
    3. `newly registered packages PyPI malicious monitoring` — Crossref 24.
    4. `package hallucination registration` (arXiv) — 0.
    5. `malicious package registration npm PyPI` (arXiv) — 0.
    6. Plus the shared sweeps.
  - WebSearch: one query on monitoring hallucinated-name registrations in the wild in 2026. It found Socket/CSA secondary write-ups of the Churilov names (Socket says it re-queried on 2026-10-27; results not seen) and "no independent public monitoring feed".
  - Closest: **Huang et al., "Package Hallucinations as Phantoms in Open Source Software Supply Chains" (ACM TOSEM 2026, 10.1145/3830237).** [abstract] Registered 107 hallucinated names on npm for 6 months: 35.2% of installs were attributed to developers, mostly within 2 weeks; web-search augmentation *raised* persistence from 11.2% to 17.3%. It also proposes NymGuard (detection, preemptive registration, a public warning registry). This **substantially fills** the "is it exploitable in the wild" part of G-e. Recommend for inclusion (high; peer-reviewed tier 1–2).
  - Result: what remains is an *independent, ≥12-month* re-check of already-published hallucinated-name lists on PyPI and npm, using metadata-only content triage. We found no such study (searches on 2026-11-12).

- **Confidence: low.**
  - For: the gap that remains is genuine but small.
  - Against: Huang et al. and vendor telemetry largely cover it, and the outcome is likely a handful of events.

- **Potential contribution:** a longer-horizon data point extending Churilov's six-month window, delivered as a cheap add-on to G1/G2 rather than a project of its own.

- **Suggested study:**
  - Re-query published names (Okwor's public anchors; Churilov's published names where available) monthly via the PyPI/npm JSON APIs and OSV.
  - For new registrations, record first-release date, maintainer count, description/placeholder text and OSV status. Never install or execute.
  - Report Kaplan–Meier-style "time to registration" curves combined with Churilov's 6-month data [@churilov2026range, p. 12].
  - Cost $0; 1 day setup plus a monthly cron.
  - **Threats:**
    - published lists are biased towards defender claims [@okwor2026hallucination, p. 6];
    - placeholder vs malicious intent cannot be judged from metadata.

- **Feasibility for a beginner: easy**, but low standalone impact.

---

## Dropped or merged candidates

| Candidate | Decision | Reason |
|---|---|---|
| IDE inline-completion suggestions (scout idea) | dropped | No analysed paper provides author-stated evidence; only our own [I] note that agent/IDE settings are uncovered in spracklen2024we. Fails the evidence test. Partly absorbed into G1. |
| "Other ecosystems" (Go/Rust/Ruby/Java) | dropped | Already covered: Go [@haque2025secure, p. 6], Rust [@zheng2026when, p. 5], Ruby/Rust [@djire2026evaluating, p. 9], JS/Rust [@twist2026library, p. 20], npm/crates/Go/Java [@dasu2026refusing, p. 8]. |
| Model-side defences (unlearning, editing, logit masking) on a laptop | dropped for this user | Evidence exists, but they need weights, gradients or logits and GPU servers [@liu2026mitigating, p. 6; @spracklen2026llm, p. 8; @liu2026packmonitor, p. 12]. Not laptop-feasible or short. |
| Typosquatting amplification via user-supplied misspelled names | dropped | Already measured: up to 25.86% one-character typos used [@twist2026library, p. 6]; misspelled names fabricated on 14% [@dasu2026refusing, p. 8]. |
| Relevance of PackMonitor's forced substitutions | merged into G1/G2 | Real [I] gap [@liu2026packmonitor, p. 6], but it needs local logit access. The black-box analogue (what replaces a failed name) is G1 metric 4. |
| Prompt-source and language-direction contradictions as separate gaps | merged into G3 | They are most plausibly method artefacts; G3 tests this directly. |
| Original G-e "registry-side monitoring" (broad) | narrowed to G5 | Largely filled by Huang et al. (TOSEM 2026) and Churilov's natural experiment. |
| Original G-a "agents install hallucinated names" (broad) | narrowed to G1 | The adversarial agent-install setting is covered by arXiv 2607.15143 and the three unanalysed attack papers. Environment-level hallucinated tool calls are covered by StateMirror. The *natural base rate and post-failure behaviour* remain open. |

## Papers recommended for inclusion (found during novelty checks; not analysed, not cited as evidence)

| Priority | Paper | Identifier | Why |
|---|---|---|---|
| high | Huang et al., "Package Hallucinations as Phantoms in Open Source Software Supply Chains: An Empirical Security Analysis", ACM TOSEM 2026 | 10.1145/3830237 | Real-world npm registration and install experiment; NymGuard; web-search augmentation amplifies persistence. Narrows G5 and informs G2. Peer-reviewed. |
| high | Bagmar & Saraf, "Setup Complete, Now You Are Compromised: Weaponizing Setup Instructions Against AI Coding Agents", 2026 | arXiv 2607.15143 | Closest agent-install work (adversarial); harness × model effects; deterministic pre-install check. Bounds G1 and G2. Preprint. |
| high | Shan et al., "StateMirror: Pre-Execution Detection of Hallucinated Tool Calls in Coding Agents", 2026 | arXiv 2610.32648 | 4,398 natural agent trajectories with hallucinated tool use, including missing packages. Must read to confirm G1's novelty. Preprint. |
| high | Hillah et al., "Bayesian-Calibrated Detection of Hallucinated Package Imports in AI-Assisted Code", 2026 | arXiv 2606.13918 | Metadata channel for registered-but-suspicious names. Closest G2 baseline. Preprint. |
| medium | Kurnaz et al., "SlopsGuard: A Defense Tool Against AI-Hallucinated Package Attacks in Software Supply Chains", NOMS 2026 (demo) | 10.1109/noms69089.2026.11668187 | Existing pre-install guard; a G2 comparator. |
| medium | Li et al., "ConfuScope: … Robust Package Confusion Detection", IEEE TSE 2026 | 10.1109/tse.2026.3721700 | Package-confusion detector; possible G2 baseline (no abstract retrieved). |
| medium | Afrin et al., "Quantize with Confidence? An Empirical Study of Quantization for Code Generation", 2026 | arXiv 2607.14181 | GGUF and other quantization methods for code models; bounds G4. |
| medium | Milliken, Kang & Yoo, "Beyond pip Install: Evaluating LLM Agents for the Automated Installation of Python Projects", SANER 2025 | 10.1109/saner64311.2025.00009 | Agent installation tasks; G1 task source. |
| medium | Arora et al., "SetupBench", 2025 | arXiv 2507.09063 | Environment-bootstrap benchmark; G1 task source. |
| low–medium | Bonfanti et al., "Hal-Detector: Is Explainable AI Helping Detect Slopsquatting?", Cyber-AI 2026 | 10.1109/cyber-ai70573.2026.11755213 | JavaScript hallucinated-name classifier. |
| low–medium | "Beyond Final Code: A Process-Oriented Error Analysis of Software Development Agents…", 2025 (WebSearch only) | arXiv 2503.12374 | ModuleNotFoundError prevalence in SWE-bench agent logs; G1 Phase 0. |
| low | Al-Zofi, "AI-Induced Supply-Chain Compromise: A Systematic Review…", Research Square 2025 | 10.21203/rs.3.rs-8007192/v1 | Background review (preprint). |
| low | Logroño & Salazar, slopsquatting in npm code (Spanish), MQRInvestigar 2026 | 10.56048/mqr.2026.e396 | Small npm measurement (320 generations, 4 models). |

Grey sources seen (context only, never as evidence): TrendAI/Trend Micro slopsquatting agents report (2025-06-05), DepScope dev.to benchmark, Socket slopsquatting glossary, CSA research note (2026-04-19).

## Recommendation: the single best project for this user

Combine **G1 + G3**, with **G2 as the defence half**, as one coherent laptop study: "Do AI coding agents actually install hallucinated packages, and can a simple pre-install guard stop it?"

1. **G3 (weeks 1–3):** build the shared scoring protocol and gold set. This is a low-risk deliverable that is publishable on its own if time runs out.
2. **G1 (weeks 3–7):** run benign everyday tasks through Aider (and optionally Claude Code) with one cheap API model and one local Ollama model. Every install request goes through a logging proxy that never executes unknown packages. This yields the first natural base rate of agent install attempts on non-existent, lookalike or post-cutoff names, plus what agents do after a failed install, which no analysed or newly found paper measures.
3. **G2 (weeks 6–9):** replay the logged install requests, plus a small labelled hard-case set, through existing guards and a reference guard, reporting per-class false positives and false negatives and laptop latency.

Expected cost is about $100–150 in API fees, with all heavy runs unattended on the laptop. It needs no GPU, reproduces no attack technique (benign tasks only, no names registered, coordinated disclosure), and produces a measurement result, a reusable harness and a practical defence evaluation.

The main risk is a very low base rate. In that case a tight upper bound plus the guard evaluation is still a solid result.

Before starting, add Huang et al. (TOSEM 2026), StateMirror, "Setup Complete" and the Bayesian-calibration paper to the project and analyse them, so that G1 and G2 novelty is re-confirmed against their full texts.
