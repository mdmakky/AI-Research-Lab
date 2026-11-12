## IWR-Bench: Can LVLMs reconstruct interactive webpage from a user interaction video?
> **Takeaway:** When AI models watch a video of someone using a website and try to rebuild it, even the best model (GPT-5) scores only 36.35 out of 100, and no model gets more than 25 on working interactions [@chen2025iwr, p. 8]. Making things work is much harder than making them look right, although part of this gap comes from how the scores are built [@chen2025iwr, p. 7].

| Item | Detail |
|---|---|
| Authors | Yang Chen, Minghao Liu, Yufan Shen, Yunwen Li, Tianyuan Huang, Xinyu Fang, et al. (21 authors) |
| Year · Venue | 2025 · arXiv |
| Status | Preprint (not peer-reviewed) |
| Identifier | DOI 10.48550/arxiv.2509.24709 (arXiv 2509.24709) |
| Paper type | Benchmark with a large model comparison |
| Relevance to us | High — RQ1, RQ2, RQ4, RQ5 (indirectly) |

### In plain words
Earlier tests asked AI to turn a single screenshot of a webpage into code. Real websites, however, react when you click, type or scroll. This paper asks whether AI models that understand images and video can rebuild a webpage, including its behaviour, just by watching a screen recording of a person using it [@chen2025iwr, p. 2]. This is a form of reverse engineering from observed behaviour, not from a written description. It matters for us because it shows how far current models are from copying what an app does, not only what it looks like.

### How they did it
1. Trained annotators recorded videos while using 100 real websites. A browser extension logged every action, such as clicks and typing [@chen2025iwr, p. 5].
2. They also collected the site's images and icons. The file names were replaced (for example asset_001.png) so the model had to match pictures by how they look [@chen2025iwr, p. 5].
3. Each model got the video (one frame per second, at most 64 frames) plus one image showing all assets. It had to write a single index.html file with all HTML, CSS and JavaScript, with no outside libraries and any server behaviour faked in JavaScript [@chen2025iwr, p. 8].
4. An "agent-as-a-judge" (an AI agent that operates the generated page) replayed the recorded actions on the new page [@chen2025iwr, p. 6]. Gemini-2.5-Pro judged whether each expected result happened [@chen2025iwr, p. 7].
5. Two scores were combined [@chen2025iwr, p. 7]. IFS (Interactive Functionality Score) is the share of actions that work. VFS (Visual Fidelity Score) measures how similar the reached screens look. The Final Score is 0.7 x IFS + 0.3 x VFS.
6. The weights were tuned so the score matched human ratings as closely as possible [@chen2025iwr, p. 17].

### Data and setup
- 113 tasks from 100 websites, cut down from 200 candidates [@chen2025iwr, p. 5].
- 1,001 recorded actions (8.9 per video on average), with 620 visual checkpoints and 403 logic checks [@chen2025iwr, p. 6].
- Task mix: 7.96% static, 47.79% simple state, 33.63% complex workflow, 10.62% algorithm or game [@chen2025iwr, p. 3].
- 28 model entries: 17 commercial, 9 open-source and 2 video-specialised models. Three models were also run in a "thinking" mode [@chen2025iwr, p. 8].
- Human checks: five PhD-level raters scored 60 outputs [@chen2025iwr, p. 17], and three PhD students watched the judge agent on 100 pages [@chen2025iwr, p. 9].
- Runs per model and random seeds are not reported [@chen2025iwr, p. 8].

### Key findings
- [V] GPT-5 is best with Final 36.35, IFS 24.39 and VFS 64.25. No model exceeds 25 IFS [@chen2025iwr, p. 8].
- [V] IFS is below VFS for every model, for example Claude-Sonnet-4 22.29 vs 61.34 [@chen2025iwr, p. 8]. [I] Part of this gap comes from the metric design: VFS only counts screens that were reached, while IFS counts every action [@chen2025iwr, p. 7].
- [V] The top eight models are all commercial. The best open-source model, Qwen3-VL (thinking), scores 31.15 and beats 9 of the 17 commercial models. Video-specialised models are lowest (13.67 and 10.07) [@chen2025iwr, p. 8].
- [V] "Thinking" modes raise the Final Score only slightly (for example 34.62 vs 34.00) and lower VFS in all three pairs [@chen2025iwr, p. 8]. [A] The authors still call the gains "Consistent but Moderate" [@chen2025iwr, p. 9].
- [V] Scores drop sharply from static to interactive tasks: GPT-5 gets 61.85 on static pages but 25.26 on algorithm or game tasks [@chen2025iwr, p. 17].
- [V] The judge agent failed in only 3 of 100 observed runs, and these errors were fixed [@chen2025iwr, p. 9].
- [V] Score weights matched human ratings only moderately: Spearman correlation 0.57 for VFS and 0.65 for the Final Score [@chen2025iwr, p. 17].

### Limitations and weaknesses
- [I] The paper has no limitations section. The authors only mention design notes, such as fixing the three judge errors [@chen2025iwr, p. 9].
- [I] VFS and IFS use different denominators, so "visual is much better than function" is partly built in [@chen2025iwr, p. 7].
- [I] Code quality is never measured. The single-file output is far from how real apps are built [@chen2025iwr, p. 20].
- [I] Gemini-2.5-Pro is both a judge and an evaluated model, and self-preference was not tested [@chen2025iwr, p. 7].
- [I] The weights were tuned and tested on the same 60 human-rated items, with no held-out check [@chen2025iwr, p. 17].
- [I] No repeated runs, confidence intervals or significance tests, so small differences such as 30.36 vs 30.31 may be noise [@chen2025iwr, p. 9].
- [I] Websites like IMDb may be in training data, and the authors do not discuss this [@chen2025iwr, p. 2].
- [I] The static and algorithm groups hold only about 9 and 12 tasks [@chen2025iwr, p. 3].

### Gaps and future work this paper leaves open
- G1: behaviour and looks are scored, code quality is not [@chen2025iwr, p. 7].
- G2: the judge is calibrated in-sample and is also an evaluated model [@chen2025iwr, p. 17].
- G5: [I] no contamination discussion was found.
- [A] The authors point to temporal reasoning, linking assets to the right places, and better state management as next steps [@chen2025iwr, p. 9].

### Why it matters for your research
[I] IWR-Bench shows that rebuilding interactive behaviour from observation is hard for every model tested. Its action-replay judge and its split into "works" and "looks right" scores are useful ideas for your own study. Learn from its weaknesses too: give both scores the same denominator, use a judge that is not also tested, run each model more than once, and add code-quality measures. Treat its numbers as weak evidence, because this is a single preprint.

### Connections to other papers
- Builds on si2025benchmarking and xiao2025benchmarking. [A] The authors describe Design2Code as static and Interaction2Code as single-step and stateless [@chen2025iwr, p. 2].
- Agrees with xiao2025benchmarking: interactive parts score lower than full pages for all six models there [@xiao2025benchmarking, p. 6].
- Only directionally consistent with bai2026recreationworld. Static structure beats interaction there as well [@bai2026recreationworld, p. 16], but its visual score is below its functional score for 9 of 10 models [@bai2026recreationworld, p. 11].
- Agrees with the agent studies that whole-app fidelity is low [@kim2026programdistill, p. 11; @yang2026programbench, p. 6].
- [I] Do not rank 36.35 against other benchmarks' numbers, such as a 58.06% average [@bai2026recreationworld, p. 11] or 49.15% of workflows [@kim2026programdistill, p. 11]. Each uses a different scoring method.
