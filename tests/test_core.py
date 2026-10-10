import unittest

from base16_hex_pair import encode, decode, DecodeError


class TestEncode(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(encode(b""), "")

    def test_single_byte(self):
        self.assertEqual(encode(b"\x00"), "00")
        self.assertEqual(encode(b"\xff"), "ff")
        self.assertEqual(encode(b"\x0a"), "0a")

    def test_multiple_bytes(self):
        self.assertEqual(encode(b"\x00\x01\x02"), "000102")
        self.assertEqual(encode(b"Hello"), "48656c6c6f")

    def test_lowercase_output(self):
        result = encode(b"\xab\xcd\xef")
        self.assertEqual(result, "abcdef")
        self.assertEqual(result.lower(), result)

    def test_bytearray_input(self):
        self.assertEqual(encode(bytearray(b"\x00\xff")), "00ff")

    def test_rejects_non_bytes(self):
        with self.assertRaises(TypeError):
            encode("not bytes")
        with self.assertRaises(TypeError):
            encode(42)


class TestDecode(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(decode(""), b"")

    def test_single_pair(self):
        self.assertEqual(decode("00"), b"\x00")
        self.assertEqual(decode("ff"), b"\xff")

    def test_multiple_pairs(self):
        self.assertEqual(decode("000102"), b"\x00\x01\x02")
        self.assertEqual(decode("48656c6c6f"), b"Hello")

    def test_uppercase_accepted(self):
        self.assertEqual(decode("FF"), b"\xff")
        self.assertEqual(decode("AABBCC"), b"\xaa\xbb\xcc")

    def test_mixed_case_accepted(self):
        self.assertEqual(decode("AbCdEf"), b"\xab\xcd\xef")

    def test_ignores_spaces(self):
        self.assertEqual(decode("00 ff"), b"\x00\xff")
        self.assertEqual(decode("  00  ff  "), b"\x00\xff")

    def test_ignores_tabs(self):
        self.assertEqual(decode("00\tff"), b"\x00\xff")

    def test_ignores_newlines(self):
        self.assertEqual(decode("00\nff"), b"\x00\xff")
        self.assertEqual(decode("00\r\nff"), b"\x00\xff")

    def test_ignores_all_whitespace_types(self):
        self.assertEqual(decode("00 \t\n\r\f\vff"), b"\x00\xff")

    def test_odd_length_raises(self):
        with self.assertRaises(DecodeError):
            decode("0")
        with self.assertRaises(DecodeError):
            decode("abc")
        with self.assertRaises(DecodeError):
            decode("00f")

    def test_odd_length_after_whitespace_raises(self):
        with self.assertRaises(DecodeError):
            decode("00 f")

    def test_invalid_char_raises(self):
        with self.assertRaises(DecodeError):
            decode("gg")
        with self.assertRaises(DecodeError):
            decode("00gg")
        with self.assertRaises(DecodeError):
            decode("0g")

    def test_invalid_char_message_contains_value(self):
        try:
            decode("zz")
        except DecodeError as exc:
            self.assertIn("z", str(exc))
        else:
            self.fail("expected DecodeError")

    def test_rejects_non_string(self):
        with self.assertRaises(TypeError):
            decode(b"00ff")
        with self.assertRaises(TypeError):
            decode(42)

    def test_decode_error_is_value_error(self):
        try:
            decode("gg")
        except ValueError:
            pass
        else:
            self.fail("DecodeError should be a ValueError")


class TestRoundTrip(unittest.TestCase):
    def test_round_trip(self):
        for data in [b"", b"\x00", b"\xff", b"Hello, World!", bytes(range(256))]:
            self.assertEqual(decode(encode(data)), data)

    def test_round_trip_with_whitespace(self):
        original = b"\x00\x01\x02\xff"
        encoded = encode(original)
        spaced = " ".join(encoded[i:i + 2] for i in range(0, len(encoded), 2))
        self.assertEqual(decode(spaced), original)


if __name__ == "__main__":
    unittest.main()
