"""
Planner Agent —— 任务规划智能体
==============================
职责：接收用户的复杂问题，调用 LLM 把大任务拆解成多个可执行的子任务。
类比：就像一个项目经理，接到需求后先列任务清单，再分给下属去做。
"""
import re
from langchain_core.messages import AIMessage
from graph.state import AgentState

# ==================== Prompt 模板（正式项目用） ====================
PLANNER_SYSTEM_PROMPT = """你是一个专业的任务规划专家。
你的职责是把用户的复杂问题拆解成 3-5 个可执行的子任务。
要求：
1. 每个子任务目标明确、可独立执行
2. 子任务之间有逻辑顺序，前一个的输出是后一个的输入
3. 输出格式为 JSON 列表，每个元素包含 id 和 task 字段
示例输出：
[
  {"id": 1, "task": "分析用户需求，明确调研目标"},
  {"id": 2, "task": "搜集相关资料和数据"},
  {"id": 3, "task": "整理分析，生成对比表格"},
  {"id": 4, "task": "撰写最终报告"}
]
"""

def planner_agent_run(state: AgentState) -> dict:
    user_query = state["user_query"]
    # ========= 新增调试打印 =========
    calc_keywords = ["计算", "算出", "等于", "算一下", "相加", "相乘", "求和", "求积"]
    has_math_expr = re.search(r"\d+\s*[\+\-\*\/×÷]\s*\d+", user_query) is not None
    is_calc_task = any(k in user_query for k in calc_keywords) and has_math_expr
    

    # =================================

    if is_calc_task:
        subtasks = [
            {
                "id": 1,
                "task": f"使用计算器完成数学计算：{user_query}",
                "status": "pending"
            }
        ]
    else:
        subtasks = [
            {
                "id": 1,
                "task": f"第一步：需求分析 —— 理解「{user_query}」的核心目标和关键维度",
                "status": "pending"
            },
            {
                "id": 2,
                "task": "第二步：资料搜集 —— 搜集相关技术资料、行业数据、对比信息",
                "status": "pending"
            },
            {
                "id": 3,
                "task": "第三步：分析整理 —— 对搜集到的资料进行归纳、对比、总结",
                "status": "pending"
            },
            {
                "id": 4,
                "task": "第四步：报告生成 —— 输出结构化 Markdown 报告",
                "status": "pending"
            },
        ]

    # ========================================================================================

    # ========================================================
    # 下面这一大段是正式项目的LLM调用代码，原样保留，不受分流影响
    # from langchain_openai import ChatOpenAI
    # from langchain_core.prompts import ChatPromptTemplate
    # llm = ChatOpenAI(model="gpt-4o")
    # prompt = ChatPromptTemplate.from_messages([
    #     ("system", PLANNER_SYSTEM_PROMPT),
    #     ("human", "{query}")
    # ])
    # chain = prompt | llm
    # result = chain.invoke({"query": user_query})
    # subtasks = parse_json(result.content)  # 解析LLM输出
    # ========================================================
    return {
        "subtasks": subtasks,
        "current_subtask_idx": 0,  # 从第0个（第一个）子任务开始
        "messages": state["messages"] + [
            AIMessage(content=f"✅ Planner：已将任务拆解为 {len(subtasks)} 个子任务，开始执行")
        ],
    }
