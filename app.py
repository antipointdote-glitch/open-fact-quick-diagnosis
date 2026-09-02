"""
公开快诊 · AI 辅助版
简单 Gradio 界面。把 system_prompt.md 的内容作为系统提示，强制结构化输出。
"""

import gradio as gr
import os
from pathlib import Path

# 读取系统提示词
PROMPT_PATH = Path(__file__).parent / "system_prompt.md"
SYSTEM_PROMPT = PROMPT_PATH.read_text(encoding="utf-8") if PROMPT_PATH.exists() else ""

# 可选：读取输出模板作为提示补充
TEMPLATE_PATH = Path(__file__).parent / "output_template.md"
OUTPUT_TEMPLATE = TEMPLATE_PATH.read_text(encoding="utf-8") if TEMPLATE_PATH.exists() else ""


def build_user_message(decision_question: str, materials: str) -> str:
    return f"""决策问题：
{decision_question.strip()}

材料：
{materials.strip()}

请严格按照系统提示词的工作流和输出模板执行，直接输出完整报告，不要输出思考过程。
"""


def run_diagnosis(decision_question: str, materials: str, api_key: str, base_url: str, model: str):
    if not decision_question.strip():
        return "请填写决策问题。"
    if not materials.strip():
        return "请提供公开材料（文本或链接+摘录）。"

    # 这里使用 OpenAI 兼容接口（支持 DeepSeek、通义、本地 vLLM、Ollama 的 OpenAI 兼容层等）
    try:
        from openai import OpenAI
    except ImportError:
        return "请先安装依赖：pip install openai"

    client = OpenAI(
        api_key=api_key or os.getenv("OPENAI_API_KEY", "sk-xxx"),
        base_url=base_url or os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"),
    )

    user_content = build_user_message(decision_question, materials)

    try:
        response = client.chat.completions.create(
            model=model or "gpt-4o",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_content},
            ],
            temperature=0.2,
            max_tokens=8192,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"调用失败：{str(e)}\n\n请检查 API Key、Base URL 和模型名称是否正确。"


# Gradio 界面
with gr.Blocks(title="公开快诊 · AI 辅助版", theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    # 公开快诊 · AI 辅助版
    
    把「已经能确认的事实」和「还只能算某方说法」严格分开，并明确对外能写到哪一句、哪句不能写。
    
    **使用方法：** 填写决策问题 + 粘贴公开材料 → 点击运行。  
    支持任何 OpenAI 兼容 API（DeepSeek、通义、月之暗面、本地 Ollama 等）。
    """)

    with gr.Row():
        with gr.Column(scale=1):
            decision = gr.Textbox(
                label="决策问题（封闭式）",
                placeholder="根据目前公开材料，能否对外表述为「……」？若不能，最多能写到哪一句？",
                lines=3,
            )
            materials = gr.Textbox(
                label="公开材料（文本 / 链接 + 关键摘录）",
                placeholder="粘贴官方公告全文、新闻报道、工商信息等……",
                lines=12,
            )

            with gr.Accordion("模型设置（可选）", open=False):
                api_key = gr.Textbox(label="API Key", type="password", placeholder="sk-...")
                base_url = gr.Textbox(label="Base URL", placeholder="https://api.deepseek.com/v1 或留空用默认")
                model = gr.Textbox(label="模型名称", value="deepseek-chat", placeholder="deepseek-chat / gpt-4o / qwen-max 等")

            btn = gr.Button("运行公开快诊", variant="primary")

        with gr.Column(scale=1):
            output = gr.Markdown(label="报告输出")

    btn.click(
        fn=run_diagnosis,
        inputs=[decision, materials, api_key, base_url, model],
        outputs=output,
    )

    gr.Markdown("""
    ---
    **纪律提醒：**  
    - 官方口径默认上限 L4，绝不能直接写成事实句  
    - 必须同时给出「建议对外表述」和「禁止对外表述」  
    - 至少一条主张主动降到 L3 或更低  
    
    作者已退出人工服务。本工具开源，欢迎 fork。
    """)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
