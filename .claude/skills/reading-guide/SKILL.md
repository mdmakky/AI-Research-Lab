---
name: reading-guide
description: Build a plain-language Reading Guide for a project (overview, one 1–2 page brief per paper, gaps and opportunities, glossary) and publish it as a styled, shareable Google Doc. Use at the end of every research run (after research-report), or when the user asks for paper summaries, documentation, a doc, or a shareable link.
---

# Reading guide + shareable Google Doc

`rlab` = `python3 scripts/rlab.py`. Rules: [docs/research-standards.md](../../../docs/research-standards.md). Audience: the user, a beginner who has NOT read the papers. Plain English, short sentences, every technical term explained on first use.

Input: project id. Needs complete analyses, `evidence-matrix.md`, `gap-report.md`, the research report. Output folder: `research/<id>/reports/reading-guide/`.

## 1. Write (delegate to `academic-writer`, in parallel)
- **Paper briefs** — 5–6 paper keys per agent, one file each: `reports/reading-guide/papers/<key>.md`. Source: `papers/<key>/analysis.md` (keep its corrections and labels), `metadata.json`, `fulltext.txt` for checks. ~600–1200 words, exactly this structure:
  - `## <Full paper title>`
  - `> **Takeaway:** <1–2 sentences>`
  - table `| Item | Detail |`: Authors · Year · Venue · Status (Peer-reviewed / Preprint; note if our copy is an arXiv version) · Identifier · Paper type · Relevance to us (High/Medium/Low — RQs)
  - `### In plain words` · `### How they did it` · `### Data and setup` · `### Key findings` (4–8 bullets, numbers, label + `[@key, p. N]`) · `### Limitations and weaknesses` · `### Gaps and future work this paper leaves open` (link gap IDs) · `### Why it matters for your research` · `### Connections to other papers`
- **Front/back matter** — one agent writes:
  - `00-front.md`: `# Overview` — topic + RQs in plain words, how to use the guide (labels, citations, preprints), main findings per RQ with evidence strength, paper map table (all papers, grouped), 5 papers to read first, where studies disagree.
  - `99-back.md`: `# Research Gaps and Opportunities` (each gap: callout, evidence, novelty verdict + closest prior work, contribution, beginner study design, feasibility, risks; any follow-up topic novelty checks in `reports/`; next-steps checklist; recommended papers not yet included), `# Glossary` (table, 30+ terms), `# About this guide` (method, dates, limitations).
  - `order.txt`: paper keys in paper-map order.
- Markdown the converter understands: `#`/`##`/`###`, paragraphs, `- ` bullets, `1. ` lists, pipe tables, single-paragraph `> ` callouts, `**bold**`. No nested bullets, italics, links, HTML, images, code.
- Every agent finishes with `rlab cite-check <id> <its files>` → OK.

## 2. Check
`rlab cite-check <id>` on all guide files; every key in `order.txt` has a brief.

## 3. Publish
Write `reports/reading-guide/10-papers.md` (`# Paper Summaries` + one line on how each brief is organised). Make appendix copies (the user wants the whole research outcome at the end): `appendix-a-research-report.md` (latest `reports/research-report-*.md`), `appendix-b-methodology-comparison.md`, `appendix-c-evidence-matrix.md` — each a copy with its first `# ` heading renamed to `# Appendix A: Full Research Report` etc. Then from the workspace root:

```bash
G=research/<id>/reports/reading-guide
python3 scripts/md2gdoc.py --title "Reading Guide: <short topic>" --subtitle "<full topic>" \
  --share anyone --md research/<id>/reports/reading-guide-YYYY-MM-DD.md --pdf research/<id>/reports/reading-guide-YYYY-MM-DD.pdf \
  $G/00-front.md $G/10-papers.md $(sed "s#^#$G/papers/#; s#\$#.md#" $G/order.txt) $G/99-back.md $G/appendix-*.md
```

Later additions go into the same doc: `python3 scripts/md2gdoc.py --append <DOC_ID> new.md`. Spot-check a few PDF pages (Read the PDF) before sending the link.

`--share anyone` = anyone with the link can view (the user's chosen default; use `--share none` if they ask for private). Auth comes from the google-doc-builder skill; on `invalid_grant` run its `gdoc_auth.py` and show the user the login URL. Rendering takes several minutes (Docs API write quota); run it in the background.

## 4. Record
Add the doc URL and file paths to `STATUS.md` (Next actions), `rlab log <id> writing "reading guide published: <url>"`. Tell the user the link, what is inside, and that local `.md`/`.pdf` copies are in `reports/`.
