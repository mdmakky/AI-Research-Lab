## Echoes of AI: Investigating the downstream effects of AI assistants on software maintainability
> **Takeaway:** When a second developer had to change code that someone else wrote with an AI assistant, they were not clearly slower and the code quality was not clearly worse. The study can only rule out large effects, and it used late-2024 assistants, not today's coding agents.

| Item | Detail |
|---|---|
| Authors | Markus Borg, Dave Hewett, Nadim Hagatulah, Noric Couderc, Emma Söderberg, Donald Graham, et al. |
| Year · Venue | 2026 · Empirical Software Engineering (journal) |
| Status | Peer-reviewed; preregistered (registered report) |
| Identifier | DOI 10.1007/s10664-026-10889-1 |
| Paper type | Controlled experiment (two phases; Phase 2 is a randomised controlled trial) |
| Relevance to us | High — RQ3 (main), RQ4, RQ5 |

### In plain words
Most studies ask whether AI helps developers write code faster. This paper asks a different question: is AI-assisted code harder for the next person to change? That is what "maintainability" means here, how easily another developer can later evolve the code [@borg2026echoes, p. 1; @borg2026echoes, p. 2]. The authors ran a two-step experiment with mostly professional developers. One group wrote a feature, some with AI and some without, and a second group then extended that code without AI. This matters because a rebuilt app is only useful if people can keep working on it.

### How they did it
1. Preregistration. The plan, hypotheses and analysis were fixed and published before data collection (a registered report) [@borg2026echoes, p. 2; @borg2026echoes, p. 9].
2. Phase 1 (write). Participants added a feature to a small Java web app, with or without AI. Who used AI was decided by their own preference and habits, not by chance, so Phase 1 is observational [@borg2026echoes, p. 10; @borg2026echoes, p. 43].
3. Phase 2 (evolve). New participants, all without AI, were randomly given a Phase 1 solution, either AI-assisted (treatment) or not (control), and asked to add another feature. This is a randomised controlled trial (RCT: groups are assigned by chance, so differences can be attributed to the treatment) [@borg2026echoes, p. 2; @borg2026echoes, p. 12].
4. Measure. They recorded completion time, CodeHealth (a 1–10 maintainability score from the tool CodeScene), test coverage (share of code run by tests) and perceived productivity (a questionnaire) [@borg2026echoes, p. 13; @borg2026echoes, p. 14].
5. Analyse two ways. Classic significance tests plus Bayesian models (which give the probability that an effect is above or below zero), adjusted for Java skill and habitual AI use [@borg2026echoes, p. 14; @borg2026echoes, p. 15; @borg2026echoes, p. 16].

### Data and setup
- Base system: RecipeFinder, a deliberately imperfect Java/Spring Boot web app of about 2,000 lines (47 files) [@borg2026echoes, p. 64; @borg2026echoes, p. 65].
- 449 valid sign-ups, 92.2% professional developers [@borg2026echoes, p. 24].
- 151 valid participants overall; Phase 2 had 75 (40 treatment, 35 control) [@borg2026echoes, p. 19; @borg2026echoes, p. 30].
- Tools used in Phase 1: GitHub Copilot 21, ChatGPT 13, Cursor 9, JetBrains AI 5, Claude 4 [@borg2026echoes, p. 27].
- Data collected Oct 2024 to Jan 2025, before agentic tools were common [@borg2026echoes, p. 3; @borg2026echoes, p. 17].
- Automated checks ran in GitHub Actions: 3 acceptance tests per task, CodeScene and JaCoCo coverage [@borg2026echoes, p. 16; @borg2026echoes, p. 17].
- Data and scripts are shared on Zenodo and GitHub [@borg2026echoes, p. 74].

### Key findings
- [V] Phase 2 completion time: median 136 min (evolving AI code) vs 173 min (control); negligible effect, p = 0.56 [@borg2026echoes, p. 33].
- [V] Phase 2 CodeHealth: 8.49 vs 8.44, p = 0.24, not significant [@borg2026echoes, p. 38].
- [V] One Bayesian subgroup effect: code first written with AI by habitual AI users scored +0.10 CodeHealth after evolution (98% probability of a positive effect). This small effect favours AI [@borg2026echoes, p. 39].
- [V] Developer skill mattered more: higher Java skill in Phase 1 gave +0.16 CodeHealth in Phase 2 [@borg2026echoes, p. 40].
- [V] Test coverage (median 0.70 in both groups, p = 0.49) and perceived productivity (p = 0.37) did not differ [@borg2026echoes, p. 35; @borg2026echoes, p. 42].
- [V] Phase 1 (not randomised): AI users finished 30.7% faster (p = 0.0029) [@borg2026echoes, p. 43].
- [V] Phase 1 AI-assisted code introduced more code duplication (23% vs 11%) and more complex conditionals (13% vs 5%), and some AI users added up to 10,788 lines [@borg2026echoes, p. 30; @borg2026echoes, p. 46].
- [A] The authors see code bloat and "cognitive debt" as the main risks, not worse file-level quality [@borg2026echoes, p. 57; @borg2026echoes, p. 58].

### Limitations and weaknesses
- [A] The trial is underpowered: 75 of 128 planned Phase 2 participants, so only large effects can be ruled out [@borg2026echoes, p. 19; @borg2026echoes, p. 61].
- [A] Short-term only, one small Java system, individual developers, no security analysis [@borg2026echoes, p. 58].
- [A] Many people worked over several sittings, so some times are self-estimated [@borg2026echoes, p. 18].
- [I] Phase 1 groups were chosen by preference, so "AI code" also means "code from people who like AI".
- [I] CodeHealth is a product of the first author's employer and was customised for this study; no open tool was used for the main outcome [@borg2026echoes, p. 13; @borg2026echoes, p. 75].
- [I] Some numbers are inconsistent: the habitual-user speedup is 55.9% in the abstract but about 60% in the results [@borg2026echoes, p. 1; @borg2026echoes, p. 33].
- [I] Code volume, the risk the authors highlight, was not an outcome of the randomised phase.

### Gaps and future work this paper leaves open
- [A] Test third-generation coding agents (such as Claude Code), second developers who also use AI, security, and long-term effects [@borg2026echoes, p. 63].
- [I] G1: this "second developer changes the code" design has never been applied to reconstructed apps [@borg2026echoes, p. 13].
- [I] G3: its static measures and its time measure did not move together, so we still do not know which maintainability tools predict real effort.

### Why it matters for your research
This is the only randomised evidence in our set on whether AI-assisted code is harder to maintain. Its design is directly reusable: give a rebuilt app and the original to a second developer (or an agent), ask for the same small change, and compare time and quality. Copy its preregistration and power analysis habits. Avoid its weak spots: plan enough participants, use an open static-analysis tool alongside any vendor metric, and measure code size as an outcome.

### Connections to other papers
- [V] Contrasts with he2026speed, where Cursor adoption raised project-level complexity [@he2026speed, p. 7]. The tools, scale and metrics differ, so the two need not conflict (evidence matrix C1).
- [V] Its Phase 1 finding of large AI code volume fits with he2026speed's +281.3% lines added in month 1 [@he2026speed, p. 8].
- [A] ehsani2026faster notes that technical-debt tools disagree on what counts as debt, which matters because this paper relies on one tool [@ehsani2026faster, p. 5].
- [V] Like borg2026echoes, asdaque2026novice finds that the human's experience shapes outcomes with AI code [@asdaque2026novice, p. 3].
