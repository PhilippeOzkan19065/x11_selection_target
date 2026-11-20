"""Conversion between X11 selection target atom names and MIME types.

X11 clipboard and primary-selection protocols identify the offered data
with an atom name such as ``UTF8_STRING`` or ``STRING``.  Modern consumers
of those selections (drag-and-drop, GTK, browsers) speak MIME types such
as ``text/plain;charset=utf-8``.  The two vocabularies overlap but are not
identical, so a fixed translation table is preferable to guessing: an
unknown atom is not silently coerced into ``text/plain``.
"""

from __future__ import annotations

# The canonical atom names are case-sensitive in X11.  We accept the
# upper-case form only, because that is what ICCCM and the common toolkits
# actually put on the wire.  Lower-casing the input would make the function
# tolerant of typos but would also collapse ``TEXT`` and ``text``, which is
# a different question than the one this library answers.

_ATOM_TO_MIME = {
    "UTF8_STRING": "text/plain;charset=utf-8",
    "COMPOUND_TEXT": "text/plain;charset=compound-text",
    "TEXT": "text/plain;charset=iso-8859-1",
    "STRING": "text/plain;charset=iso-8859-1",
}

# MIME types are case-insensitive for the type and subtype, but parameters
# such as ``charset`` are conventionally lower-case.  We normalise the
# whole input to lower-case before lookup so that ``TEXT/PLAIN;CHARSET=UTF-8``
# is accepted.  The reverse mapping is deliberately lossy: several atoms
# map to the same MIME type (``TEXT`` and ``STRING``), and ``from_mime``
# returns the preferred atom for that MIME type, not the original one.
_MIME_TO_ATOM = {
    "text/plain;charset=utf-8": "UTF8_STRING",
    "text/plain;charset=compound-text": "COMPOUND_TEXT",
    "text/plain;charset=iso-8859-1": "STRING",
    "text/plain": "STRING",
}


def to_mime(atom: str) -> str:
    """Return the MIME type corresponding to an X11 target atom name.

    ``atom`` is matched exactly, because atom names are case-sensitive on
    the wire.  An unknown atom raises :class:`ValueError` rather than
    falling back to a text type; a caller that receives an atom it does
    not understand should be told, not handed a plausible-looking string.

    >>> to_mime("UTF8_STRING")
    'text/plain;charset=utf-8'
    >>> to_mime("STRING")
    'text/plain;charset=iso-8859-1'
    """
    if not isinstance(atom, str):
        raise TypeError("atom must be a str")
    try:
        return _ATOM_TO_MIME[atom]
    except KeyError:
        raise ValueError(f"unknown X11 selection target atom: {atom!r}") from None


def from_mime(mime: str) -> str:
    """Return the preferred X11 target atom name for a MIME type.

    The lookup is case-insensitive and ignores surrounding whitespace,
    because MIME headers are commonly written with varying case and
    padding.  Parameters other than the ones in the table are not
    interpreted: ``text/plain;charset=utf-8;format=flowed`` is unknown,
    not silently reduced to ``text/plain;charset=utf-8``.

    >>> from_mime("text/plain;charset=utf-8")
    'UTF8_STRING'
    >>> from_mime("TEXT/PLAIN;CHARSET=UTF-8")
    'UTF8_STRING'
    """
    if not isinstance(mime, str):
        raise TypeError("mime must be a str")
    key = mime.strip().lower()
    try:
        return _MIME_TO_ATOM[key]
    except KeyError:
        raise ValueError(f"unknown MIME type: {mime!r}") from None
