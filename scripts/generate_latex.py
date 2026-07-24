#!/usr/bin/env python3
"""Render cv-latex/*.tex from _data/*.yml + math-bibliography, then compile
to PDF with latexmk. Two documents share one data-prep pass:
  - full-cv.tex / full-cv.pdf: everything (education..teaching), modeled on
    the author's previously hand-maintained full AltaCV vita.
  - resume.tex / resume.pdf: concise 2-column version (core sections only;
    no talks/teaching/theses).
"""
import subprocess
import sys

from jinja2 import Environment, FileSystemLoader

from cvlib import ROOT, load_bib_entries, load_yaml
from latex_pubs import build_preprint_entry, build_refereed_citation
from texutil import tex

LATEX_DIR = ROOT / "cv-latex"

JINJA_ENV = Environment(
    loader=FileSystemLoader(str(LATEX_DIR)),
    block_start_string=r"\BLOCK{",
    block_end_string="}",
    variable_start_string=r"\VAR{",
    variable_end_string="}",
    comment_start_string=r"\#{",
    comment_end_string="}",
    trim_blocks=True,
    lstrip_blocks=True,
)

SEASON_RANK = {"fall": 3, "summer": 2, "spring": 1}


def format_years(item):
    start = item.get("start_year")
    end = item.get("end_year")
    if start is None:
        return ""
    if end is None:
        return f"{start} -- Present"
    if end == start:
        return str(start)
    return f"{start} -- {end}"


def build_education(cv):
    return [
        {
            "degree": tex(e["degree"]),
            "institution": tex(e["institution"]),
            "years": format_years(e),
            "details": tex(e.get("details", "")),
        }
        for e in cv["education"]
    ]


def build_employment(cv):
    return [
        {
            "role": tex(e["role"]),
            "institution": tex(e["institution"]),
            "years": format_years(e),
            "details": tex(e.get("details", "")),
        }
        for e in cv["employment"]
    ]


def build_awards(cv):
    out = []
    for a in cv["awards_grants"]:
        years = format_years(a)
        title = tex(a["title"]) + (f" ({years})" if years else "")
        out.append({"title_with_years": title, "details": tex(a.get("details", ""))})
    return out


def build_research_interests(cv):
    ri = cv["research_interests"]
    return {
        "summary": tex(ri["summary"]),
        "applications": [tex(a) for a in ri["applications"]],
    }


def synergy_since_text(s):
    start, end = s.get("start_year"), s.get("end_year")
    if start and not end:
        return f"Since {start}."
    if start and end and start == end:
        return f"{start}."
    if start and end:
        return f"{start}--{end}."
    return ""


def build_academic_synergy(cv):
    out = []
    for s in cv["mentorship"]["academic_synergy"]:
        text = tex(s["role"]) + "."
        if s.get("details"):
            text += f" ({tex(s['details'])})"
        out.append({"since": synergy_since_text(s), "role_and_details": text})
    return out


def build_theses(cv, key):
    return [
        {
            "student": tex(t["student"]),
            "institution": tex(t["institution"]),
            "year": t["year"],
            "title": tex(t["title"]),
        }
        for t in cv["mentorship"][key]
    ]


def build_service(cv):
    out = []
    for s in cv["service"]:
        line = tex(s["role"])
        if s.get("institution"):
            line += f", {tex(s['institution'])}"
        years = format_years(s)
        if years:
            line += f" ({years})"
        line += "."
        if s.get("details"):
            line += f" {tex(s['details'])}"
        out.append({"text": line})
    return out


def build_publications(manifest, bib_entries):
    refereed, preprints, missing = [], [], []
    for pub in manifest:
        entry = bib_entries.get(pub["bibtex_key"])
        if entry is None:
            missing.append(pub["bibtex_key"])
            continue
        if pub["status"] == "refereed":
            refereed.append(build_refereed_citation(entry))
        else:
            preprints.append(build_preprint_entry(entry, pub))
    if missing:
        print(f"WARNING: publications missing from bib: {missing}", file=sys.stderr)
    return refereed, preprints


def build_talks(talks):
    research = [
        {"venue": tex(t["venue"]), "title": tex(t["title"])}
        for t in talks["research_talks"]
    ]
    outreach = [
        {"venue": tex(t["venue"]), "title": tex(t["title"])}
        for t in talks["outreach_talks"]
    ]
    return research, outreach


def build_teaching_entries(teaching):
    combined = []
    for c in teaching["courses"]:
        text = tex(c["course"]) + ("*" if c["cross_listed"] else "")
        rank = SEASON_RANK.get(c["season"].lower(), 0)
        combined.append((c["year"], rank, f"{c['season']} {c['year']}", text))
    for leave in teaching["leaves"]:
        text = f"({tex(leave['reason'])})"
        rank = SEASON_RANK.get(leave["season"].lower(), 0)
        combined.append((leave["year"], rank, f"{leave['season']} {leave['year']}", text))
    combined.sort(key=lambda x: (x[0], x[1]), reverse=True)
    return [{"term": term, "text": text} for _, _, term, text in combined]


def build_bio(cv):
    bio = cv["bio"]
    tagline = f"{bio['title']} at {bio['institution']}"
    context = {
        "name": tex(bio["name"]),
        "tagline": tex(tagline),
        "email": tex(bio["email"]),
        "location": tex(bio["location"]),
    }
    if bio.get("researchgate"):
        context["researchgate"] = True
        context["researchgate_display"] = bio["researchgate"].split("://", 1)[-1]
    if bio.get("github"):
        context["github"] = True
        context["github_display"] = bio["github"].rsplit("/", 1)[-1]
    return context


def build_context():
    cv = load_yaml("cv.yml")
    manifest = load_yaml("publications_manifest.yml")["publications"]
    talks = load_yaml("talks.yml")
    teaching = load_yaml("teaching.yml")
    bib_entries = load_bib_entries()

    refereed_publications, preprint_publications = build_publications(manifest, bib_entries)
    research_talks, outreach_talks = build_talks(talks)

    return {
        "bio": build_bio(cv),
        "education": build_education(cv),
        "employment": build_employment(cv),
        "awards_grants": build_awards(cv),
        "research_interests": build_research_interests(cv),
        "refereed_publications": refereed_publications,
        "preprint_publications": preprint_publications,
        "academic_synergy": build_academic_synergy(cv),
        "masters_theses": build_theses(cv, "masters_theses"),
        "undergraduate_theses": build_theses(cv, "undergraduate_theses"),
        "service": build_service(cv),
        "memberships": [tex(m) for m in cv["memberships"]],
        "research_talks": research_talks,
        "outreach_talks": outreach_talks,
        "teaching_entries": build_teaching_entries(teaching),
    }


def render(template_name, out_name, context):
    template = JINJA_ENV.get_template(template_name)
    (LATEX_DIR / out_name).write_text(template.render(**context), encoding="utf-8")
    print(f"wrote {out_name}")


def compile_pdf(tex_name):
    subprocess.run(
        ["latexmk", "-pdf", "-interaction=nonstopmode", "-halt-on-error", tex_name],
        cwd=LATEX_DIR,
        check=True,
    )
    print(f"compiled {tex_name}")


def main():
    context = build_context()
    render("full-cv.tex.jinja", "full-cv.tex", context)
    render("resume.tex.jinja", "resume.tex", context)

    if "--no-compile" not in sys.argv:
        compile_pdf("full-cv.tex")
        compile_pdf("resume.tex")


if __name__ == "__main__":
    main()
