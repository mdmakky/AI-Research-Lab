# Research questions — Package Hallucination and Slopsquatting in LLM Coding Assistants: Measuring Hallucinated Dependencies, Their Exploitability on PyPI/npm, and Lightweight Defences

<!-- 3-5 questions. Each must be answerable from literature evidence. -->

## RQ1: How often do LLMs and coding agents hallucinate package names, and how does the rate vary by model, programming language/ecosystem, prompt type, quantization and agentic setting?
- Type: descriptive
- Why it matters: Base rate and drivers define the size of the threat and where to measure.
- Linked objective: O1
- Status: answered (literature)
- Current answer: Package hallucination appears in every model tested, from 2023–24 open models to 2026 frontier models, and in Python, JavaScript, Rust and Go [@spracklen2024we, p. 7; @churilov2026range, p. 6; @zheng2026when, p. 5; @haque2025secure, p. 6]. Its size depends on the unit and the model class: 3.63–5.02% of package mentions for five 2026 frontier models (preprint) [@churilov2026range, p. 6], against 16.1–47.9% of packages for small open 1–8B models [@djire2026evaluating, p. 5]. The best-supported drivers are the model itself and the prompt: year-based requests and user-supplied typos or fake names push rates very high [@twist2026library, p. 5; @twist2026library, p. 6]. Effects of language, size, temperature and quantization are contested or rest on one study [@haque2025secure, p. 6], and agentic settings have not been measured [@churilov2026range, p. 14]. Strength: moderate that it is non-zero and model-dependent; weak for most drivers.

## RQ2: What makes hallucinated packages exploitable: are names repeated across runs and models, do they collide with registered or malicious packages, and is there evidence of real-world slopsquatting?
- Type: descriptive
- Why it matters: Only persistent, predictable names are worth squatting; this defines the attack model.
- Linked objective: O2
- Status: answered (literature)
- Current answer: Hallucinated names are predictable enough to squat. 43% recur in all 10 re-queries [@spracklen2024we, p. 9], and 104 names are shared by all five 2026 frontier models, 54 of them one edit from a registered package [@churilov2026range, p. 9]. Real-world registration has so far been rare: 25 of 2,282 names in about six months, one of them with malware [@churilov2026range, p. 12], and publicly listed names are claimed mostly by defenders [@okwor2026hallucination, p. 5]. Install-time code execution, the payload route, is well documented [@ohm2020backstabbers, p. 11]. Strength: moderate for persistence; weak for real-world exploitation (two preprints, short observation windows).

## RQ3: Which defences against package hallucination have been proposed (fine-tuning, model editing, unlearning, RAG/self-check, registry-side checks), and how effective, costly and deployable are they?
- Type: comparative
- Why it matters: A beginner implementation study needs a cheap defence that works on ordinary hardware.
- Linked objective: O3
- Status: answered (literature)
- Current answer: White-box defences give the largest reductions: decoding-time logit masking (0% against its own list, ×1.07–×1.28 latency) [@liu2026packmonitor, p. 13; @liu2026packmonitor, p. 14], model editing [@liu2026mitigating, p. 7] and unlearning [@spracklen2026llm, p. 10]. All of them need weights or logits and were run on data-centre GPUs. Black-box options are cheap but inconsistent. RAG helps in some ecosystems and hurts in others [@djire2026evaluating, p. 6]. Greedy decoding is the best simple trade-off for small models [@djire2026evaluating, p. 8]. Self-check prompts and a PyPI tool reduce hallucination without removing it [@twist2026library, p. 18; @twist2026library, p. 21]. A registry existence check alone cannot catch names that are already squatted [@spracklen2024we, p. 12], and the only tool-side guard evaluation is weak [@raj2026names, p. 7]. Strength: weak to moderate (single runs, selected prompt sets, no independent replication).

## RQ4: How do studies measure package hallucination (prompt sources, ground-truth registry snapshots, metrics, deduplication), and what methodological weaknesses threaten their validity?
- Type: methodological
- Why it matters: A new measurement must avoid known pitfalls (stale registry snapshots, name normalisation, contamination).
- Linked objective: O4
- Status: answered (literature)
- Current answer: Studies differ in prompt source, extraction method (install commands, model-queried lists or import parsing), existence rule (static vs live snapshot, release-date cutoff or none), stdlib and import-name handling, and the unit of the rate. Because of this, rates cannot be pooled or ranked across papers [@spracklen2024we, p. 6; @krishna2025importing, p. 4; @churilov2026range, p. 5]. The largest documented biases are counting stdlib modules (+7.6 to +9.4 pp in Python) [@djire2026evaluating, p. 5] and counting import names of real packages, which were the largest false-positive class; the live re-check lowered rates by about a fifth [@churilov2026range, p. 10]. Further threats are pseudo-replicated statistics [@krishna2025importing, p. 6], quantization confounds [@dasu2026refusing, p. 10], and labelling compliance with planted names as invention [@twist2026library, p. 6]. Strength: moderate.

## RQ5: What has not yet been tested — e.g. agentic tools that install dependencies automatically, newer models, other ecosystems, lightweight client-side defences — that a laptop-scale study could address?
- Type: methodological
- Why it matters: Directly yields the implementation project (answered via gap report + novelty check).
- Linked objective: O4
- Status: partially answered
- Current answer: the analysed papers do not test agentic tools that install dependencies on their own [@churilov2026range, p. 14; @dasu2026refusing, p. 10; @liu2026packmonitor, p. 19]. They also leave three other areas untested: local quantized models in PyPI/npm settings [@churilov2026range, p. 14]; client-side guards that run on ordinary hardware and look beyond plain existence [@raj2026names, p. 13]; and a shared live, dated, mapping- and stdlib-aware measurement protocol. Only static analysis has been run on a laptop-class machine [@mirandapena2026empirical, p. 17]. Update 2026-11-12: the three agent-side attack papers are now analysed. Under a benign Skill, three real agents executed installs in 1.05%–3.33% of runs [@hsu2026harmless, p. 6], with task counts not reported, which narrows the agent gap (G1) to a larger, transparent base-rate measurement. Instruction-file attacks steer agents toward chosen or invented packages, and content scanners miss most of them [@wang2026package, p. 19; @liu2026trust, p. 12]. Strength: preliminary; none of these is a confirmed gap until gap-report.md records a novelty check.

