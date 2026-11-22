import os

from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat import ChatCompletionUserMessageParam

load_dotenv()

client = OpenAI(base_url=os.environ["LLM_BASE_URL"], api_key=os.environ["LLM_API_KEY"])
messages: list[ChatCompletionUserMessageParam]= [
    {"role": "user", "content": "用一句话介绍你自己"}
]
resp = client.chat.completions.create(
    model=os.environ["LLM_MODEL"],
    messages=messages,
    extra_body={"thinking": {"type": "disabled"}}
)
print(resp.choices[0].message.content)
print(resp.usage)
