#!/usr/bin/env python3
"""Validate basic Amazon listing copy rules.

Input JSON:
{
  "title": "...",
  "item_highlights": "...",
  "bullets": ["Header: detail", "..."],
  "search_terms": "keyword keyword"
}
"""

from __future__ import annotations

import argparse
import json
import re
import string
import sys
from collections import Counter
from pathlib import Path


TITLE_FORBIDDEN_CHARS = set("!$?_{}^¬¦")
TITLE_PROMO_PHRASES = {
    "free shipping",
    "100% quality guaranteed",
    "best seller",
    "hot item",
    "on sale",
    "limited time",
}
SEARCH_FORBIDDEN_WORDS = {
    "amazing",
    "available",
    "best",
    "brand",
    "cheap",
    "cheapest",
    "current",
    "discounted",
    "effective",
    "fastest",
    "latest",
    "new",
    "popular",
    "sale",
    "today",
    "trending",
}
SEARCH_STOP_WORDS = {"a", "an", "and", "by", "for", "of", "the", "with"}
WORD_RE = re.compile(r"[A-Za-z0-9]+(?:'[A-Za-z0-9]+)?")


def words(text: str) -> list[str]:
    return [match.group(0).lower() for match in WORD_RE.finditer(text)]


def add_issue(issues: list[str], field: str, message: str) -> None:
    issues.append(f"{field}: {message}")


def validate_title(data: dict, issues: list[str]) -> None:
    title = str(data.get("title", "")).strip()
    if not title:
        add_issue(issues, "title", "missing")
        return

    if len(title) > 75:
        add_issue(issues, "title", f"length is {len(title)} characters; expected <= 75")

    bad_chars = sorted(TITLE_FORBIDDEN_CHARS.intersection(title))
    if bad_chars:
        add_issue(issues, "title", f"contains forbidden characters: {' '.join(bad_chars)}")

    lowered = title.lower()
    for phrase in sorted(TITLE_PROMO_PHRASES):
        if phrase in lowered:
            add_issue(issues, "title", f"contains promotional phrase: {phrase}")

    meaningful = [
        word
        for word in words(title)
        if word not in {"a", "an", "and", "for", "in", "of", "on", "or", "the", "to", "with"}
    ]
    repeated = sorted(word for word, count in Counter(meaningful).items() if count > 2)
    if repeated:
        add_issue(issues, "title", f"word appears more than twice: {', '.join(repeated)}")

    letters = [char for char in title if char.isalpha()]
    if letters and title == title.upper():
        add_issue(issues, "title", "appears to be all caps")


def validate_item_highlights(data: dict, issues: list[str]) -> None:
    highlights = str(data.get("item_highlights", "")).strip()
    if not highlights:
        return
    if "." in highlights:
        add_issue(issues, "item_highlights", "should be comma-separated phrases, not full sentences")
    if len(highlights) > 125:
        add_issue(issues, "item_highlights", f"length is {len(highlights)} characters; expected <= 125")


def validate_bullets(data: dict, issues: list[str]) -> None:
    bullets = data.get("bullets", [])
    if not isinstance(bullets, list):
        add_issue(issues, "bullets", "must be a list")
        return
    if len(bullets) < 5:
        add_issue(issues, "bullets", f"only {len(bullets)} bullets; expected at least 5")
    for index, bullet in enumerate(bullets, start=1):
        text = str(bullet).strip()
        field = f"bullets[{index}]"
        if not text:
            add_issue(issues, field, "missing")
            continue
        if len(text) < 10 or len(text) > 255:
            add_issue(issues, field, f"length is {len(text)} characters; expected 10-255")
        if ":" not in text:
            add_issue(issues, field, "missing header colon")
        if text[-1:] in ".!?":
            add_issue(issues, field, "should not use final punctuation")
        if text[:1] and text[:1].isalpha() and not text[:1].isupper():
            add_issue(issues, field, "should begin with a capital letter")
        if re.search(r"\d(?:ml|cm|mm|in|oz|kg|lb)\b", text, flags=re.IGNORECASE):
            add_issue(issues, field, "measurement should include a space between digit and unit")


def validate_search_terms(data: dict, issues: list[str]) -> None:
    search_terms = str(data.get("search_terms", "")).strip()
    if not search_terms:
        add_issue(issues, "search_terms", "missing")
        return
    if search_terms != search_terms.lower():
        add_issue(issues, "search_terms", "should be lowercase")
    punctuation = set(string.punctuation).intersection(search_terms)
    if punctuation:
        add_issue(issues, "search_terms", f"contains punctuation: {' '.join(sorted(punctuation))}")
    term_words = words(search_terms)
    repeated = sorted(word for word, count in Counter(term_words).items() if count > 1)
    if repeated:
        add_issue(issues, "search_terms", f"repeated words: {', '.join(repeated)}")
    forbidden = sorted(set(term_words).intersection(SEARCH_FORBIDDEN_WORDS))
    if forbidden:
        add_issue(issues, "search_terms", f"contains risky or forbidden words: {', '.join(forbidden)}")
    filler = sorted(set(term_words).intersection(SEARCH_STOP_WORDS))
    if filler:
        add_issue(issues, "search_terms", f"contains filler words: {', '.join(filler)}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate basic Amazon listing copy rules.")
    parser.add_argument("json_file", type=Path)
    args = parser.parse_args()

    try:
        data = json.loads(args.json_file.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"ERROR: could not read JSON: {exc}", file=sys.stderr)
        return 2

    issues: list[str] = []
    validate_title(data, issues)
    validate_item_highlights(data, issues)
    validate_bullets(data, issues)
    validate_search_terms(data, issues)

    if issues:
        print("FAILED")
        for issue in issues:
            print(f"- {issue}")
        return 1

    print("PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
