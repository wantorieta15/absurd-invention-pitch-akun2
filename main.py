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
    """Check the gate rules: 1-220 chars, one sentence, not blank.

    A single sentence means exactly one sentence-ending mark, and it
    must be the final period: no '!' or '?' anywhere, no second '.'.
    """
    stripped = text.strip()
    if not stripped:
        raise ValueError("entry is empty or only white space")
    if len(stripped) > MAX_CHARS:
        raise ValueError(
            "entry is %d characters, over the %d limit"
            % (len(stripped), MAX_CHARS)
        )
    if "\n" in stripped or "\r" in stripped:
        raise ValueError("entry must be a single line")
    enders = [ch for ch in stripped if ch in SENTENCE_ENDERS]
    if len(enders) != 1 or not stripped.endswith("."):
        raise ValueError(
            "entry must be exactly one sentence ending with a period, "
            "found enders: %r" % (enders,)
        )
    return stripped


def main():
    text = validate(ENTRY)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(text)
    os.chmod(path, 0o644)
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    print("wrote %s (%d characters, sha256 %s)" % (path, len(text), digest))


if __name__ == "__main__":
    main()
