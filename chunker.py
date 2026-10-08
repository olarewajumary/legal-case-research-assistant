import json
import os
import re
from text_extract import extract_paragraphs

MAX_CHARS = 800


ABBREV_END = re.compile(
    r"(\b(v|No|Nos|Inc|Co|Corp|Ct|Cir|Mr|Mrs|Ms|Dr|St|Cal|Dist|Dep|Cf)\.|\b[A-Z]\.)$"
)


def split_long(paragraph, max_chars=MAX_CHARS):
    """Split an oversized paragraph between sentences, without cutting inside citations."""
    raw = re.split(r"(?<=[.!?])\s+(?=[A-Z“\"‘(])", paragraph)

    sentences = []
    for piece in raw:
        if sentences and ABBREV_END.search(sentences[-1]):
            sentences[-1] = f"{sentences[-1]} {piece}"
        else:
            sentences.append(piece)

    # Fallback: a sentence that is still too long is probably a string cite,
    # so split it at the semicolons between citations.
    shorter = []
    for s in sentences:
        if len(s) > max_chars:
            shorter.extend(re.split(r"(?<=;)\s+", s))
        else:
            shorter.append(s)
    sentences = shorter

    pieces, current = [], ""
    for s in sentences:
        if current and len(current) + 1 + len(s) > max_chars:
            pieces.append(current)
            current = s
        else:
            current = f"{current} {s}".strip()
    if current:
        pieces.append(current)
    return pieces


def chunk_paragraphs(paragraphs, max_chars=MAX_CHARS):
    """Pack whole paragraphs into chunks of at most max_chars."""
    chunks, current = [], ""
    for para in paragraphs:
        parts = split_long(para, max_chars) if len(para) > max_chars else [para]
        for part in parts:
            if current and len(current) + 1 + len(part) > max_chars:
                chunks.append(current)
                current = part
            else:
                current = f"{current} {part}".strip()
    if current:
        chunks.append(current)
    return chunks


if __name__ == "__main__":
    RAW_DIR = os.path.join("data", "raw")
    for name in sorted(os.listdir(RAW_DIR)):
        with open(os.path.join(RAW_DIR, name), encoding="utf-8") as f:
            rec = json.load(f)
        paras = extract_paragraphs(rec["text"])
        chunks = chunk_paragraphs(paras)
        longest = max(len(c) for c in chunks)
        print(f"{rec['opinion_id']:>9} | {len(paras):3} paras -> {len(chunks):3} chunks | longest {longest:4} | {rec['case_name'][:30]}")