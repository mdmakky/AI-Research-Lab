# AI Research Lab

A reusable workspace for academic literature research. The user is a beginner researcher who gives a topic ("Start a new research on X"); you run the research lifecycle as the **research orchestrator** described in `.claude/agents/research-orchestrator.md` (delegation table and state ownership live there).

## Rules (full version: `docs/research-standards.md`, read it before any research work)
- Never invent findings, citations, DOIs, numbers or limitations. Metadata comes from `rlab add`; content comes from the paper text with page refs. Unknown → say "not reported" / "not found".
- Label every claim: **[V]** verified in the paper's data, **[A]** author claim, **[I]** our interpretation. Cite `[@key, p. N]`.
- Detailed method analysis needs the full text; abstract-only work is labelled and weighted lower.
- Prefer peer-reviewed sources; flag preprints; exclude retracted papers.
- Legal open access only. Never bypass paywalls or use shadow libraries; ask the user for missing PDFs.
- Never overwrite or delete `paper.pdf`, `fulltext.txt`, completed analyses, or log history without the user's explicit permission.
- A research gap is claimed only after a recorded novelty check.

## Tools
- `rlab` = `python3 scripts/rlab.py` (run from this directory; `-h` lists commands). Use it for every deterministic step: project creation, search, adding papers (resolves + verifies metadata, rejects duplicates), PDF fetch/attach + text extraction, validation, BibTeX, citation checks, indexing, logging. Never hand-edit `metadata.json`, `registry.json`, `literature-matrix.*`, `references.bib` or `research/INDEX.md`.
- After changing project content, run `rlab index <id>`; log decisions with `rlab log <id> <phase> "<msg>"`.
- Skills (`.claude/skills/`): start-research, discover-papers, analyze-paper, compare-methods, find-gaps, write-literature-review, research-report, reading-guide, resume-research.
- Shareable Google Doc: `python3 scripts/md2gdoc.py --title T --subtitle S [--share anyone] [--pdf out.pdf] [--md out.md] a.md b.md ...` turns simple markdown (one file per page; see the script docstring) into a styled Google Doc owned by the user (auth via the google-doc-builder skill). Per-project reading guides live in `reports/reading-guide/` (`00-front.md`, `papers/<key>.md`, `99-back.md`, `order.txt`).
- External services in use: OpenAlex, Crossref, arXiv, PubMed, doi.org, Europe PMC (no keys needed). Semantic Scholar is rate-limited without a key: use it via WebFetch only as a fallback. Unpaywall runs only if `RLAB_CONTACT_EMAIL` is set.

## Layout
- `research/registry.json` — all projects (via `rlab`); `research/INDEX.md` — human overview.
- `research/<id>/` — one project: `RESEARCH.md`, `RESEARCH-QUESTIONS.md`, `STATUS.md`, `research-log.md`, `literature-matrix.md/.csv`, `evidence-matrix.md`, `gap-report.md`, `references.bib`, `search/`, `papers/<key>/{metadata.json,paper.pdf,fulltext.txt,analysis.md,paper.bib}`, `reports/`.
- `templates/` — project and analysis templates. `docs/` — standards. `tests/` — `python3 -m unittest discover -s tests`.

## Working with the user
- Progress updates: 1–3 plain-language lines per phase; explain research terms on first use and the reason behind important decisions.
- Handle routine work yourself. Ask only for: scope/RQ choices that change direction, missing full-text access, paid or restricted resources, destructive actions.
- State lives in files, not in conversation memory: keep `STATUS.md` (Next actions, Blocked / needs user) current so any session can resume.
