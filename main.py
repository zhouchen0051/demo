"""
项目主入口（命令行模式）
========================
直接运行此文件，启动多智能体工作流，在终端输出结果。

使用方式：
    python main.py
"""

from graph import build_graph


# 初始状态的默认值（所有字段都要初始化，TypedDict 要求完整）
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


def run_workflow(user_query: str, human_feedback: str = None) -> dict:
    """
    运行完整的多智能体工作流
    ------------------------
    输入：
        user_query: 用户问题
        human_feedback: 人工反馈（可选，演示用）
    输出：最终状态字典，包含 final_report 等
    """
    # 构建图
    graph = build_graph()

    # 初始化状态
    init_state = INITIAL_STATE.copy()
    init_state["user_query"] = user_query

    # 如果有预填的人工反馈，直接写入状态（Demo 简化演示）
    # 正式项目中，人工反馈是在执行到 human_feedback_node 时交互式输入的
    if human_feedback:
        init_state["human_feedback"] = human_feedback

    # 执行工作流
    print("🚀 多智能体工作流启动...\n")
    result = graph.invoke(init_state)

    # 打印过程日志
    print("=" * 60)
    print("📝 执行过程：")
    for msg in result["messages"]:
        print(f"  {msg.content}")
    print()

    return result


def main():
    """命令行主函数"""
    # 示例用户问题
    demo_question = "帮我调研 2025 年主流大模型 Agent 框架的对比，输出技术选型建议"

    print("=" * 60)
    print("🤖 Multi-Agent Task Workbench")
    print("=" * 60)
    print(f"\n💬 输入问题：{demo_question}\n")

    # 运行工作流（演示用：预填人工反馈）
    result = run_workflow(
        user_query=demo_question,
        human_feedback="报告整体不错，补充一下成本对比部分。"
    )

    # 输出最终报告
    print("=" * 60)
    print("📄 最终报告：")
    print("=" * 60)
    print(result["final_report"])

    # 打印工具日志
    print("\n" + "=" * 60)
    print("🔧 工具调用日志：")
    for log in result["tool_logs"]:
        print(f"  - 任务{log['task_id']}：调用 {log['tool_used']} → {log['status']}")


if __name__ == "__main__":
    main()
