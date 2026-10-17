# OSINT Research Harness

A Python prototype for collecting evidence around a research question. It asks an LLM to split the question into claims, searches for material that could support or challenge each claim, downloads readable web pages, and ranks their text with BM25. The current command-line tool prints evidence excerpts and source URLs; it does not produce a final verdict.

## Setup

Use Python 3.10 or newer and create a virtual environment. From the repository root:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirenment.txt
python -m pip install openai python-dotenv google-genai googlesearch-python requests beautifulsoup4 rank-bm25
```

`requirenment.txt` currently lists only `google` and `ddgs`; the second install command covers imports used elsewhere in the code. The filename `requirenment.txt` is spelled as it appears in this repository.

Copy `.env.example` to `.env` and replace the placeholder with your API key:

```powershell
Copy-Item .env.example .env
```

Set `API_KEY` in `.env` to a key accepted by the OpenAI-compatible endpoint configured in `scripts/planner.py` (`https://api.aicredits.in/v1`). The planner currently requests the `openai/gpt-6-luna` model. `.env` is ignored by Git.

## Run

Run the evidence tool from the repository root so Python can resolve the `scripts` package:

```powershell
python -m tools.runtest "What is the capital of India?"
```

You can omit the question to enter it at the prompt. The tool prints each planned claim, then up to five ranked supporting and opposing results per claim, including a URL, BM25 score, and a 300-character excerpt. It requires network access to the configured LLM endpoint, search results, and source pages.

## How it works

1. `scripts/planner.py` generates a JSON research plan with claims, search queries, and retrieval hints for both evidence directions.
2. `scripts/evidence/fetcher.py` converts plan entries into research tasks.
3. `scripts/evidence/extractor.py` runs DuckDuckGo searches, deduplicates URLs for each side, fetches readable HTML, and ranks the extracted page text using `scripts/evidence/collector.py`.
4. `tools/runtest.py` displays the resulting evidence bundles.

`agents/court.py` contains prompts for supporter, opposition, and judge roles, but those roles are not called by the current tool. `main.py` is currently empty.

## Current limitations

- Search and page retrieval depend on third-party services and may return no readable results.
- Only HTML pages are extracted; PDFs and other formats are skipped.
- BM25 ranks whole-page text. A high score indicates lexical relevance, not that a claim is true.
- The command-line output is evidence for review, not an automated fact-check or synthesized answer.
