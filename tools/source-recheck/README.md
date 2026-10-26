# Source Recheck

A Python tool that checks quoted text against official source URLs and generates dated Markdown and JSON reports.

## Requirements

- Python 3.10 or newer
- Internet access for live checks

## Install

From the repository root:

    python -m pip install -r .\tools\source-recheck\requirements.txt

## Run

    python .\tools\source-recheck\recheck.py

The tool reads sources.json, fetches each distinct URL once per run, waits one second between new URL requests, and uses a 30-second timeout.

Reports are saved under tools/source-recheck/reports/ as YYYY-MM-DD.md and YYYY-MM-DD.json.

## Statuses

- OK: all quote parts were found.
- CHANGED: one or more quote parts were not found; the report includes the closest matching text and similarity score.
- MOVED: the URL redirected and the quote was found at the destination.
- UNREACHABLE: the request failed, returned an HTTP error, or produced no extractable text.

Exit code 0 means all results were OK or MOVED. Exit code 1 means at least one result was CHANGED or UNREACHABLE.

## Tests

Run the offline tests with:

    python -m pytest .\tools\source-recheck\test_recheck.py -q

Tests use mocked responses and do not need to contact official websites.

## Source records

sources.json contains each source's ID, publisher, title, URL, retrieval date, and quoted text. Text inside [...] separates a quote into ordered pieces that must each be found.

## Network behavior

The tool uses this User-Agent:

HeferonDeadlineDesk-SourceCheck/1.0 (+https://www.heferon.com)

Review CHANGED and UNREACHABLE results manually before changing any source records.
