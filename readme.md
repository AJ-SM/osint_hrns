# OSINT Research Harness

A command-line research tool that keeps the user's query as one research task, gathers web evidence for and against it, and runs an LLM-based debate and judgment. It prints trial arguments, verdicts, reasoning, and one final factual conclusion.

## Requirements and setup

- Python 3.10 or newer
- Internet access for the model API, DuckDuckGo search, and source pages
- An API key for the OpenAI-compatible endpoint configured in `scripts/planner.py` and `agents/court.py` (`https://api.aicredits.in/v1`)

From the repository root, create an environment and install the packages imported by the application:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install openai python-dotenv google-genai googlesearch-python ddgs requests beautifulsoup4 rank-bm25
Copy-Item .env.example .env
```

Replace the placeholder in `.env` with your key:

```dotenv
API_KEY=your_api_key
```

Both the planner and court currently request `openai/gpt-6-luna` through that endpoint. The `.env` file is ignored by Git. The repository's `requirenment.txt` lists only `google` and `ddgs`; it does not cover all runtime imports, so use the install command above.

## Run

From the repository root:

```powershell
python -m tools.runtest --trials 2 "What is the capital of India?"
```

Pass any claim or research question as the positional argument. If you omit it, the tool prompts for one. `--trials` sets the number of trials to run; the value must be at least 1.

The tool prints its progress as it researches and runs each court trial. It shows the supporter argument in blue, opposition argument in red, and judge verdict and reasoning in green. It does not print the retrieved evidence bundles. After all trials, it prints a final evidence-based verdict, the winning side when there is one, a self-contained factual conclusion, and trial counts. Each trial makes three model calls (supporter, opposition, and judge); the final finding makes one more call, in addition to the planning call.

## How it works

1. `scripts/planner.py` asks the model to plan one research task for the complete query, with separate supporting and opposing search plans. If it returns multiple tasks, they are combined into one before research begins.
2. `scripts/evidence/extractor.py` searches DuckDuckGo for each side, deduplicates URLs, extracts readable HTML with `scripts/stripper.py`, and ranks whole-page text using BM25 in `scripts/evidence/collector.py`.
3. `agents/court.py` gives the ranked evidence to a supporter and an opposition model call. A judge model call reviews both arguments and the original evidence, then returns a verdict. Later trials receive previous verdicts and reasoning. After all trials, a final model call reviews evidence and rulings across trials to write the conclusion.
4. `tools/runtest.py` displays the trial results and final finding for each claim.

Possible verdicts are `SUPPORTED`, `CONTRADICTED`, `PARTIALLY_SUPPORTED`, `CONFLICTING_EVIDENCE`, and `INSUFFICIENT_EVIDENCE`. The final `other` count includes the last three. Before each retrial, the tool searches and fetches evidence again using the original research plan for that claim. A research gap is reported but does not change the search queries automatically.

## Limitations

- Search results and readable pages depend on external services. The extractor skips non-HTML responses, including PDFs.
- BM25 scores measure word overlap with retrieval hints, not truth or source quality.
- Verdicts are model judgments over the retrieved evidence and should be checked against the underlying sources.
- `main.py` is empty; the supported entry point is `python -m tools.runtest`.
