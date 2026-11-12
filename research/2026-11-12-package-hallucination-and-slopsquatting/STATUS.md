# Status — Package Hallucination and Slopsquatting in LLM Coding Assistants: Measuring Hallucinated Dependencies, Their Exploitability on PyPI/npm, and Lightweight Defences

## Phases
- [x] Scoping — objectives and research questions written
- [x] Discovery — searches run and logged
- [x] Screening — candidates screened, papers included
- [x] Acquisition — open-access full texts collected, missing ones reported to user
- [x] Analysis — 20/20 complete (3 agent-attack papers analysed 2026-11-12 after user asked us to finish them)
- [x] Critical review — analyses checked against the papers
- [x] Synthesis — methods compared, evidence matrix complete
- [x] Gaps — research gaps identified and novelty-checked
- [x] Writing — literature review / report drafted (reports/research-report-2026-11-12.md)

## Statistics
<!-- rlab:stats:start -->
_Auto-updated 2026-11-12T17:54:21+06:00 by `rlab index`._

- Current phase: **complete**
- papers: 20
- fulltext: 20
- no fulltext: 0
- analysed: 20
- analysis ready: 0
- analysis draft: 0
- preprints: 13
- retracted: 0
- unverified: 3
<!-- rlab:stats:end -->

## Next actions
- Add + analyse the 4 high-priority papers from gap-report.md (Huang et al. TOSEM 2026 10.1145/3830237; StateMirror arXiv 2610.32648; Setup Complete arXiv 2607.15143; Bayesian-calibrated detection arXiv 2606.13918) via `rlab add`, then re-run G1/G2 novelty checks against their full texts. G1 is already narrowed by hsu2026harmless (see gap-report.md revision).
- First experiment (G3 week 1): scorer v0 + 200 prompts from the Spracklen/Churilov corpus (see report §8).
- Reading guide published 2026-11-12 (anyone with link can view): https://docs.google.com/document/d/1oJbn82gvNLHmlYboGnjklQo5bK8n-oXWhFOXoe7KsYc/edit — local copies reports/reading-guide-2026-11-12.md/.pdf. It covers the 17 earlier papers; briefs for the 3 attack papers and the G1 revision are not in it yet (optional: add 3 briefs to reports/reading-guide/ and republish).
- Optional: zhang2025llm OA published (ISSTA) version — replacing paper.pdf needs user permission.
- Known validate MISMATCHes, explained in analyses: liu2026packmonitor (arXiv title differs), okwor2026hallucination and raj2026names (Zenodo/DataCite DOI not in Crossref).

## Blocked / needs user
<!-- e.g. papers without open-access PDF, scope questions. Empty = nothing blocked. -->
