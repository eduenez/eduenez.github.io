#!/usr/bin/env python3
"""Export the CV publications (_data/publications_manifest.yml, resolved against
math-bibliography) as RIS, for import into SciENcv / NCBI My Bibliography.

    .venv/bin/python scripts/export_ris.py [OUT.ris] [--include-in-prep]

Works in preparation (status in_prep) are left out unless asked for. Text is
converted from LaTeX to Unicode (UTF-8 output).
"""
import re
import sys
from pathlib import Path

from pylatexenc.latex2text import LatexNodes2Text

from cvlib import arxiv_id, load_bib_entries, load_yaml

L2T = LatexNodes2Text(math_mode="text")

TYPES = {"article": "JOUR", "incollection": "CHAP", "inproceedings": "CPAPER", "book": "BOOK",
         "unpublished": "UNPB", "misc": "UNPB", "phdthesis": "THES"}
STATUS_NOTE = {"accepted": "Accepted", "submitted": "Submitted", "preprint": "Preprint"}


def text(v):
    v = re.sub(r"\s+", " ", v or "").strip()
    return re.sub(r"\s+", " ", L2T.latex_to_text(v)).strip() if v else ""


def names(field):
    out = []
    for n in re.split(r"\s+and\s+", field or ""):
        n = text(n)
        if not n:
            continue
        if "," not in n:                                    # "First Last" -> "Last, First"
            parts = n.rsplit(" ", 1)
            n = f"{parts[1]}, {parts[0]}" if len(parts) == 2 else n
        out.append(n)
    return out


def record(e, pub):
    typ = TYPES.get(e["ENTRYTYPE"], "GEN")
    doi = (e.get("doi") or "").strip()
    arx = arxiv_id(e)
    lines = [("TY", typ)]
    lines += [("AU", a) for a in names(e.get("author"))]
    lines.append(("TI", text(e.get("title"))))
    if typ == "JOUR":
        lines.append(("T2", text(e.get("fjournal") or e.get("journal"))))
        lines.append(("J2", text(e.get("journal"))))
    elif typ == "CHAP":
        lines.append(("T2", text(e.get("booktitle"))))
        lines += [("A2", a) for a in names(e.get("editor"))]
        if e.get("series"):
            lines.append(("T3", text(e["series"])))
    year = (e.get("year") or "").strip()
    if year and year != "0000":
        lines.append(("PY", year))
    for tag, f in (("VL", "volume"), ("IS", "number"), ("PB", "publisher"), ("SN", "isbn")):
        if e.get(f) and not (tag == "PB" and text(e[f]).lower() == "arxiv"):
            lines.append((tag, text(e[f])))
    pages = re.sub(r"\s*\(.*?\)", "", text(e.get("pages"))).replace("–", "-").replace("--", "-").split("-")   # "115207 (32 pp)" -> 115207
    if pages[0]:
        lines.append(("SP", pages[0].strip()))
        if len(pages) > 1 and pages[-1].strip():
            lines.append(("EP", pages[-1].strip()))
    if doi and not doi.lower().startswith("10.48550/arxiv"):
        lines.append(("DO", doi))
    url = e.get("url") or (f"https://doi.org/{doi}" if doi else "") or (f"https://arxiv.org/abs/{arx}" if arx else "")
    if url:
        lines.append(("UR", url.strip()))
    notes = [STATUS_NOTE.get(pub.get("status"), ""), text(pub.get("venue_note")) if pub.get("venue_note") else "",
             f"arXiv:{arx}" if arx else ""]
    note = "; ".join(n for n in notes if n)
    if note:
        lines.append(("N1", note))
    lines.append(("ER", ""))
    return "\n".join(f"{t}  - {v}" for t, v in lines if v or t == "ER")      # "ER  - " keeps its space (RIS spec)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    out = Path(args[0]) if args else Path("duenez-publications.ris")
    entries = load_bib_entries()
    recs = []
    for pub in load_yaml("publications_manifest.yml")["publications"]:
        if pub.get("status") == "in_prep" and "--include-in-prep" not in sys.argv:
            continue
        recs.append(record(entries[pub["bibtex_key"]], pub))
    out.write_text("\n\n".join(recs) + "\n", encoding="utf-8")
    print(f"{len(recs)} records -> {out}")


if __name__ == "__main__":
    main()
