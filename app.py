"""
Gradio Web 界面
===============
启动一个本地网页，可视化输入问题、查看执行过程和最终报告。

使用方式：
    python app.py
    然后浏览器打开终端里显示的本地地址（通常是 http://127.0.0.1:7860）
"""

import gradio as gr

from graph import build_graph


# 初始状态模板
INITIAL_STATE = {
    "user_query": "",
    "subtasks": [],
    "current_subtask_idx": 0,
    "messages": [],
    "subtask_results": [],
    "require_human_approval": False,
    "human_feedback": None,
    "final_report": "",
    "tool_logs": [],
}


def process_question(question: str, feedback: str = "") -> tuple:
    """
    Gradio 回调函数：接收用户输入，运行工作流，返回结果
    """
    if not question.strip():
        return "请输入问题", "", ""

    # 构建并运行图
    graph = build_graph()
    init_state = INITIAL_STATE.copy()
    init_state["user_query"] = question
    if feedback.strip():
        init_state["human_feedback"] = feedback

    result = graph.invoke(init_state)

    # 整理执行过程日志
    process_log = "### 📝 执行过程\n\n"
    for msg in result["messages"]:
        process_log += f"- {msg.content}\n"

    # 整理子任务列表
    subtasks_info = "### 📋 子任务拆解\n\n"
    for st in result["subtasks"]:
        status_icon = "✅" if st["status"] == "completed" else "⏳"
        subtasks_info += f"{status_icon} **任务{st['id']}**：{st['task']}\n\n"

    return result["final_report"], process_log, subtasks_info


# ==================== 构建 Gradio 界面 ====================
with gr.Blocks(title="Multi-Agent Task Workbench") as demo:
    gr.Markdown("# 🤖 Multi-Agent Task Workbench")
    gr.Markdown("基于 LangGraph 的多智能体任务执行系统")

    with gr.Row():
        with gr.Column(scale=1):
            question_input = gr.Textbox(
                label="💬 你的问题",
                placeholder="例如：帮我调研 2025 年主流大模型 Agent 框架对比...",
                lines=3
            )
            feedback_input = gr.Textbox(
                label="✍️ 人工审核反馈（可选）",
                placeholder="如果有修改意见，在这里输入...",
                lines=2
            )
            submit_btn = gr.Button("🚀 开始执行", variant="primary")

            subtasks_output = gr.Markdown()

        with gr.Column(scale=1):
            process_output = gr.Markdown()
            report_output = gr.Markdown(label="📄 最终报告")

    submit_btn.click(
        fn=process_question,
        inputs=[question_input, feedback_input],
        outputs=[report_output, process_output, subtasks_output]
    )


if __name__ == "__main__":
    # 启动 Web 服务
    demo.launch(
        server_name="127.0.0.1",
        server_port=7860,
        share=False  # 设为 True 可以生成公网临时链接
    )
