## PropGen: Automated Property Generation for Property-Based Testing of Mobile Apps

> **Takeaway:** An AI model can write down valid behaviour rules of an Android app by actually using the app, but not from the app's description alone (912 of 985 rules valid vs 0 of 240). For us, this is a method for turning an original app's observed behaviour into tests a rebuild must pass [@xiong2026propgen, p. 8; @xiong2026propgen, p. 9].

| Item | Detail |
|---|---|
| Authors | Yiheng Xiong, Shiwen Song, Bo Ma, Ting Su, Xiaofei Xie |
| Year · Venue | 2026 · Proceedings of the 41st IEEE/ACM International Conference on Automated Software Engineering (ASE 2026) |
| Status | Peer-reviewed |
| Identifier | DOI 10.1145/3832783.3837536 (arXiv 2604.13463) |
| Paper type | Tool paper with empirical evaluation |
| Relevance to us | Medium — RQ2, RQ4, RQ5 (method only; not RQ3) |

### In plain words
Many app bugs do not crash the app. The app just does the wrong thing, for example a setting that has no effect. Such bugs are hard to find because there is no "oracle" (a rule that says what the correct result is). Property-based testing helps: you write rules like "if I delete a note, it is no longer in the list", and a tool tries many random action sequences to see if a rule is broken. Writing those rules by hand is slow and expensive, and apps rarely have written specifications [A] [@xiong2026propgen, p. 1]. PropGen lets an AI model explore a running Android app, record what it sees, and turn that evidence into such rules automatically.

### How they did it
1. Exploration. A multimodal LLM (an AI model that reads both images and text) looks at the screenshot, the numbered on-screen widgets, the app name and the screen (activity) names from the app's manifest file. It guesses which functions the app has, and PropGen tries each guess step by step [V] [@xiong2026propgen, p. 4].
2. Evidence. Each tried action is saved as "behavioural evidence": the screen before, the action, the screen after, what changed, and whether it worked [V] [@xiong2026propgen, p. 5].
3. Grounding. Widget names are filtered against a list of text strings taken from the app package by static analysis (reading the files without running them) [V] [@xiong2026propgen, p. 5]. [I] So PropGen is grey-box: it mostly watches the running app, but also reads the manifest and a string list. The authors describe it as exploring "a black-box app" [A] [@xiong2026propgen, p. 11].
4. Property writing. The model first writes a rule in plain language with three parts: precondition (when it applies), interaction (what the user does) and postcondition (what must be true after). It then turns the rule into code for the testing tool Kea [V] [@xiong2026propgen, p. 6].
5. Refinement. When a human confirms that a reported "bug" is a false alarm, the model finds which of the three parts is wrong and fixes only that part [V] [@xiong2026propgen, p. 6].

### Data and setup
- 12 open-source Android apps (for example OmniNotes, Markor, AnkiDroid, NewPipe), from 57,529 to 403,785 lines of code [V] [@xiong2026propgen, p. 7].
- Model: GPT-5.2 (snapshot gpt-5.2-2025-12-11) at temperature 1.0. 3 hours per app for exploration and rule writing, then 6 hours of testing [V] [@xiong2026propgen, p. 7].
- Comparisons: DroidAgent (another AI exploration tool), a naive baseline where the LLM writes 20 rules per app from the app's description only, and four bug-finding tools (Genie, Odin, PBFDroid, VisionDroid) [V] [@xiong2026propgen, p. 7].
- Two graduate students, not co-authors, judged validity independently. Their agreement was high: Cohen's kappa (an agreement score where 1 is perfect) of 0.91, 0.82 and 0.81 [V] [@xiong2026propgen, p. 7].
- No repeated runs are reported [I] [@xiong2026propgen, p. 8].

### Key findings
- [V] PropGen found 1,282 app functions, of which 1,210 were valid (94.4%) and 977 were executed correctly (76.2%). DroidAgent found 575, with 491 valid (85.4%) and 187 correctly executed (32.5%) [@xiong2026propgen, p. 8].
- [V] PropGen wrote 985 rules, and 912 were valid (92.6%; 78.7% to 98.8% per app) [@xiong2026propgen, p. 8].
- [V] The naive baseline that only read the app description wrote 240 rules, and none were valid, because it referred to widgets that do not exist [@xiong2026propgen, p. 9].
- [V] 127 rules caused false alarms; 118 of them (92.9%) were fixed, mostly by changing the postcondition (64) or precondition (53) [@xiong2026propgen, p. 9].
- [V] The rules found 25 previously unknown functional bugs; 5 were fixed by developers at the time of writing [@xiong2026propgen, p. 9].
- [V] Only 3 of the 25 bugs were found again by the four older tools. Those tools found 13 unknown bugs themselves, of which PropGen missed 10 [@xiong2026propgen, p. 10]. [A] The authors call the approaches "complementary rather than substitutable" [@xiong2026propgen, p. 10].
- [V] Cost was about $14.86 per app for PropGen vs $13.01 for DroidAgent [@xiong2026propgen, p. 9].

### Limitations and weaknesses
- [A] Human judging can be subjective; only 12 apps were tested; the open-source apps may be in the model's training data [@xiong2026propgen, p. 11].
- [A] The model sometimes invents functions that do not exist or invents widgets while writing rules [@xiong2026propgen, p. 9].
- [I] Not fully automatic: refinement starts only after a human confirms a false alarm, and that human effort is not measured [@xiong2026propgen, p. 6].
- [I] Single runs at temperature 1.0, so we do not know how stable the numbers are [@xiong2026propgen, p. 7].
- [I] The naive baseline never sees the app, so it is a weak comparison [@xiong2026propgen, p. 7].
- [I] Three of the four comparison tools (Genie, Odin, PBFDroid) come from the authors' own research group, and the scope check was validated by the same group [@xiong2026propgen, p. 8]. Only VisionDroid is independent.
- [I] The contamination check is partial: showing that the bugs were not previously reported does not show that the model never saw how the apps behave [@xiong2026propgen, p. 11].

### Gaps and future work this paper leaves open
- [A] The authors plan a larger and broader set of apps, better step planning, and combining PropGen with other test oracles [@xiong2026propgen, p. 10; @xiong2026propgen, p. 11].
- [I] Nobody has used properties mined from an original app to test an AI-rebuilt version of it. This would serve the fidelity side of G1.
- [I] Mobile apps and their hidden back-end behaviour are barely studied in reconstruction (G8); PropGen's runtime exploration could help there.
- [I] Testing six app builds released after the model's training cutoff [A] [@xiong2026propgen, p. 11] is one of the few contamination controls in our corpus, relevant to G5.
- [I] Its rules use on-screen behaviour rather than the original's internal identifiers, which is relevant to G7.

### Why it matters for your research
PropGen does not build or rebuild apps, so it says nothing about code quality [I]. Its value is as a method. It shows how to recover what an app does from the running app, without source code or a specification. You could use the same idea to write tests from your original app and then check how many of them the rebuild satisfies. Its strongest lesson: an AI that has not observed the real app invents behaviour, so ground any test or rebuild in observed behaviour [V] [@xiong2026propgen, p. 9]. Its evaluation design, with two independent annotators and a kappa score, is a good template.

### Connections to other papers
- [V] Like bai2026recreationworld, which uses accessibility and DOM tests [@bai2026recreationworld, p. 9], it checks behaviour on the running app rather than in the code.
- [V] Its post-cutoff app builds are one of the few explicit contamination controls, next to yang2026programbench's no-internet setup and ablation [@yang2026programbench, p. 6].
- [I] In our project it is the only paper that recovers a behaviour specification from a running app rather than building an app [@xiong2026propgen, p. 4]. It is a measuring tool for the other papers' setting, not a competitor.
- [V] kim2026programdistill's test oracles use the original app's selectors (internal element identifiers) [@kim2026programdistill, p. 35]. [I] PropGen's rules are instead grounded in visible widgets and observed behaviour, which may make them fairer to rebuilds that name things differently.
