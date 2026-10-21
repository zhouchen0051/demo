"""
Planner Agent —— 任务规划智能体
==============================
职责：接收用户的复杂问题，调用 LLM 把大任务拆解成多个可执行的子任务。

类比：就像一个项目经理，接到需求后先列任务清单，再分给下属去做。
"""

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
    """
    规划器节点运行函数
    ------------------
    输入：当前全局状态（读取 user_query）
    输出：更新后的状态（写入 subtasks、current_subtask_idx、messages）
    
    正式项目：这里替换为 LLM 调用
    - 用 ChatPromptTemplate 组合系统 Prompt + 用户问题
    - 调用 llm.invoke() 获取拆解结果
    - 解析 JSON，得到结构化子任务列表
    """
    user_query = state["user_query"]

    # ========== 模拟子任务拆解（Demo 阶段用硬编码） ==========
    # 正式项目替换为：
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
    # ========================================================

    return {
        "subtasks": subtasks,
        "current_subtask_idx": 0,  # 从第0个（第一个）子任务开始
        "messages": state["messages"] + [
            AIMessage(content=f"✅ Planner：已将任务拆解为 {len(subtasks)} 个子任务，开始执行")
        ],
    }
