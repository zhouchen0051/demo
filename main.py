"""
项目主入口（命令行模式）
========================
直接运行此文件，启动多智能体工作流，在终端输出结果。
使用方式：
    python main.py
"""
from graph import build_graph
from config import settings
from utils.logger import logger


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
    """
    logger.info("🚀 多智能体工作流启动")
    logger.info(f"📝 用户问题: {user_query}")
    
    # 构建图
    graph = build_graph()
    
    # 初始化状态
    init_state = INITIAL_STATE.copy()
    init_state["user_query"] = user_query
    
    if human_feedback:
        init_state["human_feedback"] = human_feedback
    
    # 执行工作流（递归限制从配置读取）
    result = graph.invoke(
        init_state, 
        config={"recursion_limit": settings.RECURSION_LIMIT}
    )
    
    logger.info("✅ 工作流执行完成")
    return result


def main():
    """命令行主函数"""
    logger.info("=" * 60)
    logger.info("🤖 Multi-Agent Task Workbench")
    logger.info("=" * 60)
    
    # 示例用户问题
    demo_question = "帮我调研 2025 年主流大模型 Agent 框架的对比，输出技术选型建议"
    
    # 运行工作流
    result = run_workflow(
        user_query=demo_question,
        human_feedback="报告整体不错，补充一下成本对比部分。"
    )
    
    # 输出最终报告
    print("\n" + "=" * 60)
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
