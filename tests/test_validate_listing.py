"""Regression coverage for observable validator behavior; no files are created."""

from __future__ import annotations

import copy
import importlib.util
import io
import json
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
import sys
import unittest
from unittest.mock import patch


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "validate_listing.py"
spec = importlib.util.spec_from_file_location("validate_listing", SCRIPT)
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


class ListingValidationTests(unittest.TestCase):
    def setUp(self):
        self.listing = {
            "title": "Acme Silicone Spatula, Red",
            "item_highlights": "Flexible Head, Easy Grip",
            "bullets": [
                "Design: Silicone head for daily cooking",
                "Grip: Handle for comfortable use",
                "Care: Rinse after regular daily use",
                "Color: Red finish for kitchen use",
                "Includes: One spatula for cooking",
            ],
            "search_terms": "turner scraper cooking utensil",
        }

    def run_cli(self, data, *options, raw=False):
        stdout, stderr = io.StringIO(), io.StringIO()
        content = data if raw else json.dumps(data, ensure_ascii=False)
        with patch.object(sys, "argv", [str(SCRIPT), "listing.json", *options]):
            with patch.object(Path, "read_text", return_value=content):
                with redirect_stdout(stdout), redirect_stderr(stderr):
                    try:
                        code = validator.main()
                    except SystemExit as exc:
                        code = exc.code
        return code, stdout.getvalue(), stderr.getvalue()

    def test_valid_english_listing_passes(self):
        code, output, error = self.run_cli(self.listing)
        self.assertEqual(code, 0, output + error)
        self.assertIn("PASSED", output)

    def test_product_description_accepts_paragraphs_and_localized_text(self):
        self.listing["product_description"] = (
            "这款硅胶锅铲适合家庭厨房日常翻炒。\n\n"
            "红色硅胶铲头搭配手柄，包装内含一把锅铲。"
        )
        code, output, error = self.run_cli(self.listing, "--require-description")
        self.assertEqual(code, 0, output + error)

    def test_supplied_product_description_must_be_nonempty_string(self):
        for value in (None, 123, [], {}, "", "   "):
            with self.subTest(value=value):
                self.listing["product_description"] = value
                code, output, _ = self.run_cli(self.listing)
                self.assertEqual(code, 1, output)
                self.assertIn("product_description", output)

    def test_product_description_character_boundary(self):
        for size, expected in ((2000, 0), (2001, 1)):
            with self.subTest(size=size):
                self.listing["product_description"] = "文" * size
                code, output, _ = self.run_cli(self.listing)
                self.assertEqual(code, expected, output)

    def test_product_description_budget_can_be_overridden(self):
        self.listing["product_description"] = "x" * 2001
        code, output, error = self.run_cli(self.listing, "--description-max-chars", "2500")
        self.assertEqual(code, 0, output + error)
        code, _, error = self.run_cli(self.listing, "--description-max-chars", "0")
        self.assertEqual(code, 2)
        self.assertIn("error", error.lower())

    def test_description_plain_text_check_rejects_html_links_and_email(self):
        for text in ("<b>Silicone spatula</b>", "First line<br>Second line",
                     "See https://example.com", "Visit www.example.com",
                     "Contact support@example.com"):
            with self.subTest(text=text):
                self.listing["product_description"] = text
                code, output, _ = self.run_cli(self.listing)
                self.assertEqual(code, 1, output)
                self.assertIn("product_description", output)

    def test_full_listing_can_require_product_description(self):
        code, output, _ = self.run_cli(self.listing, "--require-description")
        self.assertEqual(code, 1, output)
        self.assertIn("product_description", output)

    def test_description_only_does_not_require_other_listing_fields(self):
        data = {"product_description": "Silicone spatula for everyday cooking."}
        code, output, error = self.run_cli(data, "--description-only")
        self.assertEqual(code, 0, output + error)
        code, output, _ = self.run_cli({}, "--description-only")
        self.assertEqual(code, 1, output)
        self.assertIn("product_description", output)

    def test_search_byte_boundary(self):
        for size, expected in [(249, 0), (250, 1)]:
            with self.subTest(size=size):
                self.listing["search_terms"] = "x" * size
                code, output, _ = self.run_cli(self.listing)
                self.assertEqual(code, expected, output)

    def test_search_limit_counts_utf8_bytes(self):
        # 125 e-acute characters use 250 UTF-8 bytes, despite len(text) == 125.
        self.listing["search_terms"] = "é" * 125
        code, output, _ = self.run_cli(self.listing)
        self.assertEqual(code, 1, output)
        self.assertIn("bytes", output)

    def test_search_budget_counts_supplied_outer_spaces(self):
        self.listing["search_terms"] = "x" * 249 + " "
        code, output, _ = self.run_cli(self.listing)
        self.assertEqual(code, 1, output)
        self.assertIn("250 UTF-8 bytes", output)

    def test_non_string_fields_and_bullet_items_are_rejected(self):
        for field in ("title", "item_highlights", "search_terms"):
            for value in (None, 123, [], {}):
                with self.subTest(field=field, value=value):
                    data = copy.deepcopy(self.listing)
                    data[field] = value
                    code, output, _ = self.run_cli(data)
                    self.assertEqual(code, 1, output)
                    self.assertIn(field, output)
        self.listing["bullets"][0] = {"header": "Design"}
        code, output, _ = self.run_cli(self.listing)
        self.assertEqual(code, 1, output)
        self.assertIn("bullets[1]", output)

    def test_top_level_must_be_object(self):
        for data in ([], None, "text", 123):
            with self.subTest(data=data):
                code, output, _ = self.run_cli(data)
                self.assertEqual(code, 1, output)
                self.assertIn("object", output)

    def test_invalid_json_reports_input_error(self):
        code, _, error = self.run_cli("{", raw=True)
        self.assertEqual(code, 2)
        self.assertIn("ERROR", error)

    def test_decimal_highlights_pass_but_final_period_fails(self):
        self.listing["item_highlights"] = "Thickness 1.5 mm, Flexible"
        code, output, _ = self.run_cli(self.listing)
        self.assertEqual(code, 0, output)
        self.listing["item_highlights"] = "Comfortable for daily use."
        code, output, _ = self.run_cli(self.listing)
        self.assertEqual(code, 1, output)

    def test_uncased_title_and_bullets_pass_with_fullwidth_colon(self):
        self.listing["title"] = "硅胶锅铲 红色"
        self.listing["bullets"] = [
            "设计：硅胶铲头适合日常厨房烹饪",
            "握持：加长手柄适合日常翻炒使用",
            "清洁：使用后可按照说明冲洗清洁",
            "颜色：红色外观适合家庭厨房使用",
            "包装：内含一把锅铲用于日常烹饪",
        ]
        self.listing["search_terms"] = "烹饪 厨房 用具"
        code, output, _ = self.run_cli(self.listing)
        self.assertEqual(code, 0, output)

    def test_unicode_duplicate_words_and_punctuation_are_rejected(self):
        for text in ("收纳 收纳", "整理，便携", "café cafe\u0301", "café CAFÉ", "kitchen™"):
            with self.subTest(text=text):
                self.listing["search_terms"] = text
                code, output, _ = self.run_cli(self.listing)
                self.assertEqual(code, 1, output)

    def test_combining_marks_do_not_split_distinct_words(self):
        for text in ("किताब किसान", "كِتاب كُرسي"):
            with self.subTest(text=text):
                self.listing["search_terms"] = text
                code, output, _ = self.run_cli(self.listing)
                self.assertEqual(code, 0, output)

    def test_search_words_require_single_spaces(self):
        for text in ("cooking  utensil", "cooking\tutensil", "cooking\nutensil"):
            with self.subTest(text=text):
                self.listing["search_terms"] = text
                code, output, _ = self.run_cli(self.listing)
                self.assertEqual(code, 1, output)
                self.assertIn("single spaces", output)

    def test_title_limit_can_be_overridden(self):
        self.listing["title"] = (
            "Acme Silicone Kitchen Spatula, Red, Nonstick Cookware Utensil with Long Handle"
        )
        code, _, _ = self.run_cli(self.listing)
        self.assertEqual(code, 1)
        code, output, error = self.run_cli(self.listing, "--title-max-chars", "100")
        self.assertEqual(code, 0, output + error)

    def test_three_bullets_pass_and_requested_minimum_is_enforced(self):
        self.listing["bullets"] = self.listing["bullets"][:3]
        code, output, _ = self.run_cli(self.listing)
        self.assertEqual(code, 0, output)
        code, output, _ = self.run_cli(self.listing, "--min-bullets", "5")
        self.assertEqual(code, 1, output)
        self.assertIn("5", output)

    def test_category_bullet_length_and_search_limits_can_be_overridden(self):
        self.listing["bullets"][0] = "Details: " + "x" * 280
        self.listing["search_terms"] = "x" * 300
        code, _, _ = self.run_cli(self.listing)
        self.assertEqual(code, 1)
        code, output, error = self.run_cli(
            self.listing, "--bullet-max-chars", "400", "--search-max-bytes", "400"
        )
        self.assertEqual(code, 0, output + error)

    def test_invalid_limits_are_usage_errors(self):
        for options in (("--title-max-chars", "0"),
                        ("--min-bullets", "-1"),
                        ("--bullet-min-chars", "50", "--bullet-max-chars", "20")):
            with self.subTest(options=options):
                code, _, error = self.run_cli(self.listing, *options)
                self.assertEqual(code, 2)
                self.assertIn("error", error.lower())

    def test_english_caps_and_bullet_shape_still_checked(self):
        for bullet in ("design: Useful for daily cooking", "Design: Useful for daily cooking.",
                       "Design useful for daily cooking", ": Useful for daily cooking"):
            with self.subTest(bullet=bullet):
                self.listing["bullets"][0] = bullet
                code, output, _ = self.run_cli(self.listing)
                self.assertEqual(code, 1, output)
        self.listing["title"] = "ACME SILICONE SPATULA"
        code, output, _ = self.run_cli(self.listing)
        self.assertEqual(code, 1, output)
        self.assertIn("all caps", output)


if __name__ == "__main__":
    unittest.main()
