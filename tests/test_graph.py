"""
单元测试：LangGraph工作流基础校验
"""
from graph import build_graph

def test_graph_build():
    """测试图能否正常构建编译"""
    graph = build_graph()
    assert graph is not None
    print("✅ 图编译测试通过")

def test_graph_nodes():
    """校验节点注册完整"""
    graph = build_graph()
    graph_obj = graph.get_graph()
    nodes = graph_obj.nodes
    node_names = list(nodes.keys())
    expect_nodes = {
        "planner_node",
        "executor_node",
        "reviewer_node",
        "human_feedback_node",
        "summarizer_node"
    }
    for name in expect_nodes:
        assert name in node_names
    print("✅ 节点完整性测试通过")
