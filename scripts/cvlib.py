"""Shared loading helpers for the Jekyll and LaTeX CV generators."""
import re
from pathlib import Path

import bibtexparser
import yaml
from bibtexparser.bparser import BibTexParser

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "_data"
BIB_FILE = ROOT / "math-bibliography" / "references.bib"


def load_yaml(name):
    with open(DATA / name, encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_bib_entries():
    """Return {bibtex_key: raw bibtexparser entry dict}, fields left
    LaTeX-escaped (no unicode conversion) -- callers clean/escape as needed
    for their own output format."""
    parser = BibTexParser(common_strings=True)
    with open(BIB_FILE, encoding="utf-8") as f:
        bibdb = bibtexparser.load(f, parser=parser)
    return {e["ID"]: e for e in bibdb.entries}


ARXIV_ID = re.compile(r"arXiv[:.]\s*(\d{4}\.\d{4,5}(?:v\d+)?|[a-z-]+(?:\.[A-Z]{2})?/\d{7})", re.I)


def arxiv_id(entry):
    """The entry's arXiv identifier, or None. Looked for, in order: eprint with
    archiveprefix arXiv, a 10.48550/arXiv.* DOI, an arxiv.org/abs/ URL, and an
    "arXiv:NNNN.NNNNN" mention in the note."""
    if entry.get("eprint") and entry.get("archiveprefix", "").lower() == "arxiv":
        return entry["eprint"].strip()
    doi = entry.get("doi", "")
    if "arxiv." in doi.lower():
        return doi.split("arXiv.")[-1].split("arxiv.")[-1]
    url = entry.get("url", "")
    if "arxiv.org/abs/" in url:
        return url.split("arxiv.org/abs/")[-1].strip("/")
    m = ARXIV_ID.search(entry.get("note", ""))
    return m.group(1) if m else None
