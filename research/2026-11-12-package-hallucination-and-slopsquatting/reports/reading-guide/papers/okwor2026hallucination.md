## From Hallucination to Registration: Do the Package Names That LLMs Invent Actually Get Claimed?
> **Takeaway:** This paper asks whether invented package names actually get registered. Fresh names from five local models were all still free four days later. Of 149 names already circulating publicly, 22 were registered, mostly as harmless placeholders, and none was malicious. It is a single-author Zenodo preprint with a very short time window, so use it only to support stronger evidence.

| Item | Detail |
|---|---|
| Authors | Daniel Okwor (Orygn LLC) |
| Year · Venue | 2026 · Zenodo |
| Status | Preprint (Zenodo self-deposit, not peer-reviewed, single author). We treat it as grey literature (tier 4) |
| Identifier | DOI 10.5281/zenodo.21199426 (concept DOI; the PDF prints the version DOI 10.5281/zenodo.21199427) |
| Paper type | Measurement study of registration status, with content triage and an offline install demo |
| Relevance to us | Medium — RQ2, RQ4, RQ5 |

### In plain words
A package hallucination is when an AI model suggests a code library that does not exist in a public registry such as PyPI (Python) or npm (JavaScript). Earlier studies count how often this happens; the author calls that exposure. This paper looks at the next step, harm: are the invented names registered, by whom, and with what intent [@okwor2026hallucination, p. 1; @okwor2026hallucination, p. 2]? It produces its own names with small open models run locally through Ollama, a free program for running models on your own computer [@okwor2026hallucination, p. 3]. It also inspects a public list of previously reported names.

### How they did it
1. Generate. Five local models (qwen2.5-coder:7b, deepseek-coder:6.7b, codellama:13b, codestral:22b, gpt-oss:20b) wrote Python and JavaScript solutions at temperatures 0.7 and 1.0 [@okwor2026hallucination, p. 3].
2. Extract. Code was parsed, import names were mapped to package names, names were normalised with PEP 503 (PyPI's rule for treating spelling variants as one name), and standard-library modules were dropped [@okwor2026hallucination, p. 3].
3. Two checks. A name counts as invented only if it is missing from a frozen registry snapshot taken on 30 June 2026 and the live registry also returns "not found" [@okwor2026hallucination, p. 3].
4. Validate. The check was tested on 17 real and 8 fake names and classified all correctly [@okwor2026hallucination, p. 4].
5. Inspect public names. 149 names from the Trend Micro and DepScope datasets were checked for registration date and, by reading setup and manifest files only, sorted into malicious, defensive placeholder, organic (an unrelated real package) or individual reservation [@okwor2026hallucination, p. 4].
6. Demonstrate the payload route. A harmless test package was installed in an offline lab to show code running at install time [@okwor2026hallucination, p. 7].

### Data and setup
- 6,800 generations, giving 1,641 confirmed invented names [@okwor2026hallucination, p. 4].
- All names were re-checked live on 4 July 2026, four days after the snapshot [@okwor2026hallucination, p. 5].
- No hallucination rate is reported. The task set, prompts, seeds, quantization level and hardware are not reported.
- Code is promised for later deposit and the raw name list is withheld [@okwor2026hallucination, p. 8].
- No funding or conflict-of-interest statement, despite the company affiliation [@okwor2026hallucination, p. 1].

### Key findings
- [V] No saturation: new names kept appearing at almost the same pace (0.228 against 0.247 new names per generation), and 450 of 455 new names came from a single model [@okwor2026hallucination, p. 4].
- [V] None of the 1,641 self-generated names was registered after four days. The rule of three (if zero of n cases occur, the true rate is below about 3/n with 95% confidence) bounds this below 0.2% [@okwor2026hallucination, p. 5].
- [V] 22 of 149 public names were registered: 19 defensive placeholders, 1 organic collision, 1 individual reservation, 1 typosquat from 2019, and 0 malicious (upper bound about 14%) [@okwor2026hallucination, p. 5; @okwor2026hallucination, p. 6].
- [V] All 19 placeholders carry the summary "Benign slopsquatting research package" [@okwor2026hallucination, p. 5]. [A] The author attributes them to one anonymous operator, using registry metadata that is withheld [@okwor2026hallucination, p. 6].
- [V] Code ran at install time under pip (via setup.py) and npm (via a postinstall script), before the package was ever imported [@okwor2026hallucination, p. 7].
- [A] The public npm name mirror is unreliable [@okwor2026hallucination, p. 3]. [V] This is partly supported by 11 older names the mirror missed [@okwor2026hallucination, p. 7].
- [A] Claims from grey sources, such as more than 30,000 downloads of one registered invented name, are repeated but not verified here [@okwor2026hallucination, p. 2].

### Limitations and weaknesses
- [A] "Zero malicious" is not zero risk: a placeholder can be turned malicious in a later release [@okwor2026hallucination, p. 8].
- [A] The registered sample is small and biased towards names claimed by defenders, and one person assigned the labels [@okwor2026hallucination, p. 6; @okwor2026hallucination, p. 8].
- [A] Names come from self-generated output, not real production traffic [@okwor2026hallucination, p. 8].
- [I] The 0 of 1,641 result was close to certain by design: the names were private and checked after only four days [@okwor2026hallucination, p. 5].
- [I] Reading only setup and manifest files can miss malicious code inside modules or wheels [@okwor2026hallucination, p. 4].
- [I] Cited figures from other papers are misreported. Spracklen's 21.7% is described as a share "of generations" [@okwor2026hallucination, p. 1], but Spracklen counts per package [@spracklen2024we, p. 7]. Churilov's numbers are quoted from superseded versions [@churilov2026range, p. 10].

### Gaps and future work this paper leaves open
- [A] G1: the author proposes moving from self-generated output to live coding-agent traffic [@okwor2026hallucination, p. 8].
- [A] G5: the author proposes to keep watching the 1,641 names [@okwor2026hallucination, p. 8]; a four-day window cannot show long-term weaponisation.
- [I] G2: registered placeholders pass a plain existence check [@okwor2026hallucination, p. 5], and could be weaponised later [@okwor2026hallucination, p. 8]. A useful guard must handle them.
- [I] G4: it runs Ollama models but reports neither a rate nor a quantization level [@okwor2026hallucination, p. 3].
- [I] G3: its two-check gate and the npm-mirror warning are reusable pieces of a shared protocol.

### Why it matters for your research
This is the closest template for a laptop-scale pipeline: local Ollama models, a frozen snapshot as a fast first filter, and a live registry check to confirm. Use the live registry, not the npm mirror, as ground truth. Treat its registration results as weak support for the view that weaponised slopsquatting is rare so far, not as proof.

### Connections to other papers
- [V] Compatible with churilov2026range, where 25 of 2,282 names were registered within about six months, one with malware [@churilov2026range, p. 12] (C7).
- [V] Mostly single-model names agree with spracklen2024we, where 81% of distinct names came from one model [@spracklen2024we, p. 10].
- [V] The install-time demo matches older malware data: 56% of real malicious packages run at install time [@ohm2020backstabbers, p. 11].
