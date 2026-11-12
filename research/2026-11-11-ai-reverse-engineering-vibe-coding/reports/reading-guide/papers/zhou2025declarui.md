## DeclarUI: Bridging Design and Development with Automated Declarative UI Code Generation

> **Takeaway:** Giving the AI a map of how screens connect, plus compiler feedback, turns screenshots of multi-page mobile apps into code that compiles and navigates far better than a plain AI model. But the navigation score is partly circular, and "maintainability" is judged only by five developers' ratings.

| Item | Detail |
|---|---|
| Authors | Ting Zhou, Yanjie Zhao, Xinyi Hou, Xiaoyu Sun, Kai Chen, Haoyu Wang |
| Year · Venue | 2025 · Proceedings of the ACM on Software Engineering (FSE 2025) |
| Status | Peer-reviewed. We read the arXiv v1 preprint (September 2024); numbers in the published version may differ |
| Identifier | DOI 10.1145/3715726 · arXiv 2409.11667 |
| Paper type | Tool proposal plus controlled comparison, ablation and developer user study |
| Relevance to us | High — RQ1 to RQ5; one of few studies that rebuilds existing mobile apps from screenshots |

### In plain words
Turning a designer's mock-up or an existing app's screens into working code is slow, manual work. The authors built DeclarUI, a tool that does this automatically for multi-page mobile apps [@zhou2025declarui, p. 1]. It writes declarative UI code: code that describes what each screen should contain (in React Native, Flutter or ArkUI) rather than how to draw it step by step. The key idea is that plain AI models can copy single screens but forget how screens link together, so DeclarUI first builds a map of the links and then checks the code against it [@zhou2025declarui, p. 4]. For us, it is a direct example of reverse engineering from an app's visible UI, with both fidelity and code-quality measures.

### How they did it
1. Build a Page Transition Graph (PTG): Claude-3.5 reads the screens and lists the pages and the actions that move between them. Designers or developers then review and correct this graph [@zhou2025declarui, p. 4].
2. Find components: computer-vision tools (Grounding DINO to detect and Segment Anything to cut out elements in an image) locate buttons, lists and so on, and Claude-3.5 describes what each does [@zhou2025declarui, p. 4].
3. Write a prompt that combines the graph, the component list and the full screenshot [@zhou2025declarui, p. 5].
4. Refine: a static check (reading the code without running it) compares implemented navigation with the graph, up to 3 times per page; compiler errors are fed back, up to 3 times per project [@zhou2025declarui, p. 5].
5. Build and run each app on an emulator (a simulated phone) without manual fixes [@zhou2025declarui, p. 8].
6. Explore the built app with DroidBot, an automatic app-testing tool that records which screens lead where [@zhou2025declarui, p. 7].
7. Compare with GPT-4o and Claude-3.5 given only the raw images and a carefully designed prompt [@zhou2025declarui, p. 7].
8. Add an ablation (removing parts of the tool to see what each part adds), a developer user study and a manual repair timing study [@zhou2025declarui, p. 6].

### Data and setup
- 50 apps with 5 linked pages each (250 pages): 25 Figma design mock-ups and 25 Google Play apps, in 10 categories [@zhou2025declarui, p. 6].
- Google Play apps were among the top 10 by downloads in each category; screenshots were taken by hand on an emulator [@zhou2025declarui, p. 7].
- Measures [@zhou2025declarui, p. 7]: CLIP score (how similar two images are in meaning), SSIM (similarity of layout and structure), PTG Coverage Rate (PCR, the share of planned screen links that exist in the built app, counted by hand), compile success rate, and manual repair time.
- Developer ratings of code availability, modification time, readability and maintainability on 1–5 scales [@zhou2025declarui, p. 9].
- Ablation on 13 apps; user study with 5 React Native developers on 12 apps [@zhou2025declarui, p. 9].
- No link to code or data was found in our copy; sampling settings are not reported.

### Key findings
- [V] React Native, DeclarUI with Claude-3.5: CLIP 0.88, SSIM 0.68, navigation coverage 96.8%, compile success 98%. Plain Claude-3.5: 0.65, 0.41, 43.3%, 74%. Plain GPT-4o: 0.66, 0.44, 1.4%, 76% [@zhou2025declarui, p. 9].
- [V] Plain models largely fail to implement navigation between pages (GPT-4o 1.4%) [@zhou2025declarui, p. 9]. [A] Their compile errors come from non-existent packages and missing imports [@zhou2025declarui, p. 8].
- [V] It also works for other frameworks: Flutter 99.4% coverage and 92% compile success; ArkUI 95.9% and 86% [@zhou2025declarui, p. 9].
- [V] Removing the graph and refinement drops coverage to 23.1%; removing the vision step drops SSIM from 0.72 to 0.57 [@zhou2025declarui, p. 10].
- [V] Developers rated DeclarUI code higher than the baseline: readability 4.62 vs 3.75 and maintainability 4.55 vs 3.37, all p < 0.05 [@zhou2025declarui, p. 10].
- [V] 73.3% of DeclarUI code was modified within 10 minutes, while 80% of baseline code needed more than 10 minutes [@zhou2025declarui, p. 10].
- [V] Manual repair of failed builds took on average 48 s for React Native and 183 s for ArkUI [@zhou2025declarui, p. 11].
- [A] The authors conclude that the generated code meets industrial-grade standards [@zhou2025declarui, p. 1]; this rests on ratings from five developers.

### Limitations and weaknesses
- [A] CLIP and SSIM may not match human judgement of similarity; coverage does not reflect how smooth navigation feels [@zhou2025declarui, p. 12].
- [A] 50 apps may not represent all mobile UIs; sample size was limited by AI token cost [@zhou2025declarui, p. 12].
- [I] Humans correct the graph [@zhou2025declarui, p. 4], yet the main question is framed as working "without human intervention" [@zhou2025declarui, p. 6]. How much was corrected is not reported.
- [I] The navigation score is partly circular: DeclarUI gets the graph, is checked against it, and is then scored against the same graph; the baselines never see it [@zhou2025declarui, p. 7].
- [I] Some ablation numbers are impossible for 13 apps (98% and 80% cannot be k out of 13), which suggests values were copied from the 50-app run [@zhou2025declarui, p. 10].
- [I] The user-study tests treat 60 ratings as independent, so the very small p-values overstate certainty [@zhou2025declarui, p. 10].
- [I] Maintainability is only rated, never measured with code-analysis tools. One run per setup; no back-end or business logic [@zhou2025declarui, p. 2].

### Gaps and future work this paper leaves open
- [A] The authors plan better knowledge retrieval for rare frameworks such as ArkUI [@zhou2025declarui, p. 11] and larger, more varied samples [@zhou2025declarui, p. 12].
- [I] G1: maintainability rests on Likert ratings, not validated measures compared with the original's code.
- [I] G4: the feedback loop improves exactly what it checks (compilation, navigation links); its effect on code quality is untested.
- [I] G7: structural hints given as input, and scoring against the same hints, may inflate fidelity.
- [I] G8: UI only, with no back-end behaviour [@zhou2025declarui, p. 12].

### Why it matters for your research
[I] DeclarUI shows that structuring what you observe (a screen map) and feeding compiler errors back makes rebuilds much more complete. You can reuse its idea of exploring the built app automatically and comparing the resulting screen map with the original's. Avoid its weak points: do not score a rebuild against the same hints you gave it, measure maintainability with tools as well as opinions, and analyse repeated ratings with proper statistics.

### Connections to other papers
- [V] wu2026looks studies the same task with automatic navigation tests [@wu2026looks, p. 5] and also gives the model a page-connection description [@wu2026looks, p. 3]. [I] Both rebuild with a structural hint, not from screenshots alone.
- [V] Its loop result agrees with wu2026looks, where a build-repair loop gives 100% build success [@wu2026looks, p. 6]. It contrasts with pan2026functional, where repair strategies lowered code quality [@pan2026functional, p. 8].
- [V] borg2026echoes measures maintainability by having a second developer evolve the code [@borg2026echoes, p. 13], a stronger test than ratings.
- [V] bai2026recreationworld is the only paper here that rebuilds native Android apps from a running reference [@bai2026recreationworld, p. 7].
