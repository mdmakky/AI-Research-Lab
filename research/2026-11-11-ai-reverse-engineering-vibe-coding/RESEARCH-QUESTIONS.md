# Research questions — Evaluating AI-Assisted Reverse Engineering for Software Application Reconstruction through Vibe Coding: Functional Fidelity, Code Quality, and Maintainability

## RQ1: What AI/LLM approaches exist for reconstructing or generating software applications from observable artefacts (UI screenshots, designs, interaction behaviour, specifications), and how do they relate to vibe-coding workflows?
- Type: descriptive
- Why it matters: defines what "AI-assisted reverse engineering" currently looks like in practice and research, and which inputs and tools are realistic.
- Linked objective: O1
- Status: answered (provisional, after methodology comparison 2026-11-12)
- Current answer: Six approach families exist (see reports/methodology-comparison.md §2):
  1. Screenshot or design to code [@si2025benchmarking, p. 4; @zhou2025declarui, p. 3; @wu2026looks, p. 6].
  2. Interaction video or before/after interaction screenshots to code [@chen2025iwr, p. 5; @xiao2025benchmarking, p. 2].
  3. Agentic rebuilds from a live running reference or an executable plus docs [@bai2026recreationworld, p. 3; @kim2026programdistill, p. 3; @yang2026programbench, p. 2].
  4. Natural-language spec or requirements to a full app [@liu2026benchmarking, p. 3; @lu2025webgen, p. 7; @tran2026vibe, p. 3; @pan2026functional, p. 2].
  5. Commercial vibe-coding platforms and IDE agents [@mota2026comparing, p. 2; @he2026speed, p. 4].
  6. Behavioural-spec recovery from running apps [@xiong2026propgen, p. 4].

  [I] Almost all evaluations run autonomous agents. Practitioner vibe coding is human-steered natural-language prompting with little review [@fawzy2026vibe, p. 1], and it is studied only in small or proxy studies [@mock2026vibe, p. 15; @asdaque2026novice, p. 1]. "Vibe coding" is defined inconsistently across papers, so their results must not be pooled. **Evidence strength: moderate** (consistent descriptive picture; 7 of 23 papers are preprints; fast-moving field).

## RQ2: How is functional fidelity of AI-reconstructed or AI-generated applications measured, and how well do current approaches achieve it?
- Type: descriptive / comparative
- Why it matters: a rebuild is only useful if it behaves like the original; the metrics used decide what "works" means.
- Linked objective: O2, O3
- Status: answered (provisional, after methodology comparison 2026-11-12)
- Current answer: Fidelity is measured with four kinds of oracle:
  1. Behavioural test replay against the original [@bai2026recreationworld, p. 9; @kim2026programdistill, p. 4; @yang2026programbench, p. 5; @liu2026benchmarking, p. 5].
  2. LLM or agent judges running natural-language tests [@lu2025webgen, p. 6; @tran2026vibe, p. 4; @chen2025iwr, p. 7].
  3. Visual similarity [@si2025benchmarking, p. 3; @wu2026looks, p. 4].
  4. Navigation graphs [@zhou2025declarui, p. 7].

  Fidelity is partial everywhere:
  - Full behavioural equivalence is rare: 2.8% of apps [@bai2026recreationworld, p. 11] and 0 of 200 programs [@yang2026programbench, p. 6].
  - The best workflow-level or requirement-level pass rates are about 49–62% [@kim2026programdistill, p. 11; @liu2026benchmarking, p. 6; @tran2026vibe, p. 6].
  - Interaction logic lags static structure [@bai2026recreationworld, p. 16; @chen2025iwr, p. 16]. chen2025iwr's IFS<VFS gap is partly built into its metrics [@chen2025iwr, p. 7].

  [I] Scores from different benchmarks use different oracles and are not comparable. **Evidence strength: moderate** for "far from complete; interaction is the bottleneck". **Weak** for any specific figure or cross-benchmark ranking (mostly single runs, 5 of the 8 main fidelity benchmarks are preprints).

## RQ3: What is known about the code quality and maintainability of LLM-generated or vibe-coded application code, compared with human-written code?
- Type: comparative
- Why it matters: rebuilt apps must be maintained; hidden code smells or technical debt would erase the speed gained.
- Linked objective: O2
- Status: partially answered (evidence conflicting, 2026-11-12)
- Current answer: The evidence is mixed:
  - Cursor adoption raises project-level SonarQube warnings (+30.26%) and cognitive complexity (+41.64%) [@he2026speed, p. 7]. The result is estimator-sensitive (negative and n.s. under Callaway–Sant'Anna) [@he2026speed, p. 16], and the warning rise runs mainly through more code [@he2026speed, p. 8].
  - A preregistered RCT found no significant downstream maintainability difference when a second developer evolved AI-assisted code [@borg2026echoes, p. 33; @borg2026echoes, p. 38].
  - GPT-4o code had fewer SonarQube "bugs" than a weak competitive-programming human baseline, with mixed smells [@molison2025llm, p. 8].
  - LLM code shows different smell types from human code [@zhu2026understanding, p. 7].
  - Quality varies by platform [@mota2026comparing, p. 5].
  - Rebuilds are smaller and more monolithic than their originals [@bai2026recreationworld, p. 15; @yang2026programbench, p. 9].
  - Practitioners perceive vibe-coded output as "fast but flawed" [@fawzy2026vibe, p. 8].

  [I] The measuring instruments disagree (SonarQube, PyExamine, CodeHealth, MI), and no study measures validated maintainability of reconstructed apps against their originals. **Evidence strength: weak to moderate** (conflicting results; see evidence-matrix.md C1–C3).

## RQ4: What are the methodological strengths and weaknesses of current evaluations (benchmarks, metrics, sample sizes, baselines, reproducibility) in this area?
- Type: methodological
- Why it matters: shows how far the reported results can be trusted and how a new study should be designed.
- Linked objective: O3
- Status: answered (provisional, after methodology comparison 2026-11-12)
- Current answer: Strengths:
  - Implementation-agnostic behavioural oracles with leakage controls [@yang2026programbench, p. 18; @bai2026recreationworld, p. 9].
  - Oracle audits [@yang2026programbench, p. 7; @liu2026benchmarking, p. 14].
  - Judge–human alignment checks [@tran2026vibe, p. 9; @wu2026looks, p. 13].
  - One preregistered RCT [@borg2026echoes, p. 19].

  Recurring weaknesses:
  1. Single runs with no variance or significance tests [@lu2025webgen, p. 40; @yang2026programbench, p. 10]. Measured generation variance is large [@tran2026vibe, p. 8].
  2. Same-family or weakly validated oracles and judges [@tran2026vibe, p. 9; @chen2025iwr, p. 17; @si2025benchmarking, p. 17].
  3. Uneven contamination handling.
  4. Maintainability absent or measured only by proxies [@pan2026functional, p. 3; @wu2026looks, p. 4].
  5. Oracles coupled to the original's identifiers, or given structural priors [@liu2026benchmarking, p. 16; @kim2026programdistill, p. 35; @zhou2025declarui, p. 7].
  6. No human-developer baselines in benchmarks.

  **Evidence strength: strong** for missing variance and significance testing and for absent maintainability measurement (verified across 12+ papers). **Moderate** for the judge, contamination and oracle-coupling problems.

## RQ5: Which gaps remain for jointly evaluating functional fidelity, code quality and maintainability of AI-assisted application reconstruction, and what study design could address them?
- Type: methodological
- Why it matters: turns the review into a concrete, feasible research contribution.
- Linked objective: O4
- Status: answered (provisional, after novelty check 2026-11-12)
- Current answer: [I] The main gap that survives the novelty check is a joint evaluation of behavioural fidelity and validated, size-normalised maintainability for applications rebuilt from observable artefacts, with the original app as the baseline. We found no study that does this (searches on 2026-11-12). Evidence that the gap exists is strong [@bai2026recreationworld, p. 15; @yang2026programbench, p. 9; @pan2026functional, p. 3; @wu2026looks, p. 4; @tran2026vibe, p. 9]. Five further gaps are partially novel: same-family builder and judge bias, validity of maintainability tools for AI-built apps, feedback effects on fidelity and quality together, the size of the contamination effect, and human-steered vs autonomous reconstruction. Oracles tied to the original's identifiers and native mobile apps with hidden back-ends are mostly or partly addressed by 2026 work. A related security angle (security-control preservation in black-box reconstruction) is partially novel; see reports/novelty-check-security-fidelity.md.

  Recommended study: the G1 design in gap-report.md (reference apps of known provenance, ≥3 runs, locator-independent behavioural tests, two static tools plus a maintenance task in the style of borg2026echoes [@borg2026echoes, p. 13]). G2 and G3 are easy add-ons using released Vibe Code Bench outputs [@tran2026vibe, p. 11].

  **Evidence strength: moderate** (novelty confidence medium-high for G1; re-check before submission, the field moves monthly).
