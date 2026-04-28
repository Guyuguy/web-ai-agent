import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

os.environ['NO_PROXY'] = '127.0.0.1,localhost'
os.environ['no_proxy'] = '127.0.0.1,localhost'

from openai import OpenAI

client = OpenAI(api_key="ollama", base_url="http://127.0.0.1:11434/v1")

try:
    print("正在测试 qwen2.5-coder:14b 模型...")
    resp = client.chat.completions.create(
        model="qwen2.5-coder:14b",
        messages=[{"role": "user", "content": "你好"}],
        max_tokens=10
    )
    print("✅ 模型调用成功！")
    print(f"返回内容: {resp.choices[0].message.content}")
except Exception as e:
    print(f"❌ 模型调用失败: {e}")
    import traceback
    traceback.print_exc()
