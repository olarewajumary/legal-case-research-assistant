# Legal Case Research Assistant

Ask a legal question, get back a short answer built only from real U.S. court opinions, with the court, the citation, a link, and a word-for-word quote from the opinion. If the collection has nothing relevant, it says "No relevant precedent found." instead of guessing.

## What it does

You ask something like "Will an appeals court consider an argument that was raised for the first time on appeal?" It finds the passages that matter, drafts a few claims, and checks each claim against the source before showing it. Every claim you see comes with the exact sentence from the opinion that backs it. Opinions the court marked as unpublished, or Second Circuit summary orders, carry a warning that they are not binding precedent.

The collection is small on purpose: 33 opinions from the Ninth and Second Circuits (1,100 chunks), mostly qualified immunity, plus a handful on contract and insurance disputes. It is a portfolio project, not a legal research tool. Don't rely on it for real legal work.

## What's going on under the hood

Opinions come from the CourtListener API. I strip page markers and other noise from the text, split each opinion into chunks with stable IDs, and flag the unpublished ones.

Search runs two ways at once: a sentence-embedding model (MiniLM) for meaning and BM25 for exact words, merged with reciprocal rank fusion. A cross-encoder then re-ranks the top results. If the best score falls below a threshold, the system refuses before any model is called.

If something passes the gate, a writer model (gpt-oss-120b on Groq) returns claims as JSON. A second, smaller model (gpt-oss-20b) judges each claim against its source passage and has to copy the supporting quote. A claim is kept only if:

1. the judge says the passage asserts it,
2. the judge's quote really appears in the source, and
3. the quote isn't just a string of case citations.

Anything else is dropped, and the reason is printed.

## Why it checks its own answers

Early on, a claim about punitive damages was "supported" by a line that was only a citation: a case name, reporter numbers and a parenthetical. The words were in the source, but the court was citing another case, not stating a rule. That is why there is a separate citation-fragment check, and why the quote shown to you is cut from the source text itself and not retyped by the model.

## How I tested it

I wrote 15 evaluation questions and committed the expected case, expected answer and expected warning **before** running any of them: 11 answerable and 4 that should be refused. A script (`eval_run.py`) runs them and scores the first claim on opinion and warning. Whether the quote really states the rule is judged by me, by hand, because a script can't do that reliably.

The judge also has its own 15-case regression set (`regression_judge.py`). It scores 13 of 15. The two misses (cases 14 and 15) are kept on purpose, because they are real failures I haven't fixed.

## Results

All of this is one person's small sample, so there are no percentages. Groq, from my log:

| Outcome | Questions |
|---|---|
| Correct case, claim states the rule | Q1, Q2, Q8, Q14 |
| Correct case, but flaky (some runs unverified) | Q9, Q10, Q13, Q15 |
| Right case, claim missing part of the rule | Q3, Q11 |
| Never answered safely | Q12 |
| Refused correctly | Q4 to Q7 (4 of 4) |

"Flaky" means the writer's output varies from run to run, even at temperature 0. Q9 once failed because the writer returned broken JSON (it ended in `]]}`). I added one retry for that case.

Q12 (prison officials and post-release supervision) failed on every run, five in total. The opinion is a short summary order that leans on a companion case that isn't in my collection. The judge rejected the only quote available. I left it as a miss, because tuning the judge to pass a question I wrote myself would make the test meaningless.

### Offline mode

The same pipeline runs on a local 3B model through Ollama, with no internet. I ran all 15 questions once: 4 of 4 refusals were correct. Of the 11 answerable, 2 returned the right opinion, 8 came back unverified, and 1 returned the wrong opinion (Q12, which I haven't inspected). The 3B model often cuts off its JSON mid-answer, and my retry can't fix that because it resends the identical request. So offline mode refuses correctly and usually fails safe, but it rarely answers, and once it showed the wrong case.

## Limitations

- Small collection: 33 opinions, two circuits. I wrote the questions and the labels myself.
- The judge sometimes accepts a court that is only reporting another case's reasoning (judge cases 14 and 15).
- The refusal threshold (0.0) has only been checked on a few questions.
- The writer is not repeatable. Some questions pass on one run and fail on the next.
- There is no check for later history, so an opinion that was reversed or vacated is not flagged.
- Two different opinions share the name "Chamber of Commerce of the US v. Rob Bonta", so I key everything on opinion ID, not case name.
- One opinion (San Buenaventura) is stored as XML and gets parsed as HTML, which raises a warning. The text I read looked correct, but I never compared the two parses.
- OCR typos and footnote numbers remain in some chunk text.
- A broad question can get a narrow answer. The contract answer comes from a single maritime opinion.
- A second, off-topic claim can pass verification, because the check proves the words exist, not that they answer the question.

## Running it yourself

    git clone <your repo URL>
    cd legal-rag
    python -m venv .venv
    .venv\Scripts\activate
    pip install -r requirements.txt

Copy `.env.example` to `.env` and fill in your keys. `.env` is ignored by git, so it never gets committed.

| Variable | What it is |
|---|---|
| `COURTLISTENER_TOKEN` | Your CourtListener API token, needed only to collect new opinions |
| `GROQ_API_KEY` | Your Groq API key |
| `GROQ_MODEL` | Writer model, default `openai/gpt-oss-120b` |
| `GROQ_JUDGE_MODEL` | Judge model, default `openai/gpt-oss-20b` |
| `LLM_PROVIDER` | `groq` (default) or `ollama` for offline mode |

Then:

    python ask.py "Your question here"
    python eval_run.py 3 12
    python regression_judge.py
    python tests\test_citation_fragment.py

`eval_run.py 3 12` runs question 12 three times. With no arguments it runs every question once. For offline mode, start Ollama and set `$env:LLM_PROVIDER="ollama"` before the command.

## Built with

Python, CourtListener API, sentence-transformers (MiniLM), BM25, a cross-encoder re-ranker, Groq (gpt-oss-120b and gpt-oss-20b), Ollama (llama3.2:3b).

The git history shows the order the work happened in, including the evaluation questions, which were committed with their expected answers before their first run.