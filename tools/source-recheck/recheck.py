

from datetime import date
from difflib import SequenceMatcher
from pathlib import Path
import json
import re
import sys
import time

import requests
from bs4 import BeautifulSoup
from pypdf import PdfReader
from io import BytesIO


HERE = Path(__file__).parent
REPORTS = HERE / "reports"
USER_AGENT = (
    "HeferonDeadlineDesk-SourceCheck/1.0 "
    "(+https://www.heferon.com)"
)
TIMEOUT = 30
DELAY = 1


def load_sources():
    with (HERE / "sources.json").open(encoding="utf-8") as file:
        return json.load(file)
def normalize(text):
    text = text.replace("“", '"').replace("”", '"')
    text = text.replace("‘", "'").replace("’", "'")
    text = text.replace("™", "")
    text = re.sub(r"\[\s*(?:\.{3}|…)\s*\]", " ", text)
    return re.sub(r"\s+", " ", text).strip()

def extract_text(response):
    content_type = response.headers.get("Content-Type", "").lower()
    is_pdf = (
        "pdf" in content_type
        or response.url.lower().split("?")[0].endswith(".pdf")
        or response.content.startswith(b"%PDF")
    )

    if is_pdf:
        reader = PdfReader(BytesIO(response.content))
        return "\n".join(page.extract_text() or "" for page in reader.pages)

    soup = BeautifulSoup(response.content, "html.parser")
    for tag in soup(["script", "style", "noscript", "svg"]):
        tag.decompose()
    return soup.get_text(" ", strip=True)

def quote_parts(quote):
    parts = re.split(r"\[\s*(?:\.{3}|…)\s*\]", quote)
    return [normalize(part) for part in parts if normalize(part)]

def check_quote(quote, page_text):
    page = normalize(page_text)
    parts = quote_parts(quote)
    missing = [part for part in parts if part not in page]

    if not missing:
        return "OK", "All quote parts found."

    sentences = re.split(r"(?<=[.!?])\s+", page)
    target = missing[0]
    closest = max(
        sentences,
        key=lambda sentence: SequenceMatcher(
            None, target.lower(), sentence.lower()
        ).ratio(),
        default="",
    )
    score = SequenceMatcher(None, target.lower(), closest.lower()).ratio()

    note = f"Missing quote part; closest text ({score:.0%}): {closest[:300]}"
    return "CHANGED", note


def check_source(source, session):
    url = source["url"]
    try:
        response = session.get(
            url,
            timeout=TIMEOUT,
            headers={"User-Agent": USER_AGENT},
        )
        final_url = response.url

        if response.status_code >= 400:
            return {
                "id": source["id"],
                "title": source["title"],
                "status": "UNREACHABLE",
                "note": f"HTTP {response.status_code}",
                "url": url,
            }

        text = extract_text(response)
        if not text.strip():
            return {
                "id": source["id"],
                "title": source["title"],
                "status": "UNREACHABLE",
                "note": "Page returned no extractable text.",
                "url": url,
            }

        status, note = check_quote(source["quote"], text)
        if final_url != url:
            note = f"Redirected to {final_url}. {note}"

        return {
            "id": source["id"],
            "title": source["title"],
            "status": "MOVED" if final_url != url and status == "OK" else status,
            "note": note,
            "url": url,
        }

    except (requests.RequestException, ValueError, OSError) as error:
        return {
            "id": source["id"],
            "title": source["title"],
            "status": "UNREACHABLE",
            "note": f"{type(error).__name__}: {error}",
            "url": url,
        }


def main():
    sources = load_sources()
    REPORTS.mkdir(exist_ok=True)
    session = requests.Session()
    results = []
    fetched_urls = {}

    for index, source in enumerate(sources):
        url = source["url"]

        if url not in fetched_urls:
            if index:
                time.sleep(DELAY)
            fetched_urls[url] = check_source(source, session)

        result = dict(fetched_urls[url])
        result["id"] = source["id"]
        result["title"] = source["title"]
        results.append(result)

    today = date.today().isoformat()
    json_path = REPORTS / f"{today}.json"
    md_path = REPORTS / f"{today}.md"

    json_path.write_text(
        json.dumps(results, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    lines = [
        f"# Source recheck â€” {today}",
        "",
        "| ID | Title | Status | Note |",
        "|---|---|---|---|",
    ]
    for result in results:
        note = result["note"].replace("|", "\\|").replace("\n", " ")
        title = result["title"].replace("|", "\\|")
        lines.append(
            f"| {result['id']} | {title} | {result['status']} | {note} |"
        )
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    for result in results:
        print(f"{result['status']}: {result['id']} â€” {result['note']}")

    print(f"\nReports saved to:\n{md_path}\n{json_path}")
    return 1 if any(
        result["status"] in {"CHANGED", "UNREACHABLE"}
        for result in results
    ) else 0


if __name__ == "__main__":
    sys.exit(main())

