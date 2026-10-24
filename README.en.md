# Amazon Listing Skill

![Amazon Listing Skill overview](assets/readme-banner.svg)

**A Codex skill for Amazon sellers: write, optimize, localize, and review complete listing copy from confirmed product facts.**

[中文首页](README.md) · [Chinese usage guide](使用说明.md) · [Major update notes](RELEASE_NOTES.md) · [Download source ZIP](https://github.com/sanshiliu-studio/amazon-listing-skill/archive/refs/heads/main.zip)

## What you get

| Deliverable | Purpose |
| --- | --- |
| Title | Product identity and key attributes |
| Item Highlights | Concise details that complement the title |
| Bullet Points | Distinct features, uses, and buyer decision points |
| Product Description | Connected paragraphs about verified features, uses, specifications, and buyer concerns |
| Search Terms | A space-separated product-keyword field, with internal deduplication and coverage review |
| Review Notes | Missing information, selected budgets, and verification needs |

Request a full listing or only the parts you need. Product Description is a standard text field; A+ modules are separate deliverables.

## October 2026 major update

- **Product descriptions:** standalone or full-listing generation, with a four-part content framework and a dedicated validator mode.
- **Search Terms:** source-keyword coverage, explicit exclusion reasons, and deduplication only within the backend field. Relevant title or bullet keywords remain eligible.
- **Validation:** Unicode-aware handling, UTF-8 byte budgets, strict input types, decimal specifications, and configurable limits.
- **Documentation:** copyable request templates, a Chinese usage guide, and regression coverage.

Read the [update notes](RELEASE_NOTES.md) for compatibility and migration details.

## Install

Choose one local installation location. [OpenAI's current guidance](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills) lists `~/.agents/skills` for user skills and `.agents/skills` for repository skills.

Windows PowerShell:

```powershell
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.agents\skills" | Out-Null
git clone https://github.com/sanshiliu-studio/amazon-listing-skill.git "$env:USERPROFILE\.agents\skills\amazon-listing-skill"
```

macOS / Linux:

```bash
mkdir -p ~/.agents/skills
git clone https://github.com/sanshiliu-studio/amazon-listing-skill.git ~/.agents/skills/amazon-listing-skill
```

You can also download the [complete source ZIP](https://github.com/sanshiliu-studio/amazon-listing-skill/archive/refs/heads/main.zip), extract the skill folder as `amazon-listing-skill`, and place it in a discovery directory. If an update does not appear, restart Codex. Existing legacy installations should be updated at their actual location; avoid maintaining multiple active copies with the same name.

## Quick start

```text
Use $amazon-listing-skill to generate a complete English Amazon US listing.

Product: red polypropylene storage box, open top, no lid
Dimensions: 20 × 15 × 10 cm
Quantity: one box
Use: stationery storage on a home-office desk
Buyer concerns: lid, dimensions, material, and package contents
Keywords: storage box, storage bin, desk organizer, desktop organizer,
office organizer, stationery holder, red plastic container, open top box

Use confirmed facts only. Ask about important missing details before drafting.
```

To write only a description, specify that deliverable. To write only Search Terms, provide product facts and candidate keywords, then ask for one keyword line plus concise coverage notes.

## Keyword behavior

Deduplicate words **inside Search Terms**. Do not exclude a relevant term simply because it appears in a title, bullet, highlight, or description.

For example, `desk organizer`, `desktop organizer`, and `office organizer` can contribute `desk desktop office organizer`. Coverage review checks the final backend field itself; placement in another field does not count as backend coverage. Neither coverage nor a passing validation result guarantees indexing or ranking.

## Validate a draft

Everyday use is conversational; no terminal work is required from the seller. The bundled script uses the Python standard library and performs mechanical checks.

```bash
python scripts/validate_listing.py listing.json --require-description
python scripts/validate_listing.py description.json --description-only
python scripts/validate_listing.py --help
```

Default budgets: title 75 characters; highlights 125; at least three bullets, 10–255 characters each; description 2,000 characters; full-field Search Terms 249 UTF-8 bytes including spaces. Five bullets remain a writing preference. Confirm current marketplace and product-type limits rather than treating these defaults as universal policy.

Existing JSON may omit `product_description`. Use `--require-description` for new full listings. See [SKILL.md](SKILL.md) for the schema, options, and manual-review boundaries.

## Update an existing installation

In an installation created with Git, with local changes reviewed and handled first:

```bash
git pull --ff-only
```

For ZIP installations, back up local edits and follow the [migration guidance](RELEASE_NOTES.md#如何更新已有安装).

## Scope and review

General listing workflows are supported. Saudi Arabia, Egypt, Turkiye, the UAE, and media categories require marketplace/category-specific rules for compliance review. Verify product facts, packaging, trademark use, compatibility, and regulated claims. Internet trademark checks are directional. The skill does not publish listings to Amazon automatically.

## Development

```bash
python -B -m unittest discover -s tests -v
```

Created and maintained by **三十六 / Sanshiliu** · [sanshiliu.com](https://sanshiliu.com)

Project identity belongs to the skill documentation and is not added to generated product copy unless explicitly requested.
