## Novice Developers Produce Larger Review Overhead for Project Maintainers while Vibe Coding
> **Takeaway:** On GitHub, AI-agent pull requests from less experienced users were bigger, accepted less often and needed more review than those from experienced users. For us, this means the human's experience is a variable to control when studying vibe coding.

| Item | Detail |
|---|---|
| Authors | Syed Ammar Asdaque, Imran Haider, Muhammad Umar Malik, Maryam Abdul Ghafoor, Abdul Ali Bangash |
| Year · Venue | 2026 · Proceedings of the 23rd International Conference on Mining Software Repositories (MSR 2026) |
| Status | Peer-reviewed (5-page paper; track not stated in the PDF). Our copy is the arXiv v1 version |
| Identifier | DOI 10.1145/3793302.3793597 (arXiv 2602.23905) |
| Paper type | Empirical study (repository mining) |
| Relevance to us | Low — RQ3 (indirect), RQ4, RQ5 |

### In plain words
Some people hope that AI agents let beginners do the work of experienced developers. This paper tests that idea with real open-source contributions. A pull request (PR) is a proposed code change that project maintainers review before accepting ("merging") it. The authors compared AI-agent PRs from low-experience and high-experience GitHub users [@asdaque2026novice, p. 1]. They asked whether beginners' contributions are larger and harder to get accepted [@asdaque2026novice, p. 2]. This matters because if beginners' AI code pushes more checking work onto reviewers, the speed gain is partly an illusion.

### How they did it
1. They used AIDev, a public dataset of pull requests created with AI agents such as Copilot, Codex, Claude Code, Cursor and Devin. They kept projects with more than 100 stars [@asdaque2026novice, p. 2].
2. They removed bot accounts (usernames containing "bot" or matching known agent names) [@asdaque2026novice, p. 2].
3. They gave each user an experience score: total commits divided by GitHub account age. The lower two quartiles (bottom half) became "low experience", the upper two "high experience" [@asdaque2026novice, p. 2].
4. They measured each PR's size (commits, files changed) and its review effort (acceptance rate, days to merge, review comments) [@asdaque2026novice, p. 2].
5. They compared groups with Mann-Whitney U tests (a comparison that does not assume normally distributed data) and Chi-square tests for acceptance, corrected for running many tests [@asdaque2026novice, p. 2; @asdaque2026novice, p. 4].
6. They read 15 low-experience feature PRs with the most review comments to see what caused friction [@asdaque2026novice, p. 3].

### Data and setup
- AIDev subset: 33,596 PRs and 1,796 users before filtering [@asdaque2026novice, p. 2].
- Final sample: 22,953 PRs from 1,719 users (860 low-experience, 859 high-experience) [@asdaque2026novice, p. 2].
- PRs grouped into 11 categories (for example feature, fix, docs, chore) [@asdaque2026novice, p. 2; @asdaque2026novice, p. 3].
- No comparison with human-only PRs [@asdaque2026novice, p. 2].
- Analysis in Python; replication package on GitHub [@asdaque2026novice, p. 2; @asdaque2026novice, p. 5].

### Key findings
- [V] Low-experience PRs contained 2.15x more commits; for feature PRs, 4.20 vs 1.58 mean commits [@asdaque2026novice, p. 2; @asdaque2026novice, p. 3].
- [V] They changed 1.47x more files [@asdaque2026novice, p. 3].
- [V] They had a 31% lower acceptance rate; for documentation PRs, 75.39% vs 93.06% [@asdaque2026novice, p. 3].
- [V] They took 5.16x longer from creation to merge; for chore PRs, 2.83 vs 0.61 days [@asdaque2026novice, p. 3].
- [V] They drew 4.52x more review comments. But both groups averaged under 1 comment per PR in every category, so the big ratio rests on small numbers [@asdaque2026novice, p. 3; @asdaque2026novice, p. 4].
- [A] From 15 PRs, the authors name two friction sources: "Infrastructure Mismatch" (AI code that ignores build or CI rules) and "Integration Friction" (AI code missing system context) [@asdaque2026novice, p. 3; @asdaque2026novice, p. 4].
- [A] The authors conclude that low-experience users "focus on generating more code while shifting verification burden onto reviewers" [@asdaque2026novice, p. 1].

### Limitations and weaknesses
- [A] Commit count "conflates activity with skill": someone experienced but rarely active on GitHub counts as a novice [@asdaque2026novice, p. 4].
- [A] Results may not hold under a broader definition of vibe coding [@asdaque2026novice, p. 4].
- [A] Project review policies may influence acceptance and comments [@asdaque2026novice, p. 4].
- [I] The two groups may work on different projects and use different agents; neither is controlled.
- [I] It is unclear whether tests treat each PR as independent. Users made about 13 PRs each on average, so busy users could dominate [@asdaque2026novice, p. 2].
- [I] Results are ratios of means without effect sizes or confidence intervals, and "31% lower" is not stated as relative or absolute [@asdaque2026novice, p. 3].
- [I] No code quality is measured; review effort is only a proxy. The friction categories rest on 15 PRs and two examples.

### Gaps and future work this paper leaves open
- [A] Study industrial settings and follow developers over time [@asdaque2026novice, p. 4].
- [A] Train developers in verification skills [@asdaque2026novice, p. 4].
- [I] G6: it suggests operator experience matters, which a human-steered vs autonomous reconstruction study should measure or fix.
- [I] Add code-level quality measures (static analysis, defects after merge) to separate review friction from code quality.

### Why it matters for your research
This paper does not study app reconstruction or measure code quality, so its relevance is low. Its one useful lesson is design: if humans steer the AI in your study, record their experience, because it changes outcomes. A better skill measure than commit count is advisable, such as a short pre-test. Also avoid its statistical weak spot: if one person or app contributes many data points, use models that account for that grouping.

### Connections to other papers
- [V] Agrees with borg2026echoes that the human's skill matters: higher Java skill improved later code health more than AI use did [@borg2026echoes, p. 40].
- [V] Its definition of vibe coding (supervised agent use) differs from fawzy2026vibe's minimal-review prompting [@fawzy2026vibe, p. 1]; do not pool (evidence matrix C9).
- [V] Its higher review burden converges with practitioners' "fast but flawed" view [@fawzy2026vibe, p. 8] (evidence matrix G-A8, rated weak).
- [V] Like he2026speed, it mines GitHub data for agent use [@he2026speed, p. 4], but compares users rather than before and after adoption.
