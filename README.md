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

None of these are edited by hand for publications/talks/teaching. Instead,
`scripts/generate_collections.py` resolves them (bibtex keys against
`math-bibliography/references.bib`, talks/teaching directly) into
`_publications/`, `_talks/`, `_teaching/` -- one Jekyll collection file per
entry. Those generated files ARE committed (GitHub Pages' classic Jekyll
build doesn't run submodules or custom scripts, so the generator has to be
run locally/beforehand, not at deploy time).

## Updating the site

After editing anything under `_data/`, or after `math-bibliography` gets a
new entry relevant to this CV:

```bash
git submodule update --remote math-bibliography  # pull in new bib entries
source .venv/bin/activate                        # see scripts/requirements.txt
python3 scripts/generate_collections.py
git add -A && git commit -m "Update generated collections"
git push
```

GitHub Pages rebuilds automatically on push (classic branch-based Jekyll
build, no custom Actions needed).

## Status

Live at `eduenez.github.io` / `supernumero.us` (pending DNS). CV page,
publications, talks, and teaching are all data-driven. LaTeX/PDF CV
generation is not yet wired up.
