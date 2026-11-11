"""Tests for scripts/rlab.py and the protection hook.

Offline:  python3 -m unittest discover -s tests -v
Online (hits OpenAlex/Crossref/arXiv, downloads one arXiv PDF):
          RLAB_ONLINE=1 python3 -m unittest discover -s tests -v
"""
import contextlib
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))
import rlab  # noqa: E402

HAS_POPPLER = bool(shutil.which("pdftotext") and shutil.which("pdfinfo"))


def make_pdf(path, pages):
    """Write a minimal valid PDF with one line of Helvetica text per page."""
    n = len(pages)
    objs = ["<< /Type /Catalog /Pages 2 0 R >>",
            f"<< /Type /Pages /Kids [{' '.join(f'{4 + 2 * i} 0 R' for i in range(n))}] /Count {n} >>",
            "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>"]
    for i, text in enumerate(pages):
        stream = f"BT /F1 12 Tf 72 720 Td ({text}) Tj ET"
        objs.append(f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
                    f"/Resources << /Font << /F1 3 0 R >> >> /Contents {5 + 2 * i} 0 R >>")
        objs.append(f"<< /Length {len(stream)} >>\nstream\n{stream}\nendstream")
    out, offsets = b"%PDF-1.4\n", []
    for i, o in enumerate(objs, 1):
        offsets.append(len(out))
        out += f"{i} 0 obj\n{o}\nendobj\n".encode()
    xref = len(out)
    out += f"xref\n0 {len(objs) + 1}\n0000000000 65535 f \n".encode()
    out += b"".join(f"{off:010d} 00000 n \n".encode() for off in offsets)
    out += f"trailer\n<< /Size {len(objs) + 1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode()
    Path(path).write_bytes(out)


def run(*argv):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        code = rlab.main(list(argv))
    return code, buf.getvalue()


FAKE = {
    "10.1000/alpha": dict(title="Deep Learning for Crop Yield Prediction: A Field Study", year=2021,
                          authors=[{"family": "Smith", "given": "Ann"}, {"family": "Lee", "given": "Bo"}],
                          venue="Journal of Agri Informatics", type="journal-article", venue_kind="published",
                          doi="10.1000/alpha"),
    "10.1000/beta": dict(title="Deep learning for crop-yield prediction - a field study", year=2022,
                         authors=[{"family": "Smith", "given": "Ann"}], venue="Other Journal",
                         type="journal-article", venue_kind="published", doi="10.1000/beta"),
    "10.1000/gamma": dict(title="Satellite Imagery and Soil Moisture Fusion", year=2020,
                          authors=[{"family": "Smith", "given": "Carl"}], venue="Proc. Conference on Remote Sensing",
                          type="proceedings-article", venue_kind="published", doi="10.1000/gamma",
                          is_retracted=True),
}


def fake_resolve(kind, value):
    if kind != "doi" or value not in FAKE:
        raise LookupError(f"not found {value}")
    return rlab.blank_record(**FAKE[value], sources=["crossref", "openalex"]), {"status": "verified", "checked": rlab.now()}


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="rlab-test-"))
        self._saved = (rlab.ROOT, rlab.RESEARCH, rlab.resolve)
        rlab.ROOT, rlab.RESEARCH = self.tmp, self.tmp / "research"
        rlab.resolve = fake_resolve

    def tearDown(self):
        rlab.ROOT, rlab.RESEARCH, rlab.resolve = self._saved
        shutil.rmtree(self.tmp)

    def new_project(self, topic="Crop yield prediction with machine learning"):
        code, out = run("new", topic)
        self.assertEqual(code, 0)
        return out.split()[1]


class TestIdentifiers(unittest.TestCase):
    def test_norm_doi(self):
        for raw in ("10.1038/NATURE14539", "https://doi.org/10.1038/nature14539", "doi: 10.1038/nature14539.",
                    "http://dx.doi.org/10.1038/nature14539"):
            self.assertEqual(rlab.norm_doi(raw), "10.1038/nature14539")
        self.assertIsNone(rlab.norm_doi("not a doi"))

    def test_norm_arxiv(self):
        for raw in ("1706.03762", "arXiv:1706.03762v7", "https://arxiv.org/abs/1706.03762v2",
                    "https://arxiv.org/pdf/1706.03762", "10.48550/arXiv.1706.03762"):
            self.assertEqual(rlab.norm_arxiv(raw), "1706.03762")
        self.assertEqual(rlab.norm_arxiv("hep-th/9901001v1"), "hep-th/9901001")

    def test_detect_id(self):
        self.assertEqual(rlab.detect_id("10.1000/xyz"), ("doi", "10.1000/xyz"))
        self.assertEqual(rlab.detect_id("arXiv:2101.00001"), ("arxiv", "2101.00001"))
        self.assertEqual(rlab.detect_id("10.48550/arXiv.2101.00001"), ("arxiv", "2101.00001"))
        self.assertEqual(rlab.detect_id("pmid:31452104"), ("pmid", "31452104"))
        self.assertEqual(rlab.detect_id("https://openalex.org/W2626778328"), ("openalex", "W2626778328"))
        self.assertEqual(rlab.detect_id("hello")[0], None)

    def test_slug(self):
        self.assertEqual(rlab.slugify("Café & AI: LLMs in Education!"), "cafe-ai-llms-in-education")
        self.assertEqual(rlab.slugify("large language models as intelligent tutors", 30), "large-language-models-as")
        self.assertEqual(rlab.slugify("x" * 60, 10), "x" * 10)


class TestDuplicates(unittest.TestCase):
    def test_same_identifier(self):
        self.assertEqual(rlab.same_work({"doi": "10.1/x"}, {"doi": "10.1/x"}), "doi")
        self.assertEqual(rlab.same_work({"arxiv_id": "1706.03762"}, {"arxiv_id": "1706.03762"}), "arxiv_id")

    def test_fuzzy_title_preprint_vs_published(self):
        a = {"title": "Attention Is All You Need", "year": 2017, "doi": "10.48550/arxiv.1706.03762"}
        b = {"title": "Attention is all you need.", "year": 2017, "doi": "10.5555/3295222.3295349"}
        self.assertTrue(rlab.same_work(a, b).startswith("title"))

    def test_different_papers_not_duplicates(self):
        a = {"title": "Deep learning for crop yield prediction", "year": 2020}
        b = {"title": "Deep learning for crop disease detection", "year": 2020}
        self.assertIsNone(rlab.same_work(a, b))
        c = {"title": "Deep learning for crop yield prediction", "year": 2010}
        self.assertIsNone(rlab.same_work(a, c), "same title 10 years apart is a different work")

    def test_short_titles_ignored(self):
        self.assertIsNone(rlab.same_work({"title": "Introduction"}, {"title": "Introduction"}))

    def test_merge_fills_gaps_only(self):
        p = rlab.blank_record(title="T", doi="10.1/x", sources=["crossref"])
        s = rlab.blank_record(title="Other", oa_pdf_url="https://x/y.pdf", is_retracted=True, sources=["openalex"])
        m = rlab.merge(p, s)
        self.assertEqual((m["title"], m["oa_pdf_url"], m["is_retracted"]), ("T", "https://x/y.pdf", True))
        self.assertEqual(m["sources"], ["crossref", "openalex"])


class TestParsers(unittest.TestCase):
    def test_openalex_record(self):
        w = {"id": "https://openalex.org/W1", "doi": "https://doi.org/10.1/ABC", "title": "A <i>Title</i>",
             "publication_year": 2020, "type": "article", "cited_by_count": 5, "is_retracted": False,
             "authorships": [{"author": {"display_name": "Jane van Doe"}}],
             "primary_location": {"landing_page_url": "https://pub/x", "source": {"display_name": "J", "type": "journal"}},
             "best_oa_location": {"pdf_url": "https://pub/x.pdf"}, "open_access": {"is_oa": True},
             "locations": [{"landing_page_url": "http://arxiv.org/abs/2001.00001v2"}],
             "abstract_inverted_index": {"world": [1], "hello": [0]}, "ids": {"pmid": "https://pubmed/123"}}
        r = rlab.from_openalex(w)
        self.assertEqual((r["doi"], r["title"], r["venue_kind"], r["arxiv_id"], r["abstract"], r["pmid"]),
                         ("10.1/abc", "A Title", "published", "2001.00001", "hello world", "123"))

    def test_names_and_entities(self):
        self.assertEqual(rlab.split_name("Chen, Yang"), {"family": "Chen", "given": "Yang"})
        self.assertEqual(rlab.split_name("Jane van Doe"), {"family": "Doe", "given": "Jane van"})
        self.assertEqual(rlab.strip_tags("Maintainable &amp; <i>Reliable</i>"), "Maintainable & Reliable")

    def test_crossref_record_retraction(self):
        m = {"DOI": "10.1/X", "title": ["T"], "type": "journal-article", "issued": {"date-parts": [[2019, 1]]},
             "author": [{"family": "Doe", "given": "J"}], "updated-by": [{"type": "retraction"}]}
        r = rlab.from_crossref(m)
        self.assertEqual((r["year"], r["is_retracted"], r["venue_kind"]), (2019, True, "published"))

    def test_frontmatter(self):
        with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as f:
            f.write("---\nkey: k\nstatus: ready\nmain_finding: \"X improves Y: by 5%\"\n---\n# body\nstatus: no\n")
        fm = rlab.frontmatter(f.name)
        os.unlink(f.name)
        self.assertEqual(fm, {"key": "k", "status": "ready", "main_finding": "X improves Y: by 5%"})

    def test_bibtex(self):
        m = dict(FAKE["10.1000/gamma"], key="smith2020satellite")
        bib = rlab.to_bibtex(m)
        self.assertTrue(bib.startswith("@inproceedings{smith2020satellite,"))
        self.assertIn("author = {Smith, Carl}", bib)
        m2 = dict(title="R&D at 50% scale", authors=[], year=2020, type="journal-article",
                  venue_kind="published", venue="J", key="k")
        self.assertIn(r"R\&D at 50\% scale", rlab.to_bibtex(m2))

    def test_blocked_hosts(self):
        with self.assertRaises(PermissionError):
            rlab.http_get("https://sci-hub.se/10.1/x")
        with self.assertRaises(PermissionError):
            rlab.http_get("https://libgen.is/book")


class TestWorkflow(Base):
    def test_new_project_unique_ids_and_registry(self):
        a = self.new_project()
        b = self.new_project()
        self.assertNotEqual(a, b)
        self.assertTrue(b.endswith("-2"))
        d = rlab.RESEARCH / a
        for f in ("RESEARCH.md", "STATUS.md", "RESEARCH-QUESTIONS.md", "research-log.md", "evidence-matrix.md",
                  "gap-report.md", "literature-matrix.md", "literature-matrix.csv", "search/search-log.md",
                  "search/screening.md"):
            self.assertTrue((d / f).exists(), f)
        self.assertIn("Crop yield prediction", (d / "RESEARCH.md").read_text())
        self.assertNotIn("{{", (d / "STATUS.md").read_text())
        reg = json.loads((rlab.RESEARCH / "registry.json").read_text())
        self.assertEqual([p["id"] for p in reg["projects"]], [a, b])
        self.assertIn(a, (rlab.RESEARCH / "INDEX.md").read_text())

    def test_add_dedup_and_retraction_warning(self):
        pid = self.new_project()
        code, out = run("add", pid, "10.1000/alpha", "10.1000/gamma", "--reason", "core")
        self.assertIn("ADDED smith2021deep", out)
        self.assertIn("WARNING: RETRACTED", out)
        _, out = run("add", pid, "https://doi.org/10.1000/ALPHA")
        self.assertIn("DUPLICATE", out, "same DOI, different spelling")
        _, out = run("add", pid, "10.1000/beta")
        self.assertIn("DUPLICATE", out, "near-identical title one year apart")
        self.assertIn("title-similarity", out)
        _, out = run("add", pid, "10.1000/beta", "--allow-similar")
        self.assertIn("ADDED smith2022deep", out)
        _, out = run("dedup", pid)
        self.assertIn("1 possible duplicate pair", out)
        _, out = run("add", pid, "10.1000/missing", "nonsense")
        self.assertIn("FAIL 10.1000/missing", out)
        self.assertIn("SKIP nonsense", out)
        log = (rlab.RESEARCH / pid / "research-log.md").read_text()
        self.assertIn("included smith2021deep (10.1000/alpha): core", log)

    def test_key_collisions(self):
        rec = {"authors": [{"family": "Müller"}], "year": 2020, "title": "The Study of Things"}
        self.assertEqual(rlab.make_key(rec, set()), "muller2020study")
        self.assertEqual(rlab.make_key(rec, {"muller2020study"}), "muller2020studya")
        self.assertEqual(rlab.make_key(rec, {"muller2020study", "muller2020studya"}), "muller2020studyb")

    def test_scaffold_index_matrix_status_and_resume(self):
        pid = self.new_project()
        run("add", pid, "10.1000/alpha")
        d = rlab.RESEARCH / pid
        _, out = run("scaffold", pid, "smith2021deep")
        self.assertIn("CREATED", out)
        f = d / "papers/smith2021deep/analysis.md"
        text = f.read_text().replace("status: draft", "status: ready").replace("main_finding: ", "main_finding: CNN beats RF by 12% RMSE")
        f.write_text(text)
        _, out = run("scaffold", pid, "smith2021deep")
        self.assertIn("EXISTS", out, "scaffold must never overwrite")
        self.assertIn("CNN beats RF", f.read_text())
        # tick the first phase and add a next action, then resume
        s = (d / "STATUS.md").read_text().replace("- [ ] Scoping", "- [x] Scoping")
        (d / "STATUS.md").write_text(s.replace("- Write objectives and research questions", "- Run discovery searches"))
        _, out = run("resume", pid[-12:])  # unique fragment of the id
        self.assertIn("phase:   Discovery", out)
        self.assertIn("Run discovery searches", out)
        self.assertIn("smith2021deep: fulltext=not-tried analysis=ready", out)
        self.assertIn("analysis_ready=1", out)
        self.assertIn("CNN beats RF by 12% RMSE", (d / "literature-matrix.md").read_text())
        self.assertIn("- Current phase: **Discovery**", (d / "STATUS.md").read_text())
        reg = json.loads((rlab.RESEARCH / "registry.json").read_text())
        self.assertEqual(reg["projects"][0]["phase"], "Discovery")

    def test_project_lookup_errors(self):
        self.new_project("Topic one")
        self.new_project("Topic two")
        with self.assertRaises(SystemExit):
            rlab.project_dir("topic")  # ambiguous
        with self.assertRaises(SystemExit):
            rlab.project_dir("zzz")

    def test_offline_bib(self):
        pid = self.new_project()
        run("add", pid, "10.1000/alpha", "10.1000/gamma")
        _, out = run("bib", pid, "--offline")
        self.assertIn("2 entries", out)
        bib = (rlab.RESEARCH / pid / "references.bib").read_text()
        self.assertIn("@article{smith2021deep,", bib)
        self.assertIn("@inproceedings{smith2020satellite,", bib)

    def test_cite_check(self):
        pid = self.new_project()
        run("add", pid, "10.1000/alpha", "10.1000/gamma")
        d = rlab.RESEARCH / pid
        meta = json.loads((d / "papers/smith2021deep/metadata.json").read_text())
        meta["fulltext"] = {"status": "downloaded", "pages": 10}
        (d / "papers/smith2021deep/metadata.json").write_text(json.dumps(meta))
        good = d / "reports/good.md"
        good.write_text("Yield improves [@smith2021deep, p. 4]. Mail me@example.com [see @smith2021deep].\n")
        self.assertEqual(run("cite-check", pid, str(good))[0], 0)
        bad = d / "reports/bad.md"
        bad.write_text("X [@smith2021deep, p. 40]; Y [@nobody2020x]; Z [@smith2020satellite].\n")
        code, out = run("cite-check", pid, str(bad))
        self.assertEqual(code, 1)
        for s in ("BAD PAGE", "UNKNOWN KEY", "RETRACTED"):
            self.assertIn(s, out)


@unittest.skipUnless(HAS_POPPLER, "poppler-utils not installed")
class TestPdf(Base):
    def test_pdf_meta_and_text_with_page_markers(self):
        pdf = self.tmp / "sample.pdf"
        make_pdf(pdf, ["Deep Learning for Crop Yield Prediction doi 10.1000/alpha", "Results page two arXiv:2101.00001v2"])
        pm = rlab.pdf_meta(pdf)
        self.assertEqual(pm["pages"], 2)
        self.assertIn("10.1000/alpha", pm["dois"])
        self.assertIn("2101.00001", pm["arxiv_ids"])
        n, _ = rlab.extract_text(pdf, self.tmp / "out.txt")
        txt = (self.tmp / "out.txt").read_text()
        self.assertEqual(n, 2)
        self.assertLess(txt.index("=== [PDF page 1] ==="), txt.index("Crop Yield"))
        self.assertLess(txt.index("=== [PDF page 2] ==="), txt.index("Results page two"))

    def test_stray_form_feed_does_not_create_pages(self):
        pdf = self.tmp / "ff.pdf"
        make_pdf(pdf, ["first page", "second page"])
        real = rlab.pdftotext
        rlab.pdftotext = lambda f, a=None, b=None: ("x\fy\x00" if a else "a\fb\fc\fd\f")  # simulate stray FFs
        try:
            n, _ = rlab.extract_text(pdf, self.tmp / "ff.txt")
        finally:
            rlab.pdftotext = real
        txt = (self.tmp / "ff.txt").read_text()
        self.assertEqual(n, 2)
        self.assertNotIn("\x00", txt)

    def test_attach_identity_and_no_overwrite(self):
        pid = self.new_project()
        run("add", pid, "10.1000/alpha", "10.1000/gamma")
        good, wrong = self.tmp / "good.pdf", self.tmp / "wrong.pdf"
        make_pdf(good, ["Some header doi 10.1000/alpha", "body"])
        make_pdf(wrong, ["A completely unrelated paper about birds", "body"])
        _, out = run("attach", pid, "smith2021deep", str(good))
        self.assertIn("identity: match (DOI printed in PDF)", out)
        with self.assertRaises(SystemExit):
            run("attach", pid, "smith2021deep", str(wrong))
        _, out = run("attach", pid, "smith2020satellite", str(wrong))
        self.assertIn("UNCONFIRMED", out)
        d = rlab.RESEARCH / pid / "papers/smith2021deep"
        self.assertEqual((d / "fulltext.txt").read_text().count("=== [PDF page"), 2)
        meta = json.loads((d / "metadata.json").read_text())
        self.assertEqual((meta["fulltext"]["status"], meta["fulltext"]["pages"]), ("user-supplied", 2))
        _, out = run("status", pid)
        self.assertIn("fulltext=2", out)


class TestHook(unittest.TestCase):
    HOOK = REPO / ".claude/hooks/protect_research.py"

    def call(self, event):
        r = subprocess.run([sys.executable, str(self.HOOK)], input=json.dumps(event), capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        return json.loads(r.stdout)["hookSpecificOutput"]["permissionDecision"] if r.stdout.strip() else None

    def test_rules(self):
        tmp = Path(tempfile.mkdtemp())
        try:
            p = tmp / "research/proj/papers/k"
            p.mkdir(parents=True)
            (p / "analysis.md").write_text("---\nstatus: ready\n---\n")
            self.assertIsNone(self.call({"tool_name": "Edit", "tool_input": {"file_path": str(p / "analysis.md")}}))
            (p / "analysis.md").write_text("---\nstatus: complete\n---\n")
            self.assertEqual(self.call({"tool_name": "Edit", "tool_input": {"file_path": str(p / "analysis.md")}}), "ask")
            (p / "fulltext.txt").write_text("x")
            self.assertEqual(self.call({"tool_name": "Write", "tool_input": {"file_path": str(p / "fulltext.txt")}}), "ask")
            self.assertIsNone(self.call({"tool_name": "Write", "tool_input": {"file_path": str(p / "new.md")}}))
            self.assertEqual(self.call({"tool_name": "Bash", "tool_input": {"command": f"rm -rf {tmp}/research/proj"}}), "ask")
            self.assertIsNone(self.call({"tool_name": "Bash", "tool_input": {"command": "python3 scripts/rlab.py list"}}))
        finally:
            shutil.rmtree(tmp)


@unittest.skipUnless(os.environ.get("RLAB_ONLINE") == "1", "set RLAB_ONLINE=1 for live API tests")
class TestOnline(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="rlab-online-"))
        self._saved = (rlab.ROOT, rlab.RESEARCH)
        rlab.ROOT, rlab.RESEARCH = self.tmp, self.tmp / "research"

    def tearDown(self):
        rlab.ROOT, rlab.RESEARCH = self._saved
        shutil.rmtree(self.tmp)

    def test_end_to_end_sample(self):
        _, out = run("new", "Transformer attention mechanisms")
        pid = out.split()[1]
        _, out = run("search", pid, "attention is all you need transformer", "--sources", "openalex,arxiv", "--limit", "5")
        self.assertIn("unique results", out)
        _, out = run("add", pid, "arXiv:1706.03762", "--reason", "seminal")
        self.assertIn("ADDED vaswani2017attention", out)
        _, out = run("add", pid, "10.48550/arXiv.1706.03762")
        self.assertIn("DUPLICATE", out)
        _, out = run("search", pid, "attention is all you need", "--sources", "openalex,arxiv", "--limit", "10")
        self.assertIn("IN-PROJECT:vaswani2017attention", out)
        _, out = run("fetch", pid)
        self.assertIn("GOT  vaswani2017attention", out)
        self.assertIn("identity: match", out)
        _, out = run("validate", pid)
        self.assertIn("verified", out)
        _, out = run("bib", pid)
        self.assertIn("1 entries", out)
        _, out = run("resume", pid)
        self.assertIn("fulltext=1", out)
        # DOI path: Crossref + OpenAlex cross-check
        rec, ver = rlab.resolve("doi", "10.1038/nature14539")
        self.assertEqual(rec["year"], 2015)
        self.assertEqual(ver["status"], "verified")


if __name__ == "__main__":
    unittest.main()
