#!/usr/bin/env python3
"""md2gdoc - turn simple markdown files into a styled Google Doc (OAuth-as-user).

    python3 scripts/md2gdoc.py --title "Reading Guide" --subtitle "Topic" \
        [--share anyone|none] [--pdf out.pdf] [--md combined.md] a.md b.md ...
    python3 scripts/md2gdoc.py --append DOC_ID more.md ...   # add pages to an existing doc

Each input file starts on a new page. Supported markdown (keep it simple):
  # / ## / ###  headings        - item   bullets        1. item  numbered list
  > text        callout box     | a | b |  table (row 1 = header)
  ---           page break      **bold**  inline        blank line = new paragraph
Labels [V] [A] [I] are coloured; citations [@key, p. N] are shown as [key, p. N].

Auth + Drive client come from the google-doc-builder skill (gdoc_auth.get_credentials).
"""
import argparse
import re
import sys
import time
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path.home() / ".claude/skills/google-doc-builder/scripts"))

NAVY = {"red": 0.11, "green": 0.20, "blue": 0.36}
BLUE = {"red": 0.16, "green": 0.38, "blue": 0.66}
TEAL = {"red": 0.05, "green": 0.45, "blue": 0.45}
GREY = {"red": 0.45, "green": 0.47, "blue": 0.50}
WHITE = {"red": 1, "green": 1, "blue": 1}
CALLOUT_BG = {"red": 0.92, "green": 0.95, "blue": 0.99}
ZEBRA = {"red": 0.96, "green": 0.97, "blue": 0.98}
BORDER = {"red": 0.80, "green": 0.83, "blue": 0.87}
LABEL_COLORS = {"V": {"red": 0.10, "green": 0.50, "blue": 0.25},   # verified - green
                "A": {"red": 0.15, "green": 0.35, "blue": 0.75},   # author claim - blue
                "I": {"red": 0.80, "green": 0.45, "blue": 0.05}}   # interpretation - orange
HEADINGS = {1: ("HEADING_1", NAVY), 2: ("HEADING_2", BLUE), 3: ("HEADING_3", TEAL)}


# ---------------------------------------------------------------- parsing

def u16(s):
    """Docs API indices count UTF-16 code units."""
    return len(s.encode("utf-16-le")) // 2


def inline(text):
    """Strip markup -> (plain, spans); span = (start, end, kind[, arg]) in UTF-16 units."""
    text = text.replace("`", "")
    text = re.sub(r"\[@([^\]]+)\]", lambda m: "[" + m.group(1).replace("; @", "; ") + "]", text)
    out, spans, pos = "", [], 0
    for m in re.finditer(r"\*\*(.+?)\*\*", text):
        out += text[pos:m.start()]
        s = u16(out)
        out += m.group(1)
        spans.append((s, u16(out), "bold"))
        pos = m.end()
    out += text[pos:]
    for m in re.finditer(r"\[(V|A|I)\]", out):
        s = u16(out[:m.start()])
        spans.append((s, s + 3, "label", m.group(1)))
    for m in re.finditer(r"\[[a-z][a-z0-9]*\d{4}[a-z0-9]*,[^\]]*\]", out):  # [key2026x, p. N]
        s = u16(out[:m.start()])
        spans.append((s, s + u16(m.group(0)), "cite"))
    return out, spans


PAGE_WIDTH = 468  # pt: US Letter minus 1-inch margins


def col_widths(rows):
    """Column widths (pt) proportional to average text length, so long-text columns get room."""
    n = len(rows[0])
    if n == 2:
        return [120, PAGE_WIDTH - 120]
    cols = [[r[c] for r in rows if r[c]] or [""] for c in range(n)]
    avg = [max(4, sum(map(len, col)) / len(col)) ** 0.8 for col in cols]
    # no column narrower than its longest word (~6.2pt per char at 11pt), capped so one long token can't hog
    mins = [min(64, max(36, 6.2 * max(len(w) for x in col for w in (x.split() or [""])) + 12)) for col in cols]
    if sum(mins) > 0.75 * PAGE_WIDTH:  # many columns: shrink minimums so text columns keep room
        mins = [m * 0.75 * PAGE_WIDTH / sum(mins) for m in mins]
    w = [max(m, PAGE_WIDTH * a / sum(avg)) for a, m in zip(avg, mins)]
    flex = [x - m for x, m in zip(w, mins)]
    over = sum(w) - PAGE_WIDTH
    if over > 0:  # take the excess only from columns above their minimum (sum(flex) >= over here)
        w = [x - over * f / sum(flex) for x, f in zip(w, flex)]
    return [round(x) for x in w]


def parse(md):
    """Markdown -> list of blocks: (kind, payload)."""
    blocks, para = [], []

    def flush():
        if para:
            blocks.append(("p", " ".join(para)))
            para.clear()

    lines = md.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].rstrip()
        s = line.strip()
        m_h = re.match(r"^(#{1,3})\s+(.*)", s)
        if not s:
            flush()
        elif m_h:
            flush()
            blocks.append(("h", (len(m_h.group(1)), m_h.group(2))))
        elif re.fullmatch(r"-{3,}|\*{3,}", s):
            flush()
            blocks.append(("pagebreak", None))
        elif s.startswith("|"):
            flush()
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c):
                    rows.append(cells)
                i += 1
            width = max(len(r) for r in rows)
            blocks.append(("table", [r + [""] * (width - len(r)) for r in rows]))
            continue
        elif s.startswith(">"):
            flush()
            parts = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                parts.append(lines[i].strip().lstrip(">").strip())
                i += 1
            blocks.append(("callout", " ".join(p for p in parts if p)))
            continue
        elif re.match(r"^[-*+]\s+", s):
            flush()
            blocks.append(("b", re.sub(r"^[-*+]\s+", "", s)))
        elif re.match(r"^\d+[.)]\s+", s):
            flush()
            blocks.append(("n", re.sub(r"^\d+[.)]\s+", "", s)))
        else:
            para.append(s)
        i += 1
    flush()
    return blocks


# ---------------------------------------------------------------- rendering

def width_requests(table_start, rows):
    return [{"updateTableColumnProperties": {"tableStartLocation": {"index": table_start},
             "columnIndices": [c], "tableColumnProperties": {
                 "widthType": "FIXED_WIDTH", "width": {"magnitude": w, "unit": "PT"}},
             "fields": "widthType,width"}} for c, w in enumerate(col_widths(rows))]



class Renderer:
    def __init__(self, creds):
        from googleapiclient.discovery import build
        self.docs = build("docs", "v1", credentials=creds)
        self.drive = build("drive", "v3", credentials=creds)
        self.doc_id = None
        self.pending = []  # text paragraphs waiting for one batched insert

    def _exec(self, req):
        from googleapiclient.errors import HttpError
        for attempt in range(8):
            try:
                return req.execute()
            except HttpError as e:  # write quota is ~60/min per user: back off and retry
                if e.resp.status in (429, 500, 503) and attempt < 7:
                    time.sleep(min(60, 2 ** attempt * 2))
                    continue
                raise

    def batch(self, requests):
        if requests:
            self._exec(self.docs.documents().batchUpdate(documentId=self.doc_id,
                                                         body={"requests": requests}))

    def get(self):
        return self._exec(self.docs.documents().get(documentId=self.doc_id))

    def end(self):
        return self.get()["body"]["content"][-1]["endIndex"] - 1

    @staticmethod
    def span_styles(base, spans):
        reqs = []
        for sp in spans:
            rng = {"startIndex": base + sp[0], "endIndex": base + sp[1]}
            if sp[2] == "bold":
                st, f = {"bold": True}, "bold"
            elif sp[2] == "label":
                st = {"bold": True, "foregroundColor": {"color": {"rgbColor": LABEL_COLORS[sp[3]]}}}
                f = "bold,foregroundColor"
            else:  # cite
                st = {"foregroundColor": {"color": {"rgbColor": GREY}},
                      "fontSize": {"magnitude": 9, "unit": "PT"}}
                f = "foregroundColor,fontSize"
            reqs.append({"updateTextStyle": {"range": rng, "textStyle": st, "fields": f}})
        return reqs

    # -- text paragraphs: accumulate, then insert in ONE request
    def para(self, kind, text, named="NORMAL_TEXT", color=None):
        plain, spans = inline(text)
        self.pending.append((kind, plain, spans, named, color))

    def flush(self):
        if not self.pending:
            return
        idx = self.end()
        full = "".join(p[1] + "\n" for p in self.pending)
        reqs = [{"insertText": {"location": {"index": idx}, "text": full}}]
        pos, lists = idx, []
        for kind, plain, spans, named, color in self.pending:
            rng = {"startIndex": pos, "endIndex": pos + u16(plain) + 1}
            reqs.append({"updateParagraphStyle": {"range": rng, "paragraphStyle": {
                "namedStyleType": named, "spaceBelow": {"magnitude": 4, "unit": "PT"}},
                "fields": "namedStyleType,spaceBelow"}})
            if color and plain:
                reqs.append({"updateTextStyle": {"range": {"startIndex": pos, "endIndex": pos + u16(plain)},
                             "textStyle": {"foregroundColor": {"color": {"rgbColor": color}}},
                             "fields": "foregroundColor"}})
            reqs += self.span_styles(pos, spans)
            if kind in ("b", "n"):  # merge consecutive items of the same kind into one list
                if lists and lists[-1][0] == kind and lists[-1][2] == pos:
                    lists[-1][2] = rng["endIndex"]
                else:
                    lists.append([kind, pos, rng["endIndex"]])
            pos = rng["endIndex"]
        for kind, s, e in lists:
            reqs.append({"createParagraphBullets": {"range": {"startIndex": s, "endIndex": e},
                         "bulletPreset": "BULLET_DISC_CIRCLE_SQUARE" if kind == "b"
                         else "NUMBERED_DECIMAL_NESTED"}})
        self.pending = []
        self.batch(reqs)

    def pagebreak(self):
        self.flush()
        self.batch([{"insertPageBreak": {"location": {"index": self.end()}}}])

    # -- tables (and callouts = 1x1 shaded table)
    def _find_table(self, at):
        return next(e for e in self.get()["body"]["content"] if "table" in e and e["startIndex"] >= at)

    def table(self, rows, callout=False):
        self.flush()
        at = self.end()
        self.batch([{"insertTable": {"rows": len(rows), "columns": len(rows[0]),
                                     "location": {"index": at}}}])
        parsed = [[inline(c) for c in r] for r in rows]
        t = self._find_table(at)
        cells = [(cell["content"][0]["startIndex"], parsed[r][c][0])
                 for r, row in enumerate(t["table"]["tableRows"])
                 for c, cell in enumerate(row["tableCells"])]
        self.batch([{"insertText": {"location": {"index": s}, "text": txt}}
                    for s, txt in sorted(cells, key=lambda x: -x[0]) if txt])
        t = self._find_table(at)
        start = t["startIndex"]
        reqs = []

        def cell_style(r, c, style, fields):
            reqs.append({"updateTableCellStyle": {
                "tableRange": {"tableCellLocation": {"tableStartLocation": {"index": start},
                                                     "rowIndex": r, "columnIndex": c},
                               "rowSpan": 1, "columnSpan": 1},
                "tableCellStyle": style, "fields": fields}})

        for r, row in enumerate(t["table"]["tableRows"]):
            for c, cell in enumerate(row["tableCells"]):
                cs = cell["content"][0]["startIndex"]
                plain, spans = parsed[r][c]
                reqs += self.span_styles(cs, spans)
                header = r == 0 and not callout
                if header and plain:
                    reqs.append({"updateTextStyle": {"range": {"startIndex": cs, "endIndex": cs + u16(plain)},
                                 "textStyle": {"bold": True, "foregroundColor": {"color": {"rgbColor": WHITE}}},
                                 "fields": "bold,foregroundColor"}})
                if callout:
                    edge = {"color": {"color": {"rgbColor": CALLOUT_BG}}, "width": {"magnitude": 1, "unit": "PT"},
                            "dashStyle": "SOLID"}
                    cell_style(r, c, {"backgroundColor": {"color": {"rgbColor": CALLOUT_BG}},
                                      "borderLeft": {**edge, "color": {"color": {"rgbColor": BLUE}},
                                                     "width": {"magnitude": 4, "unit": "PT"}},
                                      "borderTop": edge, "borderRight": edge, "borderBottom": edge,
                                      "paddingLeft": {"magnitude": 10, "unit": "PT"},
                                      "paddingTop": {"magnitude": 6, "unit": "PT"},
                                      "paddingBottom": {"magnitude": 6, "unit": "PT"}},
                               "backgroundColor,borderLeft,borderTop,borderRight,borderBottom,"
                               "paddingLeft,paddingTop,paddingBottom")
                else:
                    line = {"color": {"color": {"rgbColor": BORDER}}, "width": {"magnitude": 0.5, "unit": "PT"},
                            "dashStyle": "SOLID"}
                    bg = NAVY if header else ZEBRA if r % 2 == 0 else WHITE
                    cell_style(r, c, {"backgroundColor": {"color": {"rgbColor": bg}}, "borderLeft": line,
                                      "borderTop": line, "borderRight": line, "borderBottom": line,
                                      "paddingTop": {"magnitude": 3, "unit": "PT"},
                                      "paddingBottom": {"magnitude": 3, "unit": "PT"}},
                               "backgroundColor,borderLeft,borderTop,borderRight,borderBottom,paddingTop,paddingBottom")
        if not callout:
            reqs += width_requests(start, [[inline(c)[0] for c in r] for r in rows])
        self.batch(reqs)

    # -- document
    def build(self, title, subtitle, files, append_to=None):
        if append_to:  # add pages to an existing doc instead of creating one
            self.doc_id = append_to
        else:
            f = self._exec(self.drive.files().create(
                body={"name": title, "mimeType": "application/vnd.google-apps.document"}, fields="id"))
            self.doc_id = f["id"]
            self.para("p", title, "TITLE", NAVY)
            if subtitle:
                self.para("p", subtitle, "SUBTITLE", GREY)
            self.para("p", f"Generated {date.today().isoformat()}", "NORMAL_TEXT", GREY)
        for path in files:
            self.pagebreak()
            for kind, val in parse(Path(path).read_text(encoding="utf-8")):
                if kind == "h":
                    named, color = HEADINGS[val[0]]
                    self.para("p", val[1], named, color)
                elif kind in ("p", "b", "n"):
                    self.para(kind, val)
                elif kind == "pagebreak":
                    self.pagebreak()
                elif kind == "callout":
                    self.table([[val]], callout=True)
                elif kind == "table":
                    self.table(val)
            print(f"  rendered {path}", flush=True)
        self.flush()
        return self.doc_id


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="+")
    ap.add_argument("--title", default="Untitled")
    ap.add_argument("--append", metavar="DOC_ID", help="append the files to this existing Google Doc")
    ap.add_argument("--subtitle", default="")
    ap.add_argument("--share", choices=["anyone", "none"], default="none",
                    help="anyone = anyone with the link can view")
    ap.add_argument("--pdf", help="also export the finished doc as PDF to this path (never overwrites)")
    ap.add_argument("--md", help="also save the combined markdown to this path (never overwrites)")
    a = ap.parse_args()
    for out in (a.pdf, a.md):
        if out and Path(out).exists():
            sys.exit(f"{out} exists; refusing to overwrite")
    if a.md:
        Path(a.md).write_text("\n\n---\n\n".join(Path(f).read_text(encoding="utf-8") for f in a.files),
                              encoding="utf-8")
    from gdoc_auth import get_credentials
    r = Renderer(get_credentials())
    doc_id = r.build(a.title, a.subtitle, a.files, a.append)
    if a.share == "anyone":
        r._exec(r.drive.permissions().create(fileId=doc_id, body={"type": "anyone", "role": "reader"}))
    if a.pdf:
        Path(a.pdf).write_bytes(r._exec(r.drive.files().export(fileId=doc_id, mimeType="application/pdf")))
    print(f"https://docs.google.com/document/d/{doc_id}/edit")


if __name__ == "__main__":
    main()
