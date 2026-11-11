#!/usr/bin/env python3
"""rlab - deterministic helper CLI for the AI Research Lab workspace.

Handles everything that must be exact and repeatable: project folders, the
registry, literature search against academic APIs, metadata resolution,
duplicate detection, legal open-access PDF download, text extraction with page
markers, metadata validation, BibTeX and the literature matrix.

Judgement work (screening, analysis, synthesis, writing) belongs to Claude, not here.

Dependencies: Python 3.9+ standard library; poppler-utils (pdftotext, pdfinfo) for PDFs.
Optional env: RLAB_CONTACT_EMAIL (enables Unpaywall + API polite pools),
              OPENALEX_API_KEY (recommended; free at openalex.org/settings/api),
              either exported or written as KEY=VALUE lines in the git-ignored .env file.
              RLAB_ROOT (workspace root override, used by tests).
Run `python3 scripts/rlab.py -h` for commands.
"""
import argparse
import csv
import datetime as dt
import difflib
import hashlib
import html
import json
import os
import re
import shutil
import subprocess
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
# Workspace-local secrets (git-ignored): KEY=VALUE lines; real environment variables take precedence.
for _line in (REPO / ".env").read_text().splitlines() if (REPO / ".env").exists() else []:
    _k, _sep, _v = _line.strip().partition("=")
    if _sep and not _k.startswith("#"):
        os.environ.setdefault(_k.strip(), _v.strip().strip("\"'"))
ROOT = Path(os.environ.get("RLAB_ROOT", REPO))
RESEARCH = ROOT / "research"
TEMPLATES = REPO / "templates"
UA = "AI-Research-Lab/1.0 (academic literature tool; python-urllib)"
CONTACT = os.environ.get("RLAB_CONTACT_EMAIL")  # opt-in only; never hard-code a personal email
OPENALEX_KEY = os.environ.get("OPENALEX_API_KEY")  # free key: 10x the anonymous budget, survives search pauses
# Shadow libraries: copyright-infringing sources are never contacted.
BLOCKED_HOSTS = ("sci-hub", "scihub", "libgen", "library.lol", "z-lib", "zlibrary", "1lib",
                 "annas-archive", "booksc", "dokumen.pub", "libstc", "nexus")
STOP = set("a an the of on in for and to with from by at is are via using towards toward its into".split())
STATS_START, STATS_END = "<!-- rlab:stats:start -->", "<!-- rlab:stats:end -->"


# ---------------------------------------------------------------- utilities
def die(msg):
    sys.exit(f"error: {msg}")


def now():
    return dt.datetime.now().astimezone().isoformat(timespec="seconds")


def today():
    return dt.date.today().isoformat()


def ascii_lower(text):
    return unicodedata.normalize("NFKD", text or "").encode("ascii", "ignore").decode().lower()


def slugify(text, maxlen=50):
    s = re.sub(r"[^a-z0-9]+", "-", ascii_lower(text)).strip("-")
    if len(s) > maxlen:  # cut at a word boundary when possible
        s = s[:maxlen + 1].rsplit("-", 1)[0] if "-" in s[:maxlen + 1] else s[:maxlen]
    return s.strip("-") or "untitled"


def norm_title(t):
    return " ".join(re.sub(r"[^a-z0-9]+", " ", ascii_lower(strip_tags(t or ""))).split())


def strip_tags(s):
    return html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s or "")).strip())


def read_json(p, default=None):
    try:
        return json.loads(Path(p).read_text(encoding="utf-8"))
    except FileNotFoundError:
        return default


def write_json(p, data):
    p = Path(p)
    tmp = p.with_name(p.name + ".tmp")
    tmp.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    tmp.replace(p)


def frontmatter(path):
    """Parse simple `key: value` YAML frontmatter (single-line scalars only)."""
    try:
        text = Path(path).read_text(encoding="utf-8")
    except FileNotFoundError:
        return {}
    m = re.match(r"^---\s*\n(.*?)\n---\s*(\n|$)", text, re.S)
    if not m:
        return {}
    out = {}
    for line in m.group(1).splitlines():
        k, sep, v = line.partition(":")
        if sep and k.strip() and not k.startswith((" ", "#")):
            out[k.strip()] = v.strip().strip("\"'")
    return out


# ---------------------------------------------------------------- identifiers
def norm_doi(doi):
    if not doi:
        return None
    d = re.sub(r"^(https?://(dx\.)?doi\.org/|doi:\s*)", "", doi.strip().lower())
    d = d.rstrip(".,;)]")
    return d if d.startswith("10.") else None


def norm_arxiv(s):
    if not s:
        return None
    s = s.strip()
    m = re.search(r"10\.48550/arxiv\.(.+)$", s, re.I)
    if m:
        s = m.group(1)
    m = re.search(r"(\d{4}\.\d{4,5}|[a-z\-]+(?:\.[a-z]{2})?/\d{7})(?:v\d+)?", s, re.I)
    return m.group(1).lower() if m else None


def same_work(a, b):
    """Return the reason two records describe the same work, else None."""
    for f in ("doi", "arxiv_id", "pmid", "openalex_id"):
        if a.get(f) and b.get(f) and a[f] == b[f]:
            return f
    ta, tb = norm_title(a.get("title")), norm_title(b.get("title"))
    if len(ta) > 15 and len(tb) > 15:
        r = difflib.SequenceMatcher(None, ta, tb).ratio()
        ya, yb = a.get("year"), b.get("year")
        # +-2 years: a preprint and its published version are the same work.
        if r >= 0.93 and (not ya or not yb or abs(int(ya) - int(yb)) <= 2):
            return f"title-similarity {r:.2f}"
    return None


def detect_id(raw):
    """Classify a user/agent-supplied identifier -> (kind, value)."""
    s = raw.strip()
    if norm_doi(s) and not s.lower().startswith(("10.48550/arxiv", "https://doi.org/10.48550/arxiv")):
        return "doi", norm_doi(s)
    if re.match(r"^(pmid:)?\d{6,9}$", s, re.I):
        return "pmid", s.split(":")[-1]
    if re.match(r"^(https://openalex\.org/)?W\d+$", s, re.I):
        return "openalex", s.rsplit("/", 1)[-1].upper()
    if norm_arxiv(s):
        return "arxiv", norm_arxiv(s)
    return None, s


def blank_record(**kw):
    rec = {"title": None, "authors": [], "year": None, "venue": None, "type": None,
           "venue_kind": "unknown", "doi": None, "arxiv_id": None, "pmid": None, "pmcid": None,
           "openalex_id": None, "url": None, "oa_pdf_url": None, "is_oa": None,
           "is_retracted": False, "cited_by": None, "abstract": None, "sources": []}
    rec.update({k: v for k, v in kw.items() if v not in (None, "", [])})
    return rec


def merge(primary, secondary):
    """Fill gaps in primary from secondary; never overwrite primary values."""
    if not secondary:
        return primary
    out = dict(primary)
    for k, v in secondary.items():
        if out.get(k) in (None, "", [], "unknown") and v not in (None, "", []):
            out[k] = v
    out["sources"] = sorted(set(primary.get("sources", [])) | set(secondary.get("sources", [])))
    out["is_retracted"] = bool(primary.get("is_retracted") or secondary.get("is_retracted"))
    return out


def split_name(display):
    if "," in (display or ""):  # "Family, Given" form (OpenAlex sometimes uses it)
        family, _, given = display.partition(",")
        return {"family": family.strip(), "given": given.strip()}
    parts = (display or "").strip().split()
    if not parts:
        return {"family": "", "given": ""}
    return {"family": parts[-1], "given": " ".join(parts[:-1])}


# ---------------------------------------------------------------- HTTP
def check_host(url):
    host = (urllib.parse.urlparse(url).hostname or "").lower()
    if any(b in host for b in BLOCKED_HOSTS):
        raise PermissionError(f"refusing blocked host (copyright): {host}")


def http_get(url, accept=None, raw=False, timeout=30, retries=3):
    check_host(url)
    headers = {"User-Agent": UA}
    if accept:
        headers["Accept"] = accept
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=timeout) as r:
                check_host(r.geturl())
                body = r.read()
                if raw:
                    return body, r.headers.get("Content-Type", ""), r.geturl()
                return body.decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504) and attempt < retries - 1:
                time.sleep(3 * (attempt + 1))
                continue
            raise
        except urllib.error.URLError:
            if attempt < retries - 1:
                time.sleep(2 * (attempt + 1))
                continue
            raise


def http_json(url, **kw):
    return json.loads(http_get(url, accept="application/json", **kw))


def polite(params, openalex=False):
    if CONTACT:
        params["mailto"] = CONTACT
    if openalex and OPENALEX_KEY:
        params["api_key"] = OPENALEX_KEY
    return urllib.parse.urlencode(params)


def explain(e):
    """Short human-readable reason for a failed API call, including the API's own message."""
    if isinstance(e, urllib.error.HTTPError):
        try:
            body = json.loads(e.read().decode("utf-8", "replace"))
            detail = body.get("message") or body.get("error") or ""
        except Exception:
            detail = ""
        hint = " Set OPENALEX_API_KEY (see README)." if "openalex" in (e.url or "") and e.code in (403, 429, 503) else ""
        return f"HTTP {e.code} {detail}".strip()[:220] + hint
    return str(e)[:200]


# ---------------------------------------------------------------- sources
def from_openalex(w):
    locs = w.get("locations") or []
    best = w.get("best_oa_location") or {}
    prim = w.get("primary_location") or {}
    src = prim.get("source") or {}
    pdf = best.get("pdf_url") or next((l.get("pdf_url") for l in locs if l.get("is_oa") and l.get("pdf_url")), None)
    arx = next((norm_arxiv(l.get("landing_page_url")) for l in locs
                if "arxiv.org" in (l.get("landing_page_url") or "")), None)
    ids = w.get("ids") or {}
    doi = norm_doi(w.get("doi"))
    arx = arx or (norm_arxiv(doi) if doi and doi.startswith("10.48550/") else None)
    if w.get("type") == "preprint" or src.get("type") == "repository":
        kind = "preprint"
    elif src.get("type") in ("journal", "conference"):
        kind = "published"
    elif src.get("type") in ("book series", "ebook platform") or "book" in (w.get("type") or ""):
        kind = "book"
    else:
        kind = "unknown"
    inv = w.get("abstract_inverted_index")
    abstract = " ".join(t for _, t in sorted((i, t) for t, idx in inv.items() for i in idx)) if inv else None
    pmid = (ids.get("pmid") or "").rsplit("/", 1)[-1] or None
    pmcid = (ids.get("pmcid") or "").rsplit("/", 1)[-1] or None
    return blank_record(
        title=strip_tags(w.get("title") or w.get("display_name")),
        authors=[split_name((a.get("author") or {}).get("display_name")) for a in w.get("authorships") or []],
        year=w.get("publication_year"), venue=src.get("display_name"), type=w.get("type"),
        venue_kind=kind, doi=doi, arxiv_id=arx, pmid=pmid, pmcid=pmcid and pmcid.upper(),
        openalex_id=(w.get("id") or "").rsplit("/", 1)[-1] or None,
        url=prim.get("landing_page_url") or (f"https://doi.org/{doi}" if doi else None),
        oa_pdf_url=pdf, is_oa=(w.get("open_access") or {}).get("is_oa"),
        is_retracted=bool(w.get("is_retracted")), cited_by=w.get("cited_by_count"),
        abstract=abstract, sources=["openalex"])


def from_crossref(m):
    parts = ((m.get("issued") or m.get("published") or {}).get("date-parts") or [[None]])[0]
    typ = m.get("type")
    kind = {"journal-article": "published", "proceedings-article": "published", "posted-content": "preprint",
            "book-chapter": "book", "book": "book", "monograph": "book"}.get(typ, "unknown")
    retracted = any((u.get("type") or "").lower() == "retraction" for u in m.get("updated-by") or [])
    doi = norm_doi(m.get("DOI"))
    return blank_record(
        title=strip_tags((m.get("title") or [None])[0]),
        authors=[{"family": a.get("family") or a.get("name") or "", "given": a.get("given") or ""}
                 for a in m.get("author") or []],
        year=parts[0] if parts else None, venue=(m.get("container-title") or [None])[0], type=typ,
        venue_kind=kind, doi=doi, url=m.get("URL"), is_retracted=retracted,
        cited_by=m.get("is-referenced-by-count"),
        abstract=strip_tags(m.get("abstract")) or None, sources=["crossref"])


AT = "{http://www.w3.org/2005/Atom}"
AX = "{http://arxiv.org/schemas/atom}"


def from_arxiv_entry(e):
    aid = norm_arxiv(e.findtext(f"{AT}id"))
    jref = (e.findtext(f"{AX}journal_ref") or "").strip()
    return blank_record(
        title=" ".join((e.findtext(f"{AT}title") or "").split()),
        authors=[split_name(a.findtext(f"{AT}name")) for a in e.findall(f"{AT}author")],
        year=int((e.findtext(f"{AT}published") or "0")[:4]) or None, venue="arXiv",
        type="preprint", venue_kind="preprint", doi=norm_doi(e.findtext(f"{AX}doi")),
        arxiv_id=aid, url=f"https://arxiv.org/abs/{aid}", oa_pdf_url=f"https://arxiv.org/pdf/{aid}",
        is_oa=True, abstract=" ".join((e.findtext(f"{AT}summary") or "").split()) or None,
        journal_ref=jref or None, sources=["arxiv"])


def from_pubmed(doc):
    ids = {i.get("idtype"): i.get("value") for i in doc.get("articleids", [])}
    pmc = ids.get("pmc") or ids.get("pmcid")
    pmc = pmc and re.search(r"PMC\d+", pmc, re.I) and re.search(r"PMC\d+", pmc, re.I).group(0).upper()
    names = [a.get("name", "") for a in doc.get("authors", []) if a.get("authtype", "Author") == "Author"]
    return blank_record(
        title=strip_tags(doc.get("title", "")).rstrip("."),
        authors=[{"family": n.rsplit(" ", 1)[0], "given": n.rsplit(" ", 1)[-1] if " " in n else ""} for n in names],
        year=int(m.group(0)) if (m := re.search(r"\d{4}", doc.get("pubdate", ""))) else None,
        venue=doc.get("fulljournalname") or doc.get("source"), type="journal-article",
        venue_kind="preprint" if "Preprint" in doc.get("pubtype", []) else "published",
        doi=norm_doi(ids.get("doi")), pmid=str(doc.get("uid")), pmcid=pmc,
        url=f"https://pubmed.ncbi.nlm.nih.gov/{doc.get('uid')}/",
        oa_pdf_url=f"https://europepmc.org/articles/{pmc}?pdf=render" if pmc else None,
        is_oa=bool(pmc) or None, sources=["pubmed"])


def search_openalex(q, limit, y0=None, y1=None):
    params = {"search": q, "per-page": min(limit, 50)}
    filt = [f for f in (y0 and f"from_publication_date:{y0}-01-01", y1 and f"to_publication_date:{y1}-12-31") if f]
    if filt:
        params["filter"] = ",".join(filt)
    return [from_openalex(w) for w in http_json("https://api.openalex.org/works?" + polite(params, openalex=True))["results"]]


def search_crossref(q, limit, y0=None, y1=None):
    params = {"query.bibliographic": q, "rows": min(limit, 50)}
    filt = [f for f in (y0 and f"from-pub-date:{y0}", y1 and f"until-pub-date:{y1}") if f]
    if filt:
        params["filter"] = ",".join(filt)
    return [from_crossref(m) for m in http_json("https://api.crossref.org/works?" + polite(params))["message"]["items"]]


def search_arxiv(q, limit, y0=None, y1=None):
    words = [w for w in re.findall(r"\w+", q) if w.lower() not in STOP]
    # exact phrase OR all terms: arXiv's relevance ranking alone buries exact matches
    phrase = " ".join(re.findall(r"\w+", q))
    terms = f'all:"{phrase}" OR (' + " AND ".join(f"all:{w}" for w in words) + ")"
    url = "https://export.arxiv.org/api/query?" + urllib.parse.urlencode(
        {"search_query": terms, "max_results": min(limit, 50), "sortBy": "relevance"})
    recs = [from_arxiv_entry(e) for e in ET.fromstring(http_get(url)).findall(f"{AT}entry")]
    return [r for r in recs if (not y0 or (r["year"] or 0) >= int(y0)) and (not y1 or (r["year"] or 9999) <= int(y1))]


def pubmed_summaries(pmids):
    if not pmids:
        return []
    res = http_json("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?" +
                    urllib.parse.urlencode({"db": "pubmed", "id": ",".join(pmids), "retmode": "json"}))["result"]
    return [from_pubmed(res[u]) for u in res.get("uids", [])]


def search_pubmed(q, limit, y0=None, y1=None):
    params = {"db": "pubmed", "term": q, "retmax": min(limit, 50), "retmode": "json", "sort": "relevance"}
    if y0 or y1:
        params.update({"datetype": "pdat", "mindate": y0 or 1800, "maxdate": y1 or 3000})
    ids = http_json("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?" +
                    urllib.parse.urlencode(params))["esearchresult"]["idlist"]
    return pubmed_summaries(ids)


SEARCHERS = {"openalex": search_openalex, "crossref": search_crossref, "arxiv": search_arxiv, "pubmed": search_pubmed}


def lookup_crossref(doi):
    try:
        return from_crossref(http_json(f"https://api.crossref.org/works/{urllib.parse.quote(doi, safe='/')}")["message"])
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        raise


def lookup_openalex(ident):
    """ident: OpenAlex W-id or 'doi:10.x/y'."""
    try:
        return from_openalex(http_json(f"https://api.openalex.org/works/{urllib.parse.quote(ident, safe='/:')}?" + polite({}, openalex=True)))
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        raise


def lookup_arxiv(aid):
    feed = ET.fromstring(http_get("https://export.arxiv.org/api/query?" + urllib.parse.urlencode({"id_list": aid})))
    entries = [e for e in feed.findall(f"{AT}entry") if e.findtext(f"{AT}title")]
    return from_arxiv_entry(entries[0]) if entries else None


def agree(a, b):
    """Compare two metadata records of supposedly the same work."""
    sim = difflib.SequenceMatcher(None, norm_title(a.get("title")), norm_title(b.get("title"))).ratio()
    ya, yb = a.get("year"), b.get("year")
    year_ok = bool(ya and yb and abs(int(ya) - int(yb)) <= 1)
    fa = ascii_lower((a.get("authors") or [{}])[0].get("family", ""))
    fb = ascii_lower((b.get("authors") or [{}])[0].get("family", ""))
    author_ok = bool(fa and fb and (fa in fb or fb in fa))
    return {"title_similarity": round(sim, 3), "year_match": year_ok, "first_author_match": author_ok,
            "ok": sim >= 0.9 and year_ok and author_ok}


def resolve(kind, value):
    """Resolve an identifier to an authoritative, cross-checked metadata record."""
    checks = {}
    if kind == "openalex":
        oa = lookup_openalex(value)
        if not oa:
            raise LookupError(f"OpenAlex has no work {value}")
        if oa.get("doi") and not oa["doi"].startswith("10.48550/"):
            return resolve("doi", oa["doi"])
        if oa.get("arxiv_id"):
            return resolve("arxiv", oa["arxiv_id"])
        return oa, {"status": "single-source (openalex)", "checked": now()}
    if kind == "pmid":
        recs = pubmed_summaries([value])
        if not recs:
            raise LookupError(f"PubMed has no PMID {value}")
        pm = recs[0]
        if pm.get("doi"):
            rec, ver = resolve("doi", pm["doi"])
            return merge(rec, pm), ver
        return pm, {"status": "single-source (pubmed)", "checked": now()}
    if kind == "arxiv":
        ax = lookup_arxiv(value)
        if not ax:
            raise LookupError(f"arXiv has no paper {value}")
        if ax.get("doi") and not ax["doi"].startswith("10.48550/"):
            # A published (peer-reviewed) version exists: prefer its metadata, keep arXiv as OA copy.
            rec, ver = resolve("doi", ax["doi"])
            rec = merge(rec, ax)
            rec["arxiv_id"] = ax["arxiv_id"]
            return rec, ver
        oa = lookup_openalex(f"doi:10.48550/arxiv.{value}")
        if oa:
            checks["openalex"] = agree(ax, oa)
        rec = merge(ax, oa)
    elif kind == "doi":
        if value.startswith("10.48550/arxiv."):
            return resolve("arxiv", norm_arxiv(value))
        cr = lookup_crossref(value)
        oa = lookup_openalex(f"doi:{value}")
        if not cr and not oa:
            raise LookupError(f"DOI {value} not found in Crossref or OpenAlex (check for typos)")
        if cr and oa:
            checks["openalex"] = agree(cr, oa)
        rec = merge(cr or oa, oa if cr else None)
    else:
        raise LookupError(f"unrecognised identifier '{value}'")
    if not checks:
        status = f"single-source ({','.join(rec['sources'])})"
    else:
        status = "verified" if all(c["ok"] for c in checks.values()) else "MISMATCH"
    return rec, {"status": status, "checked": now(), "cross_checks": checks}


# ---------------------------------------------------------------- projects & registry
def load_registry():
    return read_json(RESEARCH / "registry.json", {"version": 1, "projects": []})


def save_registry(reg):
    RESEARCH.mkdir(parents=True, exist_ok=True)
    write_json(RESEARCH / "registry.json", reg)


def project_dir(ident):
    projects = load_registry()["projects"]
    if ident in [p["id"] for p in projects]:
        return RESEARCH / ident
    hits = [p["id"] for p in projects if ident.lower() in (p["id"] + " " + p["topic"]).lower()]
    if len(hits) == 1:
        return RESEARCH / hits[0]
    if not hits:
        die(f"no project matches '{ident}'. Run `rlab list`.")
    die(f"'{ident}' is ambiguous: {', '.join(hits)}")


def log_event(d, phase, msg):
    with open(Path(d) / "research-log.md", "a", encoding="utf-8") as f:
        f.write(f"- {dt.datetime.now().strftime('%Y-%m-%d %H:%M')} · {phase} · {msg}\n")


def load_papers(d):
    return [m for m in (read_json(p) for p in sorted((Path(d) / "papers").glob("*/metadata.json"))) if m]


def save_meta(d, meta):
    write_json(Path(d) / "papers" / meta["key"] / "metadata.json", meta)


def make_key(rec, existing):
    fam = re.sub(r"[^a-z]", "", ascii_lower((rec.get("authors") or [{}])[0].get("family", ""))) or "anon"
    word = next((w for w in norm_title(rec.get("title")).split() if w not in STOP and w.isalpha()), "paper")
    base = f"{fam}{rec.get('year') or 'nd'}{word}"
    key, i = base, 0
    while key in existing:
        key, i = base + "abcdefghijklmnopqrstuvwxyz"[i % 26] * (i // 26 + 1), i + 1
    return key


def phases(d):
    try:
        text = (Path(d) / "STATUS.md").read_text(encoding="utf-8")
    except FileNotFoundError:
        return []
    sec = re.search(r"^## Phases\s*\n(.*?)(?=^## |\Z)", text, re.M | re.S)
    if not sec:
        return []
    return [(m.group(1) == "x", m.group(2).split(" — ")[0].strip()) for m in re.finditer(r"^- \[( |x)\] (.+)$", sec.group(1), re.M)]


def current_phase(d):
    return next((name for done, name in phases(d) if not done), "complete")


# ---------------------------------------------------------------- indexing
MATRIX_COLS = ["key", "year", "title", "venue", "venue_kind", "retracted", "fulltext", "analysis",
               "evidence_basis", "design", "dataset", "sample_size", "metrics", "main_finding", "relevance"]


def matrix_row(d, m):
    fm = frontmatter(Path(d) / "papers" / m["key"] / "analysis.md")
    return {"key": m["key"], "year": m.get("year") or "", "title": m.get("title") or "",
            "venue": m.get("venue") or "", "venue_kind": m.get("venue_kind") or "",
            "retracted": "YES" if m.get("is_retracted") else "",
            "fulltext": (m.get("fulltext") or {}).get("status", "not-tried"),
            "analysis": fm.get("status", "none"),
            **{k: fm.get(k, "") for k in MATRIX_COLS[8:]}}


def refresh(d):
    """Rebuild every derived file for one project, then the registry and global index."""
    d = Path(d)
    papers = load_papers(d)
    rows = [matrix_row(d, m) for m in papers]
    with open(d / "literature-matrix.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=MATRIX_COLS)
        w.writeheader()
        w.writerows(rows)
    cell = lambda v: str(v).replace("|", "\\|").replace("\n", " ")
    md = ["# Literature matrix", "",
          "_Generated by `rlab index` from papers/*/metadata.json and analysis.md frontmatter. Do not edit by hand._", "",
          "| " + " | ".join(MATRIX_COLS) + " |", "|" + "---|" * len(MATRIX_COLS)]
    md += ["| " + " | ".join(cell(r[c]) for c in MATRIX_COLS) + " |" for r in rows]
    (d / "literature-matrix.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    stats = {"papers": len(papers),
             "fulltext": sum(r["fulltext"] in ("downloaded", "user-supplied") for r in rows),
             "no_fulltext": sum(r["fulltext"] == "unavailable" for r in rows),
             "analysed": sum(r["analysis"] == "complete" for r in rows),
             "analysis_ready": sum(r["analysis"] == "ready" for r in rows),
             "analysis_draft": sum(r["analysis"] == "draft" for r in rows),
             "preprints": sum(r["venue_kind"] == "preprint" for r in rows),
             "retracted": sum(bool(r["retracted"]) for r in rows),
             "unverified": sum((m.get("verification") or {}).get("status") != "verified" for m in papers)}
    phase = current_phase(d)
    status_md = d / "STATUS.md"
    if status_md.exists():
        block = "\n".join([STATS_START, f"_Auto-updated {now()} by `rlab index`._", "",
                           f"- Current phase: **{phase}**"] +
                          [f"- {k.replace('_', ' ')}: {v}" for k, v in stats.items()] + [STATS_END])
        text = status_md.read_text(encoding="utf-8")
        text = re.sub(re.escape(STATS_START) + r".*?" + re.escape(STATS_END), lambda _: block, text, flags=re.S)
        status_md.write_text(text, encoding="utf-8")

    reg = load_registry()
    for p in reg["projects"]:
        if p["id"] == d.name:
            p.update({"phase": phase, "stats": stats, "updated": now()})
    save_registry(reg)
    lines = ["# Research projects", "", "_Generated by `rlab index`. Resume any project with: \"Resume research <id>\"._", "",
             "| id | topic | phase | papers | full text | analysed | updated |", "|---|---|---|---|---|---|---|"]
    for p in sorted(reg["projects"], key=lambda p: p.get("updated", ""), reverse=True):
        s = p.get("stats", {})
        lines.append(f"| {p['id']} | {cell(p['topic'])} | {p.get('phase', '')} | {s.get('papers', 0)} | "
                     f"{s.get('fulltext', 0)} | {s.get('analysed', 0)} | {p.get('updated', '')[:16]} |")
    (RESEARCH / "INDEX.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return stats


# ---------------------------------------------------------------- PDF handling
def pdftotext(pdf, first=None, last=None):
    if not shutil.which("pdftotext"):
        die("pdftotext not found: install poppler-utils (Fedora: sudo dnf install poppler-utils)")
    cmd = ["pdftotext", "-layout"] + (["-f", str(first)] if first else []) + (["-l", str(last)] if last else [])
    r = subprocess.run(cmd + [str(pdf), "-"], capture_output=True, text=True, timeout=180)
    if r.returncode:
        raise RuntimeError(f"pdftotext failed: {r.stderr.strip()[:200]}")
    return r.stdout


def extract_text(pdf, out):
    """Write fulltext with explicit page markers so every claim can cite a page. Returns page count."""
    n = pdf_page_count(pdf)
    if n:  # page by page: stray form feeds inside figures must not create fake pages
        pages = [pdftotext(pdf, i, i).replace("\f", "") for i in range(1, n + 1)]
    else:
        pages = pdftotext(pdf).split("\f")
        if pages and not pages[-1].strip():
            pages = pages[:-1]
    pages = [pg.replace("\x00", "") for pg in pages]  # NUL bytes make grep treat the file as binary
    body = [f"# Full text extracted from {Path(pdf).name} by pdftotext.",
            "# [PDF page N] = Nth page of the PDF file, which may differ from the printed page number.", ""]
    for i, p in enumerate(pages, 1):
        body += [f"\n=== [PDF page {i}] ===\n", p.rstrip()]
    Path(out).write_text("\n".join(body) + "\n", encoding="utf-8")
    return len(pages), sum(len(p.strip()) for p in pages)


def pdf_page_count(pdf):
    if not shutil.which("pdfinfo"):
        return 0
    r = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True, timeout=60)
    m = re.search(r"^Pages:\s*(\d+)", r.stdout, re.M)
    return int(m.group(1)) if m else 0


def pdf_meta(pdf):
    info = {}
    if shutil.which("pdfinfo"):
        r = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True, timeout=60)
        for line in r.stdout.splitlines():
            k, _, v = line.partition(":")
            info[k.strip()] = v.strip()
    text = pdftotext(pdf, 1, 2)
    dois = list(dict.fromkeys(norm_doi(x) for x in re.findall(r"10\.\d{4,9}/[^\s\"<>,;]+", text) if norm_doi(x)))
    arx = list(dict.fromkeys(m.lower() for m in re.findall(r"arXiv:\s*(\d{4}\.\d{4,5})", text, re.I)))
    return {"pages": int(info.get("Pages", 0) or 0), "pdf_title": info.get("Title") or None,
            "pdf_author": info.get("Author") or None, "dois": dois, "arxiv_ids": arx,
            "first_lines": [l.strip() for l in text.splitlines() if l.strip()][:8], "_text": text}


def identity_check(meta, pm):
    """Does the PDF look like the paper the metadata describes?"""
    if meta.get("doi") and meta["doi"] in pm["dois"]:
        return "match (DOI printed in PDF)"
    if meta.get("arxiv_id") and meta["arxiv_id"] in pm["arxiv_ids"]:
        return "match (arXiv id printed in PDF)"
    words = norm_title(meta.get("title")).split()[:8]
    if words and " ".join(words) in norm_title(pm["_text"]):
        return "probable (title found on first pages)"
    return "UNCONFIRMED (neither DOI nor title found on first pages - check manually)"


def store_pdf(d, meta, data, origin, status):
    pdir = Path(d) / "papers" / meta["key"]
    pdf = pdir / "paper.pdf"
    with open(pdf, "xb") as f:  # x-mode: never overwrite an existing original
        f.write(data)
    pm = pdf_meta(pdf)
    npages, nchars = extract_text(pdf, pdir / "fulltext.txt")
    meta["fulltext"] = {"status": status, "source": origin, "retrieved": now(),
                        "sha256": hashlib.sha256(data).hexdigest(), "pages": npages,
                        "text_layer": "ok" if nchars > 500 * max(1, npages) * 0.2 else "POOR (scanned? needs OCR)",
                        "identity": identity_check(meta, pm)}
    save_meta(d, meta)
    return meta["fulltext"]


def oa_candidates(meta):
    urls = [meta.get("oa_pdf_url")]
    if meta.get("arxiv_id"):
        urls.append(f"https://arxiv.org/pdf/{meta['arxiv_id']}")
    if meta.get("pmcid"):
        urls.append(f"https://europepmc.org/articles/{meta['pmcid']}?pdf=render")
    if CONTACT and meta.get("doi"):
        try:
            up = http_json(f"https://api.unpaywall.org/v2/{urllib.parse.quote(meta['doi'], safe='/')}?email={urllib.parse.quote(CONTACT)}")
            urls += [l.get("url_for_pdf") for l in [up.get("best_oa_location") or {}] + (up.get("oa_locations") or [])]
        except Exception as e:  # Unpaywall is optional
            print(f"  unpaywall: {e}")
    return [u for u in dict.fromkeys(urls) if u]


# ---------------------------------------------------------------- BibTeX
def bib_escape(s):
    return re.sub(r"([&%#_$])", r"\\\1", str(s or ""))


def to_bibtex(m):
    typ, venue = m.get("type") or "", m.get("venue") or ""
    if typ in ("journal-article", "article") and m.get("venue_kind") == "published":
        etype, vfield = "article", "journal"
    elif typ == "proceedings-article" or re.search(r"conference|proceedings|symposium|workshop", venue, re.I):
        etype, vfield = "inproceedings", "booktitle"
    elif typ in ("book-chapter",):
        etype, vfield = "incollection", "booktitle"
    elif typ in ("book", "monograph"):
        etype, vfield = "book", "publisher"
    else:
        etype, vfield = "misc", "howpublished"
    authors = " and ".join(f"{a.get('family', '')}, {a.get('given', '')}".strip(", ") for a in m.get("authors", []))
    fields = [("title", "{" + bib_escape(m.get("title")) + "}"), ("author", bib_escape(authors)),
              ("year", m.get("year")), (vfield, bib_escape(venue)), ("doi", m.get("doi")),
              ("url", m.get("url"))]
    if m.get("arxiv_id"):
        fields += [("eprint", m["arxiv_id"]), ("archiveprefix", "arXiv")]
    body = ",\n".join(f"  {k} = {{{v}}}" for k, v in fields if v)
    return f"@{etype}{{{m['key']},\n{body}\n}}\n"


# ---------------------------------------------------------------- commands
def cmd_new(a):
    RESEARCH.mkdir(parents=True, exist_ok=True)
    reg = load_registry()
    base = f"{today()}-{slugify(a.slug or a.topic, 40)}"
    pid, n = base, 2
    while (RESEARCH / pid).exists() or any(p["id"] == pid for p in reg["projects"]):
        pid, n = f"{base}-{n}", n + 1
    d = RESEARCH / pid
    shutil.copytree(TEMPLATES / "project", d)
    for f in d.rglob("*.md"):
        t = f.read_text(encoding="utf-8")
        f.write_text(t.replace("{{TOPIC}}", a.topic).replace("{{PROJECT_ID}}", pid).replace("{{DATE}}", today()),
                     encoding="utf-8")
    reg["projects"].append({"id": pid, "topic": a.topic, "created": now(), "path": f"research/{pid}"})
    save_registry(reg)
    log_event(d, "setup", f"Project created. Topic: {a.topic}")
    refresh(d)
    print(f"created {pid}\npath: {d}")


def cmd_list(a):
    reg = load_registry()
    if not reg["projects"]:
        print("no research projects yet")
    for p in sorted(reg["projects"], key=lambda p: p.get("updated", ""), reverse=True):
        s = p.get("stats", {})
        print(f"{p['id']}  [{p.get('phase', '?')}]  papers={s.get('papers', 0)} analysed={s.get('analysed', 0)}  — {p['topic']}")


def cmd_status(a):
    if not a.project:
        return cmd_list(a)
    d = project_dir(a.project)
    stats = refresh(d)
    entry = next(p for p in load_registry()["projects"] if p["id"] == d.name)
    print(f"project: {d.name}\ntopic:   {entry['topic']}\npath:    {d}\nphase:   {current_phase(d)}")
    print("phases:  " + "  ".join(("[x] " if done else "[ ] ") + n for done, n in phases(d)))
    print("stats:   " + ", ".join(f"{k}={v}" for k, v in stats.items()))
    text = (d / "STATUS.md").read_text(encoding="utf-8")
    for section in ("Next actions", "Blocked / needs user"):
        m = re.search(rf"^## {section}\s*\n(.*?)(?=^## |\Z)", text, re.M | re.S)
        body = re.sub(r"<!--.*?-->", "", m.group(1), flags=re.S).strip() if m else ""
        if body:
            print(f"\n{section}:\n{body}")
    todo = [m for m in load_papers(d)
            if frontmatter(d / "papers" / m["key"] / "analysis.md").get("status") != "complete"]
    if todo:
        print("\npapers needing work:")
        for m in todo:
            ft = (m.get("fulltext") or {}).get("status", "not-tried")
            an = frontmatter(d / "papers" / m["key"] / "analysis.md").get("status", "none")
            print(f"  {m['key']}: fulltext={ft} analysis={an}")
    entries = [l for l in (d / "research-log.md").read_text(encoding="utf-8").splitlines() if l.startswith("- ")]
    if entries:
        print("\nlast log entries:\n" + "\n".join(entries[-5:]))


def cmd_search(a):
    d = project_dir(a.project)
    sources = [s.strip() for s in a.sources.split(",") if s.strip()]
    bad = [s for s in sources if s not in SEARCHERS]
    if bad:
        die(f"unknown source(s) {bad}; choose from {list(SEARCHERS)}")
    results, errors, raw = [], {}, 0
    for s in sources:
        try:
            got = SEARCHERS[s](a.query, a.limit, a.year_from, a.year_to)
        except Exception as e:  # one failing API must not sink the search
            errors[s] = explain(e)
            print(f"  {s}: FAILED ({errors[s]})")
            continue
        raw += len(got)
        for r in got:
            dup = next((x for x in results if same_work(x, r)), None)
            if dup:
                dup.update(merge(dup, r))
            else:
                results.append(r)
    existing = load_papers(d)
    for i, r in enumerate(results, 1):
        r["idx"] = i
        hit = next((m for m in existing if same_work(m, r)), None)
        r["in_project"] = hit["key"] if hit else None
    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    out = d / "search" / f"{stamp}-{slugify(a.query, 40)}.json"
    write_json(out, {"query": a.query, "sources": sources, "year_from": a.year_from, "year_to": a.year_to,
                     "run_at": now(), "raw_hits": raw, "unique": len(results), "errors": errors, "results": results})
    with open(d / "search" / "search-log.md", "a", encoding="utf-8") as f:
        f.write(f"| {now()[:16]} | `{a.query}` | {','.join(sources)} | {a.year_from or ''}-{a.year_to or ''} | "
                f"{raw} | {len(results)} | {out.name} |\n")
    log_event(d, "discovery", f"search `{a.query}` on {','.join(sources)}: {raw} hits, {len(results)} unique -> search/{out.name}")
    print(f"saved {len(results)} unique results ({raw} raw) -> {out.relative_to(ROOT)}")
    for r in results:
        ids = r.get("doi") or (r.get("arxiv_id") and f"arXiv:{r['arxiv_id']}") or r.get("openalex_id") or (r.get("pmid") and f"pmid:{r['pmid']}")
        flags = "".join([" OA" if r.get("is_oa") else "", " RETRACTED" if r.get("is_retracted") else "",
                         f" IN-PROJECT:{r['in_project']}" if r["in_project"] else ""])
        print(f"[{r['idx']}] {r.get('year') or '----'} {r['venue_kind'][:9]:9} cites={r.get('cited_by') if r.get('cited_by') is not None else '?':<5} "
              f"{(r.get('title') or '')[:100]} | {(r.get('venue') or '')[:40]} | {ids}{flags}")


def cmd_add(a):
    d = project_dir(a.project)
    added = 0
    for raw in a.ids:
        kind, value = detect_id(raw)
        if not kind:
            print(f"SKIP {raw}: not a DOI, arXiv id, OpenAlex W-id or PMID")
            continue
        existing = load_papers(d)
        probe = {"doi": value} if kind == "doi" else {"arxiv_id": value} if kind == "arxiv" else \
            {"pmid": value} if kind == "pmid" else {"openalex_id": value}
        hit = next((m for m in existing if same_work(m, probe)), None)
        if hit:
            print(f"DUPLICATE {raw}: already in project as {hit['key']} (same {next(iter(probe))})")
            continue
        try:
            rec, ver = resolve(kind, value)
        except Exception as e:
            print(f"FAIL {raw}: {explain(e)}")
            continue
        hit = next(((m, why) for m in existing if (why := same_work(m, rec))), None)
        if hit and not (a.allow_similar and hit[1].startswith("title")):
            print(f"DUPLICATE {raw}: matches {hit[0]['key']} ({hit[1]}). "
                  f"If one is a preprint, keep the peer-reviewed version.")
            continue
        key = make_key(rec, {m["key"] for m in existing})
        (d / "papers" / key).mkdir(parents=True)
        rec.update({"key": key, "added": now(), "added_reason": a.reason, "found_via": a.query,
                    "verification": ver, "fulltext": {"status": "not-tried"}})
        save_meta(d, rec)
        added += 1
        warn = "  WARNING: RETRACTED" if rec.get("is_retracted") else ""
        warn += f"  WARNING: metadata {ver['status']}" if ver["status"] != "verified" else ""
        print(f"ADDED {key}: {rec['title']} ({rec.get('year')}, {rec.get('venue')}, {rec['venue_kind']}){warn}")
        log_event(d, "screening", f"included {key} ({raw}){': ' + a.reason if a.reason else ''}")
    refresh(d)
    print(f"{added} added")


def selected(d, keys):
    papers = load_papers(d)
    if not keys:
        return papers
    by = {m["key"]: m for m in papers}
    missing = [k for k in keys if k not in by]
    if missing:
        die(f"unknown paper key(s): {missing}")
    return [by[k] for k in keys]


def cmd_fetch(a):
    d = project_dir(a.project)
    for meta in selected(d, a.keys):
        if (d / "papers" / meta["key"] / "paper.pdf").exists():
            print(f"HAVE {meta['key']}: paper.pdf already present (never overwritten)")
            continue
        tried = []
        for url in oa_candidates(meta):
            try:
                data, ctype, _ = http_get(url, accept="application/pdf", raw=True, timeout=90)
            except Exception as e:
                tried.append(f"{url} -> {explain(e)[:120]}")
                continue
            if not data.startswith(b"%PDF-"):
                tried.append(f"{url} -> not a PDF ({ctype or 'unknown'}; landing page or access wall)")
                continue
            ft = store_pdf(d, meta, data, url, "downloaded")
            print(f"GOT  {meta['key']}: {ft['pages']} pages from {url} | identity: {ft['identity']} | text: {ft['text_layer']}")
            log_event(d, "acquisition", f"downloaded OA PDF for {meta['key']} from {url}")
            break
        else:
            meta["fulltext"] = {"status": "unavailable", "checked": now(), "tried": tried}
            save_meta(d, meta)
            print(f"NONE {meta['key']}: no legal open-access PDF found. "
                  f"User may supply it: rlab attach {d.name} {meta['key']} /path/to.pdf")
            for t in tried:
                print(f"     tried {t}")
    refresh(d)


def cmd_attach(a):
    d = project_dir(a.project)
    meta = selected(d, [a.key])[0]
    src = Path(a.pdf).expanduser()
    data = src.read_bytes()
    if not data.startswith(b"%PDF-"):
        die(f"{src} is not a PDF")
    if (d / "papers" / meta["key"] / "paper.pdf").exists():
        die("paper.pdf already exists; originals are never overwritten. Remove it yourself first if intended.")
    ft = store_pdf(d, meta, data, f"user-supplied: {src.name}", "user-supplied")
    log_event(d, "acquisition", f"user-supplied PDF attached to {meta['key']} ({src.name})")
    refresh(d)
    print(f"ATTACHED {meta['key']}: {ft['pages']} pages | identity: {ft['identity']} | text: {ft['text_layer']}")


def cmd_pdf_meta(a):
    pm = pdf_meta(a.pdf)
    pm.pop("_text")
    print(json.dumps(pm, indent=2, ensure_ascii=False))


def cmd_dedup(a):
    d = project_dir(a.project)
    papers = load_papers(d)
    pairs = [(x["key"], y["key"], why) for i, x in enumerate(papers) for y in papers[i + 1:] if (why := same_work(x, y))]
    for k1, k2, why in pairs:
        print(f"DUPLICATE? {k1} <-> {k2} ({why})")
    print(f"{len(papers)} papers checked, {len(pairs)} possible duplicate pair(s)")


def cmd_validate(a):
    d = project_dir(a.project)
    for meta in selected(d, a.keys):
        checks = {}
        try:
            live = []
            if meta.get("doi") and not meta["doi"].startswith("10.48550/"):
                live += [("crossref", lookup_crossref(meta["doi"])), ("openalex", lookup_openalex(f"doi:{meta['doi']}"))]
            if meta.get("arxiv_id"):
                live.append(("arxiv", lookup_arxiv(meta["arxiv_id"])))
            for name, rec in live:
                checks[name] = agree(meta, rec) if rec else {"ok": False, "error": "not found"}
                if rec and rec.get("is_retracted"):
                    meta["is_retracted"] = True
            status = ("unverifiable (no DOI/arXiv id)" if not checks else
                      "verified" if all(c["ok"] for c in checks.values()) else "MISMATCH")
        except Exception as e:
            status = f"error: {explain(e)}"
        meta["verification"] = {"status": status, "checked": now(), "cross_checks": checks}
        pdf = d / "papers" / meta["key"] / "paper.pdf"
        if pdf.exists():
            meta.setdefault("fulltext", {})["identity"] = identity_check(meta, pdf_meta(pdf))
        save_meta(d, meta)
        print(f"{status:10} {meta['key']}" + (f" | pdf identity: {meta['fulltext']['identity']}" if pdf.exists() else "")
              + (" | RETRACTED" if meta.get("is_retracted") else ""))
    refresh(d)


def cmd_bib(a):
    d = project_dir(a.project)
    entries = []
    for meta in load_papers(d):
        f = d / "papers" / meta["key"] / "paper.bib"
        if not f.exists():
            bib = None
            if meta.get("doi") and not a.offline:
                try:  # publisher-registered BibTeX via DOI content negotiation
                    bib = http_get(f"https://doi.org/{meta['doi']}", accept="application/x-bibtex").strip()
                    bib = re.sub(r"^(@\w+\{)[^,]*,", lambda m: m.group(1) + meta["key"] + ",", bib, count=1) + "\n"
                    if not bib.startswith("@"):
                        bib = None
                except Exception:
                    bib = None
            f.write_text(bib or to_bibtex(meta), encoding="utf-8")
        entries.append(f.read_text(encoding="utf-8").strip())
    (d / "references.bib").write_text(f"% Generated by `rlab bib` on {now()} from papers/*/paper.bib\n\n" +
                                      "\n\n".join(entries) + "\n", encoding="utf-8")
    print(f"references.bib: {len(entries)} entries")


def cmd_scaffold(a):
    d = project_dir(a.project)
    tpl = (TEMPLATES / "paper-analysis.md").read_text(encoding="utf-8")
    for meta in selected(d, a.keys):
        f = d / "papers" / meta["key"] / "analysis.md"
        if f.exists():
            print(f"EXISTS {meta['key']}/analysis.md (not overwritten)")
            continue
        authors = "; ".join(f"{x.get('family')}, {x.get('given')}".strip(", ") for x in meta.get("authors", [])[:6])
        ft = meta.get("fulltext") or {}
        f.write_text(tpl.replace("{{KEY}}", meta["key"]).replace("{{TITLE}}", meta.get("title") or "")
                     .replace("{{AUTHORS}}", authors).replace("{{YEAR}}", str(meta.get("year") or ""))
                     .replace("{{VENUE}}", meta.get("venue") or "").replace("{{VENUE_KIND}}", meta.get("venue_kind") or "")
                     .replace("{{DOI}}", meta.get("doi") or "none").replace("{{URL}}", meta.get("url") or "")
                     .replace("{{BASIS}}", "full-text" if ft.get("status") in ("downloaded", "user-supplied") else "abstract-only")
                     .replace("{{DATE}}", today()), encoding="utf-8")
        print(f"CREATED {meta['key']}/analysis.md")
    refresh(d)


def cmd_cite_check(a):
    """Every [@key, p. N] must name a project paper, a page that exists, and no retracted paper."""
    d = project_dir(a.project)
    papers = {m["key"]: m for m in load_papers(d)}
    bad = 0
    for f in map(Path, a.files):
        text = f.read_text(encoding="utf-8")
        cites = [(k, p) for grp in re.findall(r"\[([^\[\]]*@[^\[\]]*)\]", text)
                 for k, p in re.findall(r"(?<![\w.])@([A-Za-z][\w:-]*)(?:,\s*pp?\.\s*(\d+))?", grp)]
        own = papers.get(f.parent.name) if f.name == "analysis.md" else None
        if own:  # analyses cite their own paper as (p. N)
            cites += [(own["key"], p) for p in re.findall(r"\(pp?\.\s*(\d+)", text)]
        for k, p in cites:
            m = papers.get(k)
            if not m:
                print(f"UNKNOWN KEY  {f.name}: @{k} is not a paper in this project")
                bad += 1
                continue
            if m.get("is_retracted"):
                print(f"RETRACTED    {f.name}: @{k} is retracted")
                bad += 1
            pages = (m.get("fulltext") or {}).get("pages")
            if p and pages and int(p) > pages:
                print(f"BAD PAGE     {f.name}: @{k} p. {p} but the PDF has {pages} pages")
                bad += 1
        print(f"{f.name}: {len(cites)} citations of {len({k for k, _ in cites})} papers")
    print("cite-check: OK" if not bad else f"cite-check: {bad} problem(s)")
    return 1 if bad else 0


def cmd_index(a):
    targets = [project_dir(a.project)] if a.project else [RESEARCH / p["id"] for p in load_registry()["projects"]]
    for d in targets:
        if d.exists():
            print(f"{d.name}: {refresh(d)}")


def cmd_log(a):
    d = project_dir(a.project)
    log_event(d, a.phase, a.message)
    print("logged")


def cmd_doctor(a):
    ok = True

    def check(cond, label, hint=""):
        nonlocal ok
        ok &= bool(cond)
        print(f"[{'ok' if cond else 'MISSING'}] {label}" + ("" if cond else f"  -> {hint}"))
    check(sys.version_info >= (3, 9), f"python {sys.version.split()[0]} (>=3.9)")
    for tool in ("pdftotext", "pdfinfo"):
        check(shutil.which(tool), tool, "install poppler-utils")
    check((TEMPLATES / "project" / "STATUS.md").exists(), "templates/project")
    for kind, pattern in (("skill", ".claude/skills/*/SKILL.md"), ("agent", ".claude/agents/*.md")):
        files = sorted(REPO.glob(pattern))
        check(files, f"{len(files)} {kind}s found", f"expected files at {pattern}")
        for f in files:
            fm = frontmatter(f)
            expect = f.parent.name if kind == "skill" else f.stem
            check(fm.get("name") == expect and fm.get("description"), f"{kind} {expect}: frontmatter name+description",
                  f"fix frontmatter in {f.relative_to(REPO)}")
    print(f"[info] OPENALEX_API_KEY {'set' if OPENALEX_KEY else 'not set (anonymous OpenAlex budget is small and search may pause; recommended)'}")
    print(f"[info] RLAB_CONTACT_EMAIL {'set (Unpaywall enabled)' if CONTACT else 'not set (Unpaywall disabled; optional)'}")
    if not a.offline:
        for name, url in (("openalex search", "https://api.openalex.org/works?" + polite({"search": "test", "per-page": 1}, openalex=True)),
                          ("crossref", "https://api.crossref.org/works?rows=1"),
                          ("arxiv", "https://export.arxiv.org/api/query?search_query=all:test&max_results=1"),
                          ("pubmed", "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/einfo.fcgi?retmode=json")):
            try:
                http_get(url, timeout=20, retries=1)
                check(True, f"network: {name}")
            except Exception as e:
                check(False, f"network: {name}", explain(e))
    print("doctor: all good" if ok else "doctor: problems found")
    return 0 if ok else 1


def main(argv=None):
    p = argparse.ArgumentParser(prog="rlab", description=__doc__.split("\n\n")[0])
    sub = p.add_subparsers(dest="cmd", required=True)

    def add(name, fn, help_):
        sp = sub.add_parser(name, help=help_)
        sp.set_defaults(fn=fn)
        return sp

    sp = add("new", cmd_new, "create a research project")
    sp.add_argument("topic")
    sp.add_argument("--slug", help="short name for the folder (default: from topic)")
    add("list", cmd_list, "list projects in the registry")
    for name in ("status", "resume"):
        sp = add(name, cmd_status, "show project state (no project: list all)")
        sp.add_argument("project", nargs="?")
    sp = add("search", cmd_search, "search academic sources, save + print deduplicated candidates")
    sp.add_argument("project")
    sp.add_argument("query")
    sp.add_argument("--sources", default="openalex,crossref,arxiv", help=f"comma list from {list(SEARCHERS)}")
    sp.add_argument("--limit", type=int, default=20, help="results per source (max 50)")
    sp.add_argument("--from", dest="year_from", type=int)
    sp.add_argument("--to", dest="year_to", type=int)
    sp = add("add", cmd_add, "resolve identifiers, verify metadata, reject duplicates, register papers")
    sp.add_argument("project")
    sp.add_argument("ids", nargs="+", help="DOI, arXiv id, OpenAlex W-id, or pmid:NNN")
    sp.add_argument("--reason", default="", help="why this paper is included (screening note)")
    sp.add_argument("--query", default=None, help="search query that found it")
    sp.add_argument("--allow-similar", action="store_true", help="add despite a title-only duplicate match")
    sp = add("fetch", cmd_fetch, "download legal open-access PDFs + extract text")
    sp.add_argument("project")
    sp.add_argument("keys", nargs="*")
    sp = add("attach", cmd_attach, "attach a PDF the user obtained legally")
    sp.add_argument("project")
    sp.add_argument("key")
    sp.add_argument("pdf")
    sp = add("pdf-meta", cmd_pdf_meta, "extract identifiers/metadata from a PDF file")
    sp.add_argument("pdf")
    sp = add("dedup", cmd_dedup, "report duplicate papers in a project")
    sp.add_argument("project")
    sp = add("validate", cmd_validate, "re-verify metadata against Crossref/OpenAlex/arXiv + PDF identity")
    sp.add_argument("project")
    sp.add_argument("keys", nargs="*")
    sp = add("bib", cmd_bib, "build per-paper BibTeX + references.bib")
    sp.add_argument("project")
    sp.add_argument("--offline", action="store_true", help="generate from metadata, skip doi.org")
    sp = add("scaffold", cmd_scaffold, "create analysis.md from the template (never overwrites)")
    sp.add_argument("project")
    sp.add_argument("keys", nargs="*")
    sp = add("cite-check", cmd_cite_check, "verify [@key, p. N] citations in markdown files")
    sp.add_argument("project")
    sp.add_argument("files", nargs="+")
    sp = add("index", cmd_index, "rebuild literature matrix, STATUS stats, registry, INDEX.md")
    sp.add_argument("project", nargs="?")
    sp = add("log", cmd_log, "append an entry to the research log")
    sp.add_argument("project")
    sp.add_argument("phase")
    sp.add_argument("message")
    sp = add("doctor", cmd_doctor, "check dependencies, skills/agents and API reachability")
    sp.add_argument("--offline", action="store_true")
    a = p.parse_args(argv)
    return a.fn(a) or 0


if __name__ == "__main__":
    sys.exit(main())
