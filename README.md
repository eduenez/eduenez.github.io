# eduenez.github.io

Source for Eduardo Dueñez's personal/professional website, published via
GitHub Pages at the custom domain `supernumero.us`. Built with
[Academic Pages](https://github.com/academicpages/academicpages.github.io)
(MIT licensed, see `LICENSE-academicpages`), a Jekyll theme.

## Data (source of truth)

All under `_data/`:

- `cv.yml` — hand-maintained CV content: bio, education, employment,
  awards & grants, research interests, mentorship, service, memberships.
- `publications_manifest.yml` — which BibTeX keys (from the
  `math-bibliography` submodule) are CV-relevant publications, plus fields
  BibTeX doesn't carry (status, venue notes).
- `talks.yml` — research and outreach talks.
- `teaching.yml` — courses taught, by term.

None of these are edited by hand for publications/talks/teaching. Instead:

- `scripts/generate_collections.py` resolves them into `_publications/`,
  `_talks/`, `_teaching/` — one Jekyll collection file per entry, for the
  website.
- `scripts/generate_latex.py` resolves the same data into `cv-latex/full-cv.tex`
  and `cv-latex/resume.tex` (via Jinja2 templates), then compiles both to
  PDF with `latexmk`. The `.tex` sources are meant to be human-readable
  (the LaTeX source, not just the PDF, is a first-class output). Compiled
  PDFs are copied to `files/cv.pdf` (concise 2-column resume) and
  `files/cv-full.pdf` (full academic vita, includes talks/teaching/theses),
  linked from the CV page.

All of these generated files (`_publications/`, `_talks/`, `_teaching/`,
`cv-latex/*.tex`, `cv-latex/*.pdf`, `files/*.pdf`) ARE committed — GitHub
Pages' classic Jekyll build doesn't run submodules or custom scripts, so
generation has to happen locally/beforehand, not at deploy time.

## Updating the site

After editing anything under `_data/`, or after `math-bibliography` gets a
new entry relevant to this CV:

```bash
git submodule update --remote math-bibliography  # pull in new bib entries
source .venv/bin/activate                        # see scripts/requirements.txt
python3 scripts/generate_collections.py
python3 scripts/generate_latex.py                # add --no-compile to skip latexmk
cp cv-latex/resume.pdf files/cv.pdf
cp cv-latex/full-cv.pdf files/cv-full.pdf
git add -A && git commit -m "Update generated collections and CV PDFs"
git push
```

GitHub Pages rebuilds automatically on push (classic branch-based Jekyll
build, no custom Actions needed).

## LaTeX toolchain

Requires a TeX Live install with `latexmk`, `pdflatex`, and the `roboto`,
`lato`, and `fontawesome5` packages (all standard in a full TeX Live
install). `cv-latex/altacv.cls` is vendored directly in this repo (MIT-ish
LPPL license, see `cv-latex/LICENSE-altacv.md`) rather than depended on via
CTAN, so no separate install step is needed for the class itself.

## Status

Live at `eduenez.github.io` / `supernumero.us`. CV page, publications,
talks, teaching, and the LaTeX/PDF CV (concise + full vita) are all
data-driven from `_data/*.yml`.
