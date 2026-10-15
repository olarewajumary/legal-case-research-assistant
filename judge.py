import re
from llm import chat

JUDGE = (
    "You check how a source passage relates to a statement. Respond in exactly two lines.\n"
    "Line 1: QUOTE: <copy, word for word, the single sentence from the passage most relevant to the statement>\n"
    "Line 2: LABEL: <one of the following>\n"
    "  ASSERTS - the passage itself states the statement as its own rule or finding, with the same scope and conditions\n"
    "  OVERGENERAL - the passage supports only a narrower version: it applies a rule to specific facts, "
    "or it adds a condition that the statement leaves out\n"
    "  CONTRADICTS - the passage states the opposite\n"
    "  CONDITIONAL_OR_WARNING - the passage mentions the statement only inside an 'if', as a hypothetical, "
    "or as something to avoid or criticize\n"
    "  NOT_STATED - the passage does not address the statement, or only reports what a different case held or did "
    "(for example inside a citation or a parenthetical) without adopting it\n"
    "Read the quoted sentence carefully, including words like 'if', 'not', 'no', 'unless', and 'in this case'.\n"
    "A citation, or a parenthetical describing what a cited case did, is never ASSERTS: label it NOT_STATED."
)


def judge(statement, passage):
    """Return (label, raw_text) for how the passage relates to the statement."""
    text, _, _ = chat(
        [
            {"role": "system", "content": JUDGE},
            {"role": "user", "content": f"Passage:\n{passage}\n\nStatement: {statement}"},
        ],
        role="judge",
    )
    match = re.search(r"LABEL:\s*([A-Z_]+)", text)
    return (match.group(1) if match else "UNPARSED"), text