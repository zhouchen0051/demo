"""
LangGraph 工作流图构建
=====================
负责组装所有节点（Node）和边（Edge），定义多智能体的执行流程。

整体流程图：
    Planner(任务拆解) → Executor(执行子任务) → 循环判断
        ↓ 还有子任务
        Executor(继续执行下一个)
        ↓ 全部完成
        Reviewer(审核判断)
        ├─ 需要人工 → HumanFeedback(人工介入) → Summarizer(汇总报告) → END
        └─ 不需要人工 → Summarizer(汇总报告) → END
"""

from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage

from .state import AgentState
from agent import (
    planner_agent_run,
    executor_agent_run,
    reviewer_agent_run,
    summarizer_agent_run,
)


# ==================== 节点函数 ====================

def human_feedback_node(state: AgentState) -> dict:
    """
    人工反馈节点（Human-in-the-Loop）
    --------------------------------
    LangGraph 支持"断点暂停"机制：执行到这里时，图会暂停，
    等待人工输入反馈后再继续执行。
    
    本节点的作用：把人工反馈写入对话历史，供汇总节点使用。
    """
    feedback = state.get("human_feedback") or "无人工反馈，审核通过"
    return {
        "messages": state["messages"] + [
            HumanMessage(content=f"📝 人工审核反馈：{feedback}")
        ]
    }


# ==================== 条件路由函数 ====================

def route_after_executor(state: AgentState) -> str:
    """
    执行器后的条件路由
    ------------------
    判断当前子任务执行完后，下一步去哪里：
    - 如果还有子任务没执行 → 回到 executor_node 继续执行下一个
    - 如果全部子任务执行完 → 进入 reviewer_node 审核
    
    原理：LangGraph 的条件边（Conditional Edge）允许根据状态动态选择下一个节点。
    """
    current_idx = state["current_subtask_idx"]
    total_tasks = len(state["subtasks"])
    
    if current_idx + 1 < total_tasks:
        # 索引 +1，指向下一个子任务
        state["current_subtask_idx"] = current_idx + 1
        return "executor_node"
    else:
        return "reviewer_node"


def route_after_reviewer(state: AgentState) -> str:
    """
    审核后的条件路由
    ----------------
    判断是否需要人工介入：
    - 需要人工审核 → 进入 human_feedback_node
    - 不需要人工 → 直接进入 summarizer_node 生成报告
    """
    if state["require_human_approval"]:
        return "human_feedback_node"
    else:
        return "summarizer_node"


# ==================== 图构建函数 ====================

def build_graph():
    """
    构建并编译 LangGraph 工作流
    ---------------------------
    这是整个项目的核心入口：把所有智能体节点、边、路由组装成一个可执行的图。
    
    返回：编译后的 LangGraph 可调用对象，用 .invoke(初始状态) 运行。
    """
    # 1. 实例化状态图，绑定我们定义的 AgentState
    graph = StateGraph(AgentState)

    # 2. 注册所有节点（节点名 → 节点函数）
    graph.add_node("planner_node", planner_agent_run)
    graph.add_node("executor_node", executor_agent_run)
    graph.add_node("reviewer_node", reviewer_agent_run)
    graph.add_node("human_feedback_node", human_feedback_node)
    graph.add_node("summarizer_node", summarizer_agent_run)

    # 3. 设置入口节点：图从哪里开始执行
    graph.set_entry_point("planner_node")

    # 4. 固定边：A执行完，固定走到B（无条件分支）
    graph.add_edge("planner_node", "executor_node")
    graph.add_edge("human_feedback_node", "summarizer_node")
    graph.add_edge("summarizer_node", END)  # END 是 LangGraph 内置结束标记

    # 5. 条件边：执行器执行完，动态路由（循环执行子任务）
    graph.add_conditional_edges(
        source="executor_node",
        path=route_after_executor,  # 这个函数返回下一个节点的名字
    )

    # 6. 条件边：审核完，判断是否需要人工
    graph.add_conditional_edges(
        source="reviewer_node",
        path=route_after_reviewer,
    )

    # 7. 编译图，得到可运行的工作流实例
    compiled_graph = graph.compile()
    return compiled_graph
