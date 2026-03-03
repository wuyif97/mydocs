"""
测试哪些大模型平台不支持 Anthropic Messages API
"""

import requests

API_KEY = "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"

# 从 OpenRouter 获取所有免费模型
r = requests.get(
    'https://openrouter.ai/api/v1/models',
    headers={'Authorization': f'Bearer {API_KEY}'}
)

models = r.json().get('data', [])
print(f"OpenRouter 上共有 {len(models)} 个模型\n")

# 测试几个典型模型
test_models = [
    "meta-llama/llama-3-70b-instruct",
    "google/gemma-2-9b-it:free", 
    "mistralai/mistral-7b-instruct:free",
    "qwen/qwen-2-7b-instruct:free",
]

print("测试各模型对 Anthropic Messages API 的支持情况:")
print("=" * 80)

for model_id in test_models:
    print(f"\n测试模型：{model_id}")
    print("-" * 60)
    
    # 尝试发送 Anthropic 格式请求
    response = requests.post(
        "https://openrouter.ai/api/v1/messages",
        json={
            "model": model_id,
            "max_tokens": 50,
            "messages": [{"role": "user", "content": "Hello"}]
        },
        headers={
            "Content-Type": "application/json",
            "Authorization": f'Bearer {API_KEY}'
        },
        timeout=10
    )
    
    if response.status_code == 200:
        data = response.json()
        if 'content' in data and isinstance(data['content'], list):
            print(f"✅ 支持 Anthropic Messages API")
            print(f"   响应类型：{data.get('type', 'N/A')}")
        else:
            print(f"⚠️  响应格式异常：{list(data.keys())}")
    elif response.status_code == 400:
        error_msg = response.text[:200]
        if 'anthropic_messages' in error_msg.lower() or 'invalid model' in error_msg.lower():
            print(f"❌ 不支持 Anthropic Messages API")
            print(f"   错误：{error_msg}")
        else:
            print(f"⚠️  其他错误 (400): {error_msg}")
    elif response.status_code == 404:
        print(f"❌ /v1/messages 端点不存在或模型不支持")
    else:
        print(f"⚠️  状态码 {response.status_code}: {response.text[:150]}")
