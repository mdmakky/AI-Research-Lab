# Overview

## What this research is about

AI coding assistants such as ChatGPT, Copilot, Claude Code and Cursor write code for you, and that code often relies on packages. A package (also called a dependency) is a ready-made piece of code that other people wrote and published. You download it with a command such as pip install (for Python) or npm install (for JavaScript). These commands fetch the package from a package registry, a public online store of packages: PyPI for Python, npm for JavaScript, crates.io for Rust.

Sometimes the AI recommends a package that does not exist. This is called package hallucination. On its own, it only causes an error. The danger starts when an attacker notices the invented name, registers it on the registry, and puts malware inside. The next developer who trusts the AI and runs the install command gets the malware. This attack is called slopsquatting. It is a new kind of software supply-chain attack, which means an attack that reaches you through third-party code your project depends on.

This project asks how often package hallucination happens, how easy it is to exploit, and which defences work. The aim is to design a small study that you can run on an ordinary laptop. We read and analysed 17 papers in full.

The five research questions (RQs), in plain words:

1. **RQ1. How often?** How often do AI models and coding agents invent package names, and what makes it more or less likely (model, programming language, prompt, model compression, agent use)?
2. **RQ2. Exploitability.** Are invented names predictable enough for an attacker to use, and has anyone actually registered them?
3. **RQ3. Defences.** Which defences exist, how well do they work, what do they cost, and can they run on a normal laptop?
4. **RQ4. Measurement.** How do studies decide that a name is invented, and which of their choices can distort the numbers?
5. **RQ5. Gaps.** What has not been tested yet that a small laptop study could address?

## How to use this guide

The guide has three parts:

- **This overview.** Read it first. It gives the main answers, a map of all 17 papers, the five papers to read first, and where studies disagree.
- **The paper briefs.** One short brief per paper, in the same order as the paper map below. Read the five "read first" briefs, then the briefs for the group closest to your interest.
- **Research gaps, glossary and notes.** The last part explains the open questions (gaps G1 to G5), the study we recommend, the safety rules for that study, a next-steps checklist, a glossary of every technical term, and how this guide was made, including what is missing from it.

If a word is new to you, look it up in the glossary at the end.

**Evidence labels.** Each important statement carries one label:

- **[V] Verified.** We checked it in the paper's own data, tables or results.
- **[A] Author claim.** The authors say it, but we could not check it ourselves (for example, a claim that something is not covered by their study).
- **[I] Interpretation.** Our own reasoning, built from the cited papers. Treat it as an argument, not a fact.

**Citations.** A citation looks like this: [@churilov2026range, p. 12]. The first part (churilov2026range) is the paper's key, which is also the name of its folder in the project. "p. 12" is the page of the PDF we hold. That example points to the page where the Range Shrinks paper reports how many invented names were later registered. Page numbers refer to our PDF copies. For six of the seven peer-reviewed papers our copy is the arXiv version, so page numbers may differ from the publisher's version.

**Peer-reviewed vs preprint.** Peer review means independent experts checked a paper before a journal or conference published it. A preprint is a paper shared publicly (often on arXiv) before or without that check.

- 7 of our 17 papers are peer-reviewed: spracklen2024we, zhao2025hfuzzer, twist2026library, zhang2025llm, djire2026evaluating, liu2026packmonitor, and the background book chapter ohm2020backstabbers.
- 10 are preprints: churilov2026range, okwor2026hallucination, krishna2025importing, haque2025secure, zheng2026when, dasu2026refusing, liu2026mitigating, spracklen2026llm, raj2026names and mirandapena2026empirical.
- Special case one: our database lists spracklen2024we as a preprint, but it appeared at USENIX Security 2025, a top peer-reviewed security conference [@churilov2026range, p. 1]. We treat it as peer-reviewed. We read its arXiv version.
- Special case two: okwor2026hallucination is a self-published report on Zenodo (an open research archive). It is openly licensed but has had no peer review.
- Special case three: mirandapena2026empirical may have been accepted by a journal, but we could not confirm this, so it stays a preprint.
- We use preprints but give them less weight. The paper map marks each paper's status.

**Evidence strength.** We rate how much we trust each answer:

- **Strong:** enough data, sound design, and several studies agree.
- **Moderate:** sound design, but a single study or limited data.
- **Weak:** small or unclear samples, design problems, or preprints nobody has repeated.

In the project's evidence table, every finding from a preprint was lowered by one step.

## Main findings at a glance

> **In one sentence:** every AI model tested invents some package names, many of those names come back again and again, attackers have so far claimed few of them, and the defences that work best need data-centre hardware, while the cheap defences that would work on a laptop have barely been tested.

### RQ1. How often do models invent package names?

> **Answer:** in every model tested, but how often depends heavily on the model, the prompt and how each study counts. Evidence strength: moderate that it is real and depends on the model; weak for most other drivers.

- [V] Every study that measured it found package hallucination in every model it tested. This covers 16 models from 2023–24 [@spracklen2024we, p. 7], five frontier models from 2026 [@churilov2026range, p. 6], and Rust and Go as well as Python and JavaScript [@zheng2026when, p. 5; @haque2025secure, p. 6].
- [V] The size of the problem depends on the model class and on what is counted. Across 16 models from 2023–24, 19.7% of 2.23 million package mentions were invented [@spracklen2024we, p. 7]. For five 2026 frontier models it was 3.63–5.02% of mentions (preprint) [@churilov2026range, p. 6]. For eight small open models with 1–8 billion parameters it was 16.1–47.9% [@djire2026evaluating, p. 5].
- [V] In Rust, about 22% of crate references (a crate is a Rust package) were invented, and nearly half of these were confusions with Rust's built-in modules (preprint) [@zheng2026when, p. 5].
- [V] The prompt matters a lot. With ordinary requests, library-name hallucination was near zero (at most 0.31% of responses) across seven commercial models [@twist2026library, p. 5]. Asking for libraries "from 2025" raised it to as much as 84.74% of tasks for one model [@twist2026library, p. 5].
- [V] When the user types a misspelled or fake library name, models often go along with it: up to 79.44% of tasks for multi-character typos and 99.22% for fake names [@twist2026library, p. 6]. Two other papers confirm this tendency [@djire2026evaluating, p. 9; @dasu2026refusing, p. 8].
- [V] Other suspected drivers are contested or rest on one study. The language that comes out worse flips between studies (see C1 below). The one significant size effect relies on repeated data points that are not independent [@krishna2025importing, p. 6]. Temperature mattered in one study [@spracklen2024we, p. 8] but not in another [@zheng2026when, p. 6]. Quantization (compressing a model so it runs on smaller hardware) was tested in only one study, on Go, and its tables are not consistent [@haque2025secure, p. 6].
- [A] No analysed paper measures AI coding agents that run install commands by themselves [@churilov2026range, p. 14].

### RQ2. What makes invented names exploitable?

> **Answer:** many invented names are predictable enough to squat, but attackers have so far registered few of them. Evidence strength: moderate for predictability; weak for real-world exploitation.

- [V] Names come back. 43% of invented names reappeared in all 10 repeated queries [@spracklen2024we, p. 9]. 104 names were invented by all five 2026 frontier models, and 54 of these are one character away from a real package (preprint) [@churilov2026range, p. 9].
- [V] Most names are still specific to one model: 81% of distinct invented names came from a single model in 2023–24 [@spracklen2024we, p. 10], and 450 of 455 newly found names in a 2026 study came from a single model [@okwor2026hallucination, p. 4].
- [V] Many invented names do not look like a real package. Only 13.4% are within one or two character changes of a real name, and 48.6% are six or more changes away [@spracklen2024we, p. 11]. A simple "looks like a famous package" check would miss these.
- [V] Real-world claiming has been rare so far. 25 of 2,282 invented names (about 1.1%) were registered within about six months, one of them with malware, and at least 23 suggested names had earlier hosted malware (preprint) [@churilov2026range, p. 12].
- [V] Of 149 publicly listed invented names, 22 were registered, none with malicious content, and 19 were placeholders apparently registered by defenders (self-published preprint) [@okwor2026hallucination, p. 5].
- [V] The route for the malware is well established. 56% of 174 real malicious packages ran their code during installation, and 96% of the PyPI ones did [@ohm2020backstabbers, p. 11]. Install-time code execution through pip and npm was reproduced offline [@okwor2026hallucination, p. 7].

### RQ3. Which defences work, and can they run on a laptop?

> **Answer:** the strongest defences need access to the model's internals and data-centre GPUs; the cheap defences that work with any AI tool are only partly effective and barely tested. Evidence strength: weak to moderate.

- [V] White-box defences (which need the model's internal weights or scores) give the largest reductions. PackMonitor, which blocks any token that cannot form a name on the PyPI list, reached 0% hallucination on five 7–8B models with 7–28% extra time [@liu2026packmonitor, p. 13; @liu2026packmonitor, p. 14].
- [V] Model editing cut the package hallucination rate from 0.4421 to 0.1529 on unseen high-risk prompts (preprint) [@liu2026mitigating, p. 7]. Unlearning cut it from 21.23% to 2.56% for a 7B model (preprint) [@spracklen2026llm, p. 10].
- [V] These defences ran on data-centre hardware: 8 A100 GPUs, or 12–24-hour runs on AMD MI210/MI300 accelerators [@liu2026packmonitor, p. 12; @spracklen2026llm, p. 19]. Retraining can also damage coding skill: in one test the score fell from 51.4% to 25.3% [@spracklen2024we, p. 13].
- [V] Black-box defences (which only need the model's text output) are cheap but inconsistent. Retrieval-augmented generation (RAG) lowered the average rate from 29.7% to 18.1% in one study but raised it by 12.7 percentage points for JavaScript [@djire2026evaluating, p. 6]. Greedy decoding was the best simple trade-off for small models [@djire2026evaluating, p. 8].
- [V] Self-check prompts and an optional PyPI lookup tool reduced hallucination without removing it, and one model called the tool on only 7.89% of responses [@twist2026library, p. 18; @twist2026library, p. 21].
- [A] Checking only whether a name exists on the registry is not enough, because an attacker can register the name first [@spracklen2024we, p. 12]. [I] PackMonitor's filter lets through any registered name, including squatted ones [@liu2026packmonitor, p. 6].
- [V] The only tool-side guard in our set finished cleanly on 228 of 300 hand-written prompts, in a small evaluation (preprint) [@raj2026names, p. 7]. [A] Its most important signal, the number of maintainers, is not available through the public PyPI interface [@raj2026names, p. 13].
- [V] Only static code analysis was run on a laptop-class machine (Apple M2, 24 GB) [@mirandapena2026empirical, p. 17]. One of its tools, Pyright, caught between 14% and 85% of library hallucinations, depending on model and benchmark [@mirandapena2026empirical, p. 8].

### RQ4. How do studies measure package hallucination, and what distorts it?

> **Answer:** every study counts differently, so their numbers cannot be put side by side. Evidence strength: moderate.

- [V] Studies differ in where prompts come from, how names are pulled out of answers, whether they check names against a saved registry list or the live registry, how they treat built-in modules, and whether they count per name, per answer or per prompt. Because of this, rates cannot be pooled or ranked across papers [@spracklen2024we, p. 6; @krishna2025importing, p. 4; @churilov2026range, p. 5].
- [V] Counting Python's standard library (built-in modules that never need installing) as invented adds 7.6 to 9.4 percentage points [@djire2026evaluating, p. 5].
- [V] Import names of real packages (for example cv2, which you install as opencv-python) were the largest class of false alarms. A live re-check of the registry lowered rates by about a fifth [@churilov2026range, p. 10].
- [V] In a small study, most early "hallucinations" were really errors in the tool that pulled names out of the answers [@raj2026names, p. 7].
- [V]/[A] Further threats: statistics built on data points that are not independent [@krishna2025importing, p. 6]; model size mixed up with quantization [@dasu2026refusing, p. 10]; and going along with a planted fake name counted as invention [@twist2026library, p. 6].
- [V] Some studies judge "does not exist" against the task's own installed environment, not a registry, so their numbers do not measure slopsquatting exposure [@zhang2025llm, p. 6; @mirandapena2026empirical, p. 4].

### RQ5. What is still missing?

> **Answer:** five gaps passed a recorded novelty check on 2026-11-12. The recommended project combines three of them: first a shared way to score names (G3), then a measurement of AI coding agents (G1), then a test of simple pre-install guards (G2). Evidence strength: preliminary to moderate, depending on the gap.

- [A] Five analysed papers name AI coding agents as untested [@churilov2026range, p. 14; @dasu2026refusing, p. 10; @twist2026library, p. 9; @liu2026packmonitor, p. 19; @okwor2026hallucination, p. 8].
- [I] The five gaps are: how often coding agents actually try to install invented names (G1); an independent comparison of laptop-friendly pre-install guards (G2); a validated, shared measurement rule (G3); the effect of compressed local models on PyPI and npm (G4); and long-term watching of published names (G5).
- [I] Each gap is phrased as "we found no paper that ...", not "this has never been studied". The gaps section at the end explains each one, with a study design for a beginner.

## Paper map

The papers are grouped by approach, following the methodology comparison:

- **M. Measurement studies.** Ask models many coding questions, pull the package names out of the answers, and check them against the registry.
- **T. Testing and benchmarks.** Search on purpose for prompts that make models invent names, or build fixed test sets.
- **D. Defences inside or around the model.** Change the model's weights, change how it picks the next word, or give it extra information.
- **S. Tool-side and static checks.** Check names or code outside the model, without changing the model.
- **B. Background.** Real supply-chain attacks from before AI coding assistants.

Relevance (high, medium, low) is our rating of how close each paper is to the project question.

| # | Group | Paper (short title) | Year | Type | Status | What it is about | Relevance |
|---|---|---|---|---|---|---|---|
| 1 | M | We Have a Package for You! (spracklen2024we) | 2024 | Large measurement + mitigation test | Peer-reviewed (USENIX Security 2025; our copy is arXiv) | 16 models, 2.23 million package mentions in Python and JavaScript; how often names repeat | high |
| 2 | M | The Range Shrinks, the Threat Remains (churilov2026range) | 2026 | Preregistered replication + natural experiment | Preprint | Repeats the study above on five 2026 frontier models with a live registry check; tracks which names get registered | high |
| 3 | M | From Hallucination to Registration (okwor2026hallucination) | 2026 | Registration measurement | Preprint (self-published on Zenodo) | Do invented names get claimed on PyPI and npm? Who claims them? | medium |
| 4 | M | Importing Phantoms (krishna2025importing) | 2025 | Measurement + correlations | Preprint | 11 models in JavaScript, Python and Rust; links to model size and coding scores | high |
| 5 | M | Secure or Suspect? (haque2025secure) | 2025 | Measurement | Preprint | Effect of model compression (quantization) on invented Go packages | high |
| 6 | M | When LLMs Invent Rust Crates (zheng2026when) | 2026 | Measurement + prompt mitigation | Preprint | Invented Rust packages; effects of model size and temperature | high |
| 7 | M | LLM Hallucinations in Practical Code Generation (zhang2025llm) | 2025 | Taxonomy study | Peer-reviewed (Proc. ACM Softw. Eng., ISSTA; our copy is arXiv) | Types of code errors in real projects; missing packages are a very small share | low |
| 8 | T | HFuzzer (zhao2025hfuzzer) | 2025 | Testing tool + experiment | Peer-reviewed (ASE 2025; our copy is arXiv) | One AI writes tasks that make another AI invent Python packages | high |
| 9 | T | Refusing the Impossible (dasu2026refusing) | 2026 | Benchmark | Preprint | Do 17 open models refuse requests that cannot be done, such as using a package that does not exist? | high |
| 10 | T | Library Hallucinations in LLM-Generated Code (twist2026library) | 2026 | Controlled experiments + benchmark | Peer-reviewed (EMNLP 2026) | Which prompt wordings, typos and fake names trigger invented libraries | high |
| 11 | D | Evaluating Inference-Time Defenses (djire2026evaluating) | 2026 | Comparative experiment | Peer-reviewed (ASE 2026; our copy is arXiv) | Eight cheap defences on eight small open models in four languages; counting biases | high |
| 12 | D | PackMonitor (liu2026packmonitor) | 2026 | Technique + experiment | Peer-reviewed (Proc. ACM Softw. Eng.; our copy is arXiv, under a different title) | Blocks invented names while the model writes a pip install command | high |
| 13 | D | Model Editing against Package Hallucination (liu2026mitigating) | 2026 | Technique + experiment | Preprint | A small add-on to the model's weights that targets invented names | medium |
| 14 | D | LLM Ghostbusters (spracklen2026llm) | 2026 | Technique + experiment | Preprint | "Unlearning" invented names by retraining the model | medium |
| 15 | S | Names Can Hurt (raj2026names) | 2026 | System + small evaluation | Preprint | A registry check plus a metadata classifier that flags risky names | high |
| 16 | S | Static Analysis for Library Hallucinations (mirandapena2026empirical) | 2026 | Comparison of detection tools | Preprint (journal acceptance not confirmed) | Code-checking tools that catch invented library features; run on a laptop | medium |
| 17 | B | Backstabber's Knife Collection (ohm2020backstabbers) | 2020 | Dataset of real attacks + taxonomy | Peer-reviewed (book chapter, Lecture Notes in Computer Science; our copy is arXiv) | 174 real malicious npm, PyPI and RubyGems packages and how they attacked | medium |

## Reading order: the five papers to read first

Start with these five. Together they cover how to measure the problem, why it matters, and what a laptop defence would need to handle.

1. **The Range Shrinks, the Threat Remains (churilov2026range, preprint).** The most careful measurement in the set. It preregistered its analysis (published the plan before collecting data), re-checked names against the live registry, reported confidence intervals, and tracked which invented names were later registered [@churilov2026range, p. 5; @churilov2026range, p. 12]. Read it as the model for a careful protocol.
2. **We Have a Package for You! (spracklen2024we, peer-reviewed).** The founding large-scale study. Later papers reuse its prompts, and it gives the repetition and lookalike results behind the attack model [@spracklen2024we, p. 9; @spracklen2024we, p. 11].
3. **Library Hallucinations in LLM-Generated Code (twist2026library, peer-reviewed).** A controlled study showing which prompts trigger invented libraries, and that a model rarely uses an optional lookup tool [@twist2026library, p. 5; @twist2026library, p. 8]. [I] This is the main argument for a check that runs every time, not one the model may skip.
4. **Evaluating Inference-Time Defenses (djire2026evaluating, peer-reviewed).** Compares cheap defences on small open models of the kind you can run on a laptop, and measures how much counting built-in modules distorts the numbers [@djire2026evaluating, p. 5; @djire2026evaluating, p. 6].
5. **Names Can Hurt (raj2026names, preprint).** The closest existing laptop-style guard. It is most useful for its pitfalls: name-extraction errors, import-name confusion, and a key signal that is hard to obtain [@raj2026names, p. 7; @raj2026names, p. 9; @raj2026names, p. 13].

## Where studies disagree

All explanations here are our interpretation [I]. None has been tested, and we do not pick a side. Full entries are in the project's evidence matrix.

- **C1. Which language is worse, Python or JavaScript?** JavaScript was worse in one study [@spracklen2024we, p. 7], Python in two others [@krishna2025importing, p. 8; @churilov2026range, p. 7]. [I] The first study takes names from install commands and from lists the model is asked for; the other two read the import lines in the code. Python import names often differ from install names (cv2 versus opencv-python), so reading imports can inflate Python's rate.
- **C2. Which prompts are worse, Stack Overflow questions or AI-written prompts, on the same prompt set?** Stack Overflow prompts gave higher rates in 2024 [@spracklen2024we, p. 20]; AI-written prompts gave higher rates in 2026 [@churilov2026range, p. 7]. [I] The models, the name extraction and the year all differ. This is the cleanest contradiction in the set, and re-scoring one set of answers with both methods would test it.
- **C3. Do bigger models invent fewer names?** Yes in one study, but its statistics rest on data points that are not independent [@krishna2025importing, p. 6]. No size effect for Rust in another [@zheng2026when, p. 6], and a newer 8B model produced more unique invented names than its predecessor [@zhao2025hfuzzer, p. 7]. [I] Size is mixed up with quantization in several studies [@spracklen2024we, p. 6; @dasu2026refusing, p. 10].
- **C4. Does temperature matter?** Rates rose sharply above temperature 1 in one study [@spracklen2024we, p. 8] and did not change for Rust in another [@zheng2026when, p. 6]. [I] Different languages and counting rules; unresolved.
- **C5. Is a registered import name valid or a squat?** One paper counts it as valid [@twist2026library, p. 4]. Another flags pil and faiss as squats [@raj2026names, p. 8]. A third probably counts unregistered import names such as cv2 as invented [@djire2026evaluating, p. 6]. [I] The field has no shared table that maps import names to install names.
- **C6. Does RAG help?** Large gains in Python in one study [@spracklen2024we, p. 13], little effect in Rust [@zheng2026when, p. 9], and small increases in two other setups [@liu2026packmonitor, p. 13; @djire2026evaluating, p. 6]. [I] "RAG" means a different retriever and document collection in each paper.
- **C7. How often do invented names get registered? (compatible, not a real contradiction).** 25 of 2,282 names over about six months [@churilov2026range, p. 12], against 0 of 1,641 unpublished names after four days [@okwor2026hallucination, p. 5]. [I] The time windows and the sources of names differ, so both can be true.
