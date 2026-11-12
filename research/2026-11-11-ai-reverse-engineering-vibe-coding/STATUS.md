# Status — Evaluating AI-Assisted Reverse Engineering for Software Application Reconstruction through Vibe Coding: Functional Fidelity, Code Quality, and Maintainability

## Phases
- [x] Scoping — objectives and research questions written
- [x] Discovery — searches run and logged
- [x] Screening — candidates screened, papers included
- [x] Acquisition — open-access full texts collected, missing ones reported to user
- [x] Analysis — every included paper analysed
- [x] Critical review — analyses checked against the papers (reports/critical-review-batch-{a,b,c}.md; all fixes applied, 23/23 complete)
- [x] Synthesis — methods compared, evidence matrix complete (evidence-matrix.md 204 rows, C1–C10; reports/methodology-comparison.md)
- [x] Gaps — research gaps identified and novelty-checked (gap-report.md G1–G8; top: G1 fidelity + validated maintainability)
- [x] Writing — literature review / report drafted (reports/research-report-2026-11-12.md)

## Statistics
<!-- rlab:stats:start -->
_Auto-updated 2026-11-12T00:35:49+06:00 by `rlab index`._

- Current phase: **complete**
- papers: 23
- fulltext: 23
- no fulltext: 0
- analysed: 23
- analysis ready: 0
- analysis draft: 0
- preprints: 7
- retracted: 0
- unverified: 2
<!-- rlab:stats:end -->

## Next actions
- 2026-11-12: ALL PHASES DONE. Report: reports/research-report-2026-11-12.md. Awaiting user decisions: (a) add ~19 recommended papers (+7 security-only)? (b) G1 vs security topic vs combined; (c) start new project on security topic? Optional: write-literature-review.
- Reading guide published 2026-11-12 (anyone with link can view): https://docs.google.com/document/d/1h_QbexTziTB5n6Saf-baVXABIko_hwp9n4k79acxSeA/edit — overview, 23 plain-English paper briefs, gaps G1–G8 + security follow-up, glossary, appendices A–C (report, methodology comparison, evidence matrix). Local copies: reports/reading-guide-2026-11-12.md / .pdf (196 pages); sources in reports/reading-guide/.
- Use corrected facts: bai lowest model = Qwen3.7-Plus (not Grok 4.6); bai code-size/structure findings = 4 models only; chen IFS<VFS gap partly definitional; ehsani's +30%/+41% = he2026speed (count once); liu multi-agent "do not consistently improve".
- User asked (2026-11-12) for a new cybersecurity-related topic; offered 3 candidates (security fidelity of AI-rebuilt apps [recommended]; detecting AI-cloned phishing sites; behaviour-derived security properties). User chose topic 1; novelty check DONE (partially novel, defensible core: security-control preservation in black-box AI reconstruction of web apps) → reports/novelty-check-security-fidelity.md. Awaiting user: start as new project?
- Known metadata issues (not blocking): he2026speed + zhu2026understanding `rlab validate` MISMATCH only because arXiv preprint title differs from published title (Crossref/OpenAlex/PDF identity match). zhao2025vibe metadata says preprint/arXiv but published at ICML 2026 (no rlab command to update venue). lu2025webgen metadata lists author "Hou, Haotian" not in PDF. zhou2025declarui, zhu2026understanding analysed from arXiv; published ACM OA version not checked (zhou ablation table suspicious).
- Synthesis cues from review: same model family builds/judges and wins (yang, tran, wu, zhao, kim, liu, lu); iterative feedback contradiction (pan vs tran/zhou/wu); molison vs he SonarQube direction (different units); "vibe coding" means different things across fawzy/asdaque/mock/he/ehsani — don't pool; contamination handling uneven (gap candidate, needs novelty check).
- Synthesis notes so far: he2026speed vs borg2026echoes contradict on maintainability harm; visual fidelity >> functional fidelity across UI/reconstruction benchmarks; code quality/maintainability almost never measured in reconstruction benchmarks

## Blocked / needs user
<!-- e.g. papers without open-access PDF, scope questions. Empty = nothing blocked. -->
