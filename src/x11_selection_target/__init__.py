"""X11 selection target atom name to MIME type conversion.

This package exposes two pure functions:

* :func:`to_mime` -- map an X11 selection target atom name to a MIME type.
* :func:`from_mime` -- map a MIME type back to the canonical X11 atom name.

The mapping is intentionally a small, closed set.  X11 selections in the
wild use a handful of well-known atom names, and inventing a general atom
parser would produce surprising results for names we have never seen.
"""

from .core import from_mime, to_mime

__all__ = ["to_mime", "from_mime"]
