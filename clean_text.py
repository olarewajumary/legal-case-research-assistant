import re

# a hyphenated word split by a page marker: "ne- *792 gleet" -> "neglect-style join"
SPLIT_WORD = re.compile(r"-\s*\*\d{1,4}\s+")
# a normal marker: remove it plus the space after it
MARKER = re.compile(r"\s*\*\d{1,4}\b\s*")


def remove_page_markers(text):
    text = SPLIT_WORD.sub("", text)
    text = MARKER.sub(" ", text)
    return text


if __name__ == "__main__":
    import json

    chunks = json.load(open("data/chunks.json", encoding="utf-8"))
    pat = re.compile(r"\*\d{1,4}\b")
    for c in chunks:
        if pat.search(c["text"]):
            after = remove_page_markers(c["text"])
            m = pat.search(c["text"])
            s = max(0, m.start() - 30)
            m2 = re.search(r"\*\d{1,4}\b", c["text"])
            s = max(0, m2.start() - 30)
            print(c["chunk_id"], "| before:", repr(c["text"][s:m2.end() + 30]))
            i = after.find(c["text"][s:m2.start()].strip()[-12:])
            print("          after: ", repr(after[i:i + 70]))