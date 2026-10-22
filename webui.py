import gradio as gr
from graph import build_graph

agent_graph = build_graph()

def chat_response(user_msg, chat_md):
    if not user_msg.strip():
        return chat_md, ""
    
    print(f"\n[WebUI] 收到用户输入：{user_msg}")
    init_state = {
        "user_query": user_msg,
        "subtasks": [],
        "current_subtask_idx": 0,
        "messages": [],
        "subtask_results": [],
        "require_human_approval": False,
        "human_feedback": None,
        "final_report": "",
        "tool_logs": [],
    }
    print("[WebUI] 开始调用LangGraph工作流...")
    result = agent_graph.invoke(init_state)
    print("[WebUI] 工作流执行完成")
    final_text = result.get("final_report", "工作流执行完成，暂无总结输出")
    print(f"[WebUI] 返回结果：{final_text}")

    # markdown拼接对话
    new_block = chat_md
    new_block += f"\n**👤 用户：**\n{user_msg}\n\n**🤖 Agent：**\n{final_text}\n\n---\n"
    return new_block, ""


with gr.Blocks(title="LangGraph 多智能体工作台") as demo:
    gr.Markdown("# 🤖 LangGraph 多智能体 Agent 工作台")
    gr.Markdown("规划-执行-评审-总结 闭环工作流，本地Web交互")

    chat_display = gr.Markdown(value="", elem_id="chat-area")
    msg = gr.Textbox(
        placeholder="输入任务，点击发送提交；Shift+Enter换行",
        lines=2,
        label="输入"
    )
    with gr.Row():
        submit_btn = gr.Button("发送", variant="primary")
        clear = gr.Button("清空对话")

    submit_btn.click(chat_response, inputs=[msg, chat_display], outputs=[chat_display, msg])
    msg.submit(chat_response, inputs=[msg, chat_display], outputs=[chat_display, msg])
    clear.click(lambda: ("", ""), None, outputs=[chat_display, msg])

if __name__ == "__main__":
    demo.launch(server_name="127.0.0.1", server_port=7861, inbrowser=True)
