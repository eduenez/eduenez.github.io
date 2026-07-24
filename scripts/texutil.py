"""LaTeX-escaping for plain-text fields (cv.yml, talks.yml, teaching.yml).
Bib-sourced fields are NOT run through this -- they're already valid LaTeX.
"""
import re

_SPECIAL = {
    "&": r"\&",
    "%": r"\%",
    "$": r"\$",
    "#": r"\#",
    "_": r"\_",
    "{": r"\{",
    "}": r"\}",
    "~": r"\textasciitilde{}",
    "^": r"\textasciicircum{}",
    "\\": r"\textbackslash{}",
}
_SPECIAL_RE = re.compile("|".join(re.escape(k) for k in _SPECIAL))


def _convert_quotes(text):
    parts = text.split('"')
    if len(parts) == 1:
        return text
    out = parts[0]
    for i, part in enumerate(parts[1:], start=1):
        out += "``" if i % 2 == 1 else "''"
        out += part
    return out


def tex(value):
    """Escape a plain-text value for safe inclusion in LaTeX source."""
    if value is None:
        return ""
    text = _convert_quotes(str(value).strip())
    return _SPECIAL_RE.sub(lambda m: _SPECIAL[m.group()], text)
