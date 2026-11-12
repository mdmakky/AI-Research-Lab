## Looks Right, Works Right: A Project-Level Benchmark for Multi-Screen Mobile App Generation

> **Takeaway:** When frontier AI models rebuild whole multi-screen mobile apps from screenshots of real apps, the code always builds, navigation works in 58–92% of tests, and visual fidelity stays at or below 2.99 out of 5. The model whose app looks best is not the one whose code is most maintainable, so one score cannot stand for all.

| Item | Detail |
|---|---|
| Authors | Fan Wu, Cuiyun Gao, Yiming Huang, Yang Xiao, Yujia Chen, Qing Liao |
| Year · Venue | 2026 · Proceedings of the 2026 Conference on Empirical Methods in Natural Language Processing (EMNLP 2026) |
| Status | Peer-reviewed. Very recent and not yet replicated |
| Identifier | DOI 10.18653/2026.emnlp-main.2650 · arXiv 2607.28645 |
| Paper type | Benchmark (MobileForge) plus five-axis empirical evaluation of 6 multimodal models |
| Relevance to us | High — RQ1 to RQ5; the closest existing design to our target study |

### In plain words
The paper opens with a direct question: "Can a multimodal LLM read a folder of mobile-app screenshots and generate the source code for that app?" [@wu2026looks, p. 1]. A multimodal LLM is an AI model that reads images as well as text. Earlier benchmarks mostly tested single pages, did not test whether buttons lead to the right screen, and did not look at the code as a whole project [@wu2026looks, p. 1]. MobileForge fixes this by scoring five things at once: does it build, does navigation work, does it look like the original, is the code maintainable, and what does it cost [@wu2026looks, p. 4]. For us, this is the nearest thing to a reconstruction study that measures fidelity and code quality together.

### How they did it
1. Collect apps: 29 real consumer apps from official app stores. Screenshots were taken by hand from default or demo screens without logging in [@wu2026looks, p. 3].
2. Annotate: a vision-language model (an AI that reads images and text) drafted a description of how pages connect, plus navigation tests. The research team reviewed every field [@wu2026looks, p. 3].
3. Build: one AI agent received all screenshots plus the page-connection description and had to produce a React + TypeScript + Tailwind web project. It had 8 tools (write file, run command and so on) and up to 50 steps. When it finished, an automatic build check (tsc + vite) sent errors back for repair [@wu2026looks, p. 6].
4. Test navigation: Playwright, a tool that drives a browser automatically, ran each test from its own starting page, did one action, and checked whether the right page appeared. Starting fresh each time stops one failure from causing many others [@wu2026looks, p. 5].
5. Test looks: a judge model (Gemini 2.5 Pro) ranked the six models' versions of a screen, with the real screenshot hidden among them as an "anchor". Rankings that did not put the real screenshot first were thrown away and redone. Ranks were turned into a Borda score between 0 and 1, a simple points-for-rank system [@wu2026looks, p. 5]. A 1–5 rubric score was also kept [@wu2026looks, p. 6].
6. Check code: simple indicators such as lines of code (LoC), lines per file, how often shared components are reused, the share of unused ("dead") components, and colour consistency [@wu2026looks, p. 4].
7. Check the judge: on 55 scenarios, its rankings were compared with human rankings [@wu2026looks, p. 13].

### Data and setup
- 29 apps in 14 categories, 309 screens (5–21 per app), 701 navigation tests [@wu2026looks, p. 3].
- Apps include Notion, Khan Academy, WhatsApp, Airbnb and Coinbase [@wu2026looks, p. 12].
- Six closed models: Claude Opus 4.6, Claude Haiku 4.5, GPT-5, GPT-5 Mini, Gemini 2.5 Pro, Gemini 2.5 Flash [@wu2026looks, p. 6].
- 29 apps × 6 models = 174 runs, one run each [@wu2026looks, p. 6].
- 64 hand-labelled navigation failures for a failure analysis [@wu2026looks, p. 8].
- Screenshots, annotations, harness and all run outputs are released (author claim) [@wu2026looks, p. 10].

### Key findings
- [V] Every model builds successfully in 100% of runs [@wu2026looks, p. 6]. [A] "Build success is a property of the harness, not the model" [@wu2026looks, p. 12].
- [V] Navigation pass rate: Opus 4.6 92%, GPT-5 89%, Haiku 4.5 85%, Gemini 2.5 Pro 82%, Gemini 2.5 Flash 62%, GPT-5 Mini 58% [@wu2026looks, p. 7].
- [V] Visual fidelity is far from solved: rubric means range from 1.60 to 2.99 out of 5, and Borda scores from 0.130 to 0.906. Opus leads in 26 of 29 apps [@wu2026looks, p. 6].
- [V] Looks and code quality diverge: Opus writes 1,441 LoC (82 per file) vs 668 (33 per file) for GPT-5, and GPT-5 has fewer dead components (7.8% vs 19.9%) [@wu2026looks, p. 7]. [A] The authors call maintainability "uncorrelated" with visual fidelity [@wu2026looks, p. 8].
- [V] Cost ranges from $0.15 to $2.90 per app; GPT-5 ($0.50) beats Haiku 4.5 and Gemini 2.5 Pro on both cost and quality [@wu2026looks, p. 7].
- [V] The biggest navigation failure is "click has no effect" (48.4%), then target unreachable (32.8%), wrong route (10.9%) and blank page (7.8%), from 64 labelled cases [@wu2026looks, p. 8]. [A] Build checks miss these silent bugs [@wu2026looks, p. 8].
- [V] The judge agrees reasonably with human rankings (Kendall τ = 0.716, a rank-agreement score where 1 is perfect; top-1 match 83.6%), and a second judge gives τ = 0.867 [@wu2026looks, p. 13].

### Limitations and weaknesses
- [A] One run per app and model; the judge comes from a competing model family; output is a web app standing in for a native app [@wu2026looks, p. 9].
- [A] Per-model failure shares rest on 8–12 cases each [@wu2026looks, p. 8].
- [I] The input is not screenshots alone: the agent also gets the human-reviewed page-connection description [@wu2026looks, p. 6]. Results describe rebuilding with a navigation map, not pure black-box observation.
- [I] The code indicators are not validated against developer judgement or standard metrics. More LoC may simply mean more content was copied.
- [I] "Uncorrelated" rests on six model averages; no correlation was computed.
- [I] The 55 human labels were made by the authors themselves [@wu2026looks, p. 13].
- [I] Two failure tables do not reconcile [@wu2026looks, p. 16], and overlays count as passing when the page content "changes meaningfully", which is lenient [@wu2026looks, p. 5].
- [I] Famous apps were chosen on purpose [@wu2026looks, p. 3], so models may have seen them in training; this is not discussed. Only page changes are tested, not data or back-end logic.

### Gaps and future work this paper leaves open
- [A] The authors call for repeated runs, native app versions [@wu2026looks, p. 9] and stricter build checks [@wu2026looks, p. 12].
- [I] G1: maintainability here is unvalidated proxies [@wu2026looks, p. 4], not a validated measure against the original's code.
- [I] G7: a structural hint is given as input [@wu2026looks, p. 3]; its effect on scores is unknown.
- [I] G8: native mobile apps with hidden back-ends are not covered [@wu2026looks, p. 9].
- [I] G4: the build-repair loop saturates build success but says nothing about behaviour or quality. G5: memorisation of famous apps is unchecked.

### Why it matters for your research
[I] This paper is the closest model for your own study. Reuse its ideas: state-isolated navigation tests, a visual judge with a hidden real screenshot, and reporting several scores side by side. Its main message supports your topic: looks, behaviour and code quality can disagree, so they must be measured separately. Improve on it by running each build several times, testing behaviour beyond navigation, using validated quality tools, and comparing with the original's code.

### Connections to other papers
- [V] Very close to zhou2025declarui, which also rebuilds multi-screen mobile UIs from screenshots and also feeds a screen-connection graph to the model [@zhou2025declarui, p. 4]. [I] MobileForge replaces manual navigation counts with automatic tests.
- [V] Agrees with pan2026functional that function and quality diverge: equal functional scores, very different non-functional scores [@pan2026functional, p. 5].
- [V] Agrees that interaction is the hard part: bai2026recreationworld finds static structure easier than actions [@bai2026recreationworld, p. 16].
- [V] Contrasts with chen2025iwr, where visual scores exceed interaction scores [@chen2025iwr, p. 8]; here navigation scores well while visuals stay low. [I] The scales are not comparable across papers.
- [V] Rebuilds in bai2026recreationworld are much smaller than the originals [@bai2026recreationworld, p. 15], while the visual leader here writes more code. [I] Code size means different things in different settings.
- [V] Like tran2026vibe, it validates its AI judge against humans [@tran2026vibe, p. 9].
