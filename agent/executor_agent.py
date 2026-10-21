"""
Executor Agent —— 任务执行智能体
===============================
职责：读取当前子任务，调用工具（搜索、文档读取等）执行任务，返回结果。

类比：就像一个执行员工，接到具体任务后，用各种工具把活干完，交回成果。
"""

from langchain_core.messages import AIMessage

from graph.state import AgentState
from tools import web_search


def executor_agent_run(state: AgentState) -> dict:
    """
    执行器节点运行函数
    ------------------
    输入：当前全局状态（读取 subtasks、current_subtask_idx）
    输出：更新后的状态（写入 subtask_results、tool_logs、messages）
    
    工作流程：
    1. 取出当前要执行的子任务
    2. 判断任务类型，调用对应的工具
    3. 把工具返回结果整理成可读的文本
    4. 追加到 subtask_results 列表
    """
    idx = state["current_subtask_idx"]
    subtask = state["subtasks"][idx]
    task_desc = subtask["task"]

    # ========== 模拟执行子任务（Demo 阶段） ==========
    # 正式项目：根据子任务类型，调用不同工具
    # 例如：
    # if "搜集" in task_desc or "搜索" in task_desc:
    #     result = web_search(task_desc)
    # elif "读取" in task_desc or "文档" in task_desc:
    #     result = read_doc(task_desc)
    # else:
    #     result = llm.invoke(task_desc)
    
    # 模拟工具调用
    search_result = web_search(task_desc)
    result = f"【子任务 {subtask['id']} 执行结果】\n{search_result}\n✓ 已完成"
    # ================================================

    # 更新子任务状态
    new_subtasks = state["subtasks"].copy()
    new_subtasks[idx]["status"] = "completed"

    # 追加执行结果
    new_results = state["subtask_results"].copy()
    new_results.append(result)

    # 记录工具日志
    new_logs = state["tool_logs"].copy()
    new_logs.append({
        "task_id": subtask["id"],
        "task_desc": task_desc,
        "tool_used": "web_search",
        "status": "success"
    })

    return {
        "subtasks": new_subtasks,
        "subtask_results": new_results,
        "tool_logs": new_logs,
        "messages": state["messages"] + [
            AIMessage(content=f"⚡ Executor：{task_desc[:30]}... 完成")
        ],
    }
