# 三十六 Amazon Listing Skill

三十六 Amazon Listing Skill 是一个面向 Amazon 卖家的 Codex skill，用于生成、优化、改写和检查 Amazon listing 文案，包括标题、Item Highlights、五点 Bullet Points 和后台 Search Terms。

该 skill 由三十六创建与维护。品牌网站：<https://sanshiliu.com>

> 注意：品牌来源信息仅用于识别 skill 来源，不应出现在生成的 Amazon listing 成品文案中。

## 功能

- 生成 Amazon 商品标题、Item Highlights、五点和 Search Terms
- 根据产品类目调整文案结构和卖点表达
- 检查标题长度、特殊符号、重复词、促销词和主观夸大词
- 检查五点格式、长度、标点、单位写法和 claim 风险
- 检查 Search Terms 的小写、去重、标点和禁用词
- 当用户提供关键词、竞品文案或其他来源文案时，联网检索潜在商标/品牌名
- 如果包含第三方品牌商标，在真实兼容关系下使用 `compatible with`、`for`、`fits`、`intended for` 等兼容表达
- 避免将第三方品牌名写入后台 Search Terms

## 适用范围

适用于除沙特阿拉伯、埃及、土耳其和阿拉伯联合酋长国以外的 Amazon 站点的一般商品 listing。

如果目标站点是沙特阿拉伯、埃及、土耳其或阿拉伯联合酋长国，或者商品属于媒体类目，需要用户提供对应站点或类目的专用规则。

## 文件结构

```text
amazon-listing-skill/
├── SKILL.md
├── README.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── amazon-title-rules.md
│   ├── amazon-bullet-rules.md
│   ├── amazon-search-terms.md
│   ├── category-writing-examples.md
│   ├── compliance-checklist.md
│   └── trademark-internet-check.md
└── scripts/
    └── validate_listing.py
```

## 如何使用

在 Codex 中输入：

```text
Use $amazon-listing-skill 帮我写一个 Amazon listing。
产品：iPhone 16 Pro 手机壳
品牌：ABC
材质：TPU + PC
颜色：黑色
卖点：防摔、MagSafe、轻薄、镜头保护
关键词：iPhone 16 Pro case, MagSafe case, shockproof phone case
目标站点：美国站
```

也可以从更简单的信息开始：

```text
Use $amazon-listing-skill
帮我根据这些关键词生成 Amazon 标题、五点和 Search Terms：
iPhone 16 Pro case, MagSafe, shockproof, slim, black
```

如果产品信息不足，skill 会优先询问 1-3 个最关键问题，例如产品类型、品牌、材质、目标站点、关键词、兼容型号或核心卖点。

## 推荐提供的信息

```text
产品名称：
品牌名：
目标站点：
输出语言：
产品类目：
颜色/尺寸/材质/数量：
核心卖点：
使用场景：
目标人群：
关键词：
是否兼容其他品牌/型号：
竞品链接或参考文案：
需要使用的 claims 及证明来源：
```

## 商标和兼容表达

当用户提供的关键词、竞品文案或其他来源文案中可能包含第三方品牌名或商标时，skill 会先进行互联网检索。若某个词看起来属于其他品牌或产品线，且商品只是兼容该品牌产品，应使用兼容表达。

推荐：

```text
Case compatible with iPhone 16 Pro
Replacement filter for Dyson V11 vacuum
Charging cable designed for Samsung Galaxy devices
```

避免：

```text
iPhone Case
Dyson V11 Filter
Samsung Charging Cable
```

联网检索只能作为方向性判断，不能替代卖家的商标、法务、Amazon Brand Registry 或账户健康审核。

## 校验脚本

如果将 listing 保存为 JSON，可以运行：

```bash
python scripts/validate_listing.py listing.json
```

JSON 示例：

```json
{
  "title": "ExampleBrand Product Type, Key Attribute",
  "item_highlights": "material, use case, size",
  "bullets": [
    "Header: detail",
    "Header: detail",
    "Header: detail",
    "Header: detail",
    "Header: detail"
  ],
  "search_terms": "keyword synonym use case"
}
```

## English Introduction

Sanshiliu Amazon Listing Skill is a Codex skill for Amazon sellers. It helps generate, optimize, rewrite, and audit Amazon listing copy, including product titles, item highlights, bullet points, and backend search terms.

Created and maintained by Sanshiliu / 三十六. Website: <https://sanshiliu.com>

> Source and brand identity are for skill attribution only and should not be included in generated Amazon listing copy.

## Features

- Generate Amazon titles, item highlights, bullet points, and backend search terms
- Adapt copy structure to product category and shopper intent
- Check title length, special characters, repeated words, promotional wording, and subjective claims
- Check bullet point format, length, punctuation, measurement spacing, and claim risk
- Clean backend search terms for lowercase formatting, repetition, punctuation, and prohibited terms
- Search the internet for potential third-party trademarks when users provide keywords, competitor copy, or other source text
- Use compatibility wording such as `compatible with`, `for`, `fits`, or `intended for` when a third-party trademark is necessary and the product is genuinely compatible
- Avoid third-party brand names in backend search terms

## Scope

This skill is intended for general Amazon listings in marketplaces except Saudi Arabia, Egypt, Turkiye, and the United Arab Emirates.

For excluded marketplaces or media product categories, provide the relevant local or category-specific rules before using the skill.

## Usage

Start with:

```text
Use $amazon-listing-skill to generate an Amazon listing.
Product: iPhone 16 Pro phone case
Brand: ABC
Material: TPU + PC
Color: Black
Benefits: drop protection, MagSafe, slim design, camera protection
Keywords: iPhone 16 Pro case, MagSafe case, shockproof phone case
Marketplace: US
```

Or:

```text
Use $amazon-listing-skill
Generate an Amazon title, bullet points, and Search Terms from these keywords:
iPhone 16 Pro case, MagSafe, shockproof, slim, black
```

If product information is incomplete, the skill asks only the most important clarification questions before drafting.

## Recommended Input

```text
Product name:
Brand:
Marketplace:
Output language:
Product category:
Color/size/material/quantity:
Core selling points:
Use cases:
Target audience:
Keywords:
Compatibility brands or models:
Competitor links or reference copy:
Claims to include and proof source:
```

## Trademark and Compatibility Handling

When user-provided keywords or source copy may contain third-party trademarks, the skill searches the internet before drafting. If a term appears to be another brand or product line and the seller's product is only compatible with it, the skill uses clear compatibility wording.

Preferred:

```text
Case compatible with iPhone 16 Pro
Replacement filter for Dyson V11 vacuum
Charging cable designed for Samsung Galaxy devices
```

Avoid:

```text
iPhone Case
Dyson V11 Filter
Samsung Charging Cable
```

Internet checks are directional only and do not replace seller legal review, Amazon Brand Registry review, or account-health review.
