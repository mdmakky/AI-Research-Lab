# AI Research Lab

A personal, reusable workspace in which Claude Code runs academic literature research for you: from a topic to research questions, papers, page-cited analyses, comparisons, evidence-backed research gaps and written reports. Each topic becomes its own project that you can resume at any time.

## Quick start

Open this folder in Claude Code and type:

> Start a new research on *your topic*

Claude creates the project, writes objectives and research questions, finds and screens papers, downloads legally available PDFs, analyses each paper, checks the analyses, compares methods, finds gaps and writes a report. It will ask you only when a decision is genuinely yours (scope, missing PDFs, paid resources, deleting things).

Other things you can say:

| You say | What happens (skill) |
|---|---|
| "Start a new research on X" | full workflow (`start-research`) |
| "Resume research" / "Continue the X research" / "What projects do I have?" | reload state and continue (`resume-research`) |
| "Find more papers on Y for this project" | search, screen, add (`discover-papers`) |
| "Analyse paper `<key>`" | page-cited analysis (`analyze-paper`) |
| "Compare the methods of the papers" | methodology comparison + evidence matrix (`compare-methods`) |
| "What are the research gaps?" | novelty-checked gap report (`find-gaps`) |
| "Write a literature review" | review with verified citations (`write-literature-review`) |
| "Summarise what we found" | plain-language report (`research-report`) |
| "I downloaded the PDF for `<key>`: ~/Downloads/x.pdf" | Claude attaches it and upgrades the analysis to full text |

You can also type a skill directly, e.g. `/resume-research`.

## Setup (once)

1. **Required**: Python ≥ 3.9 and poppler-utils (`pdftotext`, `pdfinfo`). Fedora: `sudo dnf install poppler-utils`; Debian/Ubuntu: `sudo apt install poppler-utils`; macOS: `brew install poppler`. No Python packages are needed.
2. **Install the Claude Code settings** (permissions + the file-protection hook). Claude was not allowed to modify its own settings, so do it yourself after reviewing the file:
   ```bash
   cp setup/claude-settings.json .claude/settings.json
   ```
   It pre-approves the `rlab` helper and academic websites (fewer permission prompts), blocks shadow-library sites, and enables a hook that asks you before anything overwrites a PDF, extracted text or completed analysis, or deletes research files.
3. **Strongly recommended: a free OpenAlex API key.** OpenAlex is the main search source; without a key the daily budget is small and anonymous search is sometimes paused (it was during setup). Get a key at <https://openalex.org/settings/api> and put it in the git-ignored `.env` file in this folder (already done for this workspace):
   ```bash
   OPENALEX_API_KEY=your-key
   ```
   An exported environment variable of the same name overrides `.env`.
4. Optional: `export RLAB_CONTACT_EMAIL="you@example.org"` enables Unpaywall (finds more legal open-access PDFs) and the Crossref/OpenAlex "polite pool". It is sent to those services, so set it only if you are fine with that.
5. Check everything: `python3 scripts/rlab.py doctor`
6. Optional: `git init` here to get a full history of every file Claude changes.

## How it works

```
CLAUDE.md                     rules + map, loaded in every session
docs/research-standards.md    quality rules: evidence labels, source tiers, novelty checks, copyright
.claude/skills/               8 workflow skills (procedures)
.claude/agents/               6 specialist agents (roles)
.claude/hooks/                protection hook (active after setup step 2)
scripts/rlab.py               deterministic helper CLI
templates/                    project + paper-analysis templates
tests/                        test suite
setup/claude-settings.json    settings to install (setup step 2)
research/
  registry.json               every project (managed by rlab)
  INDEX.md                    overview table
  <date>-<topic>/             one project
    RESEARCH.md               topic, scope, objectives, criteria, search strategy, decisions
    RESEARCH-QUESTIONS.md     research questions + current answers
    STATUS.md                 phase checklist, statistics, next actions, blockers
    research-log.md           append-only log of every action
    literature-matrix.md/.csv one row per paper (generated)
    evidence-matrix.md        claims per research question with page citations
    gap-report.md             evidence-backed, novelty-checked gaps
    references.bib            BibTeX for all papers (generated)
    search/                   every search's raw results, search log, screening decisions
    papers/<key>/             metadata.json, paper.pdf, fulltext.txt, analysis.md, paper.bib
    reports/                  methodology comparison, critical reviews, literature reviews, reports
```

**Agents.** `research-orchestrator` (the main session's role: plans, delegates, consolidates), `paper-scout` (search + screening), `paper-analyst` (per-paper analysis), `critical-reviewer` (checks analyses against the papers), `gap-analyst` (gaps + novelty checks), `academic-writer` (reviews and reports). Independent work runs in parallel; each agent writes only its own files, and only the orchestrator edits shared files.

**Quality safeguards.**
- Metadata is never typed by hand: `rlab add` resolves it from Crossref/OpenAlex/arXiv/PubMed and cross-checks sources; mismatches and retractions are flagged.
- Duplicates are rejected on DOI, arXiv id, PMID, OpenAlex id and near-identical titles (preprint vs published).
- Every PDF is checked to be the right paper (DOI/arXiv id/title on its first pages); text is extracted with `[PDF page N]` markers so every claim can cite a page.
- Every claim is labelled [V] verified / [A] author claim / [I] our interpretation; `rlab cite-check` rejects unknown keys, impossible page numbers and retracted papers.
- Only legal open-access PDFs are downloaded; paywalled papers are listed for you to obtain through your library.
- Analyses go `draft → ready → complete`; completed analyses, PDFs and logs are protected.

## Using it on another device

```bash
git clone git@github.com:<you>/AI-Research-Lab.git && cd AI-Research-Lab
cp .env.example .env          # then put your OpenAlex key in .env (the key is never in git)
python3 scripts/rlab.py doctor
```
Install poppler-utils (setup step 1) and open the folder in Claude Code. All projects, papers, analyses and the registry come with the clone; say "Resume research" to continue. Keep the repository **private**: it contains full-text PDFs of papers, which must not be redistributed. Commit and push when you stop (`git add -A && git commit -m "..." && git push`) and pull before you start on the other device, so two devices never edit the same project at once.

## `rlab` commands

Run from this folder as `python3 scripts/rlab.py <command>`; `-h` on any command shows options. Projects can be named by any unique part of their id or topic.

| Command | Purpose |
|---|---|
| `new "<topic>"` | create a project from the templates and register it |
| `list` · `status [project]` · `resume [project]` | list projects / show phase, stats, next actions, papers needing work |
| `search <project> "<query>" [--sources openalex,crossref,arxiv,pubmed] [--limit N] [--from Y] [--to Y]` | search, merge duplicates across sources, flag papers already in the project, save + log |
| `add <project> <DOI/arXiv/W-id/pmid:N ...> [--reason] [--query] [--allow-similar]` | resolve + verify metadata, reject duplicates, create `papers/<key>/` |
| `fetch <project> [keys]` | download legal open-access PDFs, extract page-marked text |
| `attach <project> <key> <file.pdf>` | add a PDF you obtained; checks it is the right paper |
| `pdf-meta <file.pdf>` | show DOIs/arXiv ids/title found in a PDF |
| `dedup <project>` | report possible duplicate papers |
| `validate <project> [keys]` | re-check metadata against live sources, retraction status, PDF identity |
| `scaffold <project> [keys]` | create `analysis.md` from the template (never overwrites) |
| `cite-check <project> <files>` | verify `[@key, p. N]` citations |
| `bib <project> [--offline]` | per-paper BibTeX (publisher's via doi.org when possible) + `references.bib` |
| `index [project]` | rebuild literature matrix, STATUS statistics, registry, INDEX.md |
| `log <project> <phase> "<message>"` | append to the research log |
| `doctor [--offline]` | check dependencies, skills/agents and API reachability |

## External dependencies

| Dependency | Needed for | Required? |
|---|---|---|
| Python ≥ 3.9 (standard library only) | `rlab` | yes |
| poppler-utils (`pdftotext`, `pdfinfo`) | PDF text + metadata | yes |
| OpenAlex API | search, OA locations, retractions, citations | yes (free key recommended) |
| Crossref API, doi.org | search, authoritative metadata, BibTeX | yes, no key |
| arXiv API | preprint search + PDFs | yes, no key |
| PubMed E-utilities, Europe PMC | biomedical search + OA PDFs | optional, no key |
| Unpaywall | more OA PDF locations | optional (`RLAB_CONTACT_EMAIL`) |
| Semantic Scholar | fallback lookups via web fetch | optional (rate-limited without key) |
| Claude Code WebSearch / WebFetch | recent work, snowballing, publisher pages | built in |

No MCP servers or external Claude skills are required.

## Testing

```bash
python3 -m unittest discover -s tests -v                 # offline: 24 tests (+1 skipped online test)
RLAB_ONLINE=1 python3 -m unittest discover -s tests -v   # + live end-to-end sample (needs network)
```

## Good to know

- First runs aim for ≤ 20 included papers to keep work and cost bounded; ask for more when needed.
- "Published" in the matrix means it appeared in a journal or proceedings — usually peer-reviewed, not guaranteed. Preprints are flagged.
- Page numbers in citations are PDF page positions, which can differ from the journal's printed page numbers.
- To run Claude purely as the orchestrator: `claude --agent research-orchestrator`.
