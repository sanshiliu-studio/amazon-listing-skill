# Amazon Backend Search Terms Rules

Use these rules when drafting or auditing backend Search Terms, the product-keyword field used for search matching. The deliverable is one space-separated keyword string assembled from product search terms. It has no requirement to read as a grammatical sentence.

Primary references: [Use search terms effectively](https://sellercentral.amazon.com/help/hub/reference/external/G23501?local=en-US), [Optimize your product discoverability](https://sellercentral.amazon.com/help/hub/reference/external/G10471), and [Amazon's search-term guidance](https://sellercentral.amazon.com/seller-forums/discussions/t/9a42d338-56cc-45b8-8bc5-446fd15ba579). The US byte-budget basis was checked 2026-10-21; the keyword-matching and formatting guidance was rechecked 2026-10-22. Verify the applicable limit for other marketplaces and product types.

## Keyword Selection and Coverage

Scope of deduplication for this skill: Search Terms is an independent keyword field. Deduplicate words inside that field only. A relevant keyword appearing in the title, bullets, item highlights, or product description remains eligible for Search Terms at its original relevance/user priority. Do not filter it out, deprioritize it, or mark it covered in Search Terms merely because it appears elsewhere. This is the user's keyword-selection workflow, not a claim that Amazon requires cross-field repetition.

1. Start with the user's relevant supplied product keywords. Keep source keyword phrases identifiable in a working list so their coverage can be reviewed. If none were supplied, derive candidates from confirmed product facts and buyer search intent; label inferred candidates as suggestions rather than researched search-volume data.
2. Build candidates from product/category names, synonyms and alternate names, supported material/shape/size/function terms, and relevant use/location/audience modifiers. Use keyword research or search-query data when supplied, preserving its documented priorities. Do not invent volume, conversion, or ranking evidence.
3. Remove irrelevant terms, brands/ASINs, unsupported attributes/claims, and other prohibited content. A competitor listing is not evidence that the seller's product has the same material or performance.
4. Assemble the remaining keyword words into one lowercase, space-separated field. Deduplicate words shared by multiple phrases within Search Terms while retaining useful unique terms. For example, `desk organizer`, `desktop organizer`, and `office organizer` can contribute `desk desktop office organizer`. Do not discard the latter phrases entirely because `organizer` is already present in Search Terms.
5. Check the selected byte budget and prioritize the user's important relevant terms, strong product names/synonyms, and distinct product search intent. Make selection decisions from the relevance, user priority, and space available in Search Terms itself; do not use overlap with the title or bullets as an exclusion or deprioritization criterion. Do not add irrelevant words simply to fill the remaining bytes.
6. Compare the final Search Terms field against every supplied candidate. In Review Notes, identify represented, partly represented, and excluded keywords, with reasons. Separate exclusions for byte budget from exclusions for relevance, facts, brands, or claims. A keyword appearing only in the title or bullets is not covered in Search Terms; do not substitute visible-field placement for backend coverage. A token's presence in any field is not evidence that Amazon actually indexes it.

Treat keyword coverage as a semantic review. The validator checks byte length, formatting, repetition, and its limited word lists; it cannot determine whether important source keywords were retained, whether the text reads like promotional prose, or whether Amazon will index a term. Do not replace this review with a `PASSED` result.

## Final Field Shape

- Put only the final keyword string under `Search Terms`; keep keyword coverage explanations and byte counts in Review Notes.
- Use product search words and short keyword combinations. Remove sales language, grammatical padding, first/second-person pronouns, and narrative connectors that do not add product-search intent.
- Preserve useful search modifiers such as material, use, location, or audience when supported; words that can also be verbs are not automatically invalid keywords. Do not use a generic sentence detector or arbitrary word blacklist as a substitute for relevance review.
- Word-level deduplication does not guarantee exact phrase matching, indexing, or ranking. Do not promise those outcomes.

## Drafting Rules

- Use lowercase words where the language has letter case.
- Separate words with single spaces.
- Do not use punctuation such as semicolons, colons, commas, or dashes.
- Avoid repeated words within Search Terms itself. Do not apply this as cross-field deduplication against the title, bullets, item highlights, or product description.
- Use either singular or plural, not both, unless the forms are meaningfully different.
- Include relevant synonyms, spelling variants, abbreviations, and shopper search phrases.
- Do not include common misspellings.
- Avoid articles, prepositions, and other short filler words such as `a`, `an`, `and`, `by`, `for`, `of`, `the`, and `with`.
- For US drafts, keep the complete field within a conservative 249-byte UTF-8 budget, counting spaces as well. This is a byte budget, not a character count: accented letters and CJK characters can use multiple bytes. Count the actual output, not a normalized/transliterated version.
- Confirm a different marketplace's current limit before choosing its budget; pass it with `--search-max-bytes`. The validator has a US-oriented default, not automatic marketplace detection.
- The validator normalizes Unicode for case-insensitive word comparison and detects Unicode punctuation/symbols. It detects repeated space-separated words; it does not perform semantic Chinese/Japanese word segmentation. Review such text manually for repeated concepts and relevance.

## Prohibited Terms

Do not include:

- The user's brand name or other brand names.
- ASINs.
- Profanity.
- Temporary claims such as `new`, `available now`, `on sale`, `limited time`, `today`, `this week`, or `latest`.
- Subjective claims such as `amazing`, `best`, `cheap`, `cheapest`, `effective`, `fastest`, `good deal`, `most popular`, or `trending`.
- Offensive, hateful, illegal, violent, sexual, racial, or religiously intolerant terms.

## Example With Traceable Keywords

Confirmed facts: a red, open-top polypropylene storage box for stationery on a home-office desk. No food-safety, waterproofing, stacking, or brand-compatibility evidence is supplied. The existing title is `Red Storage Box, Desk Organizer`; a bullet mentions `Office organizer for stationery`. These overlaps do not remove the product keywords from Search Terms.

User candidates:

```text
storage box
storage bin
desk organizer
desktop organizer
office organizer
stationery holder
red plastic container
open top box
polypropylene
food safe box
```

Search Terms:

```text
storage box bin desk desktop office organizer stationery holder red plastic container open top polypropylene
```

Review Notes: The first nine candidates are represented through their distinct words in Search Terms; `box` and `organizer` each appear once inside that field. Keywords such as `storage box`, `desk organizer`, and `office organizer` remain eligible despite their presence in the title or bullet. `food safe box` is excluded because its food-safety modifier is unsupported, even though the generic word `box` remains. Do not describe that candidate as fully covered. The final keyword string is 108 UTF-8 bytes including spaces and fits the selected 249-byte budget. No keyword was omitted because of that budget or because it appeared in another field. This does not establish actual indexing or ranking.

Avoid sentence-shaped output such as:

```text
organize your desk using this practical container that keeps everything tidy
```

That text spends space on narration and omits much of the supplied product-keyword coverage. Before returning Search Terms, check coverage and remove unnecessary padding, punctuation, repeated words, brands, and unsupported claims.
