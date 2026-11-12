# Research report: AI-assisted reverse engineering of applications through vibe coding

- Project: `2026-11-11-ai-reverse-engineering-vibe-coding`
- Full title: *Evaluating AI-Assisted Reverse Engineering for Software Application Reconstruction through Vibe Coding: Functional Fidelity, Code Quality, and Maintainability*
- Date: 2026-11-12
- Written for: the project owner, a beginner researcher
- Based on: 23 full-text paper analyses (`papers/*/analysis.md`), `evidence-matrix.md` (204 rows, contradictions C1–C10), `reports/methodology-comparison.md`, `gap-report.md` (gaps G1–G8), `reports/novelty-check-security-fidelity.md`, `RESEARCH-QUESTIONS.md`, `search/search-log.md` and `rlab status`.

**How to read this report.**
- Citations look like `[@borg2026echoes, p. 13]`: the paper's key (its folder name in `papers/`) and the page of the PDF we hold.
- Each important claim has a label:
  - **[V]** (verified): we checked it in the paper's own data, tables or results.
  - **[A]** (author claim): the authors say it, but we could not check it ourselves.
  - **[I]** (interpretation): our own reasoning, built from the cited papers.
- A *preprint* is a paper that has not yet passed peer review (checking by independent experts before publication). Seven of our 23 papers are preprints. We name them as such and give them less weight.
- Research terms are explained the first time they appear. All of them are also in the glossary (§9).

---

## 1. Summary in plain language

We asked a simple question. If you use an AI model to rebuild an existing app only from what you can see (its screens, its behaviour, its documentation), how good is the result? "Good" has three parts here. Does the rebuilt app behave like the original (*functional fidelity*)? Is its code well written (*code quality*)? Can people change it easily later (*maintainability*)?

We read 23 recent papers in full. The main answer is that AI rebuilds are still far from complete. In the closest studies, an exact behavioural copy of the original was very rare: 2.8% of apps in one study and 0 of 200 programs in another [@bai2026recreationworld, p. 11; @yang2026programbench, p. 6]. Both of these studies are preprints. Rebuilt apps usually copy what the screen looks like better than what happens when you click or type.

Code quality and maintainability are much less studied. Studies of AI-written code in general give mixed results, and they often use different measuring tools that do not agree. Almost no study of rebuilt apps measures maintainability properly. No study we found compares the rebuild's maintainability with the original app's.

That missing comparison is the main research gap (G1). It is also a realistic first study for you. A related security question can be added to the same study: does the rebuild keep the original's security protections?

---

## 2. What we did

**Scope.** "Reverse engineering" here means rebuilding an app from its behaviour, user interface (UI) or documentation. It does *not* mean reading its source code or its compiled program files (*binaries*). We searched for work from 2020 to 2026. Preprints were allowed but flagged. You chose these settings on 2026-11-11.

**Sources.**
- OpenAlex, Crossref and arXiv (three large academic databases), searched through `rlab`.
- Web searches for very recent work.
- *Snowballing* through OpenAlex. Snowballing means following the reference lists and citations of central papers to find more papers.

**Searches and screening (2026-11-11).**
- 33 searches are logged in `search/search-log.md`. Together they returned 1,208 raw hits (1,074 unique within each search; duplicates across searches were not counted).
- Most of these searches were run by five search helpers, one per theme: vibe coding, UI-to-code, whole-app generation, code quality, and black-box reverse engineering. They also used snowballing and web searches (`research-log.md`).
- *Screening* means checking each candidate against the inclusion rules. We included 23 papers, kept 22 as reserves, and excluded the rest with reasons (`search/screening.md`). Exclusions included one retracted paper, suspected *predatory* venues (publishers that take money without real review), vendor blogs, and studies that only measured opinions.

**Searches for the gap analysis (2026-11-12).**
- 38 more targeted searches are logged on 2026-11-12, plus 9 web searches. They were used to check whether each possible gap was already filled (`gap-report.md`).
- A separate check for the security topic used about 20 direct OpenAlex queries, arXiv and Crossref queries, and 3 web searches. One Semantic Scholar query was rate-limited and gave no results (`reports/novelty-check-security-fidelity.md` §4).

**Papers and reading depth** (from `rlab status`):

| Item | Count |
|---|---|
| Papers included | 23 |
| Full text available and read | 23 |
| Abstract-only | 0 |
| Published (peer-reviewed venue) | 16 |
| Preprints | 7: bai2026recreationworld, chen2025iwr, kim2026programdistill, mota2026comparing, pan2026functional, yang2026programbench, zhao2025vibe |
| Retracted papers in the evidence | 0 |
| Analyses completed and critically reviewed | 23 |

Note on zhao2025vibe: our database record calls it a preprint. The project notes say it was published at ICML 2026, without a DOI. We still count it as a preprint here, which is the more cautious choice.

**Analysis steps.**
1. Each paper was analysed from its full text. A second reviewer checked every analysis against the paper (three review batches).
2. All findings were collected in an *evidence matrix*: a table of 204 findings, each with its source, label and strength.
3. The study methods were compared side by side (`reports/methodology-comparison.md`).
4. Eight possible research gaps were tested with a *novelty check*. A novelty check is a set of targeted searches that asks: "has someone already done this?"

---

## 3. Answers to the research questions

**Evidence strength** describes how much we trust an answer:
- **strong**: enough data, sound design, and several studies agree;
- **moderate**: sound design but a single study or few data;
- **weak**: small or unclear samples, design problems, or preprints that nobody has repeated.

### RQ1. What AI approaches exist for rebuilding apps from observable artefacts, and how do they relate to vibe coding?

**Answer.** We found six families of approaches [V]:
1. **Screenshot or design to code.** The AI sees a picture of a page or app and writes code that looks the same [@si2025benchmarking, p. 4; @zhou2025declarui, p. 3; @wu2026looks, p. 6].
2. **Interaction to code.** The AI sees a video of someone using a web page, or before/after screenshots of an interaction, and rebuilds the page [@chen2025iwr, p. 5; @xiao2025benchmarking, p. 2]. chen2025iwr is a preprint.
3. **Agentic rebuilds from a running original.** An *AI agent* (an AI that can act on its own: click, run commands, write files) explores a live app or a runnable program and rebuilds it without its source code [@bai2026recreationworld, p. 3; @kim2026programdistill, p. 3; @yang2026programbench, p. 2]. All three are preprints. This family is the closest match to "AI-assisted reverse engineering".
4. **Written specification to a full app.** The AI gets a text description or a list of requirements and builds the whole app [@liu2026benchmarking, p. 3; @lu2025webgen, p. 7; @tran2026vibe, p. 3; @pan2026functional, p. 2]. pan2026functional is a preprint.
5. **Commercial vibe-coding platforms and AI code editors**, such as Lovable, v0, Replit and Cursor [@mota2026comparing, p. 2; @he2026speed, p. 4]. mota2026comparing is a preprint.
6. **Recovering behaviour rules from a running app.** One tool learned rules about how an Android app behaves just by running it [@xiong2026propgen, p. 4].

**How this relates to vibe coding** [I]. Real-world vibe coding means a person describes goals in natural language, re-prompts when things go wrong, and reviews the code very little [@fawzy2026vibe, p. 1]. Almost all rebuild studies instead test *autonomous* agents with no person steering them. Human-steered vibe coding has been studied only in small or indirect studies [@mock2026vibe, p. 15; @asdaque2026novice, p. 1]. Also, different papers use the words "vibe coding" for different things (see §5, C9). Their results should not be added together.

**Evidence strength: moderate.** The picture is consistent, but 7 of 23 papers are preprints and the field changes every month.

**What would change this answer.** New benchmarks of human-steered rebuilding. Also, several recent papers we found but have not yet analysed (§8, step 1).

### RQ2. How is functional fidelity measured, and how well do current approaches achieve it?

**How it is measured.** Every study needs an *oracle*: the reference that decides whether an output is correct, such as a test suite or a judge. We found four kinds [V]:
1. **Behavioural tests run against the original.** The same tests that pass on the original app are run on the rebuild [@bai2026recreationworld, p. 9; @kim2026programdistill, p. 4; @yang2026programbench, p. 5; @liu2026benchmarking, p. 5].
2. **LLM or agent judges.** An AI model reads natural-language test steps, uses the rebuilt app and decides pass or fail [@lu2025webgen, p. 6; @tran2026vibe, p. 4; @chen2025iwr, p. 7]. An *LLM* (large language model) is the kind of AI behind tools like ChatGPT and Claude.
3. **Visual similarity.** Screenshots of the rebuild are compared with the original [@si2025benchmarking, p. 3; @wu2026looks, p. 4].
4. **Navigation graphs.** A map of which screen leads to which screen is compared with the original's map [@zhou2025declarui, p. 7].

**How well it is achieved.** Fidelity is partial everywhere.
- [V] Full behavioural equivalence is rare: 2.8% of apps for the best model in one study [@bai2026recreationworld, p. 11] and 0 of 200 programs in another [@yang2026programbench, p. 6]. Both are preprints.
- [V] The best results at the level of whole workflows or requirements are about 49–62% [@kim2026programdistill, p. 11; @liu2026benchmarking, p. 6; @tran2026vibe, p. 6].
- [V] Some benchmarks report lower figures: an interaction score below 25 for all 28 models tested (preprint) [@chen2025iwr, p. 8], under 45% of tests passed (preprint) [@pan2026functional, p. 5], and 27.8% accuracy [@lu2025webgen, p. 8].
- [V] The more parts of the app depend on each other, and the larger the app, the lower the fidelity [@kim2026programdistill, p. 8; @yang2026programbench, p. 31; @tran2026vibe, p. 6].
- [V] Interaction logic lags behind static structure. Rebuilds copy what is on the screen more reliably than what happens after an action [@bai2026recreationworld, p. 16; @chen2025iwr, p. 16; @xiao2025benchmarking, p. 6]. In bai2026recreationworld, this structure-versus-action analysis covers only 4 of its 10 models. In one case a rebuild scored 100% visually but only 55.1% on behaviour tests [@bai2026recreationworld, p. 18].
- **Caution about one well-known finding** [V]. In chen2025iwr, the "visual score is higher than the interaction score" result is partly built into the metrics themselves. The visual score is averaged only over the checkpoints the agent reached, while the interaction score counts all actions [@chen2025iwr, p. 7]. So that gap is not a fair like-for-like comparison.

[I] Each benchmark uses a different oracle, input and app type. The percentages above therefore **cannot be ranked against each other**.

**Evidence strength.** **Moderate** for "fidelity is far from complete, and interaction is the weakest part". **Weak** for any exact number or any ranking across benchmarks. Most results come from a single run, and 5 of the 8 main fidelity benchmarks are preprints.

**What would change this answer.** Repeated runs with uncertainty reported. Rebuild benchmarks that are peer-reviewed. Tests that do not depend on the original's internal names (see RQ4).

### RQ3. What is known about the code quality and maintainability of AI-generated or vibe-coded app code, compared with human code?

**Answer: the evidence is mixed.**
- [V] **Real projects using Cursor (an AI code editor).** After teams adopted Cursor, project-level warnings from *SonarQube* (a widely used code-checking tool) rose by 30.26%, and *cognitive complexity* (a score for how hard code is to follow) rose by 41.64% [@he2026speed, p. 7]. But this result depends on the statistical method used. With another accepted method (Callaway–Sant'Anna), both effects became negative and not significant [@he2026speed, p. 16]. The rise in warnings also comes mainly from projects simply having more code [@he2026speed, p. 8]. We count this result **once**, from he2026speed itself. A review paper (ehsani2026faster) repeats the same numbers, so it is not independent evidence.
- [V] **A randomised experiment on maintainability.** A *randomised controlled trial* (RCT) assigns participants to groups by chance, which makes fair comparison possible. This one was also *preregistered* (its plan was published before the data were collected). A second developer had to extend code that someone else had written with or without AI help. There was no significant difference in completion time (median 136 vs 173 minutes, p = 0.56) [@borg2026echoes, p. 33] or in code health (8.49 vs 8.44) [@borg2026echoes, p. 38]. However, the study had only 75 of the 128 planned participants, so it can rule out only large effects [@borg2026echoes, p. 19].
- [V] **Single programs.** GPT-4o code had fewer SonarQube "bugs" than human solutions from a competitive-programming dataset [@molison2025llm, p. 8]. Those human solutions were written to be correct, not to be maintainable, so they are a weak baseline. The results for *code smells* (patterns that suggest code will be hard to maintain) were mixed [@molison2025llm, p. 8].
- [V] **Different kinds of problems.** LLM code showed different smell types from human code. For example, larger LLMs produced more "Long Method" smells [@zhu2026understanding, p. 7]. In AI-generated multi-file apps, smell counts closely followed code size (ρ = 0.94) [@zhu2026understanding, p. 8].
- [V] **Platform matters** (preprint, 9 apps only). Apps from Lovable had about 22.83 SonarQube issues per thousand lines, compared with about 9 for v0 and Replit [@mota2026comparing, p. 5].
- [V] **Rebuilds are smaller and more concentrated than the originals** (two preprints).
  - In bai2026recreationworld, 89.4% of rebuilds had less code than the original (median size 16.9% of the original) [@bai2026recreationworld, p. 15]. This covers only 4 of the 10 models, and only desktop and Android apps.
  - In yang2026programbench, rebuilds that passed at least 75% of tests had a median of 1,173 lines and 3 files, against 3,068 lines and 15 files in the originals [@yang2026programbench, p. 9].
  - [I] We cannot yet tell whether "smaller" means "simpler and cleaner" or "missing features".
- [V] **Perception.** Practitioners mostly describe vibe-coded output as "fast but flawed" (68% of coded statements) [@fawzy2026vibe, p. 8]. This is opinion, not code measurement.

[I] The measuring tools disagree with each other: SonarQube, PyExamine, CodeHealth and the Maintainability Index give different pictures (see §5, C3). And no study measures validated maintainability of *rebuilt* apps against their originals.

**Evidence strength: weak to moderate.** The results conflict (C1–C3), and the instruments are not validated for AI code.

**What would change this answer.** A study that applies more than one size-adjusted instrument plus a real maintenance task to rebuilds *and* to their originals (gap G1). Also a study that tests whether the instruments agree with each other (gap G3).

### RQ4. What are the methodological strengths and weaknesses of current evaluations?

**Strengths** [V]:
- Behavioural tests that do not care how the rebuild is built, with controls against copying the original [@yang2026programbench, p. 18; @bai2026recreationworld, p. 9].
- Checks of the test suites themselves [@yang2026programbench, p. 7; @liu2026benchmarking, p. 14].
- Checks of whether AI judges agree with humans [@tran2026vibe, p. 9; @wu2026looks, p. 13].
- One preregistered RCT [@borg2026echoes, p. 19].

**Recurring weaknesses:**
1. **Single runs, with no measure of uncertainty and no significance tests** [V] [@lu2025webgen, p. 40; @yang2026programbench, p. 10]. This matters because AI output changes a lot from run to run. In one study, differences between generation runs explained 73.5–92.5% of the variation in scores [@tran2026vibe, p. 8].
2. **Judges and tests made by the same AI family that is being evaluated, or judges that are poorly validated** [V]. Agreement between AI judges and humans ranged from 36.1% to 86.4%, depending on which model was the judge [@tran2026vibe, p. 9]. Some judges were tuned and tested on the same data [@chen2025iwr, p. 17; @si2025benchmarking, p. 17].
3. **Uneven handling of *contamination*** [V]. Contamination means the AI may have seen the original app's code during training. With internet access, 20–36% of the stronger models' tasks were flagged as cheating, mostly by looking up the original source code [@yang2026programbench, p. 6].
4. **Maintainability is missing or measured only through rough proxies** [V] [@pan2026functional, p. 3; @wu2026looks, p. 4].
5. **Tests tied to the original's internal names** [V]. For example, some tests look for hidden identifiers (`data-testid` labels) taken from the original's code, and those names were given to the AI in the prompt [@liu2026benchmarking, p. 16]. Others use the original's selectors [@kim2026programdistill, p. 35] or give the AI a structural map as input [@zhou2025declarui, p. 7].
6. **No human-developer baseline** in any rebuild or generation benchmark [V] [@yang2026programbench, p. 20; @tran2026vibe, p. 5; @lu2025webgen, p. 7].

**Evidence strength.** **Strong** for weaknesses 1 and 4: we verified them across 12 or more papers. **Moderate** for the judge, contamination and test-coupling problems.

**What would change this answer.** New benchmarks that report repeated runs, judges from different AI families, and validated maintainability measures.

### RQ5. Which gaps remain, and what study could address them?

**Answer** [I]. The main gap that survived the novelty check is **G1**. We found no study that rebuilds existing apps from observable artefacts and then measures, on the same rebuilds, both:
- (a) behavioural fidelity against the original, and
- (b) maintainability, using more than one size-adjusted instrument plus a maintenance task, with the original app as the baseline (searches on 2026-11-12).

Measuring each part on its own is not new. Five more gaps are partly new; two are mostly or partly addressed (§6). A security version of the question is also partly new (§6).

**Evidence strength: moderate.** The evidence that the gap exists is strong [@bai2026recreationworld, p. 15; @yang2026programbench, p. 9; @pan2026functional, p. 3; @wu2026looks, p. 4; @tran2026vibe, p. 9]. Our confidence in its novelty is medium-high. The field publishes every month, so the check must be repeated before you submit anything.

**What would change this answer.** A new paper that combines fidelity and maintainability against originals. Several close 2026 papers exist (MirrorCode, UI2App, VISTA, WebCoderBench). We read only their abstracts, so they must be analysed before we can be sure (§8).

---

## 4. Key papers to read first

Start with these five. They give you the core of the topic and the tools for a first study.

1. **bai2026recreationworld** (RecreationWorld; preprint). The closest match to the project. AI agents rebuild apps on five platforms from a running original, with no source code. It reports a 2.8% full-pass rate [@bai2026recreationworld, p. 11] and also measures how much smaller the rebuilds are than the originals [@bai2026recreationworld, p. 15].
2. **yang2026programbench** (ProgramBench; preprint). Rebuilds 200 programs from the program plus its documentation. It shows careful test design and contamination controls, and compares rebuilt code structure with the originals [@yang2026programbench, p. 6; @yang2026programbench, p. 9].
3. **borg2026echoes** (Echoes of AI; peer-reviewed, Empirical Software Engineering). The only randomised test of maintainability. Its "second developer extends the code" design is the model for the maintenance task in G1 [@borg2026echoes, p. 13].
4. **liu2026benchmarking** (E2EDev; peer-reviewed, ACL 2026). It rebuilds existing web apps from their requirements and comes with human-reviewed tests that pass 100% on the originals [@liu2026benchmarking, p. 5]. It is a good source of apps and tests for a pilot study, and it ran every setting 3 times. Note its test-coupling problem [@liu2026benchmarking, p. 16].
5. **tran2026vibe** (Vibe Code Bench; peer-reviewed, CAIS 2026). The benchmark that uses the term "vibe coding" directly. It reports judge problems [@tran2026vibe, p. 9] and run-to-run variation [@tran2026vibe, p. 8], and it releases its generated apps [@tran2026vibe, p. 11]. These apps can be reused for the easy follow-up studies G2 and G3.

---

## 5. Where studies disagree

Full entries are in `evidence-matrix.md` → "Contradictions". All explanations below are our interpretation [I]. We do not pick a side.

- **C1. Does AI assistance harm maintainability?** Project-level warnings and complexity rose after Cursor adoption [@he2026speed, p. 7]. But a randomised experiment found no difference when a second developer extended AI-assisted code [@borg2026echoes, p. 33; @borg2026echoes, p. 38].
  - Why they may differ: real open-source projects over many months versus one small Java task; whole-project totals (which grow with code size) versus per-file scores; and a result that changes with the statistical method [@he2026speed, p. 16] versus an underpowered experiment [@borg2026echoes, p. 19].
  - [I] Both fit the idea "AI adds more code, so totals rise, but per-file quality and the next developer's effort are not clearly worse". Neither study settles the question.
- **C2 and C3. Which code-quality tool should we trust?** LLM code had fewer SonarQube bugs than human code in one study [@molison2025llm, p. 8], but repository warnings rose in another [@he2026speed, p. 7]. Another study chose a different tool (PyExamine) because it considered SonarQube "superficial linting" [@zhu2026understanding, p. 2]. A large review notes that technical-debt tools disagree about what debt is [A] [@ehsani2026faster, p. 5].
  - Why: different units (single programs versus whole projects per month), baselines and tools.
  - [I] The answer to "is AI code better or worse?" may depend on which tool you use.
- **C4. Does feedback (letting the AI test and fix its own work) help?** In one preprint, three repair strategies lowered non-functional quality without improving correctness, but only one model was tested [@pan2026functional, p. 8]. Elsewhere, self-testing went together with better results [@tran2026vibe, p. 7], and targeted repair loops improved compiling and navigation [@zhou2025declarui, p. 10; @wu2026looks, p. 12].
  - [I] Feedback seems to improve whatever it checks. No study shows that it improves both fidelity and code quality together.
- **C5. Do rebuilds "look right but behave wrong"?** Several benchmarks found behaviour scores below visual scores [@chen2025iwr, p. 8; @lu2025webgen, p. 9]. But in bai2026recreationworld, the visual channel scored *lower* than the behaviour tests for 9 of 10 models [@bai2026recreationworld, p. 11]. And chen2025iwr's gap is partly built into its metrics [@chen2025iwr, p. 7].
  - [I] The studies agree only on one point: static structure is copied more easily than interaction logic. The broader claim "visual always beats functional" is not supported.
- **C6. Do multi-agent frameworks help?** In E2EDev, multi-agent frameworks "do not consistently improve" over a plain LLM (the authors' words), and MetaGPT nearly always failed [@liu2026benchmarking, p. 6]. In a small experiment, an agentic MetaGPT product scored highest [@mock2026vibe, p. 41].
  - Why: that experiment used a tiny task and newer models [@mock2026vibe, p. 17].
- **C7. Is generated code secure?** One preprint gave a high static security score (87.40% on average) [@pan2026functional, p. 6]. Another preprint found that 79.3% of the best setting's working solutions failed security tests [@zhao2025vibe, p. 6].
  - [I] The two measure different things. The first counts flagged code patterns compared with the original, and it can reward incomplete code: less code means fewer findings. The second runs targeted attack-style tests.
- **C8. More code or less code?** Rebuilds are much smaller than their originals [@bai2026recreationworld, p. 15; @yang2026programbench, p. 9]. But AI-assisted development adds code to existing projects [@he2026speed, p. 8; @borg2026echoes, p. 30].
  - [I] Size means different things in the two settings. Quality counts must be divided by code size before comparing.
- **C9. Same words, different things.** "Vibe coding" means different things in different papers [@fawzy2026vibe, p. 1; @asdaque2026novice, p. 1; @mock2026vibe, p. 15; @he2026speed, p. 4]. Fidelity percentages use different oracles. Do not pool these results.
- **C10. The same AI family builds the test and wins it.**
  - In some benchmarks, the AI family that wrote the tests or tasks also topped the results [@yang2026programbench, p. 3; @tran2026vibe, p. 3; @kim2026programdistill, p. 2; @zhao2025vibe, p. 17].
  - In others it did not. For example, the Qwen3.7-Plus model used as the visual judge in bai2026recreationworld was the lowest-scoring of the 10 models (average 9.15) [@bai2026recreationworld, p. 11].
  - [I] No paper tests this possible bias directly. It is a warning sign, not proven bias.

A related weak point: zhao2025vibe reports that the functionally weakest model had the highest secure ratio on tasks that all models solved [@zhao2025vibe, p. 6]. But the size of that shared task set is not reported. Treat this "most secure model" finding as **weak**.

---

## 6. Research gaps and possible contributions

A *research gap* is a question that the evidence shows is open and that a novelty check could not find already answered. Our checks used OpenAlex, Crossref, arXiv and web searches on 2026-11-12. "We found no study" means only that these searches found none. It does not mean that no such study exists.

| Gap | In short | Novelty | Confidence | Beginner feasibility |
|---|---|---|---|---|
| **G1** | Behavioural fidelity **and** validated maintainability of rebuilt apps, both measured against the originals | novel (narrow claim) | medium-high | moderate |
| G2 | Bias when the same AI family builds, tests and judges a benchmark | partially novel | medium | easy |
| G3 | Do maintainability tools agree, and do they predict real maintenance effort, for AI-built apps? | partially novel (narrowed) | medium | easy–moderate |
| G4 | Does feedback improve fidelity and code quality together in rebuilding? | partially novel | medium | moderate |
| G5 | How much does contamination inflate rebuild scores? | partially novel | medium-low | moderate |
| G6 | Human-steered vibe coding versus autonomous agents for rebuilding | partially novel | medium | moderate–hard |
| G7 | Bias from tests tied to the original's internal names | mostly addressed | low-medium | easy |
| G8 | Native mobile apps with hidden server behaviour | partially addressed | low | hard |

### G1 (top gap): joint fidelity and maintainability, against the original

**Why it is a gap.**
- [V] Rebuild benchmarks with behavioural tests measure the code only by size and structure [@bai2026recreationworld, p. 15; @yang2026programbench, p. 9], or not at all [@kim2026programdistill, p. 14].
- [V] UI benchmarks use rough proxies [@wu2026looks, p. 4] or ratings from 5 developers [@zhou2025declarui, p. 10].
- [V] The only maintainability score measured relative to an original is a single Maintainability Index in a preprint that rebuilds from requirements, not from observed behaviour [@pan2026functional, p. 3].
- [V] Wherever both are measured, functional correctness and other quality dimensions diverge [@molison2025llm, p. 8; @zhao2025vibe, p. 6; @wu2026looks, p. 7]. So passing tests says little about maintainability.
- [A] The Vibe Code Bench authors state that passing functional tests does not mean the code is maintainable, secure or documented [@tran2026vibe, p. 9].

**Suggested study** [I] (full design in `gap-report.md`).
- Apps: 8–10 small web apps. About 5 come from the E2EDev set, which has validated tests [@liu2026benchmarking, p. 9]. The others are apps released after the AI models' training cutoff, or apps you write yourself.
- Input to the AI: the running original and screenshots only. No source code and no hidden identifiers.
- Builders: 2–3 AI tools, each run 3 times per app (about 60–90 rebuilds).
- Fidelity: browser tests written against the original. They find elements by role and visible text, not by internal names, and each test must pass 100% on the original first.
- Maintainability, measured on the rebuild **and** the original, reported as a ratio:
  - SonarQube issues per thousand lines and cognitive complexity per function;
  - code duplication, plus a second tool;
  - a standard change task (two small feature changes) carried out by a fixed "maintainer" agent, in the spirit of borg2026echoes [@borg2026echoes, p. 13].
- Analysis: preregistered hypotheses, *mixed-effects models* (statistical models that account for repeated measures on the same app), confidence intervals, and all counts divided by code size.

**Contribution** [I]. The first profile of AI rebuilds that answers: "does the rebuild that behaves like the original also stay as easy to change as the original?" It would also show whether smaller rebuilds are simpler or just incomplete (C8).

**Feasibility: moderate.** The tools are free or have free tiers. The main work is writing the tests and managing 60–90 rebuilds. You will need some help with the statistics.

### G2 and G3: two easy studies that need no new app generation

- **G2** [I]. Re-judge the released Vibe Code Bench apps [@tran2026vibe, p. 11] with judges from three AI families, plus about 300 human-labelled steps. Then check whether judges favour apps built by their own family. Related methods exist outside app generation, so the gap is only partly new.
- **G3** [I]. Run several maintainability tools on about 60 released AI-built apps. Check whether the tools agree, and whether they predict how well a maintainer agent can make changes. A 2026 peer-reviewed paper (CodeThread, EMNLP 2026, not yet analysed) partly covers this for code changes at the level of single issues, so we narrowed the gap to whole applications.

### The cybersecurity follow-up you chose: security-control preservation

**Question** [I]. When an AI agent rebuilds a web app only from what it can observe, are the original's security protections kept, dropped, or replaced with new weaknesses? Examples of protections: login checks; rules about who may see or edit which data; protection against cross-site attacks; safe password storage.

**Verdict: partially novel, with a defensible new core** (confidence moderate; `reports/novelty-check-security-fidelity.md`).
- Already done: measuring the *absolute* security of AI-generated apps built from specifications. Also, one study (Rajput et al. 2026, peer-reviewed symposium paper, abstract plus HTML sections read) scanned AI rebuilds of command-line programs with static tools. It did not compare them with the originals [A].
- Done in a neighbouring setting: whether code *translation* keeps security (Chang et al. 2026, IEEE TIFS) [A]. There, the AI sees the original source code.
- New core [I]: a **differential** test. The same security tests run on the original and on the rebuild of multi-user web apps that were rebuilt from behaviour only.

**Why it matters, from our papers.**
- [V] Rebuilds are much smaller than their originals [@bai2026recreationworld, p. 15]. [I] Missing code may include security checks.
- [V] Working code is often insecure: 79.3% of the best setting's correct solutions failed security tests (preprint) [@zhao2025vibe, p. 6].
- [V] Vibe Code Bench does not measure security [@tran2026vibe, p. 9]. 14.8% of its failures were cases where the agent wrongly blocked allowed actions, often through misconfigured access rules [@tran2026vibe, p. 8]. [I] So rebuilt access control can fail in both directions: too open or too strict.
- [V] Static security scores can reward incomplete code. In one preprint, a model got a 97.37 security score with only 29.76 functional score [@pan2026functional, p. 6].

**Core hypothesis** [I]. AI agents keep the security controls you can *see* (such as a login form) and drop the ones you *cannot see* (such as server-side permission checks). We call this the "security-observability gap".

**Feasibility: moderate.** It needs Docker, Playwright, basic web-security knowledge (the OWASP Top 10) and about 1–2 days per app to build the security tests. It also needs an ethics section, because better app cloning could help attackers (for example, to make phishing copies of real sites). Use only open-source apps that you are allowed to modify, run everything locally, and never target live third-party sites.

**How it fits with G1** [I]. The security test suite can be added to the G1 study as an extra outcome: fidelity, maintainability **and** security preservation, all measured against the same originals.

---

## 7. Limitations of this review

- **Size of the review.** It rests on 23 papers. That is enough to map the field, but not a complete *systematic review* (a study that tries to collect every study on a question with a fixed protocol).
- **Reading depth.** All 23 papers were read in full. None is abstract-only.
- **Preprints.** 7 of 23 papers are preprints and are not peer-reviewed. All four papers that rebuild apps from observed behaviour (bai2026recreationworld, chen2025iwr, kim2026programdistill, yang2026programbench) are preprints, and this is the group closest to our topic. Conclusions about that family are therefore less certain.
- **Search date.** Searches ran on 2026-11-11 (discovery) and 2026-11-12 (gap and novelty checks). Papers that appeared after that are not covered. This field changes monthly.
- **Sources not searched.** Semantic Scholar and Google Scholar were not queried in the novelty checks. One Semantic Scholar query in the security check was rate-limited and returned nothing. Web search results were indexed in the US only. Every "we found no study" statement is limited to the sources we used.
- **Versions of papers.** For 11 of the 16 published papers, the PDF we analysed is the arXiv version, not the publisher's final version: asdaque2026novice, ehsani2026faster, fawzy2026vibe, he2026speed, lu2025webgen, molison2025llm, tran2026vibe, xiao2025benchmarking, xiong2026propgen, zhou2025declarui and zhu2026understanding. Page numbers refer to our PDFs. The final versions may differ slightly. For zhou2025declarui, one table in the arXiv version looked suspicious (impossible percentages for 13 apps) [@zhou2025declarui, p. 9], and the published version has not been checked.
- **Metadata issues** (not affecting findings). Two papers show a title mismatch only because the preprint title differs from the published title. zhao2025vibe is recorded as a preprint although it was published at ICML 2026.
- **Papers found but not yet analysed.** The gap and novelty checks found about 19 relevant 2025–2026 papers that are **not** included or analysed. Seven more are relevant only to the security topic. They are listed in §8. Statements about them in this report come from their abstracts only and are labelled [A]. Some of them (for example MirrorCode, UI2App, VISTA and CodeThread) are close to G1 and could change its novelty verdict once read in full.
- **Our judgement in the synthesis.** Evidence-strength ratings and gap scores (evidence × novelty × feasibility) are our own ratings [I]. Another team might rate some of them differently.
- **Mostly web, Python and command-line apps.** Only one paper covers native desktop and Android rebuilding [@bai2026recreationworld, p. 7]. Our conclusions may not hold for mobile apps.

---

## 8. Recommended next steps

### Step 1: decide whether to add the recommended papers

Adding them is a scope change, so it is your decision. Our advice [I]: add at least the five high-priority papers before you finalise a study design, because they are the closest prior work to G1.

**From the gap report (19 papers; not analysed yet):**

| Priority | Paper | Identifier | Why |
|---|---|---|---|
| high | Is Agent Code Less Maintainable Than Human Code? (CodeThread) | DOI 10.18653/2026.emnlp-main.2528; arXiv 2606.21804 | Measures maintainability through follow-up tasks; template for G1's maintenance task; narrows G3 |
| high | VISTA | arXiv 2605.26144 | Design to full-stack web and Android apps with behaviour probes (G1, G7, G8) |
| high | UI2App | arXiv 2607.06306 | Screenshot-only multi-page web apps (G1, G7) |
| high | MirrorCode | arXiv 2606.30182 | Rebuilding programs from behaviour alone (G1) |
| high | Why Human Guidance Matters in Collaborative Vibe Coding | arXiv 2602.10473 | Human-led versus AI-led vibe coding, 737 participants (G6) |
| medium | ConformWeb (Do LLM-Generated Web Apps Behave Correctly?) | DOI 10.18653/2026.emnlp-main.2018 | Black-box behavioural tests without a reference app (G7) |
| medium | WebCoderBench | DOI 10.18653/v1/2026.acl-long.535; arXiv 2601.02430 | Web-app metrics including simple maintainability proxies (G1, G3) |
| medium | From Runnable Code to Shippable Applications (TDDev) | DOI 10.1145/3832783.3834388; arXiv 2605.17242 | Test-driven feedback loops for full-stack apps (G4) |
| medium | Silencer: Self-Bias in LLM-as-Benchmark-Generator | DOI 10.52202/085713-4317; arXiv 2505.20738 | Method for measuring generator self-bias (G2) |
| medium | Preference Leakage | arXiv 2502.01534 | Same-family judge bias (G2) |
| medium | WebDevJudge | arXiv 2510.18560 | Reliability of AI judges for web development (G2) |
| medium | Trajectory-Level Security Debt in LLM Coding Agents | DOI 10.1609/aaaiss.v10i1.43533 | Static security scans of rebuilt programs (G1 and security topic) |
| medium | SWE-CI | arXiv 2603.03823 | Maintainability as stability over code evolution (G1, G3) |
| low | AppForge | arXiv 2510.07740 | Native Android app generation (G8) |
| low | CentaurEval | arXiv 2512.04111 | Value of human intervention (G6) |
| low | Beyond Functional Correctness: Static Code Quality Profiling | arXiv 2610.19167 | Multi-tool static profiling at scale (G3) |
| low | SRE-Bench (The Next Challenge for Agentic Cybersecurity) | arXiv 2608.11469 | Building contamination-free benchmarks (G5) |
| low | BackendForge | DOI 10.18653/2026.findings-emnlp.2236; arXiv 2607.11042 | Black-box back-end tests (G7, G8) |
| low | Comparative Analysis of Iterative Prompt Refinement | DOI 10.2139/ssrn.7435043 (SSRN preprint) | Iteration and maintainability on JavaScript tasks (G4) |

**Add only if you choose the security topic (7 more):** arXiv 2610.14766 (Last Secure Code Benchmark); DOI 10.1109/tifs.2026.3746885 (security in LLM code translation); arXiv 2606.23130 (security of vibe-coded apps in the wild); arXiv 2611.06294 (A.S.E 2.0: unseen safeguards are not reproduced); DOI 10.1109/access.2026.3727682 (SAST, DAST and penetration testing of generated web back-ends); arXiv 2502.11844 (BaxBench); DOI 10.18653/2026.findings-emnlp.1335 (DualGauge). MirrorCode, UI2App and the security-debt paper are already in the table above.

All identifiers were copied from `rlab search` output and the novelty check. They are added with `rlab add`, which checks metadata. Each added paper then needs a full-text analysis.

### Step 2: choose your study direction

You have three options [I]:

| Option | What it is | Pros | Cons |
|---|---|---|---|
| A. G1 | Fidelity + maintainability of AI rebuilds against originals | Top-ranked gap; strongest evidence; closest to the project title | Software-engineering framing only |
| B. Security topic | Security-control preservation in black-box rebuilds | Fits your interest in cybersecurity; a clear new core | Needs web-security skills and an ethics section; confidence in novelty only moderate |
| C. Combine (our suggestion) | G1 design with security preservation as an extra outcome | One pipeline gives three outcomes; the security tests reuse G1's apps and runs | More work per app; keep the first version small |

A good way to keep option C manageable: run the G1 design on 4–6 multi-user web apps, and add 20–40 security tests per app.

### Step 3: run a small pilot experiment first

A *pilot* is a small trial run that tests your setup before the real study. Suggested pilot [I]:

1. **Pick 2 apps.** One small app from the released E2EDev set, which has validated tests [@liu2026benchmarking, p. 9]. One small open-source multi-user app with logins (for example, an app that follows the "RealWorld/Conduit" specification), if you want to try the security idea. Check the licences first.
2. **Run each original locally** in Docker.
3. **Write 10–15 behaviour tests** with Playwright. Find elements by their role and visible text, not by internal names. Confirm that every test passes on the original.
4. **Optional security tests (5–10):** for example, a protected page rejects a logged-out user, and user B cannot edit user A's article. Confirm that they pass on the original.
5. **Rebuild each app 3 times** with one AI coding agent. Give it the running app and screenshots only, with no source code and no internet access to the original's code.
6. **Measure on the originals and the rebuilds:** test pass rate; lines of code; SonarQube issues per thousand lines; cognitive complexity per function.
7. **Write down** the time, the API cost, and any problems with the setup. Use this to decide the final study size.

The pilot tells you whether the full study is affordable and whether your tests work. It does not answer the research question.

### Step 4: other actions

- **Re-run the novelty check before you write a paper.** Several close papers appeared between June and November 2026.
- **Talk to a supervisor** about the statistics (mixed-effects models) and, for the security topic, about ethics approval and responsible disclosure.
- **Record tool and model versions and dates** for every run, because AI tools change quickly.
- **Optionally check the published versions** of zhou2025declarui and zhu2026understanding.

---

## 9. Glossary

- **Agent (AI agent).** An AI system that can take actions by itself, such as clicking, running commands and editing files, to reach a goal.
- **Baseline.** The thing you compare against. In G1 the baseline is the original app.
- **Behavioural test.** An automatic check that does something in the app (click, type) and verifies the result.
- **Benchmark.** A fixed set of tasks and scoring rules used to compare AI systems.
- **Binary.** The compiled, machine-readable form of a program, as opposed to its human-readable source code.
- **Code quality.** How well code is written: readable, simple, free of risky patterns.
- **Code smell.** A pattern in code that suggests it may be hard to maintain, such as a very long function.
- **Cognitive complexity.** A score for how hard code is for a person to follow.
- **Confidence interval (CI).** A range of values that probably contains the true value. It shows how uncertain a result is.
- **Contamination.** When an AI model has already seen the test material (here, the original app's code) during training, so its score may be too high.
- **Differential security testing.** Running the same security tests on the original and the rebuild, and comparing the results.
- **Estimator.** The statistical method used to calculate an effect from data. Different accepted estimators can give different answers.
- **Evidence matrix.** Our table of all findings, each with its source, label and strength.
- **Evidence strength (strong / moderate / weak).** How much we trust a finding, based on sample size, design and agreement between studies.
- **Full text / abstract-only.** Whether we read the whole paper or only its short summary.
- **Functional fidelity.** How closely a rebuilt app behaves like the original.
- **Grey literature.** Material not published through academic peer review, such as blogs, reports and talks.
- **LLM (large language model).** The type of AI behind ChatGPT, Claude and similar tools. It produces text, including code.
- **LLM judge.** An LLM used to score outputs in place of human raters.
- **Locator.** The way a test finds an element on the page: by an internal name, or (better for rebuilds) by its role and visible text.
- **Maintainability.** How easily people can understand, fix and change code later.
- **Maintainability Index (MI).** An older single-number score of maintainability, computed from code size and complexity.
- **Mixed-effects model.** A statistical model that handles repeated measurements on the same units, such as several rebuilds of the same app.
- **Multivocal literature review.** A review that combines academic papers with grey literature.
- **Novelty check.** Targeted searches to see whether a proposed study has already been done.
- **Oracle.** The reference that decides whether an output is correct, such as a test suite or a judge.
- **Peer review.** Checking of a paper by independent experts before it is published.
- **Pilot study.** A small trial run that tests the setup before the full study.
- **Preprint.** A paper shared publicly before (or without) peer review, often on arXiv.
- **Preregistration.** Publishing your hypotheses and analysis plan before collecting data, so you cannot change them after seeing the results.
- **Randomised controlled trial (RCT).** An experiment in which participants are assigned to groups by chance, so that the groups can be compared fairly.
- **Research gap.** An open question that the evidence shows is unanswered and that a novelty check could not find already answered.
- **Reverse engineering (in this project).** Rebuilding an existing app only from what can be observed (screens, behaviour, documentation), without its source code.
- **Screening.** Checking search results against inclusion rules to decide which papers to keep.
- **Security control.** A protection built into an app, such as a login check or a rule about who may edit which data.
- **Significance test / p-value.** A statistical check of whether a difference could easily be due to chance. A small p-value (for example below 0.05) suggests it probably is not.
- **Snowballing.** Finding more papers by following the references and citations of papers you already have.
- **SonarQube.** A widely used tool that scans code and reports bugs, code smells and security warnings.
- **Static analysis (SAST) / dynamic testing (DAST).** Static analysis checks code without running it; dynamic testing attacks or probes the running app.
- **Systematic review.** A review that tries to collect every study on a question using a fixed, documented procedure.
- **Technical debt.** Future extra work caused by quick or poor solutions now.
- **Underpowered.** A study with too few participants to reliably detect small effects.
- **Vibe coding.** Building software mainly by describing what you want to an AI in natural language and accepting the code it writes, with little manual review.
- **Visual fidelity.** How closely a rebuilt app looks like the original.
