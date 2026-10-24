# Amazon Listing Compliance Checklist

Use this checklist before returning final listing copy.

## Required Checks

- Title is at or below the verified marketplace/category limit or explicitly selected draft budget; these are not automatically equivalent.
- Title does not use prohibited title characters.
- Title does not repeat meaningful words more than twice.
- Title is not all caps.
- Title does not include promotional, temporary, or unsupported subjective claims.
- User-provided keywords, competitor copy, and source text have been checked for possible third-party trademarks or brand names with internet search when needed.
- Competitor or third-party brand mentions use compatibility wording when necessary.
- Backend search terms do not contain third-party brand names or trademarks.
- Item highlights are comma-separated phrases, not full sentences.
- Item highlights are at most 125 characters; manually check the preferred capitalization and title-keyword overlap. Decimal specifications are not sentence punctuation.
- Bullet count matches the requested deliverable. Five is the default writing preference; US general guidance recommends at least three. Check the target rules separately.
- Each bullet point has a nonempty header and description separated by a colon, using natural localized punctuation.
- Each bullet point follows the selected marketplace/product-type length limit; 10-255 is a default drafting budget, not a universal ceiling.
- Capitalization checks apply only to languages with letter case.
- Bullet points avoid final punctuation.
- A full listing includes Product Description; a description-only request does not require unrelated listing fields.
- Product Description naturally covers supported facts about functions/features, use scenarios, materials/specifications, and consumer concerns, without copying the five bullets.
- Description claims and measurements are grounded in supplied evidence. Missing information is omitted or asked about, with gaps in Review Notes rather than placeholders in the copy.
- Description uses plain text and stays within the selected character budget; 2,000 is a drafting default, not a universal platform ceiling.
- Description contains no seller contact information, external links, pricing/promotions, delivery promises, review requests, or unverified claims. Check beyond the script's URL/email detection manually.
- Measurements include a space between digit and unit where natural.
- Search terms are lowercase, space-separated, and free of punctuation.
- Search Terms is a product-keyword string assembled from relevant supplied keywords, product synonyms, and supported search modifiers; it is not narrative or promotional prose.
- Supplied keyword coverage has been reviewed against Search Terms itself. Deduplication applies only inside Search Terms; relevant keywords already in the title, bullets, item highlights, or description remain eligible without losing priority because of that overlap. Useful unique words remain after internal deduplication. Review Notes identify represented, partly represented, or excluded terms with reasons; byte-budget omissions are identified separately. Visible-field placement does not substitute for backend coverage.
- Search terms do not repeat words unnecessarily.
- Search terms fit the selected UTF-8 byte budget; for US drafts, use at most 249 bytes for the complete field including spaces as a conservative check. Verify other marketplaces' limits before choosing their budget.
- Unsegmented Chinese/Japanese and other languages have been manually checked for repeated concepts; Unicode token matching alone cannot establish this.
- Search terms do not contain brand names, ASINs, temporary words, subjective hype, profanity, or offensive terms.
- Claims are consistent with the product information supplied by the user.
- No source/provenance text appears in the generated listing copy.
- JSON validation input is an object with correctly typed fields; no null or coerced non-string copy is accepted.
- A script result of `PASSED` covers mechanical checks only. Source-keyword coverage, brand/ASIN removal, claims, conversions, highlight style, and current local rules still require review. Do not promise actual indexing or ranking.

## Risk Notes to Surface to the User

Mention any of these when relevant:

- Trademark or compatibility wording should be reviewed by the seller.
- Internet trademark checks are directional only; seller should confirm trademark and compatibility risk with their own legal/account-health process.
- Medical, safety, environmental, durability, warranty, or certification claims need proof.
- Seller should verify current Seller Central field limits for the target marketplace and category.
- Seller should ensure copy matches packaging, images, certificates, and the actual product.
- This skill does not replace legal, regulatory, or Amazon account-health review.

## Manual Review Pattern

After drafting, silently check:

1. Is every sentence anchored in supplied product facts?
2. Could a shopper misunderstand source, compatibility, size, material, or included pieces?
3. Could Amazon suppress this for hype, forbidden terms, brand misuse, or unverifiable claims?
4. Are important keywords present without stuffing?
5. Is the copy readable on mobile?
