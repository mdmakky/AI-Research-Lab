# Research Gaps and Opportunities

A research gap is an open question. The evidence from the analysed papers must show that it is open, and a novelty check must fail to find a study that already answers it. A novelty check is a set of targeted searches that asks: "has someone already done this?" All our checks ran on 2026-11-12. They used Crossref and arXiv (two free scholarly databases) plus web searches for very recent and non-academic work. OpenAlex, a third database, had used up its free daily limit, and Semantic Scholar and Google Scholar were not searched. So "we found no study" means only that these searches found none. It does not mean that no such study exists.

Papers found during the novelty checks are not part of our 17 analysed papers. We saw only their abstracts. Statements about them are author claims [A]. We name them in plain text with their identifiers, so you can look them up. Vendor reports and blog posts seen during the searches guided the searching but are never used as evidence.

How the gaps were ranked [I]: by how new the gap is, how feasible it is on a laptop, and how much a result would matter, given your situation (beginner, laptop only, no GPU, short project). These rankings are our judgement.

| Gap | In short | Novelty verdict | Confidence | Beginner feasibility | Estimated cost and time |
|---|---|---|---|---|---|
| G1 | How often AI coding agents actually try to install invented or suspicious packages during ordinary tasks, and what they do when the install fails | novel for the narrowed claim | medium | moderate | up to about $100 in API fees plus 20–50 hours of unattended runs; 4–6 weeks |
| G2 | An independent comparison of laptop-friendly pre-install guards on the hard cases | partially novel | medium | easy to moderate | $0; 2–3 weeks |
| G3 | A validated, shared rule for deciding whether a package name is invented | novel | medium-high | easy | $5–30; 3–4 weeks including labelling |
| G4 | The effect of local model compression levels (GGUF files run with Ollama) on invented PyPI and npm names | partially novel (an increment) | medium-low | moderate | $0; 40–80 hours of unattended runs |
| G5 | Watching published invented names for 12 months or more | mostly addressed (narrow remainder) | low | easy | $0; 1 day setup plus a monthly check |

[I] Confidence here means how sure we are that the gap is real and still open. G3 is ranked third by the gap report but should be done first, because G1, G2 and G4 all need its scoring tool (see the recommended project below).

## G1. Do AI coding agents actually install invented packages during ordinary tasks?

> **Gap.** We found no study that measures how often AI coding agents actually run pip install or npm install on names that do not exist (or look suspicious) during ordinary, non-adversarial tasks, or what the agents do after such an install fails.

An AI coding agent is an AI tool that does not just suggest code but also runs commands by itself, such as installing packages. Non-adversarial means that nobody is trying to trick the agent: the tasks are normal everyday coding requests.

**Why it is a gap.**

- [A] Five analysed papers from different groups say agents are not covered or are future work [@churilov2026range, p. 14; @dasu2026refusing, p. 10; @twist2026library, p. 9; @liu2026packmonitor, p. 19; @okwor2026hallucination, p. 8]. This makes it the most often stated gap in the set.
- [V] Installation is the harmful step, so measuring only the text the AI writes misses the point. 56% of real malicious packages run their code during installation, and 96% of the PyPI ones do [@ohm2020backstabbers, p. 11]. Install-time code execution through pip and npm was confirmed offline [@okwor2026hallucination, p. 7].
- [A] No analysed paper reports real installs. Measurement stops at the generated text or uses a stand-in, such as checking whether a web address answers [@haque2025secure, p. 7; @zheng2026when, p. 10].
- [V] Models write install commands even for names their own code comments call placeholders [@zhao2025hfuzzer, p. 9].
- [V] A model offered an optional PyPI lookup tool called it on only 7.89% of responses, and invented libraries remained in up to 38.79% of cases [@twist2026library, p. 8; @twist2026library, p. 21].
- [V] When one model gave up, retrying with a bigger model from the same family failed again on 83.5% of cases, and the same invented names came back in both models [@raj2026names, p. 10].
- [V] Invented names repeat: 43% came back in 10 of 10 repeated queries [@spracklen2024we, p. 9]. [I] So agent installs of invented names could be predictable, which is what an attacker needs.

**Novelty verdict.** Novel for the narrowed claim. Confidence: medium. Attacks where someone plants instructions for the agent, and agents confusing their own local setup, are already studied. What we did not find is a natural base rate of real install attempts on ordinary tasks, checked against the live registry, plus a description of what agents do after a failed install (searches on 2026-11-12). G1 is provisional for one more reason, explained under Limitations in About this guide.

Closest prior work (abstracts only, [A]):

- Setup Complete, Now You Are Compromised (Bagmar and Saraf; arXiv 2607.15143, preprint). An attacker edits setup files such as the README or requirements list, and the study tests real agent tools on 12 scenarios. A simple fixed pre-install check closes most of the gap. This is an attack setting, not a natural base rate.
- StateMirror (Shan et al.; arXiv 2610.32648, preprint). In 4,398 natural agent runs, agents often act on tools or packages that are missing from their local machine. This is about the local machine, not the public registry, so slopsquatting exposure is not measured. Read its full text to check.
- SetupBench (arXiv 2507.09063, preprint) and Beyond pip Install (Milliken, Kang and Yoo; SANER 2025, DOI 10.1109/saner64311.2025.00009). Agents that set up software environments. They measure ability, not security, but are useful sources of tasks.
- Beyond Final Code (arXiv 2503.12374, found by web search only). "Module not found" errors are common in agent logs from a well-known benchmark. These are setup errors, not registry checks.

**What you could do.** [I] Produce the first natural base rate, with confidence intervals, of agents trying to install invented, lookalike or very new packages. Add a simple classification of what agents do after a failed install (fix it correctly, switch to a lookalike name, write the code themselves, give up, or repeat). Compare agents with plain chat on the same tasks and the same model. The safe measurement setup you build is itself reusable.

**Suggested study design for a beginner.** [I]

1. Build the safety setup first (see Safety rules below). Every run happens in a throwaway container whose only network route is a local logging package proxy. The proxy forwards only names that exist and were released before a fixed cutoff date, and returns a normal "not found" for everything else.
2. Phase 0, free, about 1 week: search public agent-run records from benchmark submissions for install commands, and score the names with the G3 scorer. Check that the records are available and licensed for reuse.
3. Pick agents: Aider (an open-source command-line agent that works with API models and local Ollama models), plus mini-SWE-agent or OpenHands. Optionally add Claude Code if you have access.
4. Pick models: one cheap frontier API model from the churilov2026range group, and one local model, for example a 7B coding model in Ollama.
5. Write 200 Python tasks (optionally 100 JavaScript tasks) in neutral words, such as "Write and run a script that ... Install whatever you need." Convert them from the public prompt collection released with the Spracklen and Churilov studies, 39,969 prompts in total [@churilov2026range, p. 4]. Balance them by prompt source and topic recency, because both shift the rates [@churilov2026range, p. 7; @spracklen2024we, p. 8]. Use no fake names and no tricks.
6. Run each task 3 times per agent and model. As a baseline, ask the same model the same task in a single chat turn and score it the same way.
7. Measure: the share of tasks with at least one install request for a name missing from the registry (with Wilson 95% confidence intervals, or the rule-of-three upper bound if there are none); the share per install command; the share of each name type (missing, import name used as install name, registered lookalike, registered after the model's training cutoff, correct); what the agent does after a "not found"; and how often names repeat across runs and agents.
8. Analyse: compare agent and chat on the same task with a paired test (McNemar), and use a logistic mixed model with the task as a random effect. Preregister your hypotheses.

**Feasibility: moderate.** Docker, a proxy and the agent tools are well documented, and all scoring is offline Python. The hard parts are safe sandboxing and running enough tasks to see events. Phase 0 gives a no-risk start. The gap report estimates that 600 runs per setup would give about 18 events if the true rate is about 3%, and that zero events would bound the rate below 0.5%, which is still a useful result.

**Risks.**

- The base rate may be very low, so you may see few events.
- Blocking an install may change what the agent does next. Return a normal registry "not found" so the agent cannot tell.
- Agents and models change between versions. Record versions and dates.
- Tasks that happen to need many installs could make the rate look higher than it is in everyday use.
- Import names used as install names are ambiguous. G3 handles this.

## G2. An independent test of pre-install guards on the hard cases

> **Gap.** We found no independent evaluation, on a shared labelled test set, of client-side pre-install guards that run on a laptop, focused on the cases that defeat a plain "does this name exist?" check.

A pre-install guard is a small program that checks a package name before it is installed and warns or blocks if the name looks risky. Client-side means it runs on your own machine, not on the registry.

**Why it is a gap.**

- [A] Plain existence checks are not enough, because attackers can register invented names first [@spracklen2024we, p. 12]. If they do, a registry check labels the name as valid [@spracklen2026llm, p. 12].
- [I] PackMonitor lets through any registered name, and its authors did not evaluate a vetted allow-list [@liu2026packmonitor, p. 6; @liu2026packmonitor, p. 19].
- [V] The hard cases are real. Some invented names were registered within about six months, and at least 23 suggested names had earlier hosted malware [@churilov2026range, p. 12]. 19 of 22 registered public names were placeholders [@okwor2026hallucination, p. 5], and [A] a placeholder can be turned malicious in a later release [@okwor2026hallucination, p. 8].
- [V] Import names of real packages were the largest class of false alarms, 144–207 mentions per model [@churilov2026range, p. 10].
- [A] Four papers propose a guard but do not test it: a check against the model's training-cutoff date [@krishna2025importing, p. 8], registry grounding while the model writes [@dasu2026refusing, p. 9], guided decoding plus a light registry check [@djire2026evaluating, p. 11], and a Rust-specific checker [@zheng2026when, p. 9].
- [V] The only guard we analysed has known problems. Half of its "registered lookalike" flags are the import names pil and faiss [@raj2026names, p. 8]. [A] Its top signal is about zero through the public PyPI interface, which risks false alarms on small or new legitimate packages, and it does not handle changes over time [@raj2026names, p. 13; @raj2026names, p. 14].
- [V] A model rarely calls an optional lookup tool [@twist2026library, p. 8]. [I] This argues for a check that always runs, not one the model may skip.
- [V] White-box defences need model weights or internal scores and GPU servers [@liu2026packmonitor, p. 12; @liu2026mitigating, p. 6; @spracklen2026llm, p. 8]. Only static analysis ran on a laptop-class machine [@mirandapena2026empirical, p. 17].

**Novelty verdict.** Partially novel. Confidence: medium. Individual guards exist (a demo tool, a detector preprint, and several community tools). What we did not find is an independent head-to-head comparison of their false alarms and misses on a shared set of hard cases (searches on 2026-11-12).

Closest prior work (abstracts only, [A]):

- Bayesian-Calibrated Detection of Hallucinated Package Imports (Hillah et al.; arXiv 2606.13918, preprint). Adds PyPI metadata (age, number of releases, author, summary) to spot registered but suspicious packages, on 1,734 Python snippets from 6 models. It tests how well its scores are calibrated, not a comparison across tools. The closest academic work and a good baseline.
- SlopsGuard (Kurnaz et al.; NOMS 2026 demo, DOI 10.1109/noms69089.2026.11668187). A pre-install tool for several registries. The abstract reports no false-alarm or miss rates. [V] It relies partly on lookalike checks, yet 48.6% of invented names are six or more characters away from any real name [@spracklen2024we, p. 11].
- Package Hallucinations as Phantoms (Huang et al.; ACM TOSEM 2026, DOI 10.1145/3830237). Proposes NymGuard, which works on the registry side, not as a client-side guard.
- Setup Complete, Now You Are Compromised (arXiv 2607.15143, preprint). A fixed pre-install check helps in attack scenarios but is not compared with existing guards.
- Hal-Detector (Cyber-AI 2026, DOI 10.1109/cyber-ai70573.2026.11755213) and ConfuScope (IEEE TSE 2026, DOI 10.1109/tse.2026.3721700). A JavaScript name classifier and a package-confusion detector. No abstract was retrieved for ConfuScope; check it before finalising.
- Community tools seen on the web report their own false-alarm figures on different sets, so they cannot be compared.

**What you could do.** [I] Build an open, labelled test set of install requests, run the first independent comparison of existing guards on it, and add a minimal reference guard (a pip and npm wrapper plus an agent hook) with tests that show which signals matter. The result is practical advice for developers who use AI agents.

**Suggested study design for a beginner.** [I]

1. Build 1,000–2,000 labelled install requests (PyPI first, npm optional) in six classes.
2. Class C1: about 300 popular legitimate packages. Class C2: about 300 legitimate small or new packages (first released less than 90 days ago). C2 tests false alarms.
3. Class C3: about 100 import names used as install names, such as cv2, sklearn, PIL, yaml, bs4, dateutil and faiss, each labelled with its correct install name.
4. Class C4: about 300 invented, unregistered names from your own G1 or G3 runs and from published lists.
5. Class C5: about 50 invented names that are registered (placeholders and squats), re-checked live. Class C6: about 200 known-malicious names from the OSV malicious-packages data. Use names and metadata only; never download them.
6. Compare: a plain "not found" check; a check with standard name normalisation; the two-signal rule from raj2026names, re-built [@raj2026names, p. 12]; a training-cutoff date rule [@krishna2025importing, p. 3]; a top-N allow-list; community guards run as black boxes; and a reference guard that combines built-in module filtering, an import-to-install name table, a live registry check, the first-release date, an OSV lookup and simple popularity signals.
7. Measure false-alarm rates (C1–C2) and miss rates (C3–C6) per class with Wilson confidence intervals, plus speed per check on your laptop. Re-test after 4 weeks to see how results drift.
8. Finally, plug the best guard into the G1 setup and count how many would-have-installed events it stops, and how many correct installs it wrongly blocks.

**Feasibility: easy to moderate.** Pure Python and public web interfaces. No AI model is needed except to generate class C4 names. Keep registry and OSV requests to at most one per second per site, as churilov2026range did [@churilov2026range, p. 5].

**Risks.**

- The registry is used both to label the data and inside the guards (circularity). Check classes C3 and C5 by hand.
- Tools change between versions. Record versions and dates.
- Attackers can fake metadata, which was not tested in raj2026names [@raj2026names, p. 13]. You could add a small synthetic class built from metadata records only, never published.
- Class sizes do not reflect real-world frequencies, so report results per class.

## G3. A shared, validated rule for deciding whether a name is invented

> **Gap.** We found no study that re-scores the same AI answers under the different published counting rules, checks those rules against human labels, and tests whether the known contradictions survive.

**Why it is a gap.**

- [V] Papers treat import names differently. One counts any registered import name as valid [@twist2026library, p. 4; @twist2026library, p. 15]. Another flags registered import names as squats [@raj2026names, p. 8]. [I] A third probably counts unregistered import names such as cv2 as invented [@djire2026evaluating, p. 6].
- [A] One study rejects reading import lines, because module names do not map to package names [@spracklen2024we, p. 6]. [I] Its replication reads import lines anyway [@churilov2026range, p. 5].
- [V] In one case study, 34 of 46 invented names were wrong install names for a correct import [@zhao2025hfuzzer, p. 9].
- [V] Counting built-in modules as invented adds 7.6 to 9.4 percentage points in Python [@djire2026evaluating, p. 5]. Another paper does not report how it handles them [@raj2026names, p. 5].
- [V] Saved registry lists miscounted and inflated rates by about a fifth compared with a live re-check [@churilov2026range, p. 10]. Few papers apply a release-date rule, for example [@krishna2025importing, p. 3; @liu2026mitigating, p. 5]. [A] The public mirror of npm names is unreliable [@okwor2026hallucination, p. 3].
- [V] Units differ: per prompt [@krishna2025importing, p. 4], per mention [@spracklen2024we, p. 7], per string including file paths [@haque2025secure, p. 8], or per code reference including built-in modules [@zheng2026when, p. 4].
- [V] In small studies, extraction errors dominate: most early "hallucinations" were extractor mistakes [@raj2026names, p. 7].
- [I] Contradictions C1 and C2 (see the overview) may be side effects of these choices. Nobody has tested this.

**Novelty verdict.** Novel. Confidence: medium-high. The evidence is direct and comes from many papers, and no protocol-validation study was found (searches on 2026-11-12). The main risk is not novelty but attention: a methods paper may get less notice than an attack or defence paper.

Closest prior work:

- churilov2026range's live, two-round protocol (in our set). It is the most complete, but its import-name table covers only about 1,157 import names [@churilov2026range, p. 14], and it is not checked against human labels.
- Bayesian-Calibrated Detection (arXiv 2606.13918, preprint; abstract only, [A]). Calibrates one detector; it does not compare counting rules.
- AI-Induced Supply-Chain Compromise: A Systematic Review (Al-Zofi; Research Square 2025, DOI 10.21203/rs.3.rs-8007192/v1, preprint; abstract only, [A]). Summarises definitions; it does not validate a protocol.

**What you could do.** [I] Write a short, versioned checklist for counting invented names, release an open scoring tool (a small Python library), build a human-labelled gold set, and show how much each rule choice moves the rates and whether contradictions C1 and C2 flip. The scorer is then reused in G1, G2 and G4, so none of the work is wasted.

**Suggested study design for a beginner.** [I]

1. Take 1,000 prompts from the released Spracklen and Churilov prompt collection [@churilov2026range, p. 4], balanced by source (Stack Overflow or AI-written) and language (Python or JavaScript).
2. Generate one answer per prompt with two cheap API models and one local Ollama model, plus 3 answers for a 200-prompt subset. That is about 3,600 answers.
3. Build seven scorers: six that copy the published rules (spracklen2024we, churilov2026range, krishna2025importing, twist2026library, raj2026names, djire2026evaluating) and one careful rule of your own.
4. Your rule: pull names from install commands and from import lines separately; remove built-in modules; map import names to install names; normalise names the standard PyPA way [@twist2026library, p. 15]; check each name live on the registry with its first-release date; and label it as exists, not found, import name of a real package, or first released after the model's training cutoff.
5. Label a stratified sample of 400 names with a second person, and measure agreement with Cohen's kappa.
6. Report each rule's rate (per mention and per answer, with Wilson confidence intervals), its precision and recall against the gold labels, how model rankings change, and whether C1 and C2 flip. Use the churilov2026range rule as the strongest existing baseline.

**Feasibility: easy.** Deterministic Python, a small API budget and a clear result. A good first project, or the first work package of the combined project.

**Risks.**

- Some names are hard to label even for people (old aliases, names valid in another language's registry).
- The released prompts may be in the 2026 models' training data [@churilov2026range, p. 14].
- Your copies of the published rules may not match the originals exactly. Test them on any published examples.

## G4. Does local model compression change invented names on PyPI and npm?

> **Gap.** We found no study that varies the GGUF compression level of the same models, as people run them locally with Ollama, and measures spontaneous invented PyPI and npm names with careful scoring.

Quantization compresses a model by storing its numbers with fewer bits, so it fits on a laptop. GGUF is the file format most local tools use, and Ollama is a popular tool for running such models.

**Why it is a gap.**

- [A] Local compressed models are explicitly left out of the newest measurement [@churilov2026range, p. 14].
- [V] The only quantization study is about Go and uses a different compression tool. 4-bit Qwen 0.5B invented 96–99% of Go package strings, against 41–54% at full precision [@haque2025secure, p. 6]. Its 8-bit results are not consistent, and it counts file paths as packages [@haque2025secure, p. 6; @haque2025secure, p. 8].
- [V] Quantization is hidden in other studies: all open models in spracklen2024we were compressed [@spracklen2024we, p. 6], and [A] dasu2026refusing mixes size with 4-bit compression [@dasu2026refusing, p. 10]. [I] Contradiction C3 (model size) may partly be a compression effect.
- [V] Small open models are covered, but without varying compression: djire2026evaluating does not report it [@djire2026evaluating, p. 4], and okwor2026hallucination runs Ollama models but reports no rate [@okwor2026hallucination, p. 3]. [A] raj2026names lists local models as untested [@raj2026names, p. 14].

**Novelty verdict.** Partially novel: an increment over one Go study (from Go to PyPI and npm, and to the compression actually used locally). Confidence: medium-low. Existing data from other studies may already contain compressed runs, and the result may be "small effect".

Closest prior work (abstract only, [A]):

- Quantize with Confidence? (Afrin et al.; arXiv 2607.14181, preprint). Six compression methods including GGUF on coding models. It measures correctness, maintainability and security of code, not invented packages.

**What you could do.** [I] Give practical advice to laptop developers ("is a 4-bit model riskier than an 8-bit one for dependencies?") and help explain contradiction C3.

**Suggested study design for a beginner.** [I]

1. Pick qwen2.5-coder 1.5B and 7B plus llama3.2 3B at three levels: Q4_K_M, Q8_0 and F16. Use F16 for the 7B model only if your laptop has 32 GB of memory or more.
2. Use 400 Python and JavaScript prompts from the Churilov collection, 3 answers each at temperature 0.7, scored with the G3 scorer.
3. Measure per-mention and per-answer rates with Wilson intervals, the number of names mentioned (because compression can change it [@haque2025secure, p. 5]), refusals, repetition, and overlap of names across levels.
4. Analyse with a logistic mixed model (prompt as random effect; compression level crossed with language).

**Feasibility: moderate.** The code is simple, but about 7,200 answers at 20–40 seconds each take about 40–80 hours of unattended laptop time.

**Risks.** Ollama's default model tags and chat templates change over time, so pin exact versions. Laptop hardware can give slightly different outputs from run to run. Small models mention few packages, which gives few data points.

## G5. Do published invented names get claimed over a year or more?

> **Gap.** The evidence on whether invented names get registered and turned malicious over long periods is thin. What remains open is an independent re-check, over 12 months or more, of invented-name lists that have already been published.

**Why it is a gap.**

- [V] 25 of 2,282 names were registered within about six months, one with malware. The test of whether publishing names leads to registration was too small to detect anything below about 10.5% [@churilov2026range, p. 12]. [A] The authors propose ongoing monitoring [@churilov2026range, p. 15].
- [V] 0 of 1,641 unpublished names were registered after only 4 days [@okwor2026hallucination, p. 5]. [A] The author proposes to keep watching [@okwor2026hallucination, p. 8].
- [A] spracklen2024we did not register names and withheld its list [@spracklen2024we, p. 14].
- [V] Before AI assistants, malicious packages stayed available for 209 days on average [@ohm2020backstabbers, p. 11]. [I] Windows of six months or less can miss them.

**Novelty verdict.** Mostly addressed; a narrow remainder is open. Confidence: low. A peer-reviewed paper found during the novelty check covers much of the "is it exploited in the wild?" question.

Closest prior work (abstract only, [A]):

- Package Hallucinations as Phantoms in Open Source Software Supply Chains (Huang et al.; ACM TOSEM 2026, DOI 10.1145/3830237, peer-reviewed). The authors registered 107 invented names on npm for 6 months: 35.2% of installs were attributed to developers, mostly within 2 weeks, and web-search help raised how often names repeated from 11.2% to 17.3%. This largely fills the broad version of the gap.
- Security-company write-ups that re-checked the Churilov names were seen on the web, but no independent public monitoring feed was found. These are grey sources and not evidence.

**What you could do.** [I] Add a longer-term data point to Churilov's six-month window, as a cheap add-on to G1 or G2 rather than a project of its own.

**Suggested study design for a beginner.** [I]

1. Every month, look up already-published invented names (for example the public names used by okwor2026hallucination and the names published by churilov2026range, where available) through the PyPI and npm metadata interfaces and OSV.
2. For newly registered names, record the first-release date, number of maintainers, description or placeholder text, and OSV status. Never install or run anything.
3. Report "time to registration" curves combined with Churilov's six-month data [@churilov2026range, p. 12].

**Feasibility: easy.** One day of setup and a monthly scheduled job, at no cost. Low impact on its own.

**Risks.** Published lists lean towards names claimed by defenders [@okwor2026hallucination, p. 6]. Metadata alone cannot tell a harmless placeholder from a malicious one. The likely outcome is a handful of events.

## The recommended project: G3, then G1, then G2

> **Recommendation.** One coherent laptop study: "Do AI coding agents actually install invented packages, and can a simple pre-install guard stop it?"

[I] The gap report recommends combining three gaps in this order:

1. **G3, weeks 1–3.** Build the shared scoring tool and the human-labelled gold set. This is low-risk and publishable on its own if time runs out.
2. **G1, weeks 3–7.** Run benign everyday tasks through Aider (and optionally Claude Code) with one cheap API model and one local Ollama model. Every install request goes through a logging proxy that never runs unknown packages. This gives the first natural base rate of agent install attempts on missing, lookalike or very new names, plus what agents do after a failed install.
3. **G2, weeks 6–9.** Replay the logged install requests, plus a small labelled hard-case set, through existing guards and a reference guard. Report false alarms and misses per class, and speed on the laptop.

The gap report estimates about $100–150 in API fees, with all heavy runs unattended on the laptop and no GPU. The study uses only benign tasks, never registers names, and reports findings through coordinated disclosure. It produces a measurement result, a reusable safe test setup, and a practical defence evaluation. The main risk is a very low base rate. In that case, a tight upper bound plus the guard evaluation is still a solid result.

Before you start, add and analyse the four high-priority papers listed below, so that the novelty of G1 and G2 is re-confirmed against their full texts.

## Safety rules (apply from day 1)

[I] These rules come from the gap report and the research report. They are not optional.

- **Never install unknown packages.** The scorer only reads registry metadata. Any agent run (G1) happens in a throwaway container or virtual machine whose only network route is a local logging package proxy (for example devpi or a small simple-index proxy for PyPI, and Verdaccio for npm).
- **The proxy decides what gets through.** It forwards only names that exist and were first released before a fixed cutoff date (for example 2026-01-01). Everything else gets a normal "not found" and is logged as "would have installed". So no unknown or newly registered package code ever runs.
- **Never register any invented name**, not even as a harmless placeholder.
- **Use coordinated disclosure.** Report risky names privately to the PyPI and npm security teams. Do not publish lists of unregistered invented names. The only test of whether publishing names leads to registration was too small to show that publishing is harmless [@churilov2026range, p. 12].
- **Known-malicious names are data only.** For G2, use names and metadata from OSV. Never download the packages.
- **Keep registry requests polite.** At most one request per second per site, with caching [@churilov2026range, p. 5].
- **Check with a supervisor** about ethics approval and the disclosure plan before the G1 runs.

## Follow-up novelty checks

No separate follow-up topic was novelty-checked for this project, so there are no extra novelty-check reports in the reports folder. All novelty checks are recorded in the gap report. The research report recommends re-running the three shared searches (package hallucination, hallucinated packages, slopsquatting) on the day the project starts, because new preprints appear every month.

## Recommended next steps

A checklist, in order:

1. **Make the pending decision described under Limitations in About this guide.** Until then, G1 stays provisional.
2. **Add and analyse the four high-priority papers** in the table below (Huang et al., StateMirror, Setup Complete, and Bayesian-Calibrated Detection). Papers are added with rlab add, which checks their metadata, and each one then needs a full-text analysis. Then re-run the G1 and G2 novelty checks against their full texts.
3. **Choose your direction.** Our suggestion is the combined project G3, then G1, then G2. G3 alone is the safest fallback.
4. **Set up the safety rules** before any agent run: container, logging proxy, cutoff date, and no name registration.
5. **First experiment (G3, week 1): build a scorer and score 200 prompts.** Take 50 prompts each from Stack Overflow and AI-written sources, in Python and JavaScript, from the released Spracklen and Churilov collection [@churilov2026range, p. 4]. Check its licence first.
6. **Generate answers** with one free local model in Ollama (for example a 7B coding model), and optionally one cheap API model. [I] A small local model will give more invented names to work with than a frontier model.
7. **Write scorer version 0 in Python.** Pull names from install commands and import lines separately, remove built-in modules, map import names to install names starting from the table Churilov used [@churilov2026range, p. 14], normalise names the PyPA way [@twist2026library, p. 15], and look each name up live with caching.
8. **Score every answer twice,** once with a naive rule (any name not found counts as invented) and once with your scorer. Report rates with Wilson 95% confidence intervals and hand-check about 50 names where the two rules disagree. This pilot tests your setup; it does not answer the research question.
9. **Record tool and model versions and dates** for every run, because AI tools change quickly.
10. **Re-run the novelty searches** on the day the project starts, and again before you write a paper.
11. **Talk to a supervisor** about the statistics (mixed-effects models), ethics approval and coordinated disclosure.
12. **Optional:** an open-access published version of zhang2025llm exists. Replacing our arXiv copy needs your permission.

### Recommended papers not yet included (13)

Found during the gap novelty checks on 2026-11-12. Not analysed and not used as evidence. Priority is our judgement [I].

| Priority | Paper | Identifier | Why it matters |
|---|---|---|---|
| high | Huang et al., Package Hallucinations as Phantoms in Open Source Software Supply Chains: An Empirical Security Analysis (ACM TOSEM 2026, peer-reviewed) | DOI 10.1145/3830237 | Real-world npm registration and install experiment; NymGuard; narrows G5 and informs G2 |
| high | Bagmar and Saraf, Setup Complete, Now You Are Compromised: Weaponizing Setup Instructions Against AI Coding Agents (2026, preprint) | arXiv 2607.15143 | Closest agent-install work (attack setting); a fixed pre-install check; bounds G1 and G2 |
| high | Shan et al., StateMirror: Pre-Execution Detection of Hallucinated Tool Calls in Coding Agents (2026, preprint) | arXiv 2610.32648 | 4,398 natural agent runs, including missing packages; must be read to confirm G1 |
| high | Hillah et al., Bayesian-Calibrated Detection of Hallucinated Package Imports in AI-Assisted Code (2026, preprint) | arXiv 2606.13918 | Metadata signals for registered but suspicious names; closest G2 baseline |
| medium | Kurnaz et al., SlopsGuard: A Defense Tool Against AI-Hallucinated Package Attacks in Software Supply Chains (NOMS 2026 demo) | DOI 10.1109/noms69089.2026.11668187 | An existing pre-install guard to compare in G2 |
| medium | Li et al., ConfuScope: Robust Package Confusion Detection (IEEE TSE 2026) | DOI 10.1109/tse.2026.3721700 | Package-confusion detector; possible G2 baseline (no abstract retrieved) |
| medium | Afrin et al., Quantize with Confidence? An Empirical Study of Quantization for Code Generation (2026, preprint) | arXiv 2607.14181 | GGUF and other compression methods for coding models; bounds G4 |
| medium | Milliken, Kang and Yoo, Beyond pip Install: Evaluating LLM Agents for the Automated Installation of Python Projects (SANER 2025) | DOI 10.1109/saner64311.2025.00009 | Agent installation tasks; a task source for G1 |
| medium | Arora et al., SetupBench (2025, preprint) | arXiv 2507.09063 | Environment set-up benchmark; a task source for G1 |
| low to medium | Bonfanti et al., Hal-Detector: Is Explainable AI Helping Detect Slopsquatting? (Cyber-AI 2026) | DOI 10.1109/cyber-ai70573.2026.11755213 | JavaScript invented-name classifier |
| low to medium | Beyond Final Code: A Process-Oriented Error Analysis of Software Development Agents (2025, preprint; found by web search only) | arXiv 2503.12374 | How common "module not found" errors are in agent logs; G1 phase 0 |
| low | Al-Zofi, AI-Induced Supply-Chain Compromise: A Systematic Review (Research Square 2025, preprint) | DOI 10.21203/rs.3.rs-8007192/v1 | Background review |
| low | Logroño and Salazar, slopsquatting in npm code (in Spanish; MQRInvestigar 2026) | DOI 10.56048/mqr.2026.e396 | Small npm measurement (320 generations, 4 models) |

# Glossary

| Term | Plain meaning |
|---|---|
| Abstract-only | We read only the paper's short summary, not the whole paper. All 17 analysed papers were read in full. |
| Agent (AI coding agent) | An AI tool that takes actions by itself, such as running commands and installing packages, not just suggesting code. |
| Allow-list | A list of names that are approved in advance. Anything not on the list is blocked or flagged. |
| API | A defined way for one program to talk to another. "API model" means a commercial AI model used over the internet, paid per use. |
| arXiv | A free public website where researchers post papers, often before peer review. |
| Baseline | The thing you compare against, such as the plain model with no defence. |
| Benchmark | A fixed set of tasks and scoring rules used to compare AI systems. |
| Black-box method | A method that only needs the model's text output, so it also works with closed commercial models. |
| Cohen's kappa | A measure of how well two people agree when labelling, corrected for agreement by chance. 1 means perfect agreement; 0 means chance level. |
| Confidence interval (Wilson 95%) | A range that probably contains the true rate. Wider means more uncertain. Wilson's method works well for small counts. |
| Container (Docker) | An isolated, throwaway environment for running software, so nothing it does touches the rest of your computer. |
| Contradiction | Studies reporting results that disagree. |
| Coordinated disclosure | Reporting a security problem privately to those who can fix it before making it public. |
| Crate | A Rust package. crates.io is the Rust package registry. |
| Data-centre GPU (A100, MI210, MI300) | Expensive graphics processors used in server rooms to train and run AI models. Not available on an ordinary laptop. |
| DFA (deterministic finite automaton) | A simple state machine that accepts exactly a given list of strings, here valid package names. |
| Edit (Levenshtein) distance | The number of single-character changes needed to turn one name into another. |
| Evidence matrix | Our table of all findings from the papers, each with its source, label and strength. |
| Evidence strength | How much we trust a finding (strong, moderate or weak), based on sample size, design and agreement between studies. |
| False alarm (false positive) / miss (false negative) | A false alarm flags a safe name as risky. A miss lets a risky name through. |
| Fine-tuning | Training a model further on extra examples to change its behaviour. |
| Fuzzing | Automatically generating many varied test inputs to find failures. |
| GGUF / Ollama | A file format for compressed models, and a popular tool for running such models on a laptop. |
| Gold set | A set of examples labelled carefully by people and used as the reference answer. |
| Greedy decoding | Always picking the single most likely next word (temperature 0). |
| Grey literature | Reports, blogs and vendor material outside academic publishing. Not used as evidence in this guide. |
| HumanEval | A standard set of programming problems used to check that a model can still write correct code. |
| Import name vs install (distribution) name | In Python, the name you import (for example cv2) can differ from the name you install (opencv-python). |
| Install-time execution | Code inside a package that runs automatically while the package is being installed, before you ever use it. |
| LLM (large language model) | The type of AI behind tools like ChatGPT and Claude. It produces text, including code. |
| Logging proxy | A local server between your machine and the registry that records every install request and can block it. |
| Logits | The scores a model gives every possible next token (word piece) before it chooses one. |
| LoRA / model editing | Changing specific behaviours by training a small add-on set of weights instead of the whole model. |
| Mixed-effects model | A statistical model that handles repeated measurements on the same units, such as several runs of the same task. |
| Natural experiment | A study that uses a situation the researchers did not create, such as which names happen to get registered. |
| Novelty check | Targeted searches to see whether a proposed study has already been done. |
| OSV | A free public database of known vulnerabilities and malicious packages. |
| Package (dependency) | A reusable piece of third-party code that a project installs and relies on. |
| Package hallucination | An AI recommending or importing a package name that does not exist in the registry. |
| Package registry | The public store that install tools download from: PyPI for Python, npm for JavaScript, crates.io for Rust. |
| Peer review | Checking of a paper by independent experts before it is published. |
| Persistence | Whether the same invented name comes back when the same question is asked again. |
| Pilot study | A small trial run that tests the setup before the full study. |
| Placeholder package | A registered package with no real content, often registered by a defender to stop an attacker from taking the name. |
| Pre-install guard | A small program that checks a package name before it is installed and warns or blocks if it looks risky. |
| Preprint | A paper shared publicly before (or without) peer review, often on arXiv. Flagged and weighted lower in this guide. |
| Preregistration | Publishing your hypotheses and analysis plan before collecting data, so you cannot change them after seeing the results. |
| PyPA normalisation | The official Python packaging rule for treating differently written package names as the same name. |
| Quantization | Storing a model's numbers with fewer bits so it runs on smaller hardware, possibly at some cost to quality. |
| RAG (retrieval-augmented generation) | Looking up relevant documents and giving them to the model along with the question. |
| Rate per mention / per answer / per prompt | The share of invented items, which depends on what is counted. Rates with different units cannot be compared. |
| Registry snapshot vs live check | Checking names against a saved copy of the registry's list from one date, or asking the registry at the moment of checking. |
| Replication | Repeating a study to see whether the result holds. |
| Research gap | An open question that the evidence shows is unanswered and that a novelty check could not find already answered. |
| Rule of three | If 0 events are seen in n tries, the true rate is probably below 3 divided by n. |
| Saturation | The point where new searches keep returning papers you already have. |
| Self-refinement / self-check prompt | Asking the model to review its own answer, for example "check that every package you used exists". |
| Slopsquatting | Registering an AI-invented package name and filling it with malware, so that people who follow the AI's advice install it. |
| Software supply-chain attack | An attack that reaches victims through third-party code their project depends on. |
| Standard library | Modules built into a language that never need installing. |
| Static analysis | Checking code automatically without running it, for example with a type checker such as Pyright. |
| Temperature | A setting that controls how random the model's word choices are. |
| Typosquatting | Registering a misspelled version of a popular package name to catch typing mistakes. |
| Unlearning | Training a model to make specific outputs less likely. |
| White-box method | A method that needs access to the model's internals (weights or logits), so it only works with models you run yourself. |

# About this guide

## How it was made

This guide was put together on 2026-11-12 from the files of the research project, which also started on 2026-11-12. The project used the rlab tool in this workspace for every routine step, so that metadata, citations and page numbers are checked by a program rather than typed from memory.

1. **Scope.** You chose this topic from four candidate security topics. The defaults: papers from 2023–2026 (older supply-chain background allowed), peer-reviewed first, at most 20 papers in the first pass, preprints allowed but flagged.
2. **Search.** 19 discovery searches across five topics (measurement, exploitation, defences, agents and tools, testing and benchmarks) in OpenAlex, Crossref and arXiv. OpenAlex hit its free daily limit partway through.
3. **Screening.** Three search "scouts" checked the results against the inclusion rules. 20 papers were included, the planned maximum. Saturation was judged high.
4. **Full texts.** All 20 full texts were obtained legally: 19 from arXiv or the ACL Anthology, and one openly licensed report from its Zenodo record.
5. **Analysis and critical review.** 17 papers were analysed from their full text with page references. A second reviewer then checked every analysis against the paper, in two batches, and the fixes were applied.
6. **Synthesis.** All findings went into an evidence matrix (172 findings, 7 contradictions, 5 agreements). Findings from preprints were lowered one strength step. The study methods were compared side by side.
7. **Gap analysis.** Five candidate gaps were tested with 27 targeted searches on Crossref and arXiv plus web searches.
8. **Research report.** A plain-language report summarised everything. This guide reorganises the same material for reading: this overview, one brief per paper, and these closing sections.

Every citation in this guide was checked automatically: each one names a paper in the project and a page that exists in our PDF.

## Limitations

- **Three papers not analysed.** The project holds three more papers, all about attacks on AI coding agents: wang2026package (package-hallucination attacks on coding agents through instructions hidden in rule files; arXiv 2610.09264, preprint), hsu2026harmless (neutral-looking prompts that steer hallucination through agent "skills"; Findings of EMNLP 2026, our copy from the ACL Anthology) and liu2026trust (steering which dependencies an agent installs through malicious agent skills; arXiv 2605.09594, preprint). Their full texts are in the project, but they were not analysed, because an automatic safety check stopped the analysis output. What to do with them is waiting for your decision: a limited abstract-only analysis, your own reading with notes recorded, or leaving them out with a note. They are not used as evidence anywhere in this guide and have no briefs. They are the closest work to G1, so G1 stays provisional until they are handled.
- **Size.** The review rests on 17 analysed papers. That is enough to map a young field, but it is not a complete systematic review.
- **Preprints.** 10 of the 17 analysed papers are preprints, including one self-published report. Most findings rest on a single study, and almost none has been independently repeated.
- **Search sources.** OpenAlex ran out of its free daily quota, so later discovery searches and all 27 novelty searches used Crossref and arXiv only, plus web search. Semantic Scholar and Google Scholar were not used. Every "we found no study" statement is limited to the sources we used.
- **Search date.** All searches ran on a single day, 2026-11-12. This field produces new preprints every month, so re-check the gaps before you start.
- **Papers found but not analysed.** 13 relevant papers found during the novelty checks (4 of high priority) are not yet added or analysed. What this guide says about them comes from abstracts only. One of them, a peer-reviewed TOSEM 2026 field study, bears directly on RQ2 and has already narrowed G5.
- **Paper versions.** For 6 of the 7 peer-reviewed papers we analysed the arXiv version, not the publisher's final version, so page numbers may differ. An open-access published version of zhang2025llm exists; replacing our copy needs your permission. liu2026packmonitor's arXiv version has a different title from the published one.
- **Metadata.** Our database still lists spracklen2024we as a preprint, although we treat it as peer-reviewed (USENIX Security 2025). The automatic metadata check flags three known mismatches (one title difference and two Zenodo identifiers not listed in Crossref), each explained in the paper's analysis.
- **Who did the reading.** AI agents wrote the analyses. Each was checked by a critical review against the paper text, and cited pages were spot-checked, but not every number was re-checked by a person.
- **Our judgement.** Evidence-strength ratings, gap rankings and priorities are our own ratings [I]. Another team might rate some differently.
