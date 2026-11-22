# AGENTS.md

本仓库是 [aiinfra.blog《AI Agent 工程师 60 天》课程](https://aiinfra.blog/course/) 的学习记录，按天推进，按周分目录存放练习代码。

## 学习进度

- 当前进度：**D02**（最后更新：2026-11-22）
- 已完成：
  - D00 开学第一课：岗位认知、课程地图、环境搭建（uv、Python 3.12、.env 管密钥）
  - D01 模型直觉：token、上下文窗口、temperature（纯理论，无代码）
  - D02 Python 速成：`w1/repo_stats.py` —— httpx 并发抓取 GitHub 仓库信息 + pydantic 校验；`tests/test_repo_stats.py` —— pytest 单测
- 目录约定：`w<N>/` 放第 N 周的练习代码（当前为 `w1/`），后续周次类推；`common/` 预留放跨周公共代码（如课程后期的 LLMClient）

## 环境与常用命令

- 包管理用 **uv**（`pyproject.toml` + `uv.lock`），Python 3.12
  - 安装依赖：`uv sync`
  - 跑脚本：`uv run python main.py`
- 测试用 **pytest**，在项目根目录运行：
  - `uv run pytest`
  - `pyproject.toml` 已配 `pythonpath = ["."]`，`from w1.repo_stats import ...` 这类导入可直接用
- 密钥管理：复制 `.env.example` 为 `.env` 并填入 `LLM_API_KEY`；`.env` 已被 .gitignore 忽略，**永远不要提交**。`main.py` 是调用 OpenAI 兼容 API 的最小示例，依赖这三个环境变量

## 提交约定

- 每天的学习成果单独一个提交，提交信息以课程天数开头，例如 `D03: 第一次调用大模型 API`
- 跑完测试再提交；不要把 `.env`、`.venv/`、`__pycache__/` 提交进仓库
