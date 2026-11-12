## Names Can Hurt: Spotting Slopsquatting Risks Caused by Package Name Hallucinations in Local Coding LLMs
> **Takeaway:** A small preprint that builds a cheap guard: look each suggested package up on PyPI, score suspicious registered ones with a metadata classifier, and retry when needed. With one small Llama model, 76% of 300 prompts finished without a flagged name. Its headline, that half the flagged names are already registered lookalikes, is probably inflated by normal import names such as pil and faiss. The guard needs no GPU, and despite the title the models ran on a hosted API, not locally.

| Item | Detail |
|---|---|
| Authors | Akash Raj, Sargam Sahu |
| Year · Venue | 2026 · arXiv |
| Status | Preprint (arXiv v1, August 2026), not peer-reviewed. The metadata DOI is a Zenodo DOI; our metadata check returned a mismatch, and the PDF's identity is only "probable" because it prints no arXiv id |
| Identifier | arXiv 2608.23897 (metadata DOI 10.5281/zenodo.22087562) |
| Paper type | System design with a small empirical evaluation and a convenience-sample user survey |
| Relevance to us | High — RQ3 (main), RQ2, RQ1, RQ4, RQ5 |

### In plain words
The authors want a client-side guard: a tool on the developer's own machine that stops hallucinated Python package names from turning into slopsquatting installs (an attacker registering a hallucinated name and filling it with malware). They target small open-weight models of 7B to 70B parameters [@raj2026names, p. 2]. The guard first asks PyPI whether the name exists. If it does, a second layer asks whether the registered package looks like a low-quality lookalike. The authors are an M.Tech student and an intern, and the work is small, but it is the only tested guard in our set that needs no access to model internals.

### How they did it
1. Extract names. Python code blocks are parsed with an AST (abstract syntax tree, the program's structure as Python itself reads it), and "pip install" lines are read only inside code fences [@raj2026names, p. 3; @raj2026names, p. 5].
2. Layer 1. One PyPI lookup per name: "not found" (HTTP 404) means fake [@raj2026names, p. 5].
3. Layer 2. A Random Forest (a standard classifier that combines many decision trees) scores registered names with 10 features: 8 about the shape of the name, plus maintainer count and whether a GitHub link exists [@raj2026names, p. 5].
4. Import names. A 24-entry table maps import names to install names (cv2 to opencv-python, PIL to Pillow). It is used only after a 404 [@raj2026names, p. 5; @raj2026names, p. 6].
5. Retry. A flagged answer triggers a retry at higher temperature, then a hand-off to a larger fallback model; every attempt is logged [@raj2026names, p. 6].
6. A survey of 24 students rated the tool's interface [@raj2026names, p. 11].

### Data and setup
- 300 hand-written one-line Python prompts in 18 tiers, from routine tasks to adversarial "bait" prompts [@raj2026names, p. 6].
- Models: llama-3.1-8b (primary) and llama-3.3-70b (fallback), both hosted on Groq's free tier [@raj2026names, p. 2]. Hardware, quantization and model versions are not reported, and no model ran on the authors' own machine.
- Classifier data: 464 unique names from 7 models, leaving only 2–12 fake examples per test slice [@raj2026names, p. 9; @raj2026names, p. 10]. How these were labelled is not reported.
- Standard-library handling is not reported: every import is looked up, and every 404 counts as fake [@raj2026names, p. 5].
- Code is said to be on GitHub [@raj2026names, p. 15]; we did not check it.

### Key findings
- [V] 186 of 300 prompts gave clean code at once. 86 (28.7%) used up their retries, and the fallback rescued 14 of 85. In total 228 of 300 (76%) finished clean [@raj2026names, p. 7].
- [V] Most improvement came from fixing extraction bugs: the give-up rate went from 79% to 57% to about 29% across versions, measured on different prompt sets [@raj2026names, p. 7]. [A] Changing the classifier "did not help much" [@raj2026names, p. 12].
- [V] Give-ups rise with prompt type: 0–10% on routine tiers, 55% and 73.3% on bait tiers (5–30 prompts each) [@raj2026names, p. 7; @raj2026names, p. 8].
- [V] Of 179 flagged names, about half (90 flags) were registered on PyPI. 36 of these were pil and 10 were faiss [@raj2026names, p. 8; @raj2026names, p. 9]. [I] Both are normal import names of real projects (Pillow, faiss-cpu), so many "registered lookalikes" are probably correct imports, not invented names.
- [V] The classifier reduces to two metadata features (maintainers 57.6%, GitHub link 24.5% of importance). A two-feature rule matched it, F1 0.99 vs 0.98 [@raj2026names, p. 10; @raj2026names, p. 12]. F1 is a 0–1 score that balances missed and false alarms.
- [V] The first data split leaked: 72.9% of test rows contained names already seen in training. After the fix, F1 was 0.833–1.000 with very wide uncertainty [@raj2026names, p. 9; @raj2026names, p. 10].
- [V] Falling back to a bigger model of the same family failed again in 83.5% of cases, with the same invented names (pdfgenius, ultrarag) recurring [@raj2026names, p. 10].

### Limitations and weaknesses
- [A] The PyPI JSON API shows maintainers only to admins, so the top feature is basically 0 in live use, risking false alarms on small legitimate packages [@raj2026names, p. 13].
- [A] Brand-new legitimate packages will be mis-flagged, and none of the drift fixes is implemented [@raj2026names, p. 14]. The ≥30 registered names were not audited, and survey participants were the intern's friends [@raj2026names, p. 13; @raj2026names, p. 14].
- [I] There is no hand-checked ground truth: "hallucinated" means "flagged by the detector", so false alarms count as hallucinations.
- [I] The claim of cutting give-ups "from 79% (unmitigated)" compares against a buggy early version on a different prompt set [@raj2026names, p. 7; @raj2026names, p. 15].
- [I] Inconsistencies: bait refusal is 6 of 10 in the abstract but 9 of 10 in the text, and the two-feature rule is written as both AND and OR [@raj2026names, p. 1; @raj2026names, p. 11; @raj2026names, p. 12].
- [I] One model pair, one provider, Python only, single runs, no confidence intervals except for F1.

### Gaps and future work this paper leaves open
- [A] Cross-family fallback, richer features such as first-upload age, more training examples, drift handling, and squats with realistic metadata [@raj2026names, p. 13; @raj2026names, p. 14].
- [I] G2: this is the only black-box guard in our set, and its weak points (import names, new legitimate packages, realistic-looking squats) are exactly the hard cases an independent benchmark must contain.
- [I] G3: extraction and import-name handling dominated its results, which shows why a shared measurement protocol is needed.
- [I] G4: genuinely local inference, for example quantized models, was not tested.
- [I] G1: the retry loop resembles what an agent does after a failed install; repeating invented names is the behaviour to watch for.

### Why it matters for your research
This is the paper closest to a laptop-only project. The guard is one PyPI lookup plus a rule the authors say fits in "one line of Python" [@raj2026names, p. 12]. It needs no GPU and works with any model, including closed APIs. Use it as your baseline defence, but fix its weaknesses: filter standard-library modules, keep a separate import-to-package map, record PyPI status separately from "hallucinated", replace the maintainer feature with upload age or release history, and hand-label a sample to measure precision. Treat its numbers as weak evidence.

### Connections to other papers
- [V] Import-name scoring is contested: twist2026library counts registered import names as valid [@twist2026library, p. 4], and churilov2026range found import names to be the largest false-positive class [@churilov2026range, p. 10] (contradiction 5).
- [A] spracklen2024we argued that plain existence checks are inadequate because attackers can register names [@spracklen2024we, p. 12]; this paper's second layer is an attempt to answer that.
- [V] Recurring names fit earlier findings: 43% of hallucinated names recur in all 10 re-queries [@spracklen2024we, p. 9]. This paper lists pkg-resources as an invented name [@raj2026names, p. 8], while zhao2025hfuzzer found pkg_resources (a module that ships with setuptools) recommended by all nine models [@zhao2025hfuzzer, p. 7].
- [I] It credits Spracklen et al. with the term "slopsquatting" [@raj2026names, p. 2], while twist2026library attributes it to Park (2025) [@twist2026library, p. 1].
- [V] The white-box defences need data-centre GPUs [@liu2026packmonitor, p. 12], and only one study ran its pipeline on a laptop-class machine [@mirandapena2026empirical, p. 17].
