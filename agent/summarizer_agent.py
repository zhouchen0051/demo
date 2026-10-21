"""
Summarizer Agent —— 汇总智能体
==============================
职责：收集所有子任务的执行结果，整合生成最终的 Markdown 报告。
同时如果有人工反馈，会把人工意见融入报告。

类比：就像一个写报告的秘书，把各个员工交上来的材料整理成一份完整报告。
"""

from langchain_core.messages import AIMessage

from graph.state import AgentState


def summarizer_agent_run(state: AgentState) -> dict:
    """
    汇总节点运行函数
    ----------------
    输入：当前全局状态（读取 subtask_results、human_feedback、user_query）
    输出：更新后的状态（写入 final_report）
    
    工作流程：
    1. 收集所有子任务的执行结果
    2. 拼接成结构化的 Markdown 报告
    3. 如果有人工反馈，追加到报告末尾
    4. 正式项目可以用 LLM 做更流畅的润色
    """
    user_query = state["user_query"]
    results = state["subtask_results"]
    feedback = state.get("human_feedback")

    # ========== 拼接 Markdown 报告 ==========
    report = f"# 📋 多智能体任务报告\n\n"
    report += f"**原始问题**：{user_query}\n\n"
    report += "---\n\n"
    report += "## 📊 子任务执行结果\n\n"

    for i, res in enumerate(results, 1):
        report += f"### 第 {i} 部分\n\n{res}\n\n"

    report += "---\n\n"

    # 如果有人工反馈，追加审核意见
    if feedback and feedback != "无人工反馈，直接通过":
        report += "## ✍️ 人工审核意见\n\n"
        report += f"> {feedback}\n\n"

    report += "---\n\n"
    report += "*由 Multi-Agent Task Workbench 自动生成*\n"
    # =======================================

    return {
        "final_report": report,
        "messages": state["messages"] + [
            AIMessage(content="✅ Summarizer：最终报告已生成完毕")
        ],
    }
