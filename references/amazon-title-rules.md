# Amazon Title and Item Highlights Rules

Use these rules when drafting or auditing Amazon product titles and item highlights.

## Applicability

These title rules apply to general Amazon product listings except media product types and except Saudi Arabia, Egypt, Turkiye, and the United Arab Emirates. Ask for local or category-specific rules when the user targets an excluded store or a media category.

Primary references: [Amazon's 2026 title update](https://sellercentral.amazon.com/seller-forums/discussions/t/2f40628c-eb97-4b24-b983-cb1e331e06dc) and [Product title requirements and guidelines](https://sellercentral.amazon.com/help/hub/reference/GYTR6SYGFA5E3EQC), checked 2026-10-21. The announcement specifies 75-character titles and 125-character Item Highlights starting July 27, 2026. Confirm applicability in the target marketplace/category.

## Title Requirements

- Use a title budget of at most 75 characters including spaces by default. Apply a verified different marketplace/category limit when supplied. Honor an explicitly requested unverified draft budget only with a Review Note identifying the outstanding current-limit check.
- Pass a verified different limit to the validator with `--title-max-chars`; changing the budget alone does not establish marketplace compliance.
- Include the minimum information needed to clearly describe the product.
- Prefer this order when natural: brand, flavor or style, product type, key attribute, color, size or pack count, model number.
- Do not include promotional phrases such as `free shipping`, `100% quality guaranteed`, `best seller`, `hot item`, or discount wording.
- Do not include restricted phrases such as `FSA/HSA eligible` unless the user provides category proof and asks for it.
- Do not use these characters: `!`, `$`, `?`, `_`, `{`, `}`, `^`, `¬`, `¦`.
- Use symbols such as `~`, `#`, `<`, `>`, and `*` only when they are part of a real identifier or measurement. Do not use decorative symbols.
- Do not repeat the same meaningful word more than twice. Articles, prepositions, and conjunctions may repeat when needed.
- Brand names are subject to the same repetition rule.
- If mentioning another brand, first verify whether it is likely a third-party trademark or brand name. Use compatibility wording such as `for`, `compatible with`, `fits`, or `intended for`, and avoid wording that implies affiliation, source, sponsorship, or endorsement.
- Do not write the title in all caps. This check applies only to letters with case, not uncased writing systems.
- Use numerals rather than spelling out numbers in titles.
- Use standard measurement abbreviations when appropriate, such as `cm`, `oz`, `in`, and `kg`.
- When dealing with units such as dimensions or weight, the English output must include both metric and imperial units.

## Parent and Child Variation Rules

- Parent ASIN title: do not include size and color if those vary across children.
- Child ASIN title: include the selected size, color, pack count, or variation attribute.

## Item Highlights

Use item highlights when the title cannot carry all useful product details.

- Capitalize the first letter of each word, except for prepositions (in, on, over, with), conjunctions (and, or, for), or articles (the, a, an).
- Keep highlights concise.
- Write comma-separated phrases, not full sentences.
- Decimal specifications such as `1.5 mm` are valid phrases; do not treat a decimal point as a sentence boundary.
- Focus on materials, size, recommended use cases, compatibility, fit, included pieces, or care.
- Avoid repeating the exact title, It must not duplicate the keywords in the title.
- Avoid claims that require proof unless the user supplied proof.
- Keep the item highlights length within 125 characters (including punctuation and spaces).
- When dealing with units such as dimensions or weight, the English output must include both metric and imperial units.

## Examples

Good title:

```text
Amazon Essentials Women's Fleece Jacket, Black, Medium
```

Bad title:

```text
Amazon Essentials Super Comfortable Women's Winter Fleece Jacket with Pockets and Zipper Closure Perfect for Cold Weather and Outdoor Activities
```

Good compatibility wording:

```text
Case compatible with iPhone 16 Pro
```

Risky wording:

```text
iPhone Case
```

Safer compatibility wording:

```text
Case compatible with iPhone 16 Pro
```
