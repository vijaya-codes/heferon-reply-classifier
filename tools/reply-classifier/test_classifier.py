import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent))

from classifier import classify, strip_quoted

CASE_FILE = Path(__file__).parent / "cases.json"


def load_cases():
    with CASE_FILE.open("r", encoding="utf-8-sig") as file:
        return json.load(file)


@pytest.mark.parametrize("case", load_cases(), ids=lambda case: case["id"])
def test_classifier_cases(case):
    if case.get("xfail"):
        pytest.xfail(case["xfail"])

    actual = classify(
        case.get("subject", ""),
        case.get("text", ""),
        case.get("headers", {}),
    )

    assert actual == case["expected"]


def test_strip_quoted_lines():
    text = "Thanks for your email\n> old quoted text"
    assert strip_quoted(text) == "Thanks for your email"
