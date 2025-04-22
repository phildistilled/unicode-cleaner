import sys
import argparse
import unicodedata
import re

# Mapping of common emoji to tags
TAG_MAP = {
    '✅': '[CHECK]',
    '⚠️': '[WARNING]',
    '⬆️': '[UP]',
    '🔍': '[SEARCH]',
    '📦': '[PACKAGE]',
    '❌': '[ERROR]',
    '🔥': '[HOT]',
    '🕒': '[TIME]',
    '📁': '[FOLDER]',
    '📄': '[FILE]'
}

def is_printable(char):
    """Returns True if the character is printable and not a control character."""
    return char.isprintable() and not unicodedata.category(char).startswith("C")

def mode_strip(text):
    """Remove all non-printing and non-ASCII characters."""
    return ''.join(c for c in text if c in ' \n\r\t' or (32 <= ord(c) < 127))

def mode_unicode(text):
    """Replace each non-ASCII character with U+XXXX equivalent."""
    return ''.join(
        f'U+{ord(c):04X}' if not is_printable(c) or ord(c) > 127 else c
        for c in text
    )

def mode_tags(text):
    """Replace specific known emoji with plain tags."""
    result = []
    for char in text:
        result.append(TAG_MAP.get(char, char))
    return ''.join(result)

def main():
    parser = argparse.ArgumentParser(description="Unicode Cleaner Utility")
    parser.add_argument("infile", help="Input file path")
    parser.add_argument("outfile", help="Output file path")
    parser.add_argument("--mode", choices=["strip", "unicode", "tags"], required=True,
                        help="Mode: 'strip', 'unicode', or 'tags'")

    args = parser.parse_args()

    with open(args.infile, encoding="utf-8") as f:
        content = f.read()

    if args.mode == "strip":
        processed = mode_strip(content)
    elif args.mode == "unicode":
        processed = mode_unicode(content)
    elif args.mode == "tags":
        processed = mode_tags(content)

    with open(args.outfile, "w", encoding="utf-8") as f:
        f.write(processed)

    print(f"Processed file saved to: {args.outfile}")

if __name__ == "__main__":
    main()
