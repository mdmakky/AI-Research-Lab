## ProgramBench: Can Language Models Rebuild Programs From Scratch?
> **Takeaway:** Given only a working program and its manual, no AI model fully rebuilt any of 200 real programs, and the best passed at least 95% of the tests on only 3% of them [@yang2026programbench, p. 6]. The rebuilt code is much shorter, uses far fewer files and is more monolithic than the human original [@yang2026programbench, p. 9].

| Item | Detail |
|---|---|
| Authors | John Yang, Kilian Lieret, Jeffrey Ma, Parth Thakkar, Dmitrii Pedchenko, Sten Sootla, et al. (12 authors; Meta FAIR, Meta TBD, Stanford, Harvard) |
| Year · Venue | 2026 · arXiv |
| Status | Preprint (not peer-reviewed) |
| Identifier | DOI 10.48550/arxiv.2605.03546 (arXiv 2605.03546) |
| Paper type | Benchmark with an evaluation of 9 models, test-quality checks and code-structure analysis |
| Relevance to us | High — RQ1, RQ2, RQ3, RQ4, RQ5 |

### In plain words
Most coding tests for AI ask it to fix one bug or add one feature. This paper asks something much bigger: can an AI build a whole program from scratch, including its overall design, just by running the original and reading its manual [@yang2026programbench, p. 1]? The original source code is hidden, so the AI must work out the behaviour by experimenting. This is black-box reverse engineering (rebuilding something only from what it does). It matters for us because it is the clearest test of our core scenario, although the programs are command-line tools, not apps with screens.

### How they did it
1. They took 200 open-source GitHub projects written in compiled languages (Rust, Go, C/C++) that build one program file [@yang2026programbench, p. 4].
2. The AI agent got the compiled program and its usage documentation inside a sealed container with no internet [@yang2026programbench, p. 4]. The program was execute-only, so it could be run but not opened up and decompiled (turned back into code). Decompiling and tracing tools were forbidden [@yang2026programbench, p. 19].
3. The agent could use any language. It had to hand in source code plus a build script that produces a program with the same behaviour [@yang2026programbench, p. 2].
4. Hidden tests were written by a separate AI agent (Claude Sonnet 4.5) that could read the original source. It added tests until they covered most of the code [@yang2026programbench, p. 3]. Tests check only what can be observed: printed output, exit codes and files written [@yang2026programbench, p. 3].
5. Tests that a deliberately broken "dummy" program could pass were removed or made stricter [@yang2026programbench, p. 8].
6. The main score, "% resolved", counts a task only if every test passes [@yang2026programbench, p. 5].

### Data and setup
- 200 tasks: 107 Rust, 46 Go, 45 C/C++ and 2 other [@yang2026programbench, p. 4].
- Size ranges from small tools to FFmpeg and SQLite; the median original has 8,635 lines of code and 50 code files [@yang2026programbench, p. 4].
- 248,853 tests, a median of 770 per task [@yang2026programbench, p. 4].
- 9 models x 200 tasks = 1,800 runs, one run each [@yang2026programbench, p. 10].
- A simple bash-only agent tool, 1,000 steps and 6 hours per task [@yang2026programbench, p. 5].
- Two extra experiments: forcing a different language, and allowing internet access with cheating detection [@yang2026programbench, p. 6].

### Key findings
- [V] No model resolves any task. Claude Opus 4.7 passes at least 95% of tests on 3.0% of tasks, Opus 4.6 on 2.5%, and Sonnet 4.6 on 1.6% [@yang2026programbench, p. 6].
- [V] Average test pass rates range from 52.0% (Opus 4.6) to 15.9% (GPT 5 mini). They fall from easy to hard tasks, for example 73.9% to 24.7% for Opus 4.6 [@yang2026programbench, p. 31].
- [V] The generated tests cover 79.7% of code lines on average, against 56.8% for the projects' own test suites [@yang2026programbench, p. 7].
- [V] Making tests stricter cut the dummy pass rate from 18.5% to 3.7% without changing the model ranking [@yang2026programbench, p. 8].
- [V] In the 207 runs passing at least 75% of tests, rebuilds had a median of 1,173 lines vs 3,068, and 3 files vs 15 [@yang2026programbench, p. 9].
- [V] Models write 10% to 29% as many functions as the original, and their functions are longer [@yang2026programbench, p. 9].
- [V] More effort helps little: pass rate correlates only weakly with API calls (r = 0.27) and cost (r = 0.21) [@yang2026programbench, p. 33].
- [V] With internet access, 20% to 36% of tasks were flagged as cheating for the three stronger models, mostly by looking up the source code [@yang2026programbench, p. 6].

### Limitations and weaknesses
- [A] A finite test suite is only a "lower bound" on correctness; rebuilds may still differ on untested inputs [@yang2026programbench, p. 12].
- [A] Speed, memory and other non-functional properties are not tested [@yang2026programbench, p. 12].
- [A] Only a single agent was tested, with no multi-agent or human-in-the-loop setting and no human study [@yang2026programbench, p. 20].
- [I] The test-writing model is a Claude model, and Claude models top the leaderboard. This possible bias is not tested [@yang2026programbench, p. 31].
- [I] Famous programs like SQLite may be memorised. Blocking the internet stops lookup, not memory [@yang2026programbench, p. 17].
- [I] Code quality is described only by size and structure. Those numbers come from a selected subset and are mixed up with language changes, since Python rewrites of C code are naturally shorter [@yang2026programbench, p. 35].
- [I] One run per model and task, and the claimed "significantly different" pass rates are not backed by a reported test [@yang2026programbench, p. 2].
- [A] The authors say % tests passed "does not reliably correlate" with how much functionality works [@yang2026programbench, p. 5].

### Gaps and future work this paper leaves open
- G1: rebuilds are shorter and shallower, but maintainability is not measured [@yang2026programbench, p. 9].
- G2: the same model family writes the tests and wins [@yang2026programbench, p. 3].
- G5: memorisation is only partly controlled [@yang2026programbench, p. 6].
- G6: the authors name human-guided reconstruction as future work [@yang2026programbench, p. 12], and there is no human baseline [@yang2026programbench, p. 20].
- G7: its tests are implementation-independent, a model for oracle design [@yang2026programbench, p. 5].
- [I] Graphical, web and mobile apps are not covered.

### Why it matters for your research
[I] ProgramBench gives you a tested recipe for black-box rebuilding: hide the source, block the internet, accept any language, and judge only observable behaviour. Its test-quality checks (coverage plus a dummy program) are worth copying. Its main open question is yours: the rebuilds are smaller and more monolithic, but nobody has measured whether that makes them harder to maintain. Run more than one attempt per task and use test writers from a different model family than the ones you evaluate.

### Connections to other papers
- Agrees with bai2026recreationworld: rebuilds there are also much smaller and use fewer files [@bai2026recreationworld, p. 15].
- kim2026programdistill builds on it and cites it as the whole-program "behavior-to-code" setting [@kim2026programdistill, p. 1]. bai2026recreationworld uses it to test training transfer [@bai2026recreationworld, p. 6].
- Agrees with kim2026programdistill that fidelity drops with complexity [@kim2026programdistill, p. 8].
- [I] Seems to contrast with AI-assisted development, which adds code [@he2026speed, p. 8]. The settings differ: rebuilds from scratch vs additions to existing projects.
