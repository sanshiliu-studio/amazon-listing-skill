# 大版本更新说明

**2026 年 10 月更新** · 适用于从旧版升级的用户

本次更新将产品描述加入完整 Listing 流程，明确后台关键词的覆盖与去重方式，并完善校验和中文使用说明。已有技能名称 `$amazon-listing-skill` 保持不变。

[项目首页](README.md) · [使用说明](使用说明.md) · [详细更新记录](<Update Log.md>)

## 新增产品描述

完整 Listing 默认增加 `Product Description`，也支持只生成、优化或检查产品描述。内容围绕四个方向组织：

1. 产品功能与特性。
2. 使用场景。
3. 已确认的材质与规格。
4. 消费者关注的问题及已确认答案。

描述使用自然段，不将五点直接拼接成一段。没有依据的尺寸、性能、兼容性或认证不会被用来填充文案。默认 2,000 字符是可调整的写作预算，具体限制需按站点和产品类型核实。

## 调整 Search Terms 工作方式

- 先整理产品关键词候选池，再筛选、内部去重和计算字节预算。
- 以用户提供的相关关键词为起点，补充有事实支持的产品同义词、属性词和用途词。
- **去重只在 Search Terms 内部进行。** 标题、五点等其他字段已有的相关关键词仍可保留，不因跨字段重复而被排除或降低优先级。
- 多条短语共享一个词时保留各自的有效词，例如 `desk organizer`、`desktop organizer`、`office organizer` 可整理为 `desk desktop office organizer`。
- 审核备注按 Search Terms 本身核对完整覆盖、部分覆盖及未采用词，并区分字节预算、不相关、缺乏依据和品牌限制等原因。

关键词覆盖检查不保证实际索引或排名。

## 完善机械校验

| 改进 | 对使用者的影响 |
| --- | --- |
| 输入类型检查 | 空值或非字符串不再被当作文案接受；非对象 JSON 返回明确错误 |
| UTF-8 字节预算 | Search Terms 按完整字段字节数检查，保守计入空格 |
| Unicode 支持 | 改善中文、重音字符及组合字符处理；无大小写的文字不被要求首字母大写 |
| 小数规格 | `1.5 mm` 不再因小数点而被误判为完整句子 |
| 可调整预算 | 可按已确认的站点、产品类型规则调整标题、五点、描述及搜索词预算 |
| 独立描述校验 | 支持 `--description-only`；完整文案可使用 `--require-description` |

`PASSED` 仅表示机械检查通过。关键词相关性、来源关键词覆盖、受监管声明、商标、单位换算以及当前站点规则仍需审核。

## 兼容性说明

- 原有 `title`、`item_highlights`、`bullets`、`search_terms` 字段保留。
- 旧 JSON 可省略 `product_description`；提供时必须是非空字符串。
- 新完整 Listing 建议使用 `--require-description` 确保描述存在。
- 只校验描述时，可提交仅包含 `product_description` 的对象并使用 `--description-only`。
- 默认生成五条是写作偏好；脚本默认至少三条，五点长度仍需核对目标产品类型。
- 描述校验采用纯文本格式，因此拒绝 `<br>` 等 HTML 标签；这是技能的格式选择。

## 如何更新已有安装

### 通过 Git 安装

先确认当前目录是实际安装的技能目录，并处理自己修改过的文件，再执行：

```bash
git pull --ff-only
```

如果提示本地改动或分支分歧，先保留改动并检查原因，不要强制覆盖。

### 通过 ZIP 安装

1. 下载[完整源码包](https://github.com/sanshiliu-studio/amazon-listing-skill/archive/refs/heads/main.zip)。
2. 如有自定义规则或本地改动，先单独备份。
3. 将包内技能文件更新到原安装目录，保留自己的商品输出和资料。
4. 避免同时保留两份会被自动加载、且名称相同的技能。
5. 如果 Codex 未识别更新，重启后再调用。

不要根据电脑目录里的商品输出文件判断技能版本；生成的实际商品文案不是技能发布文件。

## 更新后建议验证

发送一个真实产品请求，检查是否能得到产品描述，以及 Search Terms 是否保留所需相关关键词。如果使用校验脚本，可执行：

```bash
python scripts/validate_listing.py listing.json --require-description
python -B -m unittest discover -s tests -v
```

技术细节见 [SKILL.md](SKILL.md)，逐项历史记录见[更新日志](<Update Log.md>)。
