import unittest

from x11_selection_target import from_mime, to_mime


class ToMimeTests(unittest.TestCase):
    def test_utf8_string(self):
        self.assertEqual(to_mime("UTF8_STRING"), "text/plain;charset=utf-8")

    def test_compound_text(self):
        self.assertEqual(
            to_mime("COMPOUND_TEXT"), "text/plain;charset=compound-text"
        )

    def test_text_and_string_share_mime(self):
        # Both legacy atoms describe Latin-1 text; the MIME type is the same.
        self.assertEqual(to_mime("TEXT"), "text/plain;charset=iso-8859-1")
        self.assertEqual(to_mime("STRING"), "text/plain;charset=iso-8859-1")

    def test_unknown_atom_raises(self):
        with self.assertRaises(ValueError):
            to_mime("TARGETS")

    def test_atom_lookup_is_case_sensitive(self):
        # Atom names are case-sensitive on the wire; lower-case is unknown.
        with self.assertRaises(ValueError):
            to_mime("utf8_string")

    def test_non_string_atom_raises_type_error(self):
        with self.assertRaises(TypeError):
            to_mime(None)


class FromMimeTests(unittest.TestCase):
    def test_utf8_round_trip(self):
        self.assertEqual(from_mime("text/plain;charset=utf-8"), "UTF8_STRING")

    def test_case_insensitive_lookup(self):
        self.assertEqual(from_mime("TEXT/PLAIN;CHARSET=UTF-8"), "UTF8_STRING")

    def test_surrounding_whitespace_is_ignored(self):
        self.assertEqual(from_mime("  text/plain;charset=utf-8  "), "UTF8_STRING")

    def test_plain_text_prefers_string(self):
        # TEXT and STRING both map to Latin-1; STRING is the safer default.
        self.assertEqual(from_mime("text/plain"), "STRING")

    def test_unknown_mime_raises(self):
        with self.assertRaises(ValueError):
            from_mime("application/json")

    def test_extra_parameters_are_not_stripped(self):
        # We do not interpret parameters we do not know about.
        with self.assertRaises(ValueError):
            from_mime("text/plain;charset=utf-8;format=flowed")

    def test_non_string_mime_raises_type_error(self):
        with self.assertRaises(TypeError):
            from_mime(42)


if __name__ == "__main__":
    unittest.main()
