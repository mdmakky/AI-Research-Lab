## Interaction2Code: Benchmarking MLLM-based Interactive Webpage Code Generation from Interactive Prototyping
> **Takeaway:** When AI models rebuild a webpage from screenshots taken before and after each click, they copy the interactive parts worse than the page as a whole, for every model tested [@xiao2025benchmarking, p. 6]. Even the best setup produces usable interactions about 81% of the time, and code quality is never checked [@xiao2025benchmarking, p. 6].

| Item | Detail |
|---|---|
| Authors | Jingyu Xiao, Yuxuan Wan, Yintong Huo, Zixin Wang, Xinyi Xu, Wenxuan Wang, Zhiyao Xu, Yuhang Wang, Michael R. Lyu |
| Year · Venue | 2025 · 40th IEEE/ACM International Conference on Automated Software Engineering (ASE 2025) |
| Status | Peer-reviewed (conference paper). Our copy is the later arXiv v3 version, so page numbers follow that version |
| Identifier | DOI 10.1109/ase63991.2025.00028 (arXiv 2411.03292) |
| Paper type | Benchmark and empirical study, with a failure taxonomy and a small user study |
| Relevance to us | High — RQ1, RQ2, RQ4, RQ5 (RQ3 only by absence) |

### In plain words
Earlier screenshot-to-code tests only looked at static pages. Real webpages change when you click a button or open a menu. This paper asks whether AI models that read images can rebuild those interactions from an "interactive prototype": a screenshot of the page plus screenshots of what it looks like after each interaction [@xiao2025benchmarking, p. 1]. The authors built a test set, measured how well models do, sorted their mistakes into types, and tried prompting tricks to help. It matters for us because it is a web benchmark where the AI must infer behaviour from what it observes, which is close to reverse engineering.

### How they did it
1. They took 100 pages from the C4 web collection, filtered as in Design2Code, and 27 pages from popular GitHub projects. PhD students picked pages with at least one meaningful interaction [@xiao2025benchmarking, p. 2].
2. For each page they marked 1 to 10 important interactions and took screenshots before and after each one [@xiao2025benchmarking, p. 3].
3. The model got these screenshots and had to write one HTML+CSS+JavaScript file. It had to give interactive elements fixed IDs (for example id="interact1") so a test robot could find them [@xiao2025benchmarking, p. 3].
4. A Selenium webdriver (a tool that controls a browser automatically) clicked each element, took a screenshot and cut out the part that changed [@xiao2025benchmarking, p. 4].
5. The changed part was compared with the original using visual similarity, structural similarity, text and position scores. Implement Rate counts whether the robot could find and trigger the element at all [@xiao2025benchmarking, p. 4].
6. Four PhD students with front-end experience judged whether each interaction was "usable", meaning it matched the original behaviour [@xiao2025benchmarking, p. 6].
7. They compared four prompts [@xiao2025benchmarking, p. 5]. Direct is a plain request. Chain-of-Thought asks the model to reason step by step. Mark draws red boxes around interactive areas. A failure-aware prompt lists common mistakes.

### Data and setup
- 127 webpages with 374 interactions [@xiao2025benchmarking, p. 1].
- Most interactive elements are buttons (235), then inputs (52) [@xiao2025benchmarking, p. 3].
- Six models: Gemini-1.5-flash, GPT-4o, Claude-3.5-Sonnet and Qwen2.5-VL in three sizes [@xiao2025benchmarking, p. 4].
- Temperature 0 (the most predictable output), so one run per setting [@xiao2025benchmarking, p. 4].
- Contamination check: the generated code shares little text with the original HTML (BLEU, a text-overlap score, 0.12 to 0.14) [@xiao2025benchmarking, p. 5].
- Some extra experiments use only 10 pages, and the user study has 4 participants [@xiao2025benchmarking, p. 11].

### Key findings
- [V] Interactive parts score worse than full pages for all models, for example GPT-4o CLIP 0.7059 for the full page vs 0.5598 for the interaction part [@xiao2025benchmarking, p. 6].
- [V] Claude-3.5-Sonnet has the best averages on most metrics. GPT-4o with the Mark prompt has the highest Implement Rate (0.8128) [@xiao2025benchmarking, p. 6].
- [V] Human usability rates: GPT-4o 73%, 74% and 81% (Direct, Chain-of-Thought, Mark); Claude 66% to 77%; Qwen-3B only 17% to 19% [@xiao2025benchmarking, p. 6].
- [V] The Mark prompt gives the largest gain, for example Claude +11 points over Direct [@xiao2025benchmarking, p. 6].
- [V] Ten failure types were found. A missing element, no interaction and the wrong function each leave usability below 10% [@xiao2025benchmarking, p. 8].
- [V] Small, hard-to-see interaction areas cause errors. Enlarging them by cropping helped on 10 failure pages [@xiao2025benchmarking, p. 10].
- [V] Combining all improvements raised GPT-4o's interaction CLIP from 0.5700 to 0.6937 [@xiao2025benchmarking, p. 11].
- [V] The failure-aware prompt did not help all models: the small Qwen model dropped on 7 of 8 metrics [@xiao2025benchmarking, p. 9]. [A] The authors claim it helps "all models" [@xiao2025benchmarking, p. 8].

### Limitations and weaknesses
- [A] Interactions that need a server, such as login or search, cannot be tested, because there is no back-end code [@xiao2025benchmarking, p. 11].
- [A] Long pages with many interactions may not fit the model's context window [@xiao2025benchmarking, p. 11].
- [A] Existing widget-matching tools were built for mobile apps and miss web elements [@xiao2025benchmarking, p. 5].
- [I] The authors say human results are "consistent" with the automatic metrics, but give no correlation, rater agreement or item counts [@xiao2025benchmarking, p. 6].
- [I] Implement Rate only checks that an element exists and can be triggered, not that it behaves correctly [@xiao2025benchmarking, p. 4].
- [I] Behaviour is judged from screenshots only, so effects on data, network or storage are invisible [@xiao2025benchmarking, p. 4].
- [I] A low BLEU score does not rule out a memorised layout [@xiao2025benchmarking, p. 5].
- [I] Generated JavaScript is never checked for code quality [@xiao2025benchmarking, p. 5].

### Gaps and future work this paper leaves open
- G1: no code quality or maintainability measure; code is compared with the original only to check contamination [@xiao2025benchmarking, p. 5].
- G5: it is one of the few papers with an explicit contamination check [@xiao2025benchmarking, p. 5].
- G7: [I] tests find elements by IDs the model was told to add, which makes them depend on the prompt's naming scheme [@xiao2025benchmarking, p. 3].
- G8: back-end-dependent interactions are left as future work [@xiao2025benchmarking, p. 11].
- [A] The authors also propose multi-round generation for pages with many interactions [@xiao2025benchmarking, p. 11].

### Why it matters for your research
[I] Interaction2Code moves from "does it look right" to "does it react right", which is the next step towards rebuilding real apps. Its ten failure types are a ready-made checklist for coding errors in your own rebuilds. Its human Usability Rate is a simple functional-fidelity measure you could adopt, but report rater agreement and item counts, which this paper does not. Its contamination check, BLEU against the original code, is cheap and worth copying.

### Connections to other papers
- Builds on si2025benchmarking: it filters pages using the Design2Code approach [@xiao2025benchmarking, p. 2] and adds interactions.
- [A] chen2025iwr's authors say Interaction2Code treats interactions as single-step, stateless events, and they extend it to recorded videos [@chen2025iwr, p. 2].
- Agrees that interaction is harder than static content [@chen2025iwr, p. 16; @bai2026recreationworld, p. 16; @kim2026programdistill, p. 38].
- [I] The "looks right, works worse" pattern is not general: in bai2026recreationworld the visual score is below the functional score for 9 of 10 models [@bai2026recreationworld, p. 11].
