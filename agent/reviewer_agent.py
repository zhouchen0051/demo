"""
Reviewer Agent —— 审核智能体
=============================
职责：检查所有子任务的执行结果，判断是否需要人工介入审核。

类比：就像一个质检主管，活都干完了，先自己检查一遍。
如果是重要任务，就交给人再看一遍；不重要就直接交付。
"""

from graph.state import AgentState


def reviewer_agent_run(state: AgentState) -> dict:
    """
    审核节点运行函数
    ----------------
    输入：当前全局状态（读取 subtasks、subtask_results）
    输出：更新后的状态（写入 require_human_approval）
    
    审核逻辑（Demo 简化版）：
    - 所有子任务都完成后，触发人工审核开关
    - 正式项目可以更精细：比如检测到结果质量低、或者涉及敏感话题时才需要人工
    """
    total_tasks = len(state["subtasks"])
    completed_tasks = sum(1 for t in state["subtasks"] if t.get("status") == "completed")

    # 业务规则示例：
    # 1. 所有子任务都执行完 → 需要人工审核
    # 2. 如果用户问题里包含"重要""正式""汇报"等关键词 → 必须人工审核
    # 3. 如果执行过程中有工具调用失败 → 需要人工介入
    
    all_done = completed_tasks >= total_tasks
    
    # Demo：全部完成后就需要人工审核（演示 Human-in-the-Loop 效果）
    require_approval = all_done

    return {
        "require_human_approval": require_approval,
    }
