## Evaluating Inference-Time Defenses against Package Hallucination in LLM-Generated Code
> **Takeaway:** On eight small open models in four languages, no defence applied at generation time wins everywhere. RAG gives the lowest rate most often but makes JavaScript worse, and plain greedy decoding gives the best balance between fewer fake names and useful answers. The paper also shows that counting standard-library modules as "hallucinations" inflates Python rates by 7.6–9.4 percentage points. Its measurement lessons are strong; its hardware and cost reporting is thin.

| Item | Detail |
|---|---|
| Authors | Alberick Euraste Djire, Iyiola E. Olatunji, Melissa Tessa, Earl T. Barr, Jacques Klein, Tegawendé F. Bissyandé |
| Year · Venue | 2026 · Proceedings of the 41st IEEE/ACM International Conference on Automated Software Engineering (ASE 2026) |
| Status | Peer-reviewed. Our copy is the arXiv v1 version (it carries the ACM DOI), so page numbers follow that copy |
| Identifier | DOI 10.1145/3832783.3837555 (arXiv 2608.22652) |
| Paper type | Comparative empirical evaluation (8 models × 4 languages × 8 decoding conditions, 3 runs each) |
| Relevance to us | High — RQ1, RQ3 (main), RQ4, RQ5 |

### In plain words
Small open models (1–8 billion parameters, a rough measure of size) can run on modest hardware, and they hallucinate package names more often than big ones [@djire2026evaluating, p. 2; @djire2026evaluating, p. 4]. The authors ask which inference-time defences work, meaning tricks applied while the model generates, with no retraining. They also fix a measurement mistake. If you check names only against the package registry, standard-library modules (such as os or json, which ship with Python and are never on PyPI) look like fake packages. This paper corrects for that.

### How they did it
1. Build prompts. They took the 1,000 most popular packages per registry from Libraries.io, and GPT-4o-mini wrote one coding instruction per package: 4,000 instructions in total [@djire2026evaluating, p. 3].
2. Fix the ground truth. They downloaded full registry name lists "as of March 4, 2026" and added standard-library lists [@djire2026evaluating, p. 3]. A name counts as hallucinated only if it is absent from both [@djire2026evaluating, p. 4].
3. Test defences. Greedy decoding (always pick the single most likely next token), RAG (retrieval-augmented generation: real package descriptions pasted into the prompt, k=5), Self-Refine (the model critiques its answer up to 5 times), and four decoding tricks (CD, DoLa, ALCD, Nudging) that need the model's internal scores and sometimes a second model [@djire2026evaluating, p. 4; @djire2026evaluating, p. 5].
4. Measure. Package hallucination rate (PHR) pooled over all names (micro) and averaged per prompt (macro). Package Utility (PU) asks whether the suggested packages are still useful, using similarity to the seed package; the authors call it a proxy [@djire2026evaluating, p. 4]. Code quality was checked with Semgrep, a static code checker [@djire2026evaluating, p. 7].
5. Stress test. 4,000 extra prompts asked the model to install and use a fake package name [@djire2026evaluating, p. 9].
6. Three runs per configuration, reported as mean ± standard deviation [@djire2026evaluating, p. 5].

### Data and setup
- Eight models: gemma-1b/4b, deepseek-coder-1.3b/6.7b, qwen2.5-1.5b/3b, mistral-7b and llama-3.1-8b; languages Python, JavaScript, Ruby and Rust [@djire2026evaluating, p. 3].
- Hardware: only "within the memory budget of a single GPU" [@djire2026evaluating, p. 4]. GPU type, inference software, quantization and run times are not reported. No latency or memory cost is given for any defence.
- No significance tests or confidence intervals.
- Code, data and prompts are on Zenodo [@djire2026evaluating, p. 11].

### Key findings
- [V] Treating standard-library modules as hallucinations raises pooled Python PHR from 24.7% to 32.3% (+7.6 pp), and by up to +9.4 pp for one defence [@djire2026evaluating, p. 5].
- [V] Corrected baseline PHR ranges from 16.1% (Mistral-7b) to 47.9% (Qwen-1.5b), with a peak of 63.1% (Qwen-1.5b, Rust) [@djire2026evaluating, p. 5; @djire2026evaluating, p. 6].
- [V] RAG gives the lowest PHR in 19 of 32 settings and lowers the average from 29.7% to 18.1%. But it raises JavaScript PHR for 7 of 8 models, by 12.7 pp on average [@djire2026evaluating, p. 6].
- [V] Greedy decoding matches Self-Refine at 25.6% average PHR and gives the highest utility, so it has the best overall trade-off [@djire2026evaluating, p. 6; @djire2026evaluating, p. 8].
- [V] DoLa is the worst method (38.0% average PHR; 83.5–91.2% on DeepSeek-1.3b). The decoding tricks also add syntax errors, up to 29% for DeepSeek-6.7b on Rust [@djire2026evaluating, p. 6; @djire2026evaluating, p. 7].
- [V] Prompts that name a fake package push baseline PHR to 46.6–92.5%; Ruby is the most vulnerable language [@djire2026evaluating, p. 9].
- [V] Under those prompts, RAG or Self-Refine is best in 29 of 32 settings; the lowest rate is 11.4% [@djire2026evaluating, p. 10].

### Limitations and weaknesses
- [A] Prompts are synthetic and were not checked against real developer questions. Only 8 small models, 4 ecosystems and one setting per defence were tested [@djire2026evaluating, p. 10].
- [I] Internal inconsistencies. The abstract's RAG count does not match the 19 of 32 stated in the body, and the abstract says rates rise "up to 45 pp" while the conclusion says 58.1 pp [@djire2026evaluating, p. 1; @djire2026evaluating, p. 6; @djire2026evaluating, p. 11]. The text says RAG never raises PHR in Python, Ruby or Rust, but the table shows Mistral-7b on Rust rising from 18.6 to 20.8 [@djire2026evaluating, p. 7].
- [I] In the results table, greedy equals the sampled baseline exactly for two models in all four languages [@djire2026evaluating, p. 7]. This looks like a copy error.
- [I] Prompts are built from the most popular packages, so RAG may simply retrieve the seed package. That flatters RAG and may understate hallucination on niche tasks.
- [I] There is no release-date cutoff: a name registered after the model was trained, including a squatted hallucination, counts as valid.
- [I] In the code-generation extension, imports are checked against the registry with no import-to-package map [@djire2026evaluating, p. 6]. Names like cv2 (installed as opencv-python) probably count as hallucinations.
- [I] Neither a plain registry filter nor PackMonitor-style constrained decoding was tested.

### Gaps and future work this paper leaves open
- [A] Make standard-library exclusion a baseline requirement; test indirect prompt injection and multi-turn manipulation; combine guided decoding with lightweight registry verification [@djire2026evaluating, p. 11].
- [I] G2: registry verification is proposed but not evaluated, and no defence has cost figures.
- [I] G3: the paper fixes standard-library handling but not import names or release dates, which shows how scoring rules change the numbers.
- [I] G4: small models across four ecosystems are covered, but quantization and local runtimes are not reported [@djire2026evaluating, p. 4]. Our G4 was narrowed because of this paper.

### Why it matters for your research
This is the most laptop-relevant defence study among the five briefs in this batch. Greedy decoding, RAG and Self-Refine need no access to model internals, and the 1–4B models are the kind that can plausibly run on a laptop. But the authors used a GPU and give no timings, so laptop speed is untested. Copy their measurement rules: a dated registry snapshot, a standard-library list, and both micro and macro rates. Add what they lack: an import-to-package map, a release-date cutoff, and timings on your own machine. Treat their defence rankings as moderate evidence from one study.

### Connections to other papers
- [V] RAG results disagree across studies: a slight rise in liu2026packmonitor [@liu2026packmonitor, p. 13], large drops in Python in spracklen2024we [@spracklen2024we, p. 13], and little effect in Rust in zheng2026when [@zheng2026when, p. 8] (contradiction 6).
- [V] Import-name scoring differs: twist2026library counts registered import names as valid [@twist2026library, p. 4], while raj2026names flags registered import names such as pil and faiss as squats [@raj2026names, p. 8] (contradiction 5).
- [V] Models largely go along with user-supplied fake names in other studies too [@twist2026library, p. 6; @dasu2026refusing, p. 8].
- [V] Frontier models in churilov2026range hallucinate far less (3.63–5.02% of mentions) [@churilov2026range, p. 6]. Units and models differ, so do not pool the numbers.
