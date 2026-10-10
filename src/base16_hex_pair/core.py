"""Base16 hex pair encoder and decoder.

Encodes bytes to a lowercase hexadecimal string and decodes hex pairs back to
bytes, ignoring whitespace and validating character ranges.
"""


class DecodeError(ValueError):
    """Raised when input to decode() is not valid base16.

    Subclassing ValueError keeps it catchable by callers who already handle
    ValueError, while still allowing targeted handling of decode failures.
    """


_HEX_DIGITS = "0123456789abcdef"


def encode(data: bytes) -> str:
    """Encode bytes to a lowercase hexadecimal string.

    Each byte becomes exactly two hex characters, so the output length is
    always even and twice the input length. Returns an empty string for empty
    input.
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError(
            "encode() expects bytes or bytearray, got %s" % type(data).__name__
        )
    return data.hex()


def decode(text: str) -> bytes:
    """Decode a hexadecimal string to bytes.

    Whitespace characters (space, tab, newline, carriage return, form feed,
    vertical tab) are ignored, so hex strings with separators like "0a 1b" or
    multi-line input are accepted. After stripping whitespace, the remaining
    characters must all be valid hex digits (0-9, a-f, A-F) and the total
    count must be even — each byte is a pair.

    Raises DecodeError on invalid characters or an odd length. Raises
    TypeError if text is not a str.
    """
    if not isinstance(text, str):
        raise TypeError(
            "decode() expects str, got %s" % type(text).__name__
        )

    cleaned = []
    for ch in text:
        if ch not in " \t\n\r\f\v":
            cleaned.append(ch)
    cleaned_str = "".join(cleaned)

    if len(cleaned_str) % 2 != 0:
        raise DecodeError(
            "Odd number of hex digits after stripping whitespace: %d" % len(cleaned_str)
        )

    for ch in cleaned_str:
        if ch.lower() not in _HEX_DIGITS:
            raise DecodeError("Invalid hex character: %r" % ch)

    return bytes.fromhex(cleaned_str)
