## ProgramDistill: From Interactive Web Apps to Verifiable Reference-Guided SWE Tasks
> **Takeaway:** When coding agents rebuild a whole web app by clicking through a live original, the best one recovers only 49.15% of multi-step workflows [@kim2026programdistill, p. 11]. Most failures are behaviours the agent never looked at in the original, not coding mistakes [@kim2026programdistill, p. 12].

| Item | Detail |
|---|---|
| Authors | Jeonghye Kim, Minseon Kim, Young Jin Kim, Matheus Pereira, Marc-Alexandre Côté, Alessandro Sordoni, Xingdi Yuan, Zhengyan Shi |
| Year · Venue | 2026 · arXiv |
| Status | Preprint (not peer-reviewed); authors from KAIST, Microsoft Research Montréal and Microsoft AI |
| Identifier | DOI 10.48550/arxiv.2609.18805 (arXiv 2609.18805) |
| Paper type | Benchmark with an automated task-building pipeline and an agent comparison |
| Relevance to us | High — RQ1, RQ2, RQ4, RQ5 (RQ3 only as a gap) |

### In plain words
Usually a coding AI is told exactly what to build, for example through a bug report. Here the AI must find out what to build by using a working web app, then make an incomplete or empty copy behave the same way [@kim2026programdistill, p. 1]. The authors call this a shift "from specification consumption to specification discovery" [@kim2026programdistill, p. 14]. They built thousands of such tasks automatically and tested frontier coding agents on them. This matters for us because the "full rebuild" setting is almost exactly our scenario: rebuilding a web app from its interface, without its source code.

### How they did it
The authors use a three-step pipeline they call mine, craft and patch [@kim2026programdistill, p. 2].
1. Mine: AI agents use the live app in a browser and record "traces". A trace is a replayable list of actions (clicks, typing) plus the expected visible results, such as text, page address or state. A trace is kept only if it replays the same way every time from a fresh start [@kim2026programdistill, p. 3].
2. Craft: an AI deletes the code behind one behaviour. The deletion is kept only if the app still builds, earlier steps still work, and the target trace now fails [@kim2026programdistill, p. 4]. Deleting several linked behaviours gives harder tasks. The number of linked behaviours is the "restoration depth" [@kim2026programdistill, p. 2].
3. Patch, partial: the agent gets the damaged code, a short description and browser access to the live original, with no original source and no internet [@kim2026programdistill, p. 6].
4. Patch, full: the agent starts from a near-empty scaffold and must rebuild the whole app from the live original [@kim2026programdistill, p. 6].
5. Scoring replays the recorded traces on the result without any AI judge. A task passes only if every step and expected result works [@kim2026programdistill, p. 4]. Code may look completely different from the original, as long as the behaviour replays [@kim2026programdistill, p. 6].

### Data and setup
- 26 web apps: 18 adapted from the OSWorld test suite and 8 open-source projects or SaaS clones, such as Trello and Jira clones [@kim2026programdistill, p. 19].
- 1,975 verified behaviours and 4,063 tasks [@kim2026programdistill, p. 7].
- Partial rebuilds: 300 selected tasks across all 26 apps, with depths 1 to 8, run by 9 models [@kim2026programdistill, p. 8].
- Full rebuilds: 12 apps x 3 models = 36 runs, scored with 590 single-behaviour tests and 413 workflow tests [@kim2026programdistill, p. 11].
- Agents see only structured text from the browser (visible text, element names and roles), not screenshots [@kim2026programdistill, p. 3].
- All tasks were built by one model, GPT-5.6 Sol [@kim2026programdistill, p. 2].
- [I] Runs per task in the partial setting are not stated, so probably one [@kim2026programdistill, p. 8].

### Key findings
- [V] Partial rebuilds: GPT-6 Astra passes 84.3% of tasks, Claude Opus 5 68.7% and GPT-5.6 Sol 60.7%. Gemini 3.1 Pro Preview is lowest at 22.3% [@kim2026programdistill, p. 8].
- [V] Success falls with depth. GPT-6 Astra drops from 100% at depth 1 to 64.0% at depth 8, and Claude Opus 5 from 96% to 32.0% [@kim2026programdistill, p. 8]. The drop persists when context length is held similar [@kim2026programdistill, p. 39].
- [V] Restoring the interface as well as the logic is harder: 92.9% vs 76.9% for GPT-6 Astra [@kim2026programdistill, p. 38].
- [V] Full rebuilds: GPT-6 Astra recovers 58.98% of single behaviours and 49.15% of workflows, Claude Opus 5 42.03% and 28.81%, and GPT-5.6 Sol 33.39% and 21.07% [@kim2026programdistill, p. 11].
- [V] Results vary a lot by app: GPT-6 Astra's workflow recovery ranges from 81.8% (MailHub) to 5.9% (Baserow) [@kim2026programdistill, p. 11].
- [V] Of 977 failed behaviours, 59.2% were never observed in the original, 27.9% gave the wrong state or result, and 11.1% had the wrong visible form [@kim2026programdistill, p. 12].
- [A] Agents' own checks often missed the failing workflow, so mismatches went unnoticed [@kim2026programdistill, p. 12].
- [V] 7.2% of runs tried a shortcut, such as fetching public source code. All shortcuts were blocked by design [@kim2026programdistill, p. 10].

### Limitations and weaknesses
- [A] No screenshots, so visual fidelity is not evaluated [@kim2026programdistill, p. 14].
- [A] Only self-contained web apps; external services, desktop and mobile are future work [@kim2026programdistill, p. 14].
- [A] Task quality depends on the model that built the tasks [@kim2026programdistill, p. 15].
- [I] Code quality is not measured. Full rebuilds must also use one fixed Node entry point, while the originals use Django, Angular, React or Next.js [@kim2026programdistill, p. 37].
- [I] Possible family bias: GPT-5.6 Sol built the tasks, GPT-6 Astra wins, and GPT-6 Astra also classified the failures [@kim2026programdistill, p. 12].
- [I] Tasks are built "without human intervention", and no sample was audited by hand [@kim2026programdistill, p. 1].
- [I] Full-rebuild tests require the original's selectors and labels (element identifiers), which mixes behaviour with copying page structure [@kim2026programdistill, p. 35].
- [I] The abstract reports full-rebuild results under "nine frontier coding agents" [@kim2026programdistill, p. 1], but only 3 were tested in that setting [@kim2026programdistill, p. 11].
- [I] No variance or confidence intervals are reported [@kim2026programdistill, p. 8]. Contamination is not discussed, although the 8 real apps are public projects [@kim2026programdistill, p. 19].

### Gaps and future work this paper leaves open
- G1: code quality of rebuilds is not measured [@kim2026programdistill, p. 14].
- G2: the builder model and judge are from the same family as the winner [@kim2026programdistill, p. 2].
- G4: unreliable self-checks [@kim2026programdistill, p. 12] invite a test of better feedback loops.
- G5: [I] the 8 real apps are public, but memorisation is not discussed.
- G6: only one text-only autonomous agent setup is tested [@kim2026programdistill, p. 14].
- G7: the tests depend on the original's selectors [@kim2026programdistill, p. 35].
- G8: desktop and mobile apps are left as future work [@kim2026programdistill, p. 14].

### Why it matters for your research
[I] This is the closest study to rebuilding interactive web apps from their interface. Reuse two ideas: replaying recorded browser workflows as a test, and the failure categories, which show that exploring the original is the main bottleneck. Avoid two of its choices: tests tied to the original's element identifiers, and a fixed code structure that makes rebuilds impossible to compare with the original's code.

### Connections to other papers
- Builds on yang2026programbench, which the authors cite as the whole-program "behavior-to-code" setting [@kim2026programdistill, p. 1].
- Agrees with bai2026recreationworld: whole-app fidelity is partial, and agents rarely re-check their final result [@bai2026recreationworld, p. 12].
- Agrees that fidelity falls as programs get more complex [@yang2026programbench, p. 31].
- Agrees that interaction is harder than static content [@xiao2025benchmarking, p. 6; @chen2025iwr, p. 16].
- Shares the same-family pattern with ProgramBench, where Claude wrote the tests and Claude models lead [@yang2026programbench, p. 3].
