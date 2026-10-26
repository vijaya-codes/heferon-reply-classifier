from pathlib import Path
from io import BytesIO
import sys
import json

import pytest
import requests

sys.path.insert(0, str(Path(__file__).parent))
import recheck


class FakeResponse:
    def __init__(self, content=b"", status_code=200,
                 url="https://example.com/page",
                 content_type="text/html"):
        self.content = content
        self.status_code = status_code
        self.url = url
        self.headers = {"Content-Type": content_type}


class FakeSession:
    def __init__(self, response=None, error=None):
        self.response = response
        self.error = error
        self.calls = []

    def get(self, url, **kwargs):
        self.calls.append(url)
        if self.error:
            raise self.error
        return self.response


def test_exact_html_quote_is_ok():
    response = FakeResponse(
        b"<p>The official deadline is 31 October 2026.</p>"
    )
    text = recheck.extract_text(response)
    assert recheck.check_quote(
        "The official deadline is 31 October 2026.", text
    )[0] == "OK"


def test_whitespace_and_curly_quotes_are_normalized():
    page = "The “official”  deadline isn’t changing."
    quote = "The \"official\" deadline isn't changing."
    assert recheck.check_quote(quote, page)[0] == "OK"


def test_ellipsis_quote_parts_are_checked():
    quote = "The deadline is 31 October [...] Applications close at noon."
    page = "The deadline is 31 October. Applications close at noon."
    assert recheck.check_quote(quote, page)[0] == "OK"


def test_missing_quote_text_is_changed():
    status, note = recheck.check_quote(
        "The deadline is 31 October 2026.",
        "The deadline is 30 November 2026.",
    )
    assert status == "CHANGED"
    assert "closest text" in note
    assert "%" in note


def test_http_404_is_unreachable():
    session = FakeSession(response=FakeResponse(status_code=404))
    source = {
        "id": "test-404",
        "title": "Test page",
        "url": "https://example.com/page",
        "quote": "Some text",
    }
    result = recheck.check_source(source, session)
    assert result["status"] == "UNREACHABLE"
    assert "404" in result["note"]


def test_timeout_is_unreachable():
    session = FakeSession(error=requests.Timeout("timed out"))
    source = {
        "id": "test-timeout",
        "title": "Test page",
        "url": "https://example.com/page",
        "quote": "Some text",
    }
    result = recheck.check_source(source, session)
    assert result["status"] == "UNREACHABLE"
    assert "Timeout" in result["note"]


def test_redirect_is_recorded():
    session = FakeSession(response=FakeResponse(
        content=b"<p>The official deadline is 31 October 2026.</p>",
        url="https://example.com/new-page",
    ))
    source = {
        "id": "test-redirect",
        "title": "Redirect test",
        "url": "https://example.com/old-page",
        "quote": "The official deadline is 31 October 2026.",
    }
    result = recheck.check_source(source, session)
    assert result["status"] == "MOVED"
    assert "https://example.com/new-page" in result["note"]


def test_pdf_fixture_text_is_extracted():
    fixture = (
        Path(__file__).parent
        / "fixtures"
        / "sample.pdf"
    )
    response = FakeResponse(
        content=fixture.read_bytes(),
        content_type="application/pdf",
    )

    text = recheck.extract_text(response)

    assert recheck.check_quote(
        "The official deadline is 31 October 2026.",
        text,
    )[0] == "OK"
