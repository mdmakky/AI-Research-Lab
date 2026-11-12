# Overview

## What this research is about

This project asks a practical question. Suppose you use an AI model to rebuild an existing app, and you only give it what anyone can see from the outside: the screens, how the app reacts when you click or type, and its documentation. You never show it the source code. People call this kind of work "reverse engineering". When the rebuilding is done mostly by talking to an AI in plain language and accepting the code it writes, people call it "vibe coding". How good is the rebuilt app? We judge "good" in three ways. Does it behave like the original (functional fidelity)? Is its code well written (code quality)? Can people understand and change it later (maintainability)? We read 23 recent papers in full to find out what is already known, and what is still missing.

The five research questions (RQs), in plain words:

1. **RQ1. Approaches.** What AI methods exist for rebuilding apps from what you can observe, and how do they relate to vibe coding?
2. **RQ2. Behaviour.** How do studies measure whether a rebuild behaves like the original, and how close do current AI tools get?
3. **RQ3. Code quality and maintainability.** Is AI-written or vibe-coded app code well written and easy to maintain, compared with human code?
4. **RQ4. Study quality.** How trustworthy are the current studies? What do they do well, and where are they weak?
5. **RQ5. Gaps.** What is still unknown, and what study could a beginner run to fill a gap?

## How to use this guide

The guide has three parts:

- **This overview.** Read it first. It gives the main answers, a map of all 23 papers, the five papers to read first, and where studies disagree.
- **The paper briefs.** One short brief per paper, in the same order as the paper map below. Read the five "read first" briefs, then the briefs for the group closest to your interest.
- **Research gaps, glossary and notes.** The last part explains the open questions (gaps G1 to G8), a cybersecurity follow-up, concrete next steps, a glossary of every technical term, and how this guide was made.

If a word is new to you, look it up in the glossary at the end.

**Evidence labels.** Each important statement carries one label:

- **[V] Verified.** We checked it in the paper's own data, tables or results.
- **[A] Author claim.** The authors say it, but we could not check it ourselves (for example, a claim that their tool is new).
- **[I] Interpretation.** Our own reasoning, built from the cited papers. Treat it as an argument, not a fact.

**Citations.** A citation looks like this: [@borg2026echoes, p. 13]. The first part (borg2026echoes) is the paper's key, which is also the name of its folder in the project. "p. 13" is the page of the PDF we hold. For example, that citation points to the page of the Echoes of AI paper that describes its maintenance-task design. Page numbers refer to our PDF copies, which for several papers are the arXiv versions, so they may differ from the publisher's page numbers.

**Peer-reviewed vs preprint.** Peer review means independent experts checked a paper before it was published in a journal or conference. A preprint is a paper shared publicly (often on arXiv) before or without that check.

- 16 of our 23 papers are peer-reviewed. 7 are preprints: bai2026recreationworld, chen2025iwr, kim2026programdistill, mota2026comparing, pan2026functional, yang2026programbench and zhao2025vibe.
- We use preprints but give them less weight. The paper map marks each paper's status.
- One special case: our database lists zhao2025vibe as a preprint, but the project notes say it was published at ICML 2026, without a DOI. We stay cautious and treat it as a preprint.

**Evidence strength.** We rate how much we trust each answer:

- **Strong:** enough data, sound design, and several studies agree.
- **Moderate:** sound design, but a single study or limited data.
- **Weak:** small or unclear samples, design problems, or preprints nobody has repeated.

## Main findings at a glance

> **In one sentence:** AI rebuilds of existing apps are still far from complete, they copy what the screen looks like better than what the app does, and almost nobody has checked whether the rebuilt code is as easy to maintain as the original.

### RQ1. What approaches exist?

> **Answer:** six families of approaches exist; the closest match to "AI reverse engineering" is AI agents that rebuild an app from a running original. Evidence strength: moderate.

- [V] The six families are: screenshot or design to code; interaction video or screenshots to code; agentic rebuilds from a running original; written specification to a full app; commercial vibe-coding platforms and AI code editors; and recovering behaviour rules from a running app [@si2025benchmarking, p. 4; @chen2025iwr, p. 5; @bai2026recreationworld, p. 3; @tran2026vibe, p. 3; @mota2026comparing, p. 2; @xiong2026propgen, p. 4].
- [V] Real-world vibe coding means a person describes goals in plain language, re-prompts when things go wrong, and reviews the code very little [@fawzy2026vibe, p. 1].
- [I] Almost every rebuild study tests autonomous agents, with no person steering. Human-steered vibe coding appears only in small or indirect studies [@mock2026vibe, p. 15; @asdaque2026novice, p. 1].
- [I] Papers use the words "vibe coding" for different things, so their results should not be added together.

### RQ2. Does the rebuild behave like the original?

> **Answer:** only partly, everywhere. Exact behavioural copies are very rare, and interaction logic is the weakest part. Evidence strength: moderate for this general picture, weak for any exact number.

- [V] Studies decide "correct" with four kinds of oracle (the reference that judges an output): behavioural tests run against the original, AI judges, visual similarity, and navigation maps [@bai2026recreationworld, p. 9; @tran2026vibe, p. 4; @si2025benchmarking, p. 3; @zhou2025declarui, p. 7].
- [V] A full behavioural match is rare: 2.8% of apps in one study and 0 of 200 programs in another. Both studies are preprints [@bai2026recreationworld, p. 11; @yang2026programbench, p. 6].
- [V] The best results at the level of whole workflows or requirements are about 49–62% [@kim2026programdistill, p. 11; @liu2026benchmarking, p. 6; @tran2026vibe, p. 6].
- [V] Rebuilds copy static structure more reliably than what happens after an action [@bai2026recreationworld, p. 16; @chen2025iwr, p. 16].
- [V] Caution: in chen2025iwr, the "visual beats interaction" gap is partly built into how the scores are calculated [@chen2025iwr, p. 7].
- [I] Each benchmark uses a different oracle, input and app type. Do not rank the percentages against each other.

### RQ3. Is the code good and maintainable?

> **Answer:** the evidence is mixed, and no study compares the maintainability of a rebuild with its original. Evidence strength: weak to moderate.

- [V] After teams adopted the Cursor AI editor, project-level SonarQube warnings rose by 30.26% and cognitive complexity by 41.64% [@he2026speed, p. 7]. But with another accepted statistical method both effects became negative and not significant [@he2026speed, p. 16].
- [V] A preregistered randomised experiment found no significant difference when a second developer extended code written with or without AI help [@borg2026echoes, p. 33; @borg2026echoes, p. 38]. It had fewer participants than planned, so it can rule out only large effects [@borg2026echoes, p. 19].
- [V] Rebuilds are smaller and more concentrated in a few files than their originals (two preprints) [@bai2026recreationworld, p. 15; @yang2026programbench, p. 9].
- [V] Quality differs by vibe-coding platform (preprint, 9 apps) [@mota2026comparing, p. 5], and AI code shows different kinds of code smells from human code [@zhu2026understanding, p. 7].
- [I] The code-checking tools (SonarQube, PyExamine, CodeHealth, Maintainability Index) give different pictures, so the answer may depend on the tool.

### RQ4. How trustworthy are the studies?

> **Answer:** there are good practices, but most benchmarks run each test only once, and maintainability is almost never measured properly. Evidence strength: strong for these two weaknesses, moderate for the others.

- [V] Strengths: tests that check behaviour without caring how the rebuild is built, controls against copying the original, checks of the test suites, checks of AI judges against humans, and one preregistered randomised trial [@yang2026programbench, p. 18; @liu2026benchmarking, p. 14; @tran2026vibe, p. 9; @borg2026echoes, p. 19].
- [V] Many benchmarks report a single run with no uncertainty and no significance tests [@lu2025webgen, p. 40; @yang2026programbench, p. 10]. In one study, differences between generation runs explained 73.5–92.5% of the variation in scores [@tran2026vibe, p. 8].
- [V] Some tests depend on the original's internal names, which were even given to the AI in the prompt [@liu2026benchmarking, p. 16].
- [V] No rebuild or generation benchmark compares AI with human developers [@yang2026programbench, p. 20; @tran2026vibe, p. 5].

### RQ5. What is still missing?

> **Answer:** the top gap (G1) is a study that measures, on the same AI rebuilds, both behavioural fidelity and maintainability, with the original app as the comparison. Our searches on 2026-11-12 found no such study. Evidence strength: moderate.

- [I] The evidence that this gap exists is strong [@bai2026recreationworld, p. 15; @yang2026programbench, p. 9; @pan2026functional, p. 3; @wu2026looks, p. 4; @tran2026vibe, p. 9].
- [I] Five more gaps are partly new, and two are mostly or partly addressed by 2026 work. A security version of the question is also partly new. All are explained in the gaps section at the end.

## Paper map

The papers are grouped by approach family, following the methodology comparison:

- **F1. Screenshot or design to code.** The AI sees pictures of an app and writes code that looks the same.
- **F2. Rebuild from observed behaviour.** The AI watches a video or uses a running original and rebuilds it. This is the closest match to "AI reverse engineering".
- **F3. Written specification to a full app.** The AI gets a text description or requirements and builds the whole app.
- **F4. Code-quality studies.** Studies that scan AI-written code with code-checking tools.
- **F5. Human-centred and workflow studies.** Experiments with developers, repository studies and literature reviews.
- **F6. Behaviour-rule recovery.** Learning rules about how an app behaves by running it.

Relevance (high, medium, low) is our rating of how close each paper is to the project question.

| # | Group | Paper (short title) | Year | Type | Status | What it is about | Relevance |
|---|---|---|---|---|---|---|---|
| 1 | F1 | Design2Code (si2025benchmarking) | 2025 | Benchmark | Peer-reviewed (NAACL 2025) | Real webpage screenshots turned into HTML, scored on visual similarity | high |
| 2 | F1 | Interaction2Code (xiao2025benchmarking) | 2025 | Benchmark + user study | Peer-reviewed (ASE 2025) | Rebuilding webpage interactions from before/after screenshots | high |
| 3 | F1 | DeclarUI (zhou2025declarui) | 2025 | Technique + user study | Peer-reviewed (Proc. ACM Softw. Eng.) | Mobile UI designs to React Native code with page-navigation maps | high |
| 4 | F1 | Looks Right, Works Right (wu2026looks) | 2026 | Benchmark | Peer-reviewed (EMNLP 2026) | Multi-screen mobile app screenshots to working app, with navigation tests | high |
| 5 | F2 | IWR-Bench (chen2025iwr) | 2025 | Benchmark | Preprint | Rebuilding interactive webpages from a video of someone using them | high |
| 6 | F2 | RecreationWorld (bai2026recreationworld) | 2026 | Benchmark | Preprint | AI agents rebuild apps on five platforms from a running original | high |
| 7 | F2 | ProgramDistill (kim2026programdistill) | 2026 | Benchmark | Preprint | AI agents rebuild web apps by exploring a live reference app | high |
| 8 | F2 | ProgramBench (yang2026programbench) | 2026 | Benchmark | Preprint | AI agents rebuild 200 programs from the program and its documentation | high |
| 9 | F3 | E2EDev (liu2026benchmarking) | 2026 | Benchmark | Peer-reviewed (ACL 2026) | Rebuilding existing web apps from their requirements, with executable tests | high |
| 10 | F3 | WebGen-Bench (lu2025webgen) | 2025 | Benchmark | Peer-reviewed (NeurIPS 2025) | Building websites from text instructions, judged by an AI tester | high |
| 11 | F3 | Vibe Code Bench (tran2026vibe) | 2026 | Benchmark | Peer-reviewed (CAIS 2026) | Full web apps from text specifications, judged by an AI browser agent | high |
| 12 | F3 | RAL-Bench (pan2026functional) | 2026 | Benchmark | Preprint | Python projects from requirements, scored on function and code quality | high |
| 13 | F3 | SusVibes (zhao2025vibe) | 2025 | Benchmark | Preprint (published at ICML 2026 per project notes) | Whether code written by AI agents is secure in real projects | medium |
| 14 | F4 | Is LLM Code More Maintainable? (molison2025llm) | 2025 | Comparative static analysis | Peer-reviewed (ESEM 2025) | GPT-4o versus human solutions, checked with SonarQube | medium |
| 15 | F4 | Quality of Vibe Coding Tools (mota2026comparing) | 2026 | Exploratory static analysis | Preprint | Code quality of apps from Lovable, v0 and Replit | high |
| 16 | F4 | Code and Architectural Smells (zhu2026understanding) | 2026 | Exploratory static analysis | Peer-reviewed (ASE 2026) | Code smells in LLM, agent and human code | high |
| 17 | F4 | Speed at the Cost of Quality (he2026speed) | 2026 | Quasi-experiment on repositories | Peer-reviewed (MSR 2026) | Effect of adopting the Cursor AI editor on speed and quality | high |
| 18 | F5 | Echoes of AI (borg2026echoes) | 2026 | Preregistered randomised trial | Peer-reviewed (Empirical Software Engineering) | Is AI-assisted code harder for the next developer to change? | high |
| 19 | F5 | Vibe Coding and TDD (mock2026vibe) | 2026 | Small experiment | Peer-reviewed (Empirical Software Engineering) | Solo, collaborative and agent vibe coding on small test-driven tasks | medium |
| 20 | F5 | Novice Developers and Review Overhead (asdaque2026novice) | 2026 | Repository mining | Peer-reviewed (MSR 2026) | AI-agent pull requests from novice versus experienced developers | low |
| 21 | F5 | Vibe Coding in Practice (fawzy2026vibe) | 2026 | Grey-literature review | Peer-reviewed (ICSE-SEIP 2026) | What practitioners write about vibe coding online | medium |
| 22 | F5 | Faster Code, Deeper Debt? (ehsani2026faster) | 2026 | Multivocal literature review | Peer-reviewed (TOSEM) | Technical debt caused by LLM-assisted development | high |
| 23 | F6 | PropGen (xiong2026propgen) | 2026 | Tool + evaluation | Peer-reviewed (ASE 2026) | Learning behaviour rules from running Android apps for testing | medium |

## Reading order: the five papers to read first

Start with these five. Together they cover the core of the topic and give you the tools for a first study.

1. **RecreationWorld (bai2026recreationworld, preprint).** The closest match to this project. AI agents rebuild apps on five platforms from a running original, with no source code. It reports a 2.8% full-pass rate [@bai2026recreationworld, p. 11] and measures how much smaller the rebuilds are than the originals [@bai2026recreationworld, p. 15].
2. **ProgramBench (yang2026programbench, preprint).** Rebuilds 200 programs from the program plus its documentation. Read it for careful test design, controls against copying, and a comparison of rebuilt code structure with the originals [@yang2026programbench, p. 6; @yang2026programbench, p. 9].
3. **Echoes of AI (borg2026echoes, peer-reviewed).** The only randomised test of maintainability in our set. Its "second developer extends the code" design is the model for the maintenance task in the top gap, G1 [@borg2026echoes, p. 13].
4. **E2EDev (liu2026benchmarking, peer-reviewed).** Rebuilds existing web apps from their requirements, with human-reviewed tests that pass on the originals [@liu2026benchmarking, p. 5]. It is a good source of apps and tests for a pilot study. Note its weakness: tests depend on the original's internal names [@liu2026benchmarking, p. 16].
5. **Vibe Code Bench (tran2026vibe, peer-reviewed).** The benchmark that uses the term "vibe coding" directly. It reports problems with AI judges [@tran2026vibe, p. 9] and large run-to-run variation [@tran2026vibe, p. 8], and it releases its generated apps for reuse [@tran2026vibe, p. 11].

## Where studies disagree

All explanations here are our interpretation [I]. We do not pick a side. Full entries are in the project's evidence matrix.

- **C1. Does AI assistance harm maintainability?** Warnings and complexity rose after Cursor adoption [@he2026speed, p. 7], but a randomised trial found no difference for the next developer [@borg2026echoes, p. 33]. [I] Different settings, units and statistical robustness; neither settles it.
- **C2. Fewer or more code problems in AI code?** GPT-4o code had fewer SonarQube "bugs" than human solutions [@molison2025llm, p. 8], yet repository warnings rose with Cursor [@he2026speed, p. 7]. [I] Single programs versus whole projects, with different baselines: not comparable.
- **C3. Which code-quality tool can we trust?** One study chose PyExamine over SonarQube's "superficial linting" [@zhu2026understanding, p. 2], and a review notes that technical-debt tools disagree [@ehsani2026faster, p. 5]. [I] The answer may depend on the tool.
- **C4. Does letting the AI test and fix its own work help?** Repair strategies lowered code quality without improving correctness in one single-model preprint [@pan2026functional, p. 8], while targeted repair loops helped elsewhere [@zhou2025declarui, p. 10; @wu2026looks, p. 12]. [I] Feedback seems to improve only what it checks.
- **C5. Do rebuilds "look right but behave wrong"?** Behaviour scored below appearance in some benchmarks [@chen2025iwr, p. 8], but the visual score was lower for 9 of 10 models in another [@bai2026recreationworld, p. 11]. [I] Only "structure is easier than interaction" holds up.
- **C6. Do multi-agent frameworks help?** MetaGPT nearly always failed in E2EDev [@liu2026benchmarking, p. 6] but scored highest in a small experiment [@mock2026vibe, p. 41]. [I] Task size and model generation differ.
- **C7. Is generated code secure?** One preprint gave a high static security score [@pan2026functional, p. 6]; another found that most working solutions failed security tests [@zhao2025vibe, p. 6]. [I] They measure different things; less code means fewer static findings.
- **C8. More code or less code?** Rebuilds are much smaller than originals [@bai2026recreationworld, p. 15], but AI-assisted development adds code [@he2026speed, p. 8]. [I] Size means different things here; divide quality counts by code size.
- **C9. Same words, different things.** "Vibe coding" is defined differently across papers [@fawzy2026vibe, p. 1; @asdaque2026novice, p. 1], and fidelity scores use different oracles. [I] Do not pool these results.
- **C10. The AI family that builds the test sometimes wins it.** This happened in several benchmarks [@yang2026programbench, p. 3; @tran2026vibe, p. 3] but not in others [@bai2026recreationworld, p. 11]. [I] No paper tests this bias directly; it is a warning sign, not proof.
