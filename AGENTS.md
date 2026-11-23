# AGENTS.md

本仓库是 [aiinfra.blog《AI Agent 工程师 60 天》课程](https://aiinfra.blog/course/) 的学习记录，按天推进，按周分目录存放练习代码。

## 学习进度

记录在 [`PROGRESS.md`](PROGRESS.md)，不放在本文件里，避免它随课程推进不断膨胀、每次会话都被整段加载。需要更新或查看进度时再去读它。

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
- **提交前必须更新 `PROGRESS.md` 的学习进度**：当前进度与最后更新日期改成当天，并在「已完成」列表补记当天条目
- 跑完测试再提交；不要把 `.env`、`.venv/`、`__pycache__/` 提交进仓库
