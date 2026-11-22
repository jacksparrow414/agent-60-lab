# agent-60-lab/w1/repo_stats.py
import asyncio
import time

import httpx
from pydantic import BaseModel, Field, ValidationError

REPOS = [
    "astral-sh/uv",
    "pydantic/pydantic",
    "encode/httpx",
    "openai/openai-python",
    "this-owner/does-not-exist-404",   # 故意放一个不存在的，练习错误处理
]

# (BaseModel) 表示它继承自 Pydantic 的 BaseModel
class RepoInfo(BaseModel):
    full_name: str
    stars: int = Field(alias="stargazers_count", ge=0)
    language: str | None = None
    open_issues: int = Field(alias="open_issues_count", ge=0)

# 带 async 的函数叫协程函数。调用它不会执行函数体,只会得到一个协程对象。要 await 它,或者交给 gather,里面的代码才会跑
async def fetch_repo(client: httpx.AsyncClient, repo: str) -> RepoInfo:
    r = await client.get(f"https://api.github.com/repos/{repo}")
    r.raise_for_status()
    return RepoInfo.model_validate(r.json())

async def fetch_all(repos: list[str]) -> list[RepoInfo | BaseException]:
    # async with 保证结束时把连接池关掉
    # 支持同步和异步的 HTTP 客户端
    # https://www.python-httpx.org/async/
    async with httpx.AsyncClient(timeout=15, headers={"User-Agent": "agent-60-lab"}) as client:
        # 从里往外拆:
        # (fetch_repo(client, r) for r in repos) 是一个生成器,会产出 5 个协程;
        # 前面的 * 把它们展开成 5 个独立的参数,相当于 gather(协程1, 协程2, ..., 协程5);
        # return_exceptions=True 让出错的那个不要把整批拖垮,而是把异常对象放进结果列表。
        # 实测返回列表里元素的类型依次是 RepoInfo, RepoInfo, RepoInfo, RepoInfo, HTTPStatusError,顺序和 REPOS 一一对应
        # * 是 Python 的解包（unpacking）运算符，作用是把一个可迭代对象"拆开"，把里面的元素逐个作为独立参数传给函数
        # asyncio.gather 的签名要求的就是把每个协程/任务作为独立的位置参数传入，所以必须解包
        return await asyncio.gather(*(fetch_repo(client, r) for r in repos), return_exceptions=True)

def summarize(results: list[RepoInfo | BaseException], repos: list[str]) -> tuple[list[RepoInfo], list[str]]:
    ok: list[RepoInfo] = []
    failed:list[str] = []
    # zip 把两个列表按位置配成对:第一轮是 ("astral-sh/uv", RepoInfo(...)),……,第五轮是 ("this-owner/does-not-exist-404", HTTPStatusError(...))
    for repo, res in zip(repos, results):
        if isinstance(res, RepoInfo):
            ok.append(res)
        elif isinstance(res, httpx.HTTPStatusError):
            failed.append(f"{repo}: HTTP {res.response.status_code}")
        elif isinstance(res, ValidationError):
            failed.append(f"{repo}: 返回数据不合法 {res.error_count()} 处")
        else:
            failed.append(f"{repo}: {type(res).__name__} {res}")
    return ok, failed

def main() -> None:
    start = time.perf_counter()
    # main 是普通函数,要靠 asyncio.run 才能进入异步世界,跑完再回来
    results = asyncio.run(fetch_all(REPOS))
    ok, failed = summarize(results, REPOS)
    for info in sorted(ok, key=lambda x: x.stars, reverse=True):
        print(f"{info.full_name:<28} ⭐ {info.stars:>7}  {info.language or '-'}")
    for f in failed:
        print("失败:", f)
    print(f"耗时 {time.perf_counter() - start:.2f}s")

if __name__ == "__main__":
    main()