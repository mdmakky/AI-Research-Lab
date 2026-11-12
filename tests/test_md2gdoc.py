import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from md2gdoc import PAGE_WIDTH, col_widths, inline, parse, u16  # noqa: E402


class TestMd2Gdoc(unittest.TestCase):
    def test_parse_blocks(self):
        md = ("# Title\n\nline one\nline two\n\n- a\n- b\n1. x\n> **Note:** hi\n> there\n\n"
              "| H1 | H2 |\n|---|---|\n| a | b |\n\n---\n### Sub")
        self.assertEqual(parse(md), [
            ("h", (1, "Title")), ("p", "line one line two"), ("b", "a"), ("b", "b"), ("n", "x"),
            ("callout", "**Note:** hi there"), ("table", [["H1", "H2"], ["a", "b"]]),
            ("pagebreak", None), ("h", (3, "Sub"))])

    def test_inline_spans(self):
        plain, spans = inline("**Bold** [V] fact [@he2026speed, p. 7; @borg2026echoes, p. 2]")
        self.assertEqual(plain, "Bold [V] fact [he2026speed, p. 7; borg2026echoes, p. 2]")
        self.assertIn((0, 4, "bold"), spans)
        self.assertIn((5, 8, "label", "V"), spans)
        cite = [s for s in spans if s[2] == "cite"][0]
        self.assertEqual(plain[cite[0]:cite[1]], "[he2026speed, p. 7; borg2026echoes, p. 2]")

    def test_col_widths(self):
        rows = [["RQ", "Claim", "Label"], ["RQ1", "a long claim text " * 5, "[V]"]]
        w = col_widths(rows)
        self.assertAlmostEqual(sum(w), PAGE_WIDTH, delta=3)
        self.assertEqual(max(w), w[1])
        self.assertGreaterEqual(min(w), 30)
        self.assertEqual(col_widths([["Item", "Detail"]]), [120, PAGE_WIDTH - 120])

    def test_utf16_offsets(self):  # Docs indices are UTF-16 units: emoji = 2
        plain, spans = inline("😀 **x**")
        self.assertEqual(u16("😀 "), 3)
        self.assertEqual(spans, [(3, 4, "bold")])


if __name__ == "__main__":
    unittest.main()
