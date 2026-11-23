# 学习进度

本文件记录《AI Agent 工程师 60 天》课程的学习进度，由 `AGENTS.md` 的提交约定引用：每天提交前更新此处（更新当天条目即可，按需读取，不必整段历史都过一遍）。

- 当前进度：**D03**（最后更新：2026-11-23）
- 已完成：
  - D00 开学第一课：岗位认知、课程地图、环境搭建（uv、Python 3.12、.env 管密钥）
  - D01 模型直觉：token、上下文窗口、temperature（纯理论，无代码）
  - D02 Python 速成：`w1/repo_stats.py` —— httpx 并发抓取 GitHub 仓库信息 + pydantic 校验；`tests/test_repo_stats.py` —— pytest 单测
  - D03 第一次调用大模型 API：`w1/ask.py` —— 命令行问答脚本，argparse 解析参数 + dotenv 加载环境 + OpenAI SDK 调用兼容 API（重试、超时、异常分类处理），打印 token 用量与花费估算

## 目录约定

- `w<N>/` 放第 N 周的练习代码（当前为 `w1/`），后续周次类推
- `common/` 预留放跨周公共代码（如课程后期的 LLMClient）
