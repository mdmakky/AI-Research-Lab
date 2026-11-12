## We Have a Package for You! A Comprehensive Analysis of Package Hallucinations by Code Generating LLMs
> **Takeaway:** This is the founding large-scale study. Across 16 code models from 2023–24, about one in five suggested package names did not exist, and many invented names came back again and again. That repeatability is what makes "slopsquatting" (registering an invented name to plant malware) a realistic attack.

| Item | Detail |
|---|---|
| Authors | Joseph Spracklen, Raveen Wijewickrama, A H M Nazmus Sakib, Anindya Maiti, Bimal Viswanath, Murtuza Jadliwala |
| Year · Venue | 2024 (arXiv) · published at USENIX Security 2025 |
| Status | Peer-reviewed (USENIX Security 2025); our copy is the arXiv v3 version, so page numbers follow that copy |
| Identifier | DOI 10.48550/arxiv.2406.10279 (arXiv 2406.10279) |
| Paper type | Empirical measurement study plus mitigation experiment |
| Relevance to us | High — RQ1, RQ2, RQ3, RQ4 |

### In plain words
When you ask an AI coding assistant for code, it often tells you to install extra packages. A package is a ready-made code library downloaded from a public registry, such as PyPI for Python or npm for JavaScript. Sometimes the model (a large language model, or LLM) names a package that does not exist. This is a package hallucination. If an attacker registers that invented name and uploads malware, anyone who follows the model's advice installs the malware. The authors asked how often this happens, what makes it worse, what the invented names look like, and whether it can be reduced [@spracklen2024we, p. 4]. Their attacker can query the same models, check names against the registry and register the missing ones, while victims install suggested packages without checking [@spracklen2024we, p. 4].

### How they did it
1. Build prompts. One set came from Stack Overflow questions; the other was written by the Llama-2 70B model from the descriptions of the 5,000 most-downloaded PyPI and npm packages [@spracklen2024we, p. 5].
2. Generate code. 16 models wrote Python and JavaScript code, giving 30 model-language tests [@spracklen2024we, p. 6].
3. Collect package names in three ways: install commands the model wrote on its own, asking the model which packages its code needs, and asking which packages would solve the task. Reading import lines was rejected, because module names do not map one-to-one onto package names [@spracklen2024we, p. 6].
4. Decide what is hallucinated. A name counts as hallucinated if it is missing from a master list of PyPI or npm names taken on 10 January 2024 [@spracklen2024we, p. 7].
5. Probe behaviour. Extra experiments varied temperature (a setting that controls how random the output is), repeated prompts 10 times, and asked models to spot their own invented names [@spracklen2024we, p. 8; @spracklen2024we, p. 9; @spracklen2024we, p. 10].
6. Test fixes on two open models: RAG (retrieval-augmented generation, which adds looked-up facts to the prompt), self-refinement (the model re-checks its answer), and fine-tuning (extra training on correct examples) [@spracklen2024we, p. 12; @spracklen2024we, p. 13].

### Data and setup
- 576,000 code samples and 2.23 million package mentions [@spracklen2024we, p. 6; @spracklen2024we, p. 7]. The contributions list says 586,000 samples instead, and the paper does not explain the difference [@spracklen2024we, p. 2].
- Models from 2023 to early 2024, including GPT-4 Turbo, GPT-3.5, CodeLlama and DeepSeek Coder. Open models were run in GPTQ-quantized (compressed) form [@spracklen2024we, p. 6].
- Temperature 0.7 for code and 0.01 for the package questions [@spracklen2024we, p. 19]. Experiments ran on a GPU cluster [@spracklen2024we, p. 18].
- Name normalisation (treating variants such as my-pkg and my_pkg as the same) and standard-library exclusion are not reported.
- Prompts and code were released, which a later replication confirms [@churilov2026range, p. 15]. The list of hallucinated names is withheld [@spracklen2024we, p. 14].

### Key findings
- [V] 440,445 of 2.23 million package mentions (19.7%) were hallucinated, covering 205,474 unique invented names [@spracklen2024we, p. 7].
- [V] GPT models averaged 5.2% and open-source models 21.7% [@spracklen2024we, p. 7]. [I] Our recomputation shows these are averages of per-test rates, not pooled rates, and GPT-4 Turbo's "lowest" 3.59% is its Python-only figure [@spracklen2024we, p. 20].
- [V] Invented names repeat: in 10 re-runs of 500 prompts, 43% of names came back every time and 39% never came back [@spracklen2024we, p. 9].
- [V] 81% of distinct invented names came from only one model [@spracklen2024we, p. 10].
- [V] They are mostly not typos: only 13.4% are within 1–2 character edits of a real package, while 48.6% are 6 or more edits away [@spracklen2024we, p. 11].
- [V] Rates rise with temperature, sharply above 1; GPT-3.5 reached 31.8% at maximum temperature [@spracklen2024we, p. 8].
- [V] Fine-tuning cut DeepSeek 6.7B from 16.14% to 2.66%, but its HumanEval coding score fell from 51.4% to 25.3%. RAG cut CodeLlama 7B from 26.28% to 13.40% [@spracklen2024we, p. 13].
- [V] Deleted PyPI packages explain only 0.17% of names, and 8.7% of invented Python names are real npm packages [@spracklen2024we, p. 11].

### Limitations and weaknesses
- [A] The master list may already contain squatted names, so the rates are a lower bound [@spracklen2024we, p. 7].
- [A] For ethical reasons no names were registered, so real exploitation was not shown [@spracklen2024we, p. 14].
- [I] The rate mixes install commands with direct "which packages?" answers [@spracklen2024we, p. 6]. So it is not the same as "invented dependency in code" and cannot be compared directly with studies that read import lines.
- [I] Headline numbers mix pooled and averaged rates [@spracklen2024we, p. 20].
- [I] Each condition was run once, with no confidence intervals or significance tests, so small differences cannot be judged [@spracklen2024we, p. 13].
- [I] The fine-tuning data came from the same prompt pool used for evaluation, so the 2.66% may be partly in-sample [@spracklen2024we, p. 12].
- [I] Several internal inconsistencies (sample count, heuristic numbering between main text and appendix) lower confidence in exact numbers [@spracklen2024we, p. 2; @spracklen2024we, p. 18].

### Gaps and future work this paper leaves open
- [A] The authors call for finding root causes, building code-specific mitigations and fine-tuning that keeps code quality [@spracklen2024we, p. 13].
- [A] G2: they argue a plain existence check is an ineffective defence, because an attacker could publish a hallucinated name immediately [@spracklen2024we, p. 12]. Which extra signals work is still untested.
- [I] G1: only chat-style generation was studied. The 43% persistence [@spracklen2024we, p. 9] makes predictable installs by coding agents plausible, but nobody has measured them.
- [I] G3: its way of collecting names differs from later studies, which is a main reason rates across papers cannot be compared.
- [I] G4: all open models were quantized [@spracklen2024we, p. 6], but quantization was never varied.
- [A] G5: names were not registered and the list was withheld [@spracklen2024we, p. 14], so registration over time was not tracked.

### Why it matters for your research
This is the baseline every later paper compares against. Its prompt corpus is public and reusable [@churilov2026range, p. 4]. Two practical lessons: sample each prompt several times, because about four in ten names repeat every time; and do not rely on an existence check alone. When you quote 19.7%, add that it concerns 2023–24 models, counts per mention, and mixes name sources.

### Connections to other papers
- [V] churilov2026range re-ran the same prompts on five 2026 frontier models and found 3.63–5.02% of mentions hallucinated [@churilov2026range, p. 6]. [I] It parses imports, which this paper rejects, so the comparison is not like-for-like [@churilov2026range, p. 5].
- [V] Language direction disagrees: JavaScript above Python here [@spracklen2024we, p. 7], Python above JavaScript in krishna2025importing and churilov2026range [@krishna2025importing, p. 8; @churilov2026range, p. 7] (contradiction C1).
- [V] Prompt-source ordering reverses on the same corpus: Stack Overflow higher here [@spracklen2024we, p. 20], LLM-written prompts higher in churilov2026range [@churilov2026range, p. 7] (C2).
- [V] The temperature and RAG effects do not hold in Rust [@zheng2026when, p. 6; @zheng2026when, p. 8] (C4, C6).
- [V] Shared names across models also appear in zhao2025hfuzzer [@zhao2025hfuzzer, p. 7].
