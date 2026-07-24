#!/usr/bin/env python3
"""Regenerate _publications/, _talks/, _teaching/ from _data/*.yml and the
math-bibliography submodule. Safe to re-run: only removes files it
previously generated (marked with `generated: true` in front matter)
before writing fresh ones.
"""
import re
from pathlib import Path

import bibtexparser
import yaml
from bibtexparser.bparser import BibTexParser
from pylatexenc.latex2text import LatexNodes2Text

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "_data"
BIB_FILE = ROOT / "math-bibliography" / "references.bib"

L2T = LatexNodes2Text()

STATUS_TO_CATEGORY = {
    "refereed": "refereed",
    "accepted": "preprints",
    "submitted": "preprints",
    "in_prep": "preprints",
}

MONTHS = {
    m.lower(): i
    for i, m in enumerate(
        [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December",
        ],
        start=1,
    )
}
MONTHS.update({
    "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
    "jul": 7, "aug": 8, "sep": 9, "sept": 9, "oct": 10, "nov": 11, "dec": 12,
})

SEASON_MONTH = {"spring": 1, "summer": 6, "fall": 8}


def clean(text):
    if text is None:
        return ""
    text = L2T.latex_to_text(text).strip()
    text = text.replace("--", "–").replace("~", " ")
    return re.sub(r" {2,}", " ", text)


def slugify(s, maxlen=60):
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return re.sub(r"-+", "-", s).strip("-")[:maxlen].rstrip("-")


def load_yaml(name):
    with open(DATA / name, encoding="utf-8") as f:
        return yaml.safe_load(f)


def clear_generated(directory):
    directory.mkdir(exist_ok=True)
    for f in directory.glob("*.md"):
        if "generated: true" in f.read_text(encoding="utf-8"):
            f.unlink()


def yaml_str(value):
    return yaml.safe_dump(value, allow_unicode=True).strip()


def format_authors(raw_author_field, name_variants):
    authors_html = []
    for chunk in raw_author_field.split(" and "):
        chunk = clean(chunk).strip()
        if "," in chunk:
            last, _, first = chunk.partition(",")
            name = f"{first.strip()} {last.strip()}"
        else:
            name = chunk
        is_self = any(v.lower() in name.lower() for v in name_variants)
        authors_html.append(f"<strong>{name}</strong>" if is_self else name)
    return ", ".join(authors_html)


def guess_venue(entry):
    for key in ("journal", "booktitle", "publisher"):
        if entry.get(key):
            return clean(entry[key])
    return ""


def build_citation(entry, name_variants):
    authors = format_authors(entry.get("author", ""), name_variants)
    title = clean(entry.get("title", ""))
    venue = guess_venue(entry)
    year = entry.get("year", "")
    bits = [f"{authors}.", f"&quot;{title}.&quot;"]
    if venue:
        bits.append(f"<i>{venue}</i>.")
    vol_bits = []
    if entry.get("volume"):
        vol_bits.append(str(entry["volume"]))
    if entry.get("number"):
        vol_bits.append(f"({entry['number']})")
    if vol_bits:
        bits.append(" ".join(vol_bits) + ("." if not entry.get("pages") else ","))
    if entry.get("pages"):
        bits.append(f"{clean(entry['pages'])}.")
    if year:
        bits.append(f"({year}).")
    return " ".join(bits)


def paper_url(entry):
    for key in ("url", "doi"):
        if entry.get(key):
            v = entry[key]
            if key == "doi" and not v.startswith("http"):
                v = f"https://doi.org/{v}"
            return v
    return ""


def generate_publications(name_variants):
    parser = BibTexParser(common_strings=True)
    with open(BIB_FILE, encoding="utf-8") as f:
        bibdb = bibtexparser.load(f, parser=parser)
    entries_by_key = {e["ID"]: e for e in bibdb.entries}

    manifest = load_yaml("publications_manifest.yml")["publications"]
    out_dir = ROOT / "_publications"
    clear_generated(out_dir)

    missing = []
    for pub in manifest:
        key = pub["bibtex_key"]
        entry = entries_by_key.get(key)
        if entry is None:
            missing.append(key)
            continue
        status = pub["status"]
        category = STATUS_TO_CATEGORY[status]
        title = clean(entry.get("title", ""))
        year = int(entry.get("year", 0)) or 1900
        venue = guess_venue(entry)
        if pub.get("venue_note"):
            venue = f"{venue} ({pub['venue_note']})" if venue else pub["venue_note"]
        citation = build_citation(entry, name_variants)
        slug = slugify(key)
        front_matter = {
            "title": title,
            "collection": "publications",
            "category": category,
            "permalink": f"/publication/{slug}",
            "date": f"{year}-01-01",
            "venue": venue,
            "citation": citation,
            "generated": True,
        }
        url = paper_url(entry)
        if url:
            front_matter["paperurl"] = url
        text = "---\n" + yaml_str(front_matter) + "\n---\n"
        (out_dir / f"{slug}.md").write_text(text, encoding="utf-8")

    print(f"publications: wrote {len(manifest) - len(missing)}, missing bib keys: {missing}")


def guess_talk_month(venue_text):
    lower = venue_text.lower()
    for name, num in MONTHS.items():
        if re.search(rf"\b{name}\b", lower):
            return num
    return 1


def generate_talks():
    talks = load_yaml("talks.yml")
    out_dir = ROOT / "_talks"
    clear_generated(out_dir)

    all_talks = talks["research_talks"] + talks["outreach_talks"]
    for t in all_talks:
        month = guess_talk_month(t["venue"] or "")
        talk_type = "Research Talk" if t["kind"] == "research" else "Outreach Talk / Short Course"
        front_matter = {
            "title": t["title"],
            "collection": "talks",
            "type": talk_type,
            "permalink": f"/talks/{t['id']}",
            "venue": t["venue"],
            "date": f"{t['year']}-{month:02d}-01",
            "generated": True,
        }
        text = "---\n" + yaml_str(front_matter) + "\n---\n"
        (out_dir / f"{t['id']}.md").write_text(text, encoding="utf-8")

    print(f"talks: wrote {len(all_talks)}")


def generate_teaching():
    teaching = load_yaml("teaching.yml")
    out_dir = ROOT / "_teaching"
    clear_generated(out_dir)

    for c in teaching["courses"]:
        month = SEASON_MONTH.get(c["season"].lower(), 1)
        course_type = "Cross-listed / graduate course" if c["cross_listed"] else "Course"
        front_matter = {
            "title": c["course"],
            "collection": "teaching",
            "type": course_type,
            "permalink": f"/teaching/{c['id']}",
            "venue": "The University of Texas at San Antonio",
            "date": f"{c['year']}-{month:02d}-01",
            "generated": True,
        }
        text = "---\n" + yaml_str(front_matter) + "\n---\n"
        (out_dir / f"{c['id']}.md").write_text(text, encoding="utf-8")

    print(f"teaching: wrote {len(teaching['courses'])}")


def main():
    cv = load_yaml("cv.yml")
    name_variants = cv["bio"]["name_variants"]
    generate_publications(name_variants)
    generate_talks()
    generate_teaching()


if __name__ == "__main__":
    main()
