# 🤖 Multi-Agent Task Workbench

基于 **LangGraph** 的多智能体任务执行系统，演示任务规划 → 子任务执行 → 人工审核 → 报告汇总的完整工作流。

---

## 📖 项目简介

本项目是一个**多智能体协作框架**的教学/演示项目，展示如何用 LangGraph 构建一个包含多个角色的 AI 工作流：

- **Planner（规划者）**：把用户的复杂问题拆解成多个子任务
- **Executor（执行者）**：逐个执行子任务，调用工具获取信息
- **Reviewer（审核者）**：检查结果，判断是否需要人工介入
- **Human Feedback（人工反馈）**：支持 Human-in-the-Loop，人可以介入审核修改
- **Summarizer（汇总者）**：把所有结果整合成最终报告

---

## 🏗️ 系统架构

```
┌─────────────┐
│  用户输入    │
└──────┬──────┘
       ▼
┌─────────────┐
│   Planner    │  ← 任务拆解
│  (规划Agent) │
└──────┬──────┘
       ▼
┌─────────────┐
│   Executor   │◄──────────┐
│  (执行Agent) │           │ 循环执行
└──────┬──────┘           │
       │                   │
       ▼ 还有子任务？       │
   ┌───┴───┐ 是            │
   │  是    │───────────────┘
   └───┬───┘
       │ 否
       ▼
┌─────────────┐
│   Reviewer   │  ← 质量审核
│  (审核Agent) │
└──────┬──────┘
       ▼ 需要人工？
   ┌───┴───┐
   │  是    │     否
   └───┬───┘     │
       │         ▼
       │   ┌─────────────┐
       │   │ Summarizer   │
       │   │ (汇总Agent)  │
       │   └──────┬──────┘
       ▼          │
┌─────────────┐   │
│ Human Feedback│  │
│  (人工介入)   │   │
└──────┬──────┘   │
       └──────────┘
              ▼
        ┌───────────┐
        │ 最终报告   │
        └───────────┘
```

---

## 📁 项目结构

```
demo/
├── graph/                  # LangGraph 图定义与全局状态
│   ├── __init__.py
│   ├── state.py            # 全局状态 AgentState 定义
│   └── workflow.py         # 图构建、节点、条件路由
├── agent/                  # 各个智能体
│   ├── __init__.py
│   ├── planner_agent.py    # 规划者：任务拆解
│   ├── executor_agent.py   # 执行者：调用工具执行任务
│   ├── reviewer_agent.py   # 审核者：判断是否人工介入
│   └── summarizer_agent.py # 汇总者：生成最终报告
├── tools/                  # 外部工具
│   ├── __init__.py
│   ├── search_tool.py      # 网络搜索工具
│   └── doc_reader.py       # 本地文档读取工具
├── data/                   # 数据文件目录
├── evals/                  # 评测脚本
│   └── eval_runner.py
├── main.py                 # 命令行入口
├── app.py                  # Gradio Web 界面入口
├── requirements.txt        # Python 依赖
├── Dockerfile              # 容器化部署配置
├── .gitignore              # Git 忽略规则
└── README.md               # 项目说明
```

---

## 🚀 快速开始

### 环境要求
- Python 3.10 ~ 3.12（推荐 3.12，兼容性最好）
- pip 包管理器

### 1. 克隆项目
```bash
git clone https://github.com/zhouchen0051/demo.git
cd demo
```

### 2. 创建虚拟环境（推荐）
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. 安装依赖
```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 4. 配置 API Key（可选，正式接入 LLM 时需要）
在项目根目录创建 `.env` 文件：
```env
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxx
# TAVILY_API_KEY=tvly-xxxxxxxxxxxx  # 搜索工具用
```

### 5. 运行

#### 方式一：命令行运行
```bash
python main.py
```

#### 方式二：启动 Web 界面
```bash
python app.py
```
然后浏览器打开：http://127.0.0.1:7860

---

## 🧠 核心概念说明

### 1. State（全局状态）
整个多智能体系统共享一个状态字典（`AgentState`），所有节点都读写这个状态。
- 优点：信息传递清晰，可追踪每一步变化
- 类似：浏览器里的 URL 参数 / 全局变量

### 2. Node（节点）
每个 Agent 就是一个节点函数，接收状态、返回状态更新。
```python
def planner_node(state: AgentState) -> dict:
    # 读 state → 处理 → 返回要更新的字段
    return {"subtasks": [...]}
```

### 3. Edge（边）
定义节点之间的连接关系：
- **固定边**：A 执行完一定去 B（`add_edge`）
- **条件边**：根据状态动态选择下一个节点（`add_conditional_edges`）

### 4. Human-in-the-Loop（人工介入）
LangGraph 支持在工作流中间暂停，等待人工审核输入后再继续。
这是实际生产中非常重要的能力：**AI 出草稿，人来把关**。

---

## 🔧 后续扩展方向

- [ ] 接入真实 LLM（OpenAI / 通义千问 / DeepSeek）替换硬编码
- [ ] 接入真实搜索 API（Tavily / SerpAPI）
- [ ] 增加更多工具：代码执行、数据库查询、API 调用
- [ ] 增加记忆模块：跨会话记住用户偏好
- [ ] 增加多智能体协作模式：辩论、投票、互评
- [ ] 增加流式输出：实时显示执行进度
- [ ] 增加数据库：保存历史任务记录

---

## 📝 技术栈

| 技术 | 用途 |
|------|------|
| LangGraph | 多智能体工作流编排 |
| LangChain | LLM 调用与提示词管理 |
| Gradio | Web 可视化界面 |
| Python 3.12 | 开发语言 |

---

## 📄 License

MIT License
