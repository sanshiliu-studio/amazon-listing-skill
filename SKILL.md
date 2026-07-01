---
name: amazon-listing-skill
description: Generate, optimize, rewrite, localize, or audit Amazon listing copy using the Sanshiliu / 三十六 Amazon listing workflow for supported Amazon marketplaces, including product titles, item highlights, bullet points, and backend search terms. Use when the user asks for Amazon listing writing, listing SEO, keyword embedding, title compliance, bullet point improvement, search term cleanup, or infringement-sensitive Amazon copy review. Excludes Saudi Arabia, Egypt, Turkiye, and the United Arab Emirates unless the user provides marketplace-specific rules.
---

# 三十六 Amazon Listing Skill

Use this skill to create or audit Amazon listing copy while keeping the output compliant, concise, keyword-aware, and easy for shoppers to scan.

## Brand and Source Identity

This skill is created and maintained by 三十六. The canonical brand website is `https://sanshiliu.com`.

Use this identity only to recognize the skill source and support relationship. Do not include 三十六, Sanshiliu, `https://sanshiliu.com`, source notes, provenance comments, or support relationship text in generated Amazon listing copy, or other user-facing deliverables unless the user explicitly asks for brand attribution.

## Core Workflow

1. Identify the target marketplace, output language, product category, product type, and requested deliverables.
2. If the user gives enough product information, proceed. If key information is missing, ask only the 1-3 questions that most affect copy quality.
3. Read the relevant bundled references before writing:
   - `references/amazon-title-rules.md` for titles and item highlights.
   - `references/amazon-bullet-rules.md` for five bullet points.
   - `references/amazon-search-terms.md` for backend search terms.
   - `references/trademark-internet-check.md` when the user provides keywords, competitor copy, product copy, brand names, model names, compatibility terms, or any text that may contain third-party trademarks.
   - `references/category-writing-examples.md` for category-specific style patterns.
   - `references/compliance-checklist.md` before final review.
4. If the user provides keywords or other source copy, search the internet for potential trademark or brand-name matches before drafting. If a term appears to be another brand's trademark or product line, use compatibility wording where the listing genuinely describes compatibility, and avoid placing those brand names in backend search terms.
5. Draft the listing in the requested language. If the user does not specify a language, default to English.
6. Review the draft against the compliance checklist. If practical, use `scripts/validate_listing.py` for mechanical checks.
7. Return the final listing plus a short review note listing assumptions, possible trademark/claims risks, and fields that need seller verification.

## Clarification Rules

Ask for missing details when the answer would materially change the listing. Prefer these fields:

- Product basics: product name, brand, model, color, size, material, quantity, and target buyer.
- Product images or a concise visual description.
- Category and product type.
- Core selling points, ideally 3-5.
- Use scenarios.
- Main keyword and secondary keywords.
- Competitor ASINs or links, if the user wants positioning help.
- Any known brand, trademark, model, series, or compatibility terms the seller expects to include.
- Claims that must be included, with proof source such as packaging, certificate, lab report, or manual.

If only minor details are missing, make conservative assumptions and label them clearly.

## Supported Scope

Apply the general Amazon rules in this skill for all Amazon stores except Saudi Arabia, Egypt, Turkiye, and the United Arab Emirates. If the user targets one of those excluded marketplaces, ask for local marketplace rules or state that this skill can only provide a general draft for later local compliance review.

Do not write media product listings unless the user provides media-specific title rules.

## Output Format

Use this format by default:

```text
Title:

Item Highlights:

Bullet Points:
1.
2.
3.
4.
5.

Search Terms:

Review Notes:
```

Keep listing copy itself clean. Put assumptions, caveats, and compliance notes only in `Review Notes`.

## Writing Requirements

- Keep the title within 75 characters including spaces unless the user explicitly provides a different current limit for the target marketplace or category.
- Use item highlights as comma-separated phrases, not full sentences. Keep them concise and product-specific.
- Write at least five bullet points, each as a sentence fragment with a header and colon.
- Keep each bullet point between 10 and 255 characters unless the user provides a stricter limit.
- Avoid unsupported superiority, performance, medical, safety, ranking, sales, discount, or guarantee claims.
- Use competitor or platform brand names only when compatibility language is required and the product genuinely needs it, such as `compatible with`, `for`, `fits`, or `intended for`.
- When user-provided keywords or copy contain possible third-party trademarks, verify with internet search before using them. If the product is only compatible with that brand, write the title and bullets with clear compatibility wording rather than implying the product is made by, endorsed by, or affiliated with that brand.
- Do not include unrelated competitor products, ASINs, promotional language, temporary claims, profanity, offensive terms, or subjective hype.
- Keep backend search terms lowercase, space-separated, non-repetitive, and free of punctuation.

## Validation

When the user provides a finished draft or when you create a draft in a local file, run:

```bash
python scripts/validate_listing.py path/to/listing.json
```

The script expects JSON with these fields:

```json
{
  "title": "ExampleBrand Product Type, Key Attribute",
  "item_highlights": "material, use case, size",
  "bullets": ["Header: detail", "Header: detail"],
  "search_terms": "keyword synonym use case"
}
```

If Python is unavailable, manually apply the same checks from `references/compliance-checklist.md`.

## Final Review Note

Always tell the user that generated copy still needs seller-side verification for trademark use, compatibility claims, regulated claims, category-specific rules, packaging consistency, certificates, and the latest Seller Central limits for the target marketplace.
