"""
评测脚本
========
批量运行测试用例，评估多智能体系统的输出质量。

正式项目可以扩展：
- 人工评分：人工打分报告质量
- 自动评分：用 LLM-as-Judge 自动评估
- 回归测试：每次代码改动后跑一遍，防止功能退化
"""

from graph import build_graph


# 测试用例集（正式项目可以存成 JSON/CSV 文件）
TEST_CASES = [
    {
        "id": 1,
        "question": "帮我调研 Python 和 JavaScript 的优缺点对比",
        "expected_keywords": ["Python", "JavaScript", "优点", "缺点"]
    },
    {
        "id": 2,
        "question": "写一个关于时间管理的学习计划",
        "expected_keywords": ["时间管理", "计划", "步骤"]
    },
    {
        "id": 3,
        "question": "介绍一下机器学习的基本概念",
        "expected_keywords": ["机器学习", "概念", "算法"]
    },
]


def run_single_test(test_case: dict) -> dict:
    """
    运行单个测试用例
    """
    graph = build_graph()
    init_state = {
        "user_query": test_case["question"],
        "subtasks": [],
        "current_subtask_idx": 0,
        "messages": [],
        "subtask_results": [],
        "require_human_approval": False,
        "human_feedback": None,
        "final_report": "",
        "tool_logs": [],
    }

    result = graph.invoke(init_state)

    # 简单自动检查：报告中是否包含预期关键词
    report = result["final_report"]
    found_keywords = [kw for kw in test_case["expected_keywords"] if kw in report]
    coverage = len(found_keywords) / len(test_case["expected_keywords"])

    return {
        "test_id": test_case["id"],
        "question": test_case["question"],
        "status": "passed" if coverage >= 0.5 else "failed",
        "keyword_coverage": f"{coverage:.0%}",
        "report_length": len(report)
    }


def run_all_tests():
    """
    运行全部测试用例，输出汇总报告
    """
    print("=" * 60)
    print("🧪 开始运行评测测试...")
    print("=" * 60)

    results = []
    for case in TEST_CASES:
        print(f"\n运行测试 #{case['id']}: {case['question'][:30]}...")
        res = run_single_test(case)
        results.append(res)
        print(f"  状态：{res['status']}，关键词覆盖：{res['keyword_coverage']}")

    # 汇总
    passed = sum(1 for r in results if r["status"] == "passed")
    total = len(results)

    print("\n" + "=" * 60)
    print(f"📊 评测汇总：{passed}/{total} 通过")
    print("=" * 60)

    return results


if __name__ == "__main__":
    run_all_tests()
