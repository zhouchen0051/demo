"""
搜索工具模块
============
封装外部搜索 API（如 Tavily、SerpAPI、Google Search），供 Executor Agent 调用。

正式项目推荐使用：
- Tavily Search：专门为 LLM Agent 设计的搜索 API
- SerpAPI：Google 搜索结果 API
- Bing Search API：微软官方搜索服务
"""

import os
from typing import List, Dict


def web_search(query: str, max_results: int = 3) -> str:
    """
    网络搜索工具
    ------------
    输入：搜索关键词 query
    输出：格式化的搜索结果文本
    
    正式项目接入示例（Tavily）：
    ----------
    import tavily
    
    tavily_api_key = os.getenv("TAVILY_API_KEY")
    client = tavily.TavilyClient(api_key=tavily_api_key)
    response = client.search(query=query, max_results=max_results)
    
    results_text = ""
    for i, result in enumerate(response["results"], 1):
        results_text += f"{i}. {result['title']}\n"
        results_text += f"   {result['content'][:200]}...\n\n"
    return results_text
    ----------
    """
    # Demo 阶段：返回模拟搜索结果
    # 正式项目替换为真实 API 调用
    
    mock_results = [
        {
            "title": f"关于「{query[:20]}」的最新资料 1",
            "content": f"这是搜索结果1的摘要内容，介绍了 {query} 的基本概念、发展现状和主要应用场景。"
        },
        {
            "title": f"关于「{query[:20]}」的技术对比 2",
            "content": f"这是搜索结果2的摘要内容，对比了不同方案的优缺点、性能指标和适用场景。"
        },
        {
            "title": f"关于「{query[:20]}」的行业报告 3",
            "content": f"这是搜索结果3的摘要内容，包含了最新的市场数据、趋势预测和案例分析。"
        },
    ]

    # 格式化输出
    output = f"🔍 搜索关键词：{query}\n\n"
    for i, r in enumerate(mock_results[:max_results], 1):
        output += f"**{i}. {r['title']}**\n"
        output += f"{r['content']}\n\n"

    return output
