"""
Summarizer Agent —— 报告汇总智能体
=================================
职责：收集全部子任务结果，合并、排版，生成最终Markdown结构化报告
类比：文档编辑，把所有人交付的成果整理成一份干净完整报告
"""
from langchain_core.messages import AIMessage
from graph.state import AgentState

def summarizer_agent_run(state: AgentState) -> dict:
    """
    汇总节点：动态遍历所有子任务结果，自动渲染，有多少条就输出多少块
    """
    user_query = state["user_query"]
    subtask_results = state["subtask_results"]

    content_blocks = []
    for idx, res in enumerate(subtask_results):
        block = f"""第 {idx+1} 部分
{res}
"""
        content_blocks.append(block)
    
    all_blocks_text = "\n".join(content_blocks)

    final_report = f"""📋 多智能体任务报告
原始问题：{user_query}
📊 子任务执行结果
{all_blocks_text}
由 Multi-Agent Task Workbench 自动生成"""

    return {
        "final_report": final_report,
        "messages": state["messages"] + [
            AIMessage(content=f"✅ Summarizer：报告汇总完成，共 {len(subtask_results)} 条子任务结果")
        ]
    }
