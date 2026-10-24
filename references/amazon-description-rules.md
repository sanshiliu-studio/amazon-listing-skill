# Amazon Product Description Writing

Use for full-listing descriptions, description-only writing, optimization, localization, or audits. This is the standard Product Description field; A+ modules and images are separate deliverables.

## Content Framework

Organize the supplied product facts into a connected explanation of the product's value:

| Dimension | What to explain | Evidence needed |
| --- | --- | --- |
| Functions and features / 产品功能与特性 | Main purpose, key features, and the practical benefit of each | User-confirmed construction, functions, or performance evidence |
| Use scenarios / 使用场景 | Where, when, and for whom the product is useful; show how it fits a real task | Confirmed intended uses and limitations |
| Materials and specifications / 材质与规格 | Material, dimensions, color, weight, size, quantity, and contents where relevant | Supplied specifications, packaging, or manual |
| Consumer concerns / 消费者关注点 | Category-specific questions such as fit, compatibility, cleaning, setup, or what is included | Confirmed answers; do not invent reassurance or promises |

Cover all four dimensions when facts support them. Combine them naturally in short paragraphs rather than forcing four headings. Do not copy the bullet points line for line; connect a feature to its use and practical value. Integrate relevant keywords naturally without keyword stuffing or repeating a search-term list.

If an important fact is missing, ask only the questions that affect purchase accuracy. Otherwise omit the unsupported detail and identify the gap in Review Notes. Do not insert placeholders, assumed material/measurements, invented scenarios, certifications, compatibility, or unverified performance into the finished description. Consumer concerns must come from the brief or clearly labeled category-based judgment; do not claim to have analyzed reviews unless reviews were actually supplied or retrieved.

## Format and Limits

- Match the requested language and tone. Prefer a brief opening followed by concise paragraphs that explain usage, specifications, and the buyer's main concerns as relevant.
- Default to plain text with ordinary paragraph breaks and natural sentence punctuation. Do not emit Markdown tables, bullets copied from the five points, or HTML by default. This skill's validator checks plain-text descriptions, including rejection of HTML break tags; this is a formatting choice, not a claim that Amazon forbids every break-tag exception.
- Use 2,000 characters, including whitespace and paragraph breaks, as a drafting budget. Do not present it as a universal current Amazon limit. Verify the target marketplace/product-type field limit or use an explicitly requested draft budget, marking unverified limits in Review Notes. Pass the selected budget with `--description-max-chars`.
- Preserve consistency with the title, item highlights, bullets, images, packaging, and actual product. Apply the existing English convention for metric/imperial measurements and check conversions manually.
- Exclude seller contact information, external links, pricing/discounts, delivery promises, review requests/testimonials, competitor comparisons, and unsupported claims. Apply the trademark/compatibility reference when needed.

## Example Grounded in Supplied Facts

Facts: a red silicone spatula; one included; intended for daily home cooking; a handle for holding the utensil. No size, temperature rating, dishwasher claim, or cookware-safety evidence is supplied.

```text
Bring a simple cooking utensil to your daily kitchen routine with this red silicone spatula. Designed for everyday home cooking, it has a handle for holding the utensil while preparing meals.

The package includes one spatula with a silicone head. Check your cooking needs and the product information before choosing utensils for specific cookware or care routines.
```

Review Notes should identify missing dimensions and care/cookware compatibility facts if relevant. The example deliberately makes no heat-resistance, non-scratch, dishwasher-safe, or certification claim without evidence. In real output, replace generic purchase guidance with concrete verified answers when available.

## Validation

Store the final text as a nonempty JSON string in `product_description`:

```json
{"product_description": "Opening paragraph.\n\nUsage, specifications, and confirmed buyer-relevant details."}
```

Run `python scripts/validate_listing.py description.json --description-only`. A full listing should include this field and be checked with `--require-description`. Older listing JSON without this field remains accepted by default.

Mechanical checks do not establish whether the four content dimensions are adequately covered or whether statements are supported. Review those manually, especially when the available facts do not support a dimension.

## Policy Source

[Amazon US Product detail page rules](https://sellercentral.amazon.com/gp/help/external/G200390640?locale=en-US), checked 2026-10-21. The guidance calls for accurate descriptions and excludes links/contact information and advertising. It generally disallows HTML/JavaScript/code, with a description line-break exception. Check the applicable marketplace/category rules before treating a field format or length as current policy.
