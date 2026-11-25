"""One-Sentence Absurd Invention Pitch (Make Fun, Akun 2).

Writes a single-sentence pitch for a ridiculous invention that fixes a
tiny everyday annoyance to /output/entry.txt.

Gate (from RULES.txt): entry.txt must be UTF-8 text of 1 to 220
characters, not only white space. The entry below is one sentence of
138 characters, no trailing newline, so the judge reads exactly the
sentence as written.
"""

import hashlib
import os

ENTRY = (
    "A belt that lets itself out one notch after every meal and blames "
    "the chair, so your trousers never have to admit they shrank in "
    "the wash."
)

MAX_CHARS = 220
SENTENCE_ENDERS = (".", "!", "?")


def validate(text):
    """Check the gate rules strictly: 1-220 chars, one sentence, one line.

    Hard validation, all failures raise ValueError (never assert, never
    silent repair): the entry is checked exactly as written -- no
    stripping, no newline fix-ups. A single sentence means exactly one
    sentence-ending mark, and it must be the final period: no '!' or
    '?' anywhere, no second '.'.
    """
    if not isinstance(text, str):
        raise ValueError("entry must be str, got %s" % type(text).__name__)
    if not text:
        raise ValueError("entry is empty")
    if text != text.strip():
        raise ValueError(
            "entry has leading or trailing white space: %r" % (text,)
        )
    if len(text) > MAX_CHARS:
        raise ValueError(
            "entry is %d characters, over the %d limit"
            % (len(text), MAX_CHARS)
        )
    if len(text) < 1:
        raise ValueError("entry is empty or only white space")
    bad_controls = [ch for ch in text if ord(ch) < 0x20 or ord(ch) == 0x7F]
    if bad_controls:
        raise ValueError(
            "entry contains control characters: %r" % (bad_controls,)
        )
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    enders = [ch for ch in text if ch in SENTENCE_ENDERS]
    if len(enders) != 1 or not text.endswith("."):
        raise ValueError(
            "entry must be exactly one sentence ending with a period, "
            "found enders: %r" % (enders,)
        )
    return text


def main():
    text = validate(ENTRY)
    expected = text.encode("utf-8")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    # Direct write only: plain open() + explicit chmod 0644. Never use
    # tempfile.mkstemp / NamedTemporaryFile / os.replace here -- an
    # atomic-write temp file lands at mode 0600 and the grader (a
    # different uid) cannot read entry.txt.
    with open(path, "wb") as handle:
        handle.write(expected)
    os.chmod(path, 0o644)
    # Round-trip verification: bytes on disk must be byte-identical to
    # the validated entry, and the mode must be exactly 0644.
    with open(path, "rb") as handle:
        on_disk = handle.read()
    if on_disk != expected:
        raise ValueError(
            "round-trip mismatch: wrote %d bytes, read back %d bytes"
            % (len(expected), len(on_disk))
        )
    mode = os.stat(path).st_mode & 0o777
    if mode != 0o644:
        raise ValueError("entry.txt mode is %o, expected 644" % mode)
    digest = hashlib.sha256(expected).hexdigest()
    print("wrote %s (%d characters, sha256 %s)" % (path, len(text), digest))


if __name__ == "__main__":
    main()
