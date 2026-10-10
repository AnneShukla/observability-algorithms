# Base16 Hex Pair

Encodes bytes to a lowercase hexadecimal string and decodes hex pairs back to bytes, ignoring whitespace and validating character ranges.

## Usage

```python
from base16_hex_pair import encode, decode, DecodeError

encoded = encode(b"Hello")  # "48656c6c6f"
decoded = decode("48 65 6c 6c 6f")  # b"Hello"

try:
    decode("xyz")
except DecodeError as exc:
    print(f"invalid input: {exc}")
```

## Why

Working with hex-encoded data often means dealing with strings that have been formatted for human readability — spaces between byte pairs, line breaks in long sequences. This library accepts those directly rather than forcing the caller to pre-clean the input.

The trade-off: decode ignores all ASCII whitespace (space, tab, newline, carriage return, form feed, vertical tab) but does not accept other separators like colons or dashes. If your input uses `:` or `-` as separators, strip them yourself before calling decode.

## Edge cases

- Empty input encodes to `""` and decodes to `b""`.
- After stripping whitespace, an odd number of hex digits raises `DecodeError`.
- Both uppercase and lowercase hex are accepted on decode; encode always produces lowercase.
- `DecodeError` is a subclass of `ValueError`, so existing `except ValueError` handlers will catch it.
