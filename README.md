# Open Fact Quick Diagnosis
An executable AI Workflow that turns public-information verification into a disciplined, auditable process.

## What it does
Input a closed decision question + public materials → outputs:
1. Direct answer to the decision question
2. Source ledger (reliability A–F)
3. Claim register (L1–L5 with mandatory “why not higher” justification)
4. Conflict comparison table
5. Findings with **suggested wording** + **forbidden wording**
6. Forced Self-check checklist (blocks output until all rules pass)

## Core Discipline
- Official statements / single-party narratives are capped at L4 and can never be written as plain facts
- Reposts and secondary reporting do not count as independent corroboration
- Every claim must actively consider downgrading
- Must output both “what can be said” and “what must never be said”

## Quick Start
1. Copy the full content of `system_prompt.md` into any long-context LLM
2. Or run the Gradio prototype locally / deploy to Hugging Face Spaces

## Why this matters for AI products
This is a concrete example of **information boundary control** and **output evaluation framework** design — exactly the kind of systematic thinking needed for production LLM systems, red-teaming, and high-stakes conversational AI.

# 公开快诊 · AI 辅助版（Open Fact Quick Diagnosis）

把「公开信息研判」工作流固化成可复用的 AI 工具。  
作者已退出人工服务，本仓库仅作方法留存与开源交接。

## 这是什么

输入一个**决策问题** + 公开材料（链接或文本），工具会按固定纪律输出：

1. 决策问题直接回答（能 / 不能 / 最多能写到哪一句）
2. 来源台账（可靠度 A–F）
3. 主张登记（L1–L5，必须写「为什么不是上一级」）
4. 冲突对照
5. 发现与对外表述（**建议表述** + **禁止表述**）
6. 自检清单强制通过

核心纪律：
- 官方口径、单方解释默认上限 **L4**，绝不能直接写成事实句
- 转载/通稿不算独立印证
- 每条主张必须主动考虑降级
- 必须同时给出「可以写」和「绝对不能写」的句子

## 快速使用

### 方式 1：直接复制 System Prompt（最快）

1. 打开 `system_prompt.md`
2. 把完整内容复制到任意支持长上下文的 LLM（Claude、GPT-4o、DeepSeek、通义、Kimi 等）
3. 用户消息格式：

```
决策问题：
[你的封闭式问题，例如：根据目前公开材料，能否对外表述为「……」？若不能，最多能写到哪一句？]

材料：
[粘贴公开材料文本，或列出链接 + 关键摘录]
```

### 方式 2：本地 Gradio 界面

```bash
pip install -r requirements.txt
python app.py
```

浏览器打开后即可使用。支持切换模型 API。

### 方式 3：Hugging Face Spaces

把本仓库直接部署到 Spaces（Gradio SDK），一键公开。

## 文件说明

| 文件 | 用途 |
|------|------|
| `system_prompt.md` | 完整系统提示词（核心） |
| `output_template.md` | 强制输出结构模板 |
| `app.py` | Gradio 简易界面 |
| `requirements.txt` | 依赖 |
| `examples/` | 使用示例（基于原样本） |

## 方法来源

本工具严格复刻原「公开快诊」工作流（样本_01 三菱合资终止案例）。  
等级定义、自检清单、禁止把 L4 升级为事实句等纪律均原样保留。

## 免责声明

- 仅处理**已公开**信息
- 不查人、不碰隐私、不替代律师或公关
- 输出仅供参考，最终对外表述责任由使用者自行承担
- 作者不再接受任何人工委托

## License

MIT

---

发布即退出。欢迎 fork 和改进。
