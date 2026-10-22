"""
Executor Agent —— 任务执行智能体
===============================
职责：读取当前子任务，调用工具（搜索、文档读取、计算器等）执行任务，返回结果。
类比：就像一个执行员工，接到具体任务后，用各种工具把活干完，交回成果。
"""
from langchain_core.messages import AIMessage
from graph.state import AgentState
# 导入全部三个工具
from tools import web_search, read_local_doc, calculator
def executor_agent_run(state: AgentState) -> dict:
    idx = state["current_subtask_idx"]
    subtasks = state["subtasks"]
    # 新增打印，看清楚每一步进来的时候是什么
    print(f"==== Executor进入 ==== idx={idx}, subtasks列表={subtasks}")

    # ========== 新增边界保护：索引越界直接返回 ==========
    if idx >= len(subtasks):
        print(f"==== 越界保护触发 idx={idx}, len={len(subtasks)}，直接退出")
        return {
            "subtasks": state["subtasks"],
            "subtask_results": state["subtask_results"],
            "tool_logs": state["tool_logs"],
            "current_subtask_idx": idx,
            "messages": state["messages"]
        }
    # ==========================================================

    subtask = subtasks[idx]
    task_desc = subtask["task"]
    ... # 剩下原有代码不动

    # -------------------------- 工具自动判断分支（新增） --------------------------
    if any(keyword in task_desc for keyword in ["计算", "算出", "等于", "公式"]):
        tool_name = "calculator"
        tool_input = task_desc
        tool_result = calculator(tool_input)
    elif any(keyword in task_desc for keyword in ["读取文档", "打开文件", "doc", "pdf", "txt"]):
        tool_name = "read_local_doc"
        tool_input = task_desc
        tool_result = read_local_doc(tool_input)
    else:
        # 默认走搜索
        tool_name = "web_search"
        tool_input = task_desc
        tool_result = web_search(tool_input)
    # -----------------------------------------------------------------------------
    result = f"【子任务 {subtask['id']} 执行结果】\n{tool_result}\n✓ 已完成"
    # 更新子任务状态（原有逻辑不变）
    new_subtasks = subtasks.copy()
    new_subtasks[idx]["status"] = "completed"
    # 追加执行结果
    new_results = state["subtask_results"].copy()
    new_results.append(result)
    # 记录工具日志（自动记录当前使用的工具名称）
    new_logs = state["tool_logs"].copy()
    new_logs.append({
    "task_id": subtask["id"],
    "task_desc": task_desc,
    "tool_used": tool_name,
    "status": "success"
})
    return {
        "subtasks": new_subtasks,
        "subtask_results": new_results,
        "tool_logs": new_logs,
        "task_results": new_results,
        "current_subtask_idx": state["current_subtask_idx"] + 1,
        "messages": state["messages"] + [
            AIMessage(content=f"⚡ Executor：{task_desc[:30]}... 完成")
        ],
    }

