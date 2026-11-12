## Faster Code, Deeper Debt? A Multivocal Literature Review on Technical Debt and Its Early Signs in LLM-Assisted Software Development
> **Takeaway:** This review maps what academics and practitioners say about long-term "technical debt" from AI-written code. Its clearest message for us is that there are no standard benchmarks or AI-specific metrics for this debt, and most evaluations only check whether code works.

| Item | Detail |
|---|---|
| Authors | Ramtin Ehsani, Shriya Rawal, Yuanfang Cai, Preetha Chatterjee |
| Year · Venue | 2026 · ACM Transactions on Software Engineering and Methodology (TOSEM) |
| Status | Peer-reviewed. Our copy is the arXiv pre-acceptance manuscript, so counts may differ slightly from the published version |
| Identifier | DOI 10.1145/3820165 (arXiv 2606.14796) |
| Paper type | Multivocal literature review (secondary study of papers plus blogs and industry reports) |
| Relevance to us | High — RQ3 (main), RQ4, RQ5; RQ1 (minor) |

### In plain words
"Technical debt" means shortcuts in code that save time now but make later changes harder, like a loan that must be repaid with interest. AI tools let people write code very fast, and many worry this creates hidden debt. The authors collected what both researchers and practitioners have written about this up to January 2026. They sorted the material into types of debt, ways to reduce it, tools to detect it, and benchmarks and metrics to measure it [@ehsani2026faster, p. 3; @ehsani2026faster, p. 7]. This matters because a rebuilt app must be maintained, and we need to know how debt can even be measured.

### How they did it
1. They followed published guidelines for a multivocal literature review (a review that includes "grey" sources such as blogs and company reports as well as peer-reviewed papers) [@ehsani2026faster, p. 6].
2. One search string combined 13 kinds of debt (code, design, documentation and others) with AI terms such as "LLM", "ChatGPT" and "Copilot" [@ehsani2026faster, p. 9].
3. Grey sources came from Google (first 10 result pages). Each was scored on 22 quality criteria, and only those scoring above 11 were kept [@ehsani2026faster, p. 9].
4. Academic sources came from four digital libraries. Two authors screened them, then added papers by snowballing (following reference lists both ways). Only peer-reviewed work was kept [@ehsani2026faster, p. 11; @ehsani2026faster, p. 12].
5. Two authors extracted data from every source; a third resolved conflicts. Agreement was high (Cohen's kappa, a chance-corrected agreement score, of 0.93 for debt types) [@ehsani2026faster, p. 12; @ehsani2026faster, p. 13].
6. They coded each source against a known 13-type debt taxonomy and added new categories where needed. Results are counts of mentions, not measured effects [@ehsani2026faster, p. 14; @ehsani2026faster, p. 16].

### Data and setup
- 104 sources in total: 31 peer-reviewed papers and 73 grey sources [@ehsani2026faster, p. 1; @ehsani2026faster, p. 3].
- Academic search: 551 hits, 27 kept after screening, plus 4 from snowballing [@ehsani2026faster, p. 11; @ehsani2026faster, p. 12].
- Grey search: about 375,000 Google hits, 132 unique sources checked, 73 kept [@ehsani2026faster, p. 9].
- Grey sources by tier: 38 company blogs, 18 developer platforms, 14 media outlets, 3 personal blogs [@ehsani2026faster, p. 10].
- Search done in January 2026 [@ehsani2026faster, p. 8].
- Supplementary data on figshare [@ehsani2026faster, p. 4].

### Key findings
- [V] The most-mentioned debt types (academic / grey mentions): code 14 / 56, design 2 / 30, documentation 0 / 17 [@ehsani2026faster, p. 16].
- [V] Six new AI-related debt types were proposed: governance (0 / 19), prompt (8 / 5), fast-integration (0 / 13), data (9 / 0), ethical (3 / 2) and provenance (1 / 1) [@ehsani2026faster, p. 16].
- [A] "Fast-integration debt" means quickly adding AI output without checking it. The authors link it directly to vibe coding [@ehsani2026faster, p. 17]. It rests on grey sources only.
- [V] The main advice in practice is human review: 58 of 73 grey sources recommend a human in the loop [@ehsani2026faster, p. 20].
- [A] No standard benchmarks or datasets exist for debt in AI code; benchmarks focus "almost exclusively on binary correctness" (works or not) [@ehsani2026faster, p. 23].
- [A] Existing tools such as SonarQube are seen as not designed for AI-specific debt, and no new metric is widely used [@ehsani2026faster, p. 22; @ehsani2026faster, p. 24].
- [A] Commercial AI-aware quality tools are rarely tested independently [@ehsani2026faster, p. 28].
- [A] Reported from He et al. (not this review's own finding): Cursor adoption was followed by about +30% static-analysis warnings and +41% code complexity [@ehsani2026faster, p. 18].
- [I] The review leaves out the original study's caveat: under another estimator these quality effects turn negative and non-significant [@he2026speed, p. 16]. Cite he2026speed, not this review, for these numbers.

### Limitations and weaknesses
- [A] Search terms centred on "debt" may miss studies framed as maintainability or code quality [@ehsani2026faster, p. 30].
- [A] Company blogs make up 52% of the grey sources, which may bias results [@ehsani2026faster, p. 30].
- [A] English only; search-engine rankings are undocumented [@ehsani2026faster, p. 30].
- [I] Counting how often something is mentioned is not the same as evidence that it happens. Two of the new debt types (governance, fast-integration) have no academic support at all [@ehsani2026faster, p. 16].
- [I] No quality appraisal of the 31 academic papers is described, so weak position papers count like empirical studies [@ehsani2026faster, p. 11; @ehsani2026faster, p. 21].
- [I] The rule excluding correctness-only studies means maintainability comparisons that never say "debt" may be missing (for example, molison2025llm is not cited) [@ehsani2026faster, p. 12].
- [I] It is about AI-assisted coding in general, not app reconstruction.

### Gaps and future work this paper leaves open
- [A] Build community benchmarks and new metrics for maintainability, adaptability and reproducibility across runs [@ehsani2026faster, p. 29].
- [A] Run longitudinal studies of how AI-related debt builds up over time [@ehsani2026faster, p. 25].
- [I] G1: its finding that benchmarks check correctness only supports our main gap, a joint check of fidelity and maintainability [@ehsani2026faster, p. 23].
- [I] G3: it reports that debt tools disagree, which motivates testing whether maintainability tools agree for AI-built apps [@ehsani2026faster, p. 5].
- [I] Its grey-only categories (fast-integration debt) could be tested empirically with controlled vibe-coding sessions.

### Why it matters for your research
Use this paper as a map, not as proof. Its debt taxonomy can structure the maintainability part of your study, and its tool list (SonarQube, ESLint, Pylint, CodeScene) shows common measuring options [@ehsani2026faster, p. 23]. Cite it for the field-level gap: no standard maintainability benchmark for AI code. Do not cite it for effect sizes; for the Cursor numbers, cite he2026speed directly.

### Connections to other papers
- [A] Re-reports he2026speed's figures [@ehsani2026faster, p. 18]; the primary study adds that the warning rise runs mainly through more code [@he2026speed, p. 8]. Count the effect once.
- [V] Its "fast-integration" concern agrees with practitioners' "fast but flawed" view of vibe-coded output in fawzy2026vibe [@fawzy2026vibe, p. 8]. Both rest on grey sources (evidence matrix G-A8).
- [V] Its claim that tools disagree fits the conflicting results from different instruments in our corpus, such as borg2026echoes' CodeHealth [@borg2026echoes, p. 13] and he2026speed's SonarQube totals [@he2026speed, p. 7] (C3).
