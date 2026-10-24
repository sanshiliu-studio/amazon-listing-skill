#!/usr/bin/env python3
"""Validate basic Amazon listing copy rules (not a full compliance assessment).

Input JSON:
{
  "title": "...",
  "item_highlights": "...",
  "bullets": ["Header: detail", "..."],
  "product_description": "Plain-text product description (optional for legacy input)",
  "search_terms": "keyword keyword"
}
"""

from __future__ import annotations

import argparse
import json
import re
import string
import sys
import unicodedata
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


def words(text: str) -> list[str]:
    normalized = unicodedata.normalize("NFC", text.casefold())
    # Python's Unicode \w excludes combining marks, splitting e.g. Hindi words.
    # Preserve marks with their base letters; this is not semantic segmentation.
    tokens: list[str] = []
    current: list[str] = []
    for char in normalized:
        category = unicodedata.category(char)[0]
        if category in {"L", "N"} or (current and category == "M"):
            current.append(char)
        elif current and char in "'’":
            current.append(char)
        elif current:
            token = "".join(current).rstrip("'’")
            if token:
                tokens.append(token)
            current = []
    if current:
        token = "".join(current).rstrip("'’")
        if token:
            tokens.append(token)
    return tokens


def add_issue(issues: list[str], field: str, message: str) -> None:
    issues.append(f"{field}: {message}")


def text_field(
    data: dict, field: str, issues: list[str], *, required: bool = True
) -> str | None:
    value = data.get(field, "")
    if not isinstance(value, str):
        add_issue(issues, field, "must be a string")
        return None
    value = value.strip()
    if required and not value:
        add_issue(issues, field, "missing")
        return None
    return value


def validate_title(data: dict, issues: list[str], max_chars: int = 75) -> None:
    title = text_field(data, "title", issues)
    if title is None:
        return

    if len(title) > max_chars:
        add_issue(issues, "title", f"length is {len(title)} characters; expected <= {max_chars}")

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

    cased_letters = [char for char in title if char.lower() != char.upper()]
    if cased_letters and all(char.isupper() for char in cased_letters):
        add_issue(issues, "title", "appears to be all caps")


def validate_item_highlights(data: dict, issues: list[str]) -> None:
    highlights = text_field(data, "item_highlights", issues, required=False)
    if not highlights:
        return
    # A decimal separator is part of a specification, not sentence punctuation.
    if re.search(r"(?<!\d)\.|\.(?!\d)|[!?。！？]", highlights):
        add_issue(issues, "item_highlights", "should be comma-separated phrases, not full sentences")
    if len(highlights) > 125:
        add_issue(issues, "item_highlights", f"length is {len(highlights)} characters; expected <= 125")


def validate_bullets(
    data: dict, issues: list[str], min_count: int = 3,
    min_chars: int = 10, max_chars: int = 255,
) -> None:
    bullets = data.get("bullets", [])
    if not isinstance(bullets, list):
        add_issue(issues, "bullets", "must be a list")
        return
    if len(bullets) < min_count:
        add_issue(issues, "bullets", f"only {len(bullets)} bullets; expected at least {min_count}")
    for index, bullet in enumerate(bullets, start=1):
        field = f"bullets[{index}]"
        if not isinstance(bullet, str):
            add_issue(issues, field, "must be a string")
            continue
        text = bullet.strip()
        if not text:
            add_issue(issues, field, "missing")
            continue
        if len(text) < min_chars or len(text) > max_chars:
            add_issue(issues, field, f"length is {len(text)} characters; expected {min_chars}-{max_chars}")
        sections = re.split(r"[:：]", text, maxsplit=1)
        if len(sections) != 2 or not all(section.strip() for section in sections):
            add_issue(issues, field, "expected a nonempty header and description separated by a colon")
        if text[-1:] in ".!?。！？":
            add_issue(issues, field, "should not use final punctuation")
        if text[0].islower():
            add_issue(issues, field, "should begin with a capital letter")
        if re.search(r"\d(?:ml|cm|mm|in|oz|kg|lb)\b", text, flags=re.IGNORECASE):
            add_issue(issues, field, "measurement should include a space between digit and unit")


def validate_search_terms(data: dict, issues: list[str], max_bytes: int = 249) -> None:
    search_terms = text_field(data, "search_terms", issues)
    if search_terms is None:
        return
    # Check the supplied field, including outer whitespace, not its trimmed copy.
    search_terms = data["search_terms"]
    # Count the complete field, including spaces, as a conservative byte budget.
    byte_length = len(search_terms.encode("utf-8"))
    if byte_length > max_bytes:
        add_issue(issues, "search_terms", f"length is {byte_length} UTF-8 bytes; expected <= {max_bytes}")
    if search_terms != search_terms.lower():
        add_issue(issues, "search_terms", "should be lowercase")
    if search_terms != " ".join(search_terms.split()):
        add_issue(issues, "search_terms", "separate words with single spaces")
    punctuation = {
        char for char in search_terms
        if char in string.punctuation or unicodedata.category(char)[0] in {"P", "S"}
    }
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


def validate_product_description(
    data: dict, issues: list[str], max_chars: int = 2000, *, required: bool = False
) -> None:
    if "product_description" not in data and not required:
        return
    description = text_field(data, "product_description", issues)
    if description is None:
        return
    # Count the actual field, including paragraph breaks and outer whitespace.
    description = data["product_description"]
    if len(description) > max_chars:
        add_issue(issues, "product_description",
                  f"length is {len(description)} characters; expected <= {max_chars}")
    if re.search(r"<\s*/?\s*[A-Za-z][^>]*>", description):
        add_issue(issues, "product_description",
                  "HTML tags are outside this skill's plain-text description format")
    if re.search(r"https?://|www\.|[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}",
                 description, flags=re.IGNORECASE):
        add_issue(issues, "product_description", "contains external links or email contact information")


def positive_int(value: str) -> int:
    number = int(value)
    if number < 1:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return number


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate mechanical listing checks; verify current marketplace/category rules separately."
    )
    parser.add_argument("json_file", type=Path)
    parser.add_argument("--title-max-chars", type=positive_int, default=75,
                        help="title character budget (default: 75)")
    parser.add_argument("--min-bullets", type=positive_int, default=3,
                        help="minimum bullet count to check (default: 3; writing preference: 5)")
    parser.add_argument("--bullet-min-chars", type=positive_int, default=10,
                        help="minimum bullet length (default: 10)")
    parser.add_argument("--bullet-max-chars", type=positive_int, default=255,
                        help="bullet length budget; confirm product type (default: 255)")
    parser.add_argument("--search-max-bytes", type=positive_int, default=249,
                        help="conservative full-field UTF-8 byte budget (default: 249)")
    parser.add_argument("--description-max-chars", type=positive_int, default=2000,
                        help="product description draft budget; verify category limit (default: 2000)")
    parser.add_argument("--require-description", action="store_true",
                        help="require product_description in a full listing")
    parser.add_argument("--description-only", action="store_true",
                        help="validate only a required product_description field")
    args = parser.parse_args()
    if args.bullet_min_chars > args.bullet_max_chars:
        parser.error("--bullet-min-chars must not exceed --bullet-max-chars")

    try:
        data = json.loads(args.json_file.read_text(encoding="utf-8-sig"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        print(f"ERROR: could not read JSON: {exc}", file=sys.stderr)
        return 2

    issues: list[str] = []
    if not isinstance(data, dict):
        add_issue(issues, "input", "must be a JSON object")
    else:
        if not args.description_only:
            validate_title(data, issues, args.title_max_chars)
            validate_item_highlights(data, issues)
            validate_bullets(data, issues, args.min_bullets, args.bullet_min_chars, args.bullet_max_chars)
            validate_search_terms(data, issues, args.search_max_bytes)
        validate_product_description(data, issues, args.description_max_chars,
                                     required=args.require_description or args.description_only)

    if issues:
        print("FAILED")
        for issue in issues:
            print(f"- {issue}")
        return 1

    print("PASSED")
    print("Review: mechanical checks only; manually verify marketplace/category rules, "
          "claims, trademarks, and language-specific word segmentation.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
