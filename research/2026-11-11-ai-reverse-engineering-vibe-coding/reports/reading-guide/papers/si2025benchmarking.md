## Design2Code: Benchmarking Multimodal Code Generation for Automated Front-End Engineering
> **Takeaway:** AI models can turn a screenshot of a webpage into code that looks quite similar, and GPT-4o was best on every visual measure [@si2025benchmarking, p. 6]. But the benchmark only checks how the page looks. It never checks whether anything works or whether the code is maintainable [@si2025benchmarking, p. 3].

| Item | Detail |
|---|---|
| Authors | Chenglei Si, Yanzhe Zhang, Ryan Li, Zhengyuan Yang, Ruibo Liu, Diyi Yang |
| Year · Venue | 2025 · Proceedings of NAACL 2025 (Nations of the Americas Chapter of the ACL: Human Language Technologies, Volume 1: Long Papers) |
| Status | Peer-reviewed (conference long paper) |
| Identifier | DOI 10.18653/v1/2025.naacl-long.199 (arXiv 2403.03163) |
| Paper type | Benchmark with automatic metrics and a human evaluation |
| Relevance to us | High — RQ1, RQ2, RQ4, RQ5 (RQ3 only by absence) |

### In plain words
Front-end developers often turn a visual design into web code by hand. This paper asks how well AI models that read images (multimodal models) can do this automatically: you give them a screenshot of a real webpage, and they write the HTML and CSS [@si2025benchmarking, p. 1]. The authors built the first real-world test set for this task and new ways to score how close the result looks to the original. This is the starting point of the "screenshot to code" research line. It matters for us because many later reconstruction studies reuse its metrics, and because it clearly shows what visual scoring leaves out.

### How they did it
1. They took real webpages linked from C4 (a large public collection of web text), cleaned them and put all styling into one HTML file per page [@si2025benchmarking, p. 2].
2. Automatic filters cut the pool to 14k pages. Scripts, iframes, SVGs and external links were removed, and images were replaced by placeholders. The first two authors then hand-picked 484 test pages [@si2025benchmarking, p. 13].
3. Models were asked to write one HTML+CSS file from the screenshot. The prompt says no JavaScript is needed [@si2025benchmarking, p. 14].
4. They tried three prompting styles [@si2025benchmarking, p. 4]. Direct gives just the screenshot. Text-Augmented adds the page's text. Self-Revision lets the model see its own output and fix it.
5. They also fine-tuned (further trained on example data) their own open model, Design2Code-18B [@si2025benchmarking, p. 5].
6. They rendered each result and compared it with the original screenshot using five measures: Block-Match (are the text blocks there), Text, Position, Color and CLIP (overall visual similarity from an image-understanding model) [@si2025benchmarking, p. 4].
7. Paid human raters compared outputs in pairs and judged whether a generated page could replace the original [@si2025benchmarking, p. 5].

### Data and setup
- 484 test webpages, plus a harder set of 80 pages from GitHub [@si2025benchmarking, p. 8].
- Pages are long: 31,216 tokens and 158 HTML tags on average [@si2025benchmarking, p. 3].
- Models: GPT-4o, GPT-4V, Claude 3 Opus, Gemini 1.0 Pro Vision, several open models and two fine-tuned models [@si2025benchmarking, p. 5].
- Commercial models used greedy decoding (always the most likely output), so one run per setting [@si2025benchmarking, p. 14].
- Human evaluation: 100 sampled pages, 5 raters per item, 60 participants in total [@si2025benchmarking, p. 15].

### Key findings
- [V] GPT-4o Direct is best on all automatic measures: Block 93.0, Text 98.2, Position 85.5, Color 84.1, CLIP 90.4 [@si2025benchmarking, p. 6]. Humans preferred it over the Gemini baseline 92% of the time [@si2025benchmarking, p. 7].
- [A] Models "mostly lag in recalling visual elements" and in getting the layout right [@si2025benchmarking, p. 1].
- [V] On the hard set, Block-Match falls to 56.6 to 75.1, and GPT-4o Direct scores 56.6 [@si2025benchmarking, p. 8].
- [V] Adding the page text raised Block-Match for 4 of 7 models but lowered it for GPT-4o (93.0 to 92.4) and Claude 3 Opus (90.2 to 89.8) [@si2025benchmarking, p. 6].
- [V] 49% of GPT-4V self-revised pages were judged able to replace the original [@si2025benchmarking, p. 6].
- [V] The measures predict human preference with 79.9% accuracy. Exact text similarity counted negatively: humans care more about layout and content than exact wording [@si2025benchmarking, p. 7].
- [V] Human raters agreed only moderately or weakly with each other: Fleiss' kappa (a chance-corrected agreement score) of 0.46, 0.32 and 0.26 [@si2025benchmarking, p. 16].
- [V] Pages with more HTML tags are harder (r = −0.28 with Block-Match) [@si2025benchmarking, p. 15].

### Limitations and weaknesses
- [A] Only static pages are covered; dynamic pages need evaluation of "interactive functions beyond just visual similarity" [@si2025benchmarking, p. 10].
- [A] Humans should not be "blindly trusted as the oracle" because of attention bias [@si2025benchmarking, p. 7].
- [A] Complex pages need better prompting, such as generating page parts step by step [@si2025benchmarking, p. 10].
- [I] Fidelity is purely visual. There is no test of behaviour or code quality [@si2025benchmarking, p. 3].
- [I] The task rebuilds a stripped-down snapshot of a page, not a working application [@si2025benchmarking, p. 13].
- [I] The very high agreement with humans (r = 0.975) is based on 10 data points and partly on the same pages used to fit the model, so it is not an independent check [@si2025benchmarking, p. 17].
- [I] C4 pages are common training data, and contamination is not discussed [@si2025benchmarking, p. 2].
- [I] There are no significance tests or run-to-run variance for model comparisons [@si2025benchmarking, p. 6].

### Gaps and future work this paper leaves open
- G1: no code quality or maintainability measure [@si2025benchmarking, p. 3].
- G2: metric agreement with humans is checked in-sample, and human agreement is low [@si2025benchmarking, p. 17].
- G5: [I] no contamination discussion was found.
- [A] The authors call for interactive pages, Figma or sketch inputs, and evaluation beyond looks [@si2025benchmarking, p. 10].

### Why it matters for your research
[I] Design2Code tells you how to measure whether a rebuild looks like the original, and its five visual metrics are widely reused. Use them only as a secondary score. Visual similarity says nothing about whether buttons work or whether the code is easy to change. If you use human ratings, report agreement between raters and validate on pages you did not use for fitting.

### Connections to other papers
- xiao2025benchmarking builds on it, filtering pages the same way and adding interactions [@xiao2025benchmarking, p. 2].
- [A] chen2025iwr's authors describe Design2Code as limited to static reconstruction [@chen2025iwr, p. 2]. bai2026recreationworld also cites it as related work [@bai2026recreationworld, p. 21].
- Like xiao2025benchmarking and kim2026programdistill, it measures no code quality [@xiao2025benchmarking, p. 5; @kim2026programdistill, p. 14].
- [I] Its weak human agreement echoes other judge checks in the project, such as a moderate 0.65 correlation in chen2025iwr [@chen2025iwr, p. 17].
