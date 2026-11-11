# Screening decisions

Record every candidate considered and the decision. Included papers are also logged by `rlab add --reason`.

| results file | idx | title (short) | decision | reason |
|---|---|---|---|---|
| F1 vibe-coding searches + snowball | — | Vibe Coding in Practice (grey lit review) [fawzy2026vibe] | include | ICSE-SEIP; 101 sources/518 accounts; anchor review of vibe-coding practice |
| F1 | — | Vibe Coding: experiment with TDD [mock2026vibe] | include | EMSE controlled pre-experiment; = arXiv 2607.22406 (not added twice) |
| F1 | — | Is Vibe Coding Safe? SusVibes [zhao2025vibe] | include | 186 real tasks; correctness vs security diverge; published ICML 2026 (PMLR v306, no DOI) though record is arXiv |
| F1 | — | Novice developers larger review overhead [asdaque2026novice] | include | MSR 2026; 22,953 PRs; downstream maintenance cost |
| F1/F4 | — | Comparing quality of vibe coding tools [mota2026comparing] | include | only direct SonarQube study of whole vibe-coded apps; preprint, n=9 — illustrative |
| F2 UI-to-code searches + snowball | — | Design2Code [si2025benchmarking] | include | NAACL 2025; main static screenshot-to-code benchmark |
| F2 | — | Interaction2Code [xiao2025benchmarking] | include | ASE 2025; interaction fidelity |
| F2 | — | IWR-Bench [chen2025iwr] | include | reconstruction from interaction video; functional vs visual fidelity; preprint |
| F2 | — | DeclarUI [zhou2025declarui] | include | FSE/PACMSE; mobile; measures fidelity + code quality |
| F2 | — | Looks Right, Works Right (MobileForge) [wu2026looks] | include | EMNLP 2026; fidelity and maintainability together |
| F3 app-level searches + snowball | — | WebGen-Bench [lu2025webgen] | include | NeurIPS 2025; functional tests on generated websites |
| F3 | — | E2EDev [liu2026benchmarking] | include | ACL 2026; requirement-traceable BDD tests |
| F3 | — | RAL-Bench [pan2026functional] | include | reference-project black-box tests + ISO 25010 non-functional; preprint |
| F3 | — | Vibe Code Bench [tran2026vibe] | include | CAIS 2026; browser-agent judged web apps; explicit vibe coding |
| F4 quality searches + snowball | — | Speed at the Cost of Quality (Cursor) [he2026speed] | include | MSR 2026; causal DiD on real projects |
| F4 | — | Echoes of AI [borg2026echoes] | include | EMSE; preregistered RCT n=151 on maintainability |
| F4 | — | Code & architectural smells of LLMs/agents [zhu2026understanding] | include | ASE 2026; multi-file agent systems |
| F4 | — | LLM vs human maintainability (ESEM) [molison2025llm] | include | ESEM 2025; SonarQube LLM vs human |
| F4 | — | Faster Code, Deeper Debt? MLR [ehsani2026faster] | include | TOSEM; the review for technical debt of LLM-assisted dev |
| F5 reverse-engineering searches + WebSearch + snowball | — | ProgramBench [yang2026programbench] | include | rebuild programs from executable+docs only; preprint |
| F5 | — | ProgramDistill [kim2026programdistill] | include | black-box web-app reconstruction from reference app; preprint |
| F5 | — | RecreationWorld [bai2026recreationworld] | include | rebuild GUI apps on 5 platforms from running reference; preprint |
| F5 | — | PropGen [xiong2026propgen] | include | ASE 2026; LLM spec recovery from running Android apps |
| reserves (not added, first pass ≤ 23) | — | DCGen 10.1145/3729364; Video2Code 10.18653/2026.emnlp-main.2243; DesignBench arXiv 2506.06251; Sketch2Code 10.18653/v1/2025.naacl-long.198; WebCompat arXiv 2608.12518; ProjectEval 10.18653/v1/2025.findings-acl.1036; BaxBench arXiv 2502.11844 (ICML 2025); RepoZero arXiv 2605.07122; RealDevWorld arXiv 2508.14104; WebCoderBench 10.18653/v1/2026.acl-long.535; CLI-Tool-Bench arXiv 2604.06742; ISSRE human-vs-AI 10.1109/issre66568.2025.00035; TOSEM ChatGPT quality 10.1145/3643674; Debt behind AI boom arXiv 2603.28592; EMNLP agent maintainability 10.18653/2026.emnlp-main.2528; insecurity of vibe-coded apps arXiv 2606.23130; IJASEIT vibe experiment 10.18517/ijaseit.16.4.21812 (mid-tier); vibe MLR arXiv 2607.21652; MirrorCode arXiv 2606.30182; Trace2World arXiv 2610.30792; SpecFirst arXiv 2607.27167; pix2code 10.1145/3220134.3220135 (background) | reserve | relevant but redundant with included set or lower priority |
| all facets | — | GLM-5, VibeContract, VIBE-HI, vibe position papers | exclude | model report / vision / conceptual, no evidence |
| all facets | — | perception-only vibe-coding studies (Good Vibrations, "Professional developers don't vibe", CHI Throw-Away to Takeaway) | exclude | no code outcomes |
| all facets | — | IJFMR / IJMSERH / ICICI vibe-quality papers | exclude | suspected predatory or low-tier venue, unclear sample |
| all facets | — | NVLM, Cambrian-1, ChartLlama, MME-Survey, MM-Embed | exclude | general multimodal models, not UI reconstruction |
| all facets | — | UCRBench, LLM vs MDRE (OCL), Rebuild Dossier, ReviveBench | exclude | reconstruction from source code, not behaviour |
| all facets | — | Visual Identification of Mobile App GUI Elements (10.1155/2023/9805091) | exclude | RETRACTED |
| all facets | — | Mercor SWE-Marathon blog, Web Clone Bench (benchlm.ai) | exclude | grey/vendor material (tier 5) |
