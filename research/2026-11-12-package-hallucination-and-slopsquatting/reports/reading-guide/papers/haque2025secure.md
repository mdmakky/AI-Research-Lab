## Secure or Suspect? Investigating Package Hallucinations of Shell Command in Original and Quantized LLMs
> **Takeaway:** This is the only study in our set that directly varies quantization, the compression that lets models run on ordinary hardware. For small Qwen models writing Go install commands, 4-bit versions invented package paths almost every time. But the effect is not uniform, and the measurement counts file paths as "packages", so treat it as weak evidence.

| Item | Detail |
|---|---|
| Authors | Md Nazmul Haque, Elizabeth Lin, Lawrence Arkoh, Biruk Tadesse, Bowen Xu |
| Year · Venue | 2025 · arXiv |
| Status | Preprint (not peer-reviewed). The PDF still carries conference-template residue, suggesting an early draft |
| Identifier | DOI 10.48550/arxiv.2512.08213 (arXiv 2512.08213) |
| Paper type | Empirical measurement study (5 model sizes × 3 precision levels × 3 prompt sets) |
| Relevance to us | High — RQ1, RQ2, RQ4, RQ5 |

### In plain words
Most people who run AI models on a laptop use quantized versions. Quantization stores the model's numbers with fewer bits (for example 8 or 4 instead of 16 or 32), so the model needs less memory but may become less accurate. This paper asks whether quantized models invent more package names when they write shell commands that install Go packages [@haque2025secure, p. 2]. In Go, packages are named by web addresses such as a GitHub repository path and installed with go get. An attacker could squat an invented path by creating a free GitHub account and repository with that name [@haque2025secure, p. 2; @haque2025secure, p. 7].

### How they did it
1. Build three prompt sets with GPT-4o: Stack Overflow Go questions rewritten as tasks, MBPP programming tasks adapted to Go, and paraphrased descriptions from the awesome-go package list [@haque2025secure, p. 4].
2. Run Qwen models of five sizes (0.5B to 14B) at full precision, 8-bit and 4-bit, using the bitsandbytes library [@haque2025secure, p. 4; @haque2025secure, p. 5].
3. Take the package paths from go get or go install commands and request each address over the network. An unreachable address counts as hallucinated [@haque2025secure, p. 4].
4. Check reachable packages for known vulnerabilities in OSV, a public vulnerability database [@haque2025secure, p. 4].
5. Report the Package Hallucination Rate (hallucinated strings divided by all generated package strings) and the Vulnerable Package Rate [@haque2025secure, p. 4; @haque2025secure, p. 5].

### Data and setup
- 5,435 Stack Overflow, 974 MBPP and 1,746 awesome-go prompts, 8,155 in total, each run on 15 model configurations [@haque2025secure, p. 4].
- The number of package strings per condition ranges from 0 to 21,439 [@haque2025secure, p. 6].
- Run on one A100 GPU [@haque2025secure, p. 5].
- Exact model versions, prompt wording, temperature, the extraction method and the date of the checks are not reported. Each prompt appears to have been run once, with no statistical tests.
- A replication package is offered at an anonymous link [@haque2025secure, p. 2].

### Key findings
- [V] At 4-bit, the 0.5B model invented 96.11%, 98.78% and 96.66% of package strings on the three prompt sets, against 41–54% at full precision [@haque2025secure, p. 6].
- [V] The 3B model at 4-bit reached 92.09%, 97.60% and 87.74% [@haque2025secure, p. 6].
- [V] Exception: the 7B model on Stack Overflow prompts fell from 34.00% to 10.21% at 4-bit, while producing far fewer package strings [@haque2025secure, p. 5].
- [A] The authors call the 8-bit effect a "moderate and consistent increase" [@haque2025secure, p. 5]. [V] Their own table shows several cells falling at 8-bit and one rising sharply, 48.39% to 69.59% for 7B on MBPP [@haque2025secure, p. 6].
- [V] Some rates rest on tiny counts: the 3B model produced 3 and 1 package strings on Stack Overflow at full and 8-bit precision, and none on MBPP [@haque2025secure, p. 6].
- [V] In the one breakdown table, 2,333 of 4,751 "hallucinated" strings (49%) are file paths or free-form text, not installable package paths [@haque2025secure, p. 8].
- [V] The quantization effect on known-vulnerable packages is mixed: up from 12.89% to 19.58% for 7B on Stack Overflow, down in other cells [@haque2025secure, p. 5; @haque2025secure, p. 6].
- [A] The authors recommend 8-bit for constrained settings and "extreme caution" with 4-bit [@haque2025secure, p. 7].

### Limitations and weaknesses
- [A] Existence was checked by web reachability for simplicity; an unreachable address might still be a valid Go package, and the authors suggest running go get instead [@haque2025secure, p. 7].
- [A] Prompts were not varied [@haque2025secure, p. 7].
- [I] The summary percentages in the discussion use only the Stack Overflow set [@haque2025secure, p. 7], and the "consistent increase" claim goes beyond the data.
- [I] Counting file paths and free text as packages [@haque2025secure, p. 8] overstates the number of squattable names.
- [I] One model family and one quantization library. Laptop runtimes such as Ollama use a different format (GGUF), so the results may not transfer.
- [I] GPT-4o kept only tasks it answered with install commands [@haque2025secure, p. 4], which biases the prompts towards install-heavy tasks.
- [I] No repeated runs, so persistence of names is not measured, and whether invented GitHub paths could actually be registered was not checked.

### Gaps and future work this paper leaves open
- [I] G4: this is the only quantization study, and it covers Go only with bitsandbytes [@haque2025secure, p. 6]. The effect of the quantization levels shipped by local runtimes on PyPI and npm is untested.
- [A] G1: the authors call for verifying packages by actually running go get [@haque2025secure, p. 7]; no study yet records real installs.
- [I] G3: its reachability check and counting of non-package strings are a clear example of why the field needs a shared measurement rule.
- [I] G2: the setting suggests a simple guard: check every install target against the registry or module proxy before running it.

### Why it matters for your research
It is the main motivation for G4, because quantized small models are exactly what a laptop runs. It is also a list of pitfalls to avoid: count only installable names, report every denominator, run each prompt several times, and use a proper registry lookup. Quote its 4-bit numbers only with the caveats above.

### Connections to other papers
- [V] spracklen2024we ran all open models in quantized form [@spracklen2024we, p. 6], so model size and quantization are mixed up in earlier results (contradiction C3).
- [A] churilov2026range explicitly leaves quantized local models out of scope [@churilov2026range, p. 14].
- [V] okwor2026hallucination runs local models through Ollama but reports no hallucination rate [@okwor2026hallucination, p. 3].
- [V] Go adds to other ecosystems studied elsewhere, such as Rust [@zheng2026when, p. 5].
