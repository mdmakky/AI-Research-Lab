## Vibe Coding in Practice: Motivations, Challenges, and a Future Outlook – a Grey Literature Review
> **Takeaway:** Practitioners who write about vibe coding mostly do it for speed, and they mostly describe the result as "fast but flawed", often skipping quality checks. This is evidence about how people feel and behave, not a measurement of the code.

| Item | Detail |
|---|---|
| Authors | Ahmed Fawzy, Amjed Tahir, Kelly Blincoe |
| Year · Venue | 2026 · Proceedings of the IEEE/ACM 48th International Conference on Software Engineering: Software Engineering in Practice (ICSE-SEIP 2026) |
| Status | Peer-reviewed. Our copy is the arXiv v1 pre-acceptance version; the underlying sources are non-peer-reviewed grey literature |
| Identifier | DOI 10.1145/3786583.3786866 (arXiv 2510.00328) |
| Paper type | Systematic grey literature review with thematic analysis |
| Relevance to us | Medium — RQ1, RQ3 (perceptions only), RQ5 |

### In plain words
"Vibe coding" is a new term, and most of what we know about it comes from blogs and forums, not research papers. The authors define it as building software mainly by describing goals to an AI in plain language, prompting again and again, and barely reviewing the code [@fawzy2026vibe, p. 1]. They read 101 first-hand online accounts and asked four questions. Why do people vibe code, what is it like, what do they think of the code, and how do they check quality [@fawzy2026vibe, p. 2]? This matters for us because your project title says "through vibe coding", and this paper describes what that workflow looks like in practice.

### How they did it
1. They ran a grey literature review (a systematic review of non-peer-reviewed sources such as blogs and forum posts), following published guidelines [@fawzy2026vibe, p. 3].
2. They built a Google search string in six stages, switching to the words practitioners actually use, and checked it against a small set of known key posts [@fawzy2026vibe, p. 3; @fawzy2026vibe, p. 4].
3. They screened results until no new themes appeared, and also followed links from the first 100 results (snowballing) [@fawzy2026vibe, p. 4].
4. Each source was scored 0–3 on five quality criteria (authority, evidence, objectivity, currency, purpose); only sources scoring 10 or more out of 15 were kept [@fawzy2026vibe, p. 4; @fawzy2026vibe, p. 5].
5. They cut each source into "behavioural units" (quotes describing one behaviour or opinion) and grouped them into themes per question. This is thematic analysis (finding recurring patterns in text) [@fawzy2026vibe, p. 5].
6. Results are counts and percentages of quotes per theme [@fawzy2026vibe, p. 6; @fawzy2026vibe, p. 8].

### Data and setup
- 154 sources retrieved, 101 included; 40 dropped for low quality and 13 by the inclusion rules [@fawzy2026vibe, p. 5].
- 518 behavioural units: 140 on motivation, 132 on experience, 114 on perceived code quality, 132 on quality assurance [@fawzy2026vibe, p. 5].
- Inclusion: English, 2022–2025, named author, public full text, and evidence of vibe-coding behaviour [@fawzy2026vibe, p. 4].
- Coding was done mainly by the first author, with a subset cross-checked by a co-author [@fawzy2026vibe, p. 4; @fawzy2026vibe, p. 5].
- No code was inspected; no tools or models were tested.
- Replication package on Zenodo [@fawzy2026vibe, p. 10].

### Key findings
- [V] Speed is the main reason: Speed & Efficiency is 87 of 140 motivation units (62%); Accessibility & Empowerment 20 (14%) [@fawzy2026vibe, p. 6].
- [V] The experience is mostly positive: Instant Success & Flow is 85 of 132 units (64%); Code Breakdown or Abandonment is 14 (11%) [@fawzy2026vibe, p. 8].
- [V] The code is seen as "Fast but Flawed" in 78 of 114 units (68%) and "Fragile or Error-Prone" in 22 (19%); only 3 units (3%) call it high quality [@fawzy2026vibe, p. 8].
- [V] Quality checks are often weak: Skipped QA 48 of 132 units (36%), Uncritical Trust 24 (18%), Delegated QA to AI 13 (10%), Reprompting Instead of Debugging 6 (5%) [@fawzy2026vibe, p. 8].
- [A] The authors describe a "speed–quality trade-off paradox": people knowingly accept flawed code to move fast [@fawzy2026vibe, p. 9].
- [A] They warn of a "new class of vulnerable developers" who can build but not debug, with reported apps lacking login protection or containing hardcoded secrets [@fawzy2026vibe, p. 9].

### Limitations and weaknesses
- [A] The search cannot capture all grey literature, and some quality bias remains [@fawzy2026vibe, p. 10].
- [A] Only people who chose to post online are included, so results do not generalise to all vibe coders [@fawzy2026vibe, p. 10].
- [A] Theme coding is subjective and mostly done by one author [@fawzy2026vibe, p. 10].
- [I] Percentages count quotes, not people, yet the discussion reads them as shares of people [@fawzy2026vibe, p. 9]. One prolific source can contribute many quotes.
- [I] Accounts of careful developers who did not skip quality checks were excluded by design [@fawzy2026vibe, p. 4]. This likely inflates the "Skipped QA" share.
- [I] Maintainability is barely covered: "Sloppy or Low Maintainability" is only 5 units (4%) [@fawzy2026vibe, p. 8].
- [I] No inter-rater agreement statistic is reported.

### Gaps and future work this paper leaves open
- [A] Does vibe coding produce different defects and vulnerabilities than other AI-assisted or human coding? Which review practices work? How does practice change with experience [@fawzy2026vibe, p. 10]?
- [I] G6: its human-steered prompting workflow has not been compared with autonomous agents in app reconstruction [@fawzy2026vibe, p. 1].
- [I] G1: its "fast but flawed" perception has not been tested on measured fidelity and maintainability of rebuilt apps.

### Why it matters for your research
Use this paper for two things. First, its clear definition of vibe coding, which you can adopt or contrast in your methods. Second, its list of typical behaviours (re-prompting, run-and-see testing, letting the AI check itself), which a reconstruction study should either imitate or control. Do not use it as evidence that vibe-coded code is low quality: no code was measured. Weight it as perception evidence only.

### Connections to other papers
- [V] Other papers define "vibe coding" differently. asdaque2026novice uses a supervised agent workflow [@asdaque2026novice, p. 1], and mock2026vibe uses fixed scripted prompts [@mock2026vibe, p. 15]. Do not pool their results (evidence matrix C9).
- [A] Agrees with ehsani2026faster, which links vibe coding to "fast-integration debt", also from grey sources [@ehsani2026faster, p. 17].
- [V] The perceived "fast but flawed" pattern converges with higher review burden for novice agent users [@asdaque2026novice, p. 3] (evidence matrix G-A8, rated weak).
- [V] he2026speed gives measured, not perceived, evidence on quality after agentic tool adoption [@he2026speed, p. 7].
