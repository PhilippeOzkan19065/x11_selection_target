# x11_selection_target

Translate between X11 selection target atom names (`UTF8_STRING`,
`COMPOUND_TEXT`, `TEXT`, `STRING`) and their MIME type equivalents.

```python
from x11_selection_target import to_mime, from_mime

to_mime("UTF8_STRING")
# 'text/plain;charset=utf-8'

from_mime("text/plain;charset=utf-8")
# 'UTF8_STRING'
```

## Why this exists

X11 selections name their payload with an atom such as `UTF8_STRING`, while
the rest of the world (GTK, browsers, drag-and-drop) describes the same
payload as `text/plain;charset=utf-8`.  A converter between the two is a
few lines, but the edges are where bugs live: atom names are case-sensitive
on the wire, MIME types are not, and several atoms (`TEXT` and `STRING`)
collapse onto the same MIME type.  This library fixes one interpretation of
that mapping and documents it.

The trade-off is that the table is closed.  An atom or MIME type outside it
raises `ValueError` instead of being coerced to a plausible text type.  A
caller that receives an unknown atom should decide what to do, not be handed
`text/plain` by a library that guessed.

## The awkward edge

The reverse mapping is lossy.  `TEXT` and `STRING` both map to
`text/plain;charset=iso-8859-1`, and `from_mime` returns `STRING` for that
MIME type.  If you need to preserve which atom was originally seen, you must
keep that information separately; `from_mime` cannot recover it.

## API

- `to_mime(atom: str) -> str` — exact, case-sensitive atom lookup.
- `from_mime(mime: str) -> str` — case-insensitive MIME lookup, ignoring
  surrounding whitespace but not extra parameters.
