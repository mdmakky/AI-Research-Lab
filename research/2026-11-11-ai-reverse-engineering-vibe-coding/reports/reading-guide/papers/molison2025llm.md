## Is LLM-Generated Code More Maintainable & Reliable Than Human-Written Code?

> **Takeaway:** GPT-4o code had far fewer SonarQube-flagged "bugs" than human competition code, but it was often functionally wrong, and the fine-tuned model with the best quality scores had the lowest correctness. Static quality and correctness must be measured together, and the "fewer bugs" headline rests on a weak human baseline [@molison2025llm, p. 8].

| Item | Detail |
|---|---|
| Authors | Alfred Santa Molison, Marcia Moraes, Glaucia Melo, Fabio Santos, Wesley K. G. Assunção |
| Year · Venue | 2025 · ACM/IEEE International Symposium on Empirical Software Engineering and Measurement (ESEM 2025) |
| Status | Peer-reviewed (our copy: arXiv v1, page numbers refer to it) |
| Identifier | DOI 10.1109/esem64174.2025.00036 (arXiv 2508.00700) |
| Paper type | Quantitative comparative study (static analysis) |
| Relevance to us | Medium — RQ3 (main), RQ2, RQ4, RQ5 |

### In plain words
People worry that AI-written code is harder to maintain than human code. This paper compares Python code written by GPT-4o with code written by humans for the same programming puzzles. It uses SonarQube, a widely used tool that scans code without running it and flags problems. The authors look at "bugs" (rule-based warnings about likely errors), "code smells" (signs of messy or hard-to-change code) and the estimated time to fix them. They also run a small check of whether the code actually gives the right answers. The study matters because it is one of the few peer-reviewed, direct AI-versus-human quality comparisons in our set.

### How they did it
1. They took coding puzzles from the APPS dataset, a public set of 10,000 Python problems at three difficulty levels (introductory, interview, competition), with human solutions from sites such as Codeforces [V] [@molison2025llm, p. 3].
2. GPT-4o (version 2024-08-06) wrote solutions in three ways. Zero-shot: just the problem and the instruction to solve it. Few-shot: the problem plus all human solutions to that same problem as examples. Fine-tuned: a GPT-4o model trained on 240 question–answer pairs (80 per level), tested on 480 questions (160 per level) [V] [@molison2025llm, p. 4].
3. All solutions were scanned with SonarQube using its default Python rules [V] [@molison2025llm, p. 4; @molison2025llm, p. 5].
4. They compared groups with odds ratios (how much more or less likely a problem is in one group than another) and, for fix time, a Mann-Whitney U test with Cliff's delta (an effect-size measure) [V] [@molison2025llm, p. 5].
5. Three authors ran 15 solutions per approach (5 per level) by hand to compute Pass@1 (share of solutions that pass the tests on the first try) [V] [@molison2025llm, p. 8].

### Data and setup
- Dataset: APPS, Python, three difficulty levels [V] [@molison2025llm, p. 3].
- Model: GPT-4o-2024-08-06, temperature 1.00, max 2,048 tokens [V] [@molison2025llm, p. 4].
- Number of human and zero-/few-shot solutions actually scanned: not reported [I] [@molison2025llm, p. 4].
- Tool: SonarQube Free Server edition, default quality profile [V] [@molison2025llm, p. 4].
- Correctness check: 15 solutions per approach [V] [@molison2025llm, p. 8].
- Replication package on Zenodo [V] [@molison2025llm, p. 11].

### Key findings
- [V] SonarQube found no security vulnerabilities in any group [@molison2025llm, p. 5].
- [V] The odds of a SonarQube bug in GPT-4o code vs human code were tiny in every setting and level (odds ratios 0.00 to 0.019, all p < 0.001) [@molison2025llm, p. 8]. [I] The 0.00 means one group had no bugs at all, so it is not a real estimate.
- [V] Code smells were mixed: zero-shot code had 3.57 times the odds of a smell on introductory problems, while fine-tuned code had fewer smells; several comparisons were not significant [@molison2025llm, p. 8].
- [V] Estimated fix effort was lower for AI code on easy tasks but not on competition tasks (human 6.95 min, few-shot 7.33, fine-tuned 7.60) [@molison2025llm, p. 7].
- [V] Pass@1 was 1.0 for humans, 0.87 few-shot, 0.53 zero-shot and 0.47 fine-tuned [@molison2025llm, p. 8].
- [A] The fine-tuned model has "the best quality metrics" yet struggled with complex solutions [@molison2025llm, p. 8].
- [A] On competition-level problems, AI code may carry more critical-severity issues than human code [@molison2025llm, p. 6].

### Limitations and weaknesses
- [A] Python only, puzzle-style tasks, one model, and possible prompt sensitivity [@molison2025llm, p. 10].
- [A] SonarQube may not capture all aspects of quality, and its fix-time estimates may not match real developer effort [@molison2025llm, p. 10].
- [I] Leakage: the few-shot prompt contains the human solutions it is compared against, so few-shot vs human is not an independent comparison [@molison2025llm, p. 4].
- [I] A SonarQube "bug" is a rule-based warning, not a failing program. Quality was also measured on solutions that fail the tests, so "fewer bugs" does not mean "more correct" [@molison2025llm, p. 8].
- [I] The human baseline is competition code written to be correct, not maintainable, as the authors admit [@molison2025llm, p. 9].
- [I] Group sizes are not reported, there are no confidence intervals and no correction for many comparisons, and the Pass@1 check uses only 15 solutions per approach [@molison2025llm, p. 8].
- [I] APPS has been public since 2021, so GPT-4o may have seen it in training; this is not discussed [@molison2025llm, p. 11].
- [I] Some numbers are inconsistent, for example few-shot Pass@1 is 0.86 in the introduction and 0.87 in the table [@molison2025llm, p. 1; @molison2025llm, p. 8].

### Gaps and future work this paper leaves open
- [A] The authors suggest other LLMs, more languages and quality metrics, retrieval-augmented generation and cost–quality trade-off studies [@molison2025llm, p. 10].
- [I] It studies single small programs, not applications, and has no original app to compare against. This is the core of G1.
- [I] Its "fewer bugs" result conflicts in direction with studies that use other units or tools. Whether quality tools agree, and whether they predict real maintenance effort, is G3.
- [I] Public benchmark data and possible training exposure link to G5.

### Why it matters for your research
This paper gives you a ready-made recipe for the code-quality part of a study: SonarQube default profile, bugs, smells, severity and fix effort [I]. It also gives a strong warning. The model with the best quality scores was the least correct, so always report quality and correctness side by side, ideally quality only for code that works. Avoid its design mistakes: do not show the baseline to the model, report group sizes, use a realistic human baseline, and run several samples per task.

### Connections to other papers
- [V] Agrees with zhao2025vibe that correctness and another quality dimension diverge: there, 79.3% of working solutions failed security tests [@zhao2025vibe, p. 6].
- [V] Seems to disagree with he2026speed, where adopting Cursor raised repository SonarQube warnings by 30.26% [@he2026speed, p. 7]. [I] The units differ (single puzzle solutions vs whole repositories over months), so neither result refutes the other.
- [V] zhu2026understanding builds directly on this paper: its first experiment mirrors this design, without fine-tuning [@zhu2026understanding, p. 3].
- [A] zhu2026understanding also criticises it: SonarQube "issues" mix superficial linting with real design flaws, so the authors switch to PyExamine [@zhu2026understanding, p. 2]. With that tool, larger models wrote more Long Method smells than humans [V] [@zhu2026understanding, p. 7].
