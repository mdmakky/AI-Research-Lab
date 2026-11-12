## The Range Shrinks, the Threat Remains: Re-evaluating LLM Package Hallucinations on the 2026 Frontier-Model Cohort
> **Takeaway:** Re-running Spracklen's public prompts on five 2026 frontier models gives much lower rates, about 4–5% of package mentions. But every model still invents names, 104 names are invented by all five, and about 1% of invented names were registered by someone within six months. It is a single-author preprint, yet its live registry check is the most careful measurement protocol in our set.

| Item | Detail |
|---|---|
| Authors | Aleksandr Churilov (independent researcher) |
| Year · Venue | 2026 · arXiv |
| Status | Preprint (not peer-reviewed). Our copy is version 4 (November 2026), which replaces all numbers in versions 1–3 and in a SCORED '26 workshop version |
| Identifier | DOI 10.48550/arxiv.2605.17062 (arXiv 2605.17062) |
| Paper type | Replication study with a preregistered live-registry re-check and a natural experiment on registrations |
| Relevance to us | High — RQ1, RQ2, RQ4, RQ5 |

### In plain words
Do the newest AI models still make up package names? A package is a ready-made code library downloaded from a public registry such as PyPI (Python) or npm (JavaScript). The author took the prompt set released by Spracklen et al. and ran it unchanged on Claude Sonnet 4.6, Claude Haiku 4.5, GPT-5.4-mini, Gemini 2.5 Pro and DeepSeek V3.2 [@churilov2026range, p. 4]. Every suggested name was then checked against the live registries. The paper also asks whether invented names actually get registered, and whether publishing a list of them speeds that up [@churilov2026range, p. 1; @churilov2026range, p. 2].

### How they did it
1. Generate. The 39,969 prompts were sent to each model between 22 and 28 April 2026 [@churilov2026range, p. 4].
2. Extract names from pip install commands, npm install commands inside code blocks, and import statements read with proper code parsers [@churilov2026range, p. 5].
3. Clean the list. Standard-library modules, names that break registry naming rules, and import names that pipreqs (a tool that maps import names to package names) links to a real package were removed [@churilov2026range, p. 5].
4. Check live. Each registry was asked in two ways, in two rounds at least 12 hours apart. A name counts as missing only if all four answers say "absent". Package creation time was compared with generation time, and OSV (a public database of known malicious and vulnerable packages) was queried [@churilov2026range, p. 5].
5. Plan in advance. The analysis plan was preregistered (written down before looking at the data), with a log of 20 deviations [@churilov2026range, p. 6].
6. Test properly. Rates come with Wilson confidence intervals (a range likely to hold the true rate), and model comparisons use chi-square tests with Holm correction for multiple comparisons plus permutation tests [@churilov2026range, p. 6].
7. Natural experiment. A list of shared names had been exposed publicly by accident. Registration of those names was compared with similar unpublished names [@churilov2026range, p. 11; @churilov2026range, p. 12].

### Data and setup
- 199,840 generations in total [@churilov2026range, p. 4]. 2,282 unique hallucinated names: 1,746 on PyPI and 536 on npm [@churilov2026range, p. 11].
- Refusal rates range from 1.27% to 31.51% [@churilov2026range, p. 4]. Temperatures were recorded but not printed [@churilov2026range, p. 4].
- Estimated API cost $1,160.29 [@churilov2026range, p. 17].
- At most one request per second per registry host [@churilov2026range, p. 5].
- Code and aggregate results are public on GitHub; raw responses are available on request [@churilov2026range, p. 15].
- Self-funded apart from a Google Cloud credit grant. The author used Claude to write analysis code and draft the text [@churilov2026range, p. 15].

### Key findings
- [V] Rates range from 3.63% (Haiku 4.5) to 5.02% (GPT-5.4-mini) of package mentions, and from 2.15% to 3.39% of generations [@churilov2026range, p. 6; @churilov2026range, p. 7].
- [V] Python is higher than JavaScript for every model, by 2.34 to 3.47 percentage points [@churilov2026range, p. 7].
- [V] LLM-written prompts give higher rates than Stack Overflow prompts: pooled 4.79% and 5.44% against 2.28% and 3.10% [@churilov2026range, p. 7].
- [V] 104 names (88 PyPI, 16 npm) are invented by all five models; 54 of them are one character away from a registered package [@churilov2026range, p. 9]. The mean overlap between models is modest (Jaccard 0.219) [@churilov2026range, p. 8].
- [V] The live re-check lowered every model's rate by about a fifth. The biggest correction was import names of real packages, 144–207 mentions per model [@churilov2026range, p. 10].
- [V] 25 of 2,282 invented names (1.1%) were registered within about six months; one npm placeholder carried a malicious-package record [@churilov2026range, p. 12].
- [V] Publishing names made no detectable difference (0 of 87 published vs 2 of 101 unpublished, p = 0.50), but the test can only detect large effects [@churilov2026range, p. 12].
- [V] At least 23 suggested names had previously hosted malware that the registries later removed [@churilov2026range, p. 12].

### Limitations and weaknesses
- [A] Smaller, fine-tuned and quantized local models, and agentic setups, are out of scope [@churilov2026range, p. 14].
- [A] The prompts may already be in 2026 training data, and no new held-out prompts were used [@churilov2026range, p. 14].
- [A] The pipreqs map covers only about 1,157 import names, and some install forms are missed [@churilov2026range, p. 14].
- [I] The paper says it follows Spracklen's extraction [@churilov2026range, p. 5], but it parses imports, which Spracklen rejects [@spracklen2024we, p. 6]. Its "level with 2024's best model" compares a pooled 3.63% with Spracklen's Python-only 3.59% [@spracklen2024we, p. 20]; its own Python-only rate for Haiku is 4.38% [@churilov2026range, p. 7].
- [I] One sample per prompt, so persistence is not measured.
- [I] It is the fourth version of a fast-revised single-author paper, and several earlier numbers could not be reproduced [@churilov2026range, p. 10].

### Gaps and future work this paper leaves open
- [A] G1: agentic setups are named as untested [@churilov2026range, p. 14].
- [A] G4: quantized local models are out of scope [@churilov2026range, p. 14].
- [I] G3: this is the most complete protocol in our set, but its import map is small [@churilov2026range, p. 14] and it was never checked against human labels.
- [A] G5: the author proposes monitoring registrations [@churilov2026range, p. 15]; the six-month window and low power leave long-term weaponisation open [@churilov2026range, p. 12].
- [I] G2: registered names and names with a malware history [@churilov2026range, p. 12] show why a plain existence check is not enough.

### Why it matters for your research
This is the protocol to copy: two lookups per registry, two rounds, a creation-date check, OSV lookups and confidence intervals, all runnable on a laptop. It also gives the best current base rate for frontier API models. Cite it as a preprint, report per-language and pooled rates separately, and split results by prompt source, because that factor flipped since 2024.

### Connections to other papers
- [V] Same prompts as spracklen2024we, but two results reverse: language direction [@spracklen2024we, p. 7] (contradiction C1) and prompt source [@spracklen2024we, p. 20] (C2).
- [V] Registration evidence is compatible with okwor2026hallucination: 0 of 1,641 private names after 4 days and 22 of 149 public names, none malicious [@okwor2026hallucination, p. 5] (C7).
- [V] Python above JavaScript agrees with krishna2025importing [@krishna2025importing, p. 8].
- [V] Import-name confusion also appears in zhao2025hfuzzer, where 34 of 46 GPT-4o hallucinations are wrong install names for correct imports [@zhao2025hfuzzer, p. 9].
