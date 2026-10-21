"""
LangGraph 全局状态定义
====================
定义整个多智能体工作流中所有节点共享的状态结构。
LangGraph 的核心思想：状态在节点之间流转，每个节点读取状态、处理逻辑、返回状态更新。
"""

from typing import TypedDict, List, Optional
from langchain_core.messages import BaseMessage


class AgentState(TypedDict):
    """
    全局状态（AgentState）
    --------------------
    这是整个多智能体系统的"共享内存"，所有节点都可以读写。
    
    字段说明：
    - user_query: 用户原始输入问题
    - subtasks: 规划器拆解出的子任务列表
    - current_subtask_idx: 当前正在执行的子任务索引
    - messages: 对话历史消息列表（LLM 用）
    - subtask_results: 各子任务的执行结果
    - require_human_approval: 是否需要人工审核
    - human_feedback: 人工反馈内容
    - final_report: 最终汇总报告
    - tool_logs: 工具调用日志
    """
    # 用户原始提问
    user_query: str
    
    # 子任务列表，格式：[{"id": 1, "task": "任务描述", "status": "pending"}]
    subtasks: List[dict]
    
    # 当前正在执行的子任务索引（从0开始）
    current_subtask_idx: int
    
    # LLM 对话历史消息
    messages: List[BaseMessage]
    
    # 各子任务执行结果，按顺序存储
    subtask_results: List[str]
    
    # 人工审核开关：True = 暂停等待人工反馈
    require_human_approval: bool
    
    # 人工反馈内容（审核者输入的修改意见）
    human_feedback: Optional[str]
    
    # 最终生成的 Markdown 报告
    final_report: str
    
    # 工具调用日志（用于调试和追踪）
    tool_logs: List[dict]
