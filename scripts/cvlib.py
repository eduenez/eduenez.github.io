"""Shared loading helpers for the Jekyll and LaTeX CV generators."""
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
