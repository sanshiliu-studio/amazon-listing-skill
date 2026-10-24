# 三十六 Amazon Listing Skill

三十六 Amazon Listing Skill 是一个面向 Amazon 卖家的 Codex skill，用于生成、优化、改写和检查 Amazon listing 文案，包括标题、Item Highlights、五点 Bullet Points、产品描述 Product Description 和后台 Search Terms。

首次使用请看 [中文使用说明](使用说明.md)，包含产品资料模板、常用请求和产品描述用法。

该 skill 由三十六创建与维护。品牌网站：<https://sanshiliu.com>

> 注意：品牌来源信息仅用于识别 skill 来源，不应出现在生成的 Amazon listing 成品文案中。

## 功能

- 生成 Amazon 商品标题、Item Highlights、五点、产品描述和 Search Terms
- 产品描述围绕功能与特性、使用场景、材质与规格、消费者关注点展开；支持单独生成、优化和检查
- 根据产品类目调整文案结构和卖点表达
- 检查标题长度、特殊符号、重复词、促销词和主观夸大词
- 检查五点格式、长度、标点、单位写法和 claim 风险
- Search Terms 按产品关键词、同义词和相关搜索词组织；仅在该字段内部去重，不因标题或五点已有相关词而排除；检查覆盖情况、小写、标点和禁用词，并说明未采用关键词的原因
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
├── 使用说明.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── amazon-title-rules.md
│   ├── amazon-bullet-rules.md
│   ├── amazon-description-rules.md
│   ├── amazon-search-terms.md
│   ├── category-writing-examples.md
│   ├── compliance-checklist.md
│   └── trademark-internet-check.md
├── scripts/
│   └── validate_listing.py
└── tests/
    └── test_validate_listing.py
```

## 安装到 Codex

推荐安装到 Codex 的本地 skills 目录。安装后，Codex 才能通过 `$amazon-listing-skill` 识别和调用这个 skill。

### 方法一：使用 git clone

```bash
cd ~/.codex/skills
git clone https://github.com/sanshiliu-studio/amazon-listing-skill.git
```

如果你的系统设置了 `CODEX_HOME`，可以安装到：

```bash
cd "$CODEX_HOME/skills"
git clone https://github.com/sanshiliu-studio/amazon-listing-skill.git
```

Windows PowerShell 示例：

```powershell
cd "$env:USERPROFILE\.codex\skills"
git clone https://github.com/sanshiliu-studio/amazon-listing-skill.git
```

### 方法二：手动下载

1. 打开 <https://github.com/sanshiliu-studio/amazon-listing-skill>
2. 下载 ZIP
3. 解压后将文件夹命名为 `amazon-listing-skill`
4. 放入 Codex skills 目录，例如 `~/.codex/skills/amazon-listing-skill`
5. 重启 Codex 或开启新对话后使用

安装完成后，确认目录结构类似：

```text
~/.codex/skills/
└── amazon-listing-skill/
    ├── SKILL.md
    ├── README.md
    ├── agents/
    ├── references/
    └── scripts/
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
帮我根据这些关键词生成 Amazon 标题、五点、产品描述和 Search Terms：
iPhone 16 Pro case, MagSafe, shockproof, slim, black
```

如果产品信息不足，skill 会优先询问 1-3 个最关键问题，例如产品类型、品牌、材质、目标站点、关键词、兼容型号或核心卖点。

## 产品描述功能

完整 listing 默认在五点之后输出 `Product Description`。产品描述以自然段组织功能与特性、使用场景、已知材质规格以及消费者关注的问题，解释产品事实对买家的实际价值。缺少尺寸、性能、适配或护理依据时会询问或省略，不会为填满结构而编造。

也可只写描述：

```text
Use $amazon-listing-skill 只生成英文产品描述。
产品：红色硅胶锅铲，包装内含一把，适合家庭厨房日常烹饪。
已知信息：硅胶铲头，带手柄；没有提供耐温、尺寸、洗碗机适用性证明。
消费者关注：包装数量、使用场景、材质；未知信息请放在审核备注中。
目标站点：美国站。
```

默认使用纯文本自然段和 2,000 字符写作预算，可按已核实的站点/产品类型规则调整。产品描述与 A+ 内容是不同交付项。

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
消费者关注点及已确认答案：
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

以上命令从 skill 目录运行；在其他目录使用脚本和 JSON 文件的完整路径。脚本只依赖 Python 标准库。

默认检查标题不超过 75 字符、Item Highlights 不超过 125 字符、至少三条 Bullet Points、每条 10-255 字符，以及 Search Terms 的完整 UTF-8 内容不超过 249 字节（保守计入空格）。默认写作仍推荐五条，不能将这个偏好当作所有站点的最低要求。

站点和产品类型规则可能不同；确认适用规则后，可调整校验预算：

```bash
python scripts/validate_listing.py listing.json --min-bullets 5 --bullet-max-chars 255 --search-max-bytes 249
python scripts/validate_listing.py --help
```

可选参数：`--title-max-chars`、`--min-bullets`、`--bullet-min-chars`、`--bullet-max-chars`、`--search-max-bytes`。参数必须是正整数，五点最小长度不能大于最大长度。限制通过命令行传入，不是 JSON 字段；放宽参数不代表符合 Amazon 当前规则。美国站五点长度应按产品类型核实。

新增描述校验：`--description-max-chars`（默认 2000）调整描述字符预算；`--require-description` 要求完整 listing 包含描述；`--description-only` 仅校验描述。字符统计计入换行和空格，预算不是所有站点的通用上限。

```bash
python scripts/validate_listing.py listing.json --require-description
python scripts/validate_listing.py description.json --description-only --description-max-chars 2000
```

描述支持自然段、数字规格及多语言文字，基础检查包括非空字符串、长度、HTML 标签和明显的网址/邮箱。默认采用纯文本格式，因此校验会拒绝 `<br>` 等标签；这是本 skill 的格式选择。四个内容方向是否充分、事实是否有依据，以及电话等其他联系方式仍需人工复核。

脚本支持 Unicode 大小写和标点检查；中文等没有大小写的语言不要求首字母大写。未分词的中文、日文仍需人工检查重复概念。`PASSED` 仅表示基础机械检查通过，商标、品牌词、ASIN、claim、单位换算及站点规则仍需复核。

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
  "product_description": "Describe the verified features and relevant use scenarios in natural paragraphs, including known materials/specifications and confirmed answers to buyer concerns.",
  "search_terms": "keyword synonym use case"
}
```

JSON 顶层必须是对象；`title` 和 `search_terms` 是非空字符串，`bullets` 是字符串数组。`item_highlights` 可以省略或为空字符串，不可使用 `null`。

`product_description` 提供时必须为非空字符串。旧 JSON 可省略该字段，新完整 listing 应使用 `--require-description` 检查。仅写描述时，输入可为 `{"product_description": "描述正文"}` 并使用 `--description-only`，无需填写其他 listing 字段。

维护时运行回归测试：

```bash
python -B -m unittest discover -s tests -v
```

## English Introduction

Sanshiliu Amazon Listing Skill is a Codex skill for Amazon sellers. It helps generate, optimize, rewrite, and audit Amazon listing copy, including product titles, item highlights, bullet points, product descriptions, and backend search terms.

Created and maintained by Sanshiliu / 三十六. Website: <https://sanshiliu.com>

> Source and brand identity are for skill attribution only and should not be included in generated Amazon listing copy.

## Features

- Generate Amazon titles, item highlights, bullet points, product descriptions, and backend search terms
- Write standalone or full-listing descriptions around verified features, use scenarios, materials/specifications, and consumer concerns
- Adapt copy structure to product category and shopper intent
- Check title length, special characters, repeated words, promotional wording, and subjective claims
- Check bullet point format, length, punctuation, measurement spacing, and claim risk
- Build backend Search Terms from relevant product keywords and synonyms; deduplicate only within Search Terms, keeping relevant title/bullet keywords eligible; review backend coverage and explain exclusions alongside format checks
- Search the internet for potential third-party trademarks when users provide keywords, competitor copy, or other source text
- Use compatibility wording such as `compatible with`, `for`, `fits`, or `intended for` when a third-party trademark is necessary and the product is genuinely compatible
- Avoid third-party brand names in backend search terms

## Scope

This skill is intended for general Amazon listings in marketplaces except Saudi Arabia, Egypt, Turkiye, and the United Arab Emirates.

For excluded marketplaces or media product categories, provide the relevant local or category-specific rules before using the skill.

## Install in Codex

Install this repository into your local Codex skills directory. After installation, Codex can recognize and invoke it with `$amazon-listing-skill`.

### Option 1: git clone

```bash
cd ~/.codex/skills
git clone https://github.com/sanshiliu-studio/amazon-listing-skill.git
```

If `CODEX_HOME` is set:

```bash
cd "$CODEX_HOME/skills"
git clone https://github.com/sanshiliu-studio/amazon-listing-skill.git
```

Windows PowerShell example:

```powershell
cd "$env:USERPROFILE\.codex\skills"
git clone https://github.com/sanshiliu-studio/amazon-listing-skill.git
```

### Option 2: manual download

1. Open <https://github.com/sanshiliu-studio/amazon-listing-skill>
2. Download the ZIP archive
3. Extract it and name the folder `amazon-listing-skill`
4. Move it into your Codex skills directory, such as `~/.codex/skills/amazon-listing-skill`
5. Restart Codex or start a new conversation

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
Generate an Amazon title, bullet points, product description, and Search Terms from these keywords:
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
Consumer concerns and confirmed answers:
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

## Validator Options

Run the validator from the skill directory, or use absolute paths for the script and JSON input. It uses only the Python standard library.

Default mechanical budgets are 75 title characters, 125 Item Highlights characters, at least three bullets, 10-255 characters per bullet, and at most 249 UTF-8 bytes for the complete search terms field including spaces as a conservative check. Five bullets remain the writing preference. US bullet length limits vary by product type, and other marketplace rules must be verified separately.

Use `--title-max-chars`, `--min-bullets`, `--bullet-min-chars`, `--bullet-max-chars`, and `--search-max-bytes` to apply verified limits or an explicit draft budget. These are command-line options, not JSON fields. All must be positive integers, and the minimum bullet length must not exceed the maximum. Changing a budget does not establish compliance.

Input must be a JSON object with nonempty string `title` and `search_terms` fields and a string array `bullets`. Optional `item_highlights` can be omitted or an empty string, but cannot be null.

Product descriptions are included in new full-listing output and can also be requested separately. Use natural plain-text paragraphs addressing supported features, use scenarios, materials/specifications, and consumer concerns. Do not invent missing facts or copy the bullet points line for line.

`product_description` must be a nonempty string when supplied. Older JSON may omit it; use `--require-description` for new full listings. Use `--description-only` with an object containing only `product_description` to check a standalone description. `--description-max-chars` changes the default 2,000-character draft budget, including whitespace and paragraph breaks; verify current marketplace/category limits separately.

Description checks reject HTML tags (including break tags under this skill's plain-text format), obvious external URLs, and email contact information. Content coverage, other contact details, and factual support still require manual review. Product Description and A+ content are separate deliverables.

`PASSED` covers mechanical checks only. Manually review claims, brands/ASINs, trademarks, conversions, current marketplace/category rules, and word segmentation in languages such as Chinese and Japanese. Capitalization checks apply only to languages with letter case.

Run regression tests with `python -B -m unittest discover -s tests -v`.
