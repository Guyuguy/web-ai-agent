import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GLM_TOKEN"),
    base_url=os.getenv("GLM_BASE_URL"),
    http_client=None
)
MODEL = os.getenv("GLM_MODEL", "glm-4.7")

try:
    print(f"Testing API connection with model: {MODEL}")
    resp = client.chat.completions.create(
        model=MODEL,
        messages=[{"role":"user","content":"Hello, can you respond with just 'OK'?"}]
    )
    print("API Response:", resp.choices[0].message.content)
except Exception as e:
    print(f"API Error: {e}")
