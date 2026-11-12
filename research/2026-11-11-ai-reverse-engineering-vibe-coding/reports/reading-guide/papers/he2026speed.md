## Speed at the Cost of Quality: How Cursor AI Increases Short-Term Velocity and Long-Term Complexity in Open-Source Projects
> **Takeaway:** In real open-source projects, adopting the agentic coding tool Cursor gave a short burst of extra code, while code complexity rose and stayed higher. The quality result is not robust to every statistical method, so treat it as strong-but-contested evidence, not settled fact.

| Item | Detail |
|---|---|
| Authors | Hao He, Courtney Miller, Shyam Agarwal, Christian Kästner, Bogdan Vasilescu |
| Year · Venue | 2026 · Proceedings of the 23rd International Conference on Mining Software Repositories (MSR 2026) |
| Status | Peer-reviewed. Our copy is the arXiv v3 version (with appendices), so page numbers follow that copy |
| Identifier | DOI 10.1145/3793302.3793349 (arXiv 2511.04427) |
| Paper type | Empirical study (quasi-experimental causal analysis of GitHub repository data) |
| Relevance to us | High — RQ3 (main), RQ4, RQ5 |

### In plain words
Many developers now use AI coding agents that can edit many files on their own. People claim these tools make teams faster, but nobody knew whether that speed lasts or whether the code gets worse. The authors looked at real open-source projects on GitHub that started using Cursor, an AI-powered code editor with an "agent" mode that can plan, edit and debug code with the human mainly supervising [@he2026speed, p. 3]. They compared these projects with similar projects that did not adopt Cursor, month by month. This matters because if AI speed is bought with harder-to-maintain code, the speed may not pay off later.

### How they did it
1. Find adopters. They searched GitHub for Cursor configuration files (such as .cursorrules). The first commit of such a file counts as the moment a project "adopted" Cursor [@he2026speed, p. 4].
2. Find look-alike controls. For each adopter they picked similar projects that never adopted Cursor, using propensity-score matching (a statistical way to find projects with a similar history of activity, size and popularity) [@he2026speed, p. 4; @he2026speed, p. 5].
3. Measure every month. For each project and month they counted commits and lines added (speed), and ran SonarQube (a widely used code-checking tool) to get static-analysis warnings, code duplication and cognitive complexity (a score for how hard code is to understand) [@he2026speed, p. 5].
4. Compare before and after. They used difference-in-differences (comparing how adopters changed over time against how controls changed, so shared trends cancel out). The main version is the Borusyak imputation estimator, chosen because simpler methods can be biased when projects adopt at different times [@he2026speed, p. 6].
5. Test how speed and quality feed into each other. A second model (Arellano-Bond dynamic panel, a method for data where this month depends on last month) checked whether more complexity or warnings slow down later work [@he2026speed, p. 6; @he2026speed, p. 8].
6. Robustness checks. They re-ran the analysis with two other estimators and on many subsets [@he2026speed, p. 9; @he2026speed, p. 16].

### Data and setup
- 806 GitHub projects with at least 10 stars that adopted Cursor, with adoption dates between Jan 2024 and Mar 2025 and most adoptions between Aug 2024 and Mar 2025 [@he2026speed, p. 2; @he2026speed, p. 4].
- 1,380 matched control projects in the text; a table lists 801 treated and 1,172 control projects with 21,699 project-months [@he2026speed, p. 2; @he2026speed, p. 17]. The paper does not explain the difference.
- Monthly data from Jan 2024 to Aug 2025 [@he2026speed, p. 5].
- Main languages: TypeScript 366, Python 118, JavaScript 60, Go 36, Rust 24 projects [@he2026speed, p. 4].
- The comparison is against "current practice", not against no AI: controls may use Copilot or ChatGPT without leaving traces [@he2026speed, p. 7].
- Replication package on Zenodo [@he2026speed, p. 11].

### Key findings
- [V] Overall, lines added rose by +28.58% and commits by +2.63% (not significant) [@he2026speed, p. 7].
- [V] The speed boost is short-lived: lines added +281.3% in month 1 and +48.4% in month 2, then no significant effect [@he2026speed, p. 8].
- [V] With the main estimator, static-analysis warnings rose by +30.26% and code complexity by +41.64% (both p < 0.001); duplication +7.03% was not significant [@he2026speed, p. 7].
- [V] These quality effects depend on the estimator. Another method (Callaway–Sant'Anna) gives negative, non-significant results: warnings −10.49%, complexity −3.80%. The authors say the quality findings need caution [@he2026speed, p. 16].
- [V] Once codebase size is controlled, Cursor has no significant direct effect on warnings, but it still raises complexity (coefficient 0.086, p < 0.01) [@he2026speed, p. 8].
- [V] More complexity and warnings go with slower later work: a 100% rise in complexity or warnings goes with a 64.5% or 50.3% drop in next-month lines added [@he2026speed, p. 8].
- [A] The authors read the warning rise as mostly "more code, more warnings", while complexity is inherently higher in Cursor code [@he2026speed, p. 10].

### Limitations and weaknesses
- [A] Only projects that commit Cursor files are seen, and how much they really used Cursor is unknown. The results are "intent-to-treat" (the effect of adopting, not of using heavily) [@he2026speed, p. 7].
- [A] Unmeasured differences (team skill, practices) may remain despite matching [@he2026speed, p. 7].
- [A] The quality metrics may miss aspects of quality, and complexity metrics were designed for human code [@he2026speed, p. 11].
- [I] Warnings and complexity are totals for the whole project, so they grow with project size. "+30% warnings" mainly means "more code", not more warnings per line (based on [@he2026speed, p. 8]).
- [I] The abstract does not mention the estimator sensitivity reported in the appendix [@he2026speed, p. 16].
- [I] Some numbers are inconsistent: the discussion cites a 25.1% complexity rise, while the tables report +41.64% and a coefficient of about 9% [@he2026speed, p. 10; @he2026speed, p. 7; @he2026speed, p. 8]. Use the table values.
- [I] Quality is measured by static analysis only; no tests or functional correctness are measured.

### Gaps and future work this paper leaves open
- [A] Replicate with other and newer AI tools, in company (enterprise) settings and in more languages [@he2026speed, p. 7; @he2026speed, p. 11; @he2026speed, p. 16].
- [A] Find out why AI tools produce overly complex code [@he2026speed, p. 11].
- [I] G1: it does not study rebuilding an app from its interface or behaviour. A reconstruction study still has to measure fidelity and maintainability together.
- [I] G3: its quality story changes with the measuring method, which supports checking whether quality tools agree for AI-built apps.

### Why it matters for your research
This is the strongest real-world causal evidence in our set that agent-style coding can raise code complexity. It does not study reconstruction, so it informs your quality question (RQ3) by analogy only. Reuse its metric set: SonarQube warnings, cognitive complexity and duplication. Avoid its main weakness: always normalise counts by code size (for example per 1,000 lines), and check results with more than one method. When you quote "+30% warnings / +41.6% complexity", always add that they are estimator-sensitive.

### Connections to other papers
- [V] Contrasts with borg2026echoes: a randomised experiment found no significant difference when a second developer evolved AI-assisted code [@borg2026echoes, p. 33; @borg2026echoes, p. 38]. Our evidence matrix treats the two as not necessarily in conflict (contradiction C1).
- [A] ehsani2026faster repeats this paper's +30% / +41% figures without the caveats; count the effect once, from this paper [@ehsani2026faster, p. 18].
- [V] Consistent with the idea that AI adds code volume: AI-assisted outliers of up to 10,788 lines in borg2026echoes [@borg2026echoes, p. 30], and architectural smells that track code size in zhu2026understanding [@zhu2026understanding, p. 8].
- [V] Uses a different meaning of "vibe coding" from fawzy2026vibe [@fawzy2026vibe, p. 1], so results should not be pooled (C9).
