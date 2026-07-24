"""Build LaTeX-ready publication/preprint citation strings from raw
bibtexparser entries (still LaTeX-escaped -- unlike the HTML path, we pass
bib fields through mostly as-is since they're already valid LaTeX)."""

STATUS_NOTE = {
    "in_prep": "In preparation.",
    "accepted": "Accepted.",
    "submitted": "Submitted.",
}


def format_authors_tex(raw_author_field):
    names = []
    for chunk in raw_author_field.split(" and "):
        chunk = chunk.strip()
        if "," in chunk:
            last, _, first = chunk.partition(",")
            names.append(f"{first.strip()} {last.strip()}")
        else:
            names.append(chunk)
    return ", ".join(names)


def venue_and_style(entry):
    if entry.get("journal"):
        return entry["journal"], "journal"
    if entry.get("series") and entry.get("volume"):
        return entry["series"], "series"
    if entry.get("booktitle"):
        return entry["booktitle"], "booktitle"
    if entry.get("publisher"):
        return entry["publisher"], "publisher"
    return None, None


def build_refereed_citation(entry):
    authors = format_authors_tex(entry.get("author", ""))
    title = entry.get("title", "")
    year = entry.get("year", "")
    venue, style = venue_and_style(entry)

    bits = [f"{authors}.", f"\\emph{{{title}.}}"]
    if venue:
        piece = venue
        if style in ("journal", "series") and entry.get("volume"):
            piece += f" \\textbf{{{entry['volume']}}}"
            if style == "journal" and entry.get("number"):
                piece += f":{entry['number']}"
        elif style == "booktitle" and entry.get("publisher"):
            piece += f", {entry['publisher']}"
        bits.append(piece)

    tail = []
    if year:
        tail.append(f"({year})")
    if entry.get("pages"):
        tail.append(entry["pages"])
    bits.append((" ".join(tail) if tail else "") + ".")
    return " ".join(b for b in bits if b)


def arxiv_href(entry):
    doi = entry.get("doi", "")
    if "arXiv" in doi:
        arxiv_id = doi.split("arXiv.")[-1]
        return f"\\href{{https://doi.org/{doi}}}{{arXiv:{arxiv_id}}}"
    url = entry.get("url", "")
    if "arxiv.org/abs/" in url:
        arxiv_id = url.rsplit("/", 1)[-1]
        return f"\\href{{{url}}}{{arXiv:{arxiv_id}}}"
    return None


def build_preprint_entry(entry, pub):
    authors = format_authors_tex(entry.get("author", ""))
    title = entry.get("title", "")
    note = pub.get("venue_note")
    note_text = f"({note}.)" if note else f"({STATUS_NOTE.get(pub['status'], '')})"
    href = arxiv_href(entry)

    parts = [f"{authors}.", f"\\emph{{{title}}}", note_text]
    if href:
        parts.append(href + ".")
    return " ".join(parts)
