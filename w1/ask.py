# agent-60-lab/w1/ask.py
"""命令行问答：uv run w1/ask.py "你的问题" [--env .env.deepseek]"""
import argparse
import json
import os
import sys

import openai
from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat import ChatCompletionUserMessageParam


def parse_price(raw: str) -> tuple[float, float, float]:
    hit, miss, out = (float(x) for x in raw.split(','))
    return hit, miss, out

def cost_yuan(usage, price: tuple[float, float, float]) -> float:
    hit_price, miss_price, out_price = price
    # getattr(对象, 属性名, 默认值):有这个属性就取它,没有就返回 None,不会报错
    hit = getattr(usage, "prompt_cache_hit_tokens", None) or 0
    miss = getattr(usage, "prompt_cache_miss_tokens", None)
    if miss is None:
        miss = usage.prompt_tokens - hit
    # 花费 = (命中 tokens × 命中价 + 未命中 tokens × 未命中价 + 输出 tokens × 输出价) ÷ 1,000,000
    return (hit * hit_price + miss * miss_price + usage.completion_tokens * out_price) / 1_000_000

def main() -> int:
    # 参数解析器
    parser = argparse.ArgumentParser()
    parser.add_argument("question")
    parser.add_argument("--env", default=".env")
    parser.add_argument("--max-tokens", type=int, default=500)
    args = parser.parse_args()

    load_dotenv(args.env, override=True)
    client = OpenAI(
        base_url=os.environ["LLM_BASE_URL"],
        api_key=os.environ["LLM_API_KEY"],
        # SDK 遇到 429 和 5xx 自动重试 3 次,带退避等待。默认是 2 次
        max_retries=3,
        # 单次请求最多等 60 秒。默认是 10 分钟,太长了
        # 429 和 5xx 要重试，而且要越等越久. OpenAI 官方 Python SDK 已经替你做了这件事：默认对连接错误、408、409、429 和 5xx 自动重试 2 次，带指数退避
        # 指数退避的意思是：重试间隔按 1s、2s、4s……递增，避免一起重试把服务压垮
        timeout=60.0,
    )
    # .get 取不到时用默认值 "{}"
    extra_body = json.loads(os.environ.get("LLM_EXTRA_BODY", "{}"))
    price = parse_price(os.environ.get("LLM_PRICE", "0,0,0"))

    messages: list[ChatCompletionUserMessageParam]= [
        {"role": "system", "content": "你是一个简洁的技术助手，用中文回答。"},
        {"role": "user", "content": args.question},
    ]
    try:
        resp = client.chat.completions.create(
            model=os.environ["LLM_MODEL"],
            messages=messages,
            # 限制一次请求中模型生成 completion 的最大 token 数。取值范围为 1 到 384K（393216）。未设置时，非思考模式默认 8K，思考模式默认 64K（reasoning_effort 为 max 时为 128K）
            max_tokens=args.max_tokens,
            # 采样温度，介于 0 和 2 之间。更高的值，如 0.8，会使输出更随机，而更低的值，如 0.2，会使其更加集中和确定
            temperature=0.3,
            extra_body=extra_body,
        )
    except openai.AuthenticationError:
        print("401：API key 不对。检查", args.env, "里的 LLM_API_KEY。", file=sys.stderr)
        return 1
    except openai.RateLimitError as e:
        print("429：请求太快或额度用完（已自动重试 3 次）。", e.message, file=sys.stderr)
        return 1
    except openai.BadRequestError as e:
        print("400：请求参数有问题，通常是模型名或扩展参数不对：", e.message, file=sys.stderr)
        return 1
    except openai.APIConnectionError:
        print("连不上服务器：检查网络、代理和 LLM_BASE_URL。", file=sys.stderr)
        return 1
    # 其他所有 HTTP 错误的父类。放在最后是因为 except 按顺序匹配,上面几个都是它的子类,它要是放在前面,就会把 401、429 全吞掉
    except openai.APIStatusError as e:
        print(f"HTTP {e.status_code}：{e.message}", file=sys.stderr)
        return 1

    choice = resp.choices[0]
    print(choice.message.content)
    # 字符串乘数字就是重复,打出 40 个 - 当分隔线
    print("-" * 40)
    print("模型:", resp.model, "| finish_reason:", choice.finish_reason)
    if choice.finish_reason == "length":
        print("⚠ 回答被 max_tokens 截断了，调大 --max-tokens 再试")
    u = resp.usage
    assert u is not None
    print(f"tokens: 输入 {u.prompt_tokens} / 输出 {u.completion_tokens}，花费约 ¥{cost_yuan(u, price):.5f}")
    return 0

if __name__ == "__main__":
    sys.exit(main())