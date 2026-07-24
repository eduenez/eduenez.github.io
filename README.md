# eduenez.github.io

Source for Eduardo Dueñez's personal/professional website, published via
GitHub Pages at the custom domain `supernumero.us`.

## Data (source of truth)

- `cv.yml` — hand-maintained CV content: bio, education, employment,
  awards & grants, research interests, mentorship, service, memberships.
- `publications_manifest.yml` — which BibTeX keys (from the
  `math-bibliography` submodule, added once the Jekyll scaffold lands) are
  CV-relevant publications, plus fields BibTeX doesn't carry (status,
  venue notes).
- `talks.yml` — research and outreach talks.
- `teaching.yml` — courses taught, by term.

None of these are edited by hand for publications/talks/teaching once the
BibTeX submodule and generator script are in place — see the header
comment in each file for its canonical/derived status.

## Status

Data layer only so far. Jekyll (Academic Pages theme), the LaTeX/PDF build,
and CI are not yet wired up.
