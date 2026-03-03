import requests
import json

anthropic_response = requests.post(
    "https://openrouter.ai/api/v1/messages",
    json={
        "model": "stepfun/step-3.5-flash:free",
        "max_tokens": 256,
        "messages": [
            {"role": "user", "content": "你好！请用中文回答，只用一句话介绍你自己"}
        ]
    },
    headers={
        "Content-Type": "application/json",
        "Authorization": "Bearer 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"
    },
    timeout=30
)

if anthropic_response.status_code == 200:
    data = anthropic_response.json()
    print("OpenRouter 原生 Anthropic 格式响应:")
    print(json.dumps(data, indent=2, ensure_ascii=False))
else:
    print(f"Error: {anthropic_response.status_code}")
    print(anthropic_response.text)
