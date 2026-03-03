"""
测试 OpenRouter 是否原生支持 Anthropic 格式
直接向 OpenRouter 发送 Anthropic 格式请求（不经过 LiteLLM）
"""

import requests
import json

print("=" * 80)
print("测试 OpenRouter 是否原生支持 Anthropic 格式")
print("=" * 80)
print()

# 测试 1: 直接使用 Anthropic 端点
print("🚀 测试 1: 直接向 OpenRouter 发送 Anthropic 格式请求...")
print()

anthropic_response = requests.post(
    "https://openrouter.ai/api/v1/messages",  # Anthropic 端点
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

print(f"状态码：{anthropic_response.status_code}")
print()

if anthropic_response.status_code == 200:
    data = anthropic_response.json()
    print("✅ OpenRouter 原生支持 Anthropic 格式！")
    print()
    print("响应内容:")
    if 'content' in data and len(data['content']) > 0:
        text = data['content'][0].get('text', '')
        print(f"   {text}")
    print()
    
    print("响应结构:")
    print(f"   - id: {data.get('id', 'N/A')}")
    print(f"   - type: {data.get('type', 'N/A')}")
    print(f"   - role: {data.get('role', 'N/A')}")
    print(f"   - content: {len(data.get('content', []))} 条")
    
    native_anthropic_support = True
    
elif anthropic_response.status_code == 404:
    print("❌ OpenRouter 不支持 /v1/messages 端点 (404 Not Found)")
    print("   这意味着 OpenRouter 只支持 OpenAI 格式")
    native_anthropic_support = False
    
elif anthropic_response.status_code == 400:
    print("❌ OpenRouter 拒绝 Anthropic 格式请求 (400 Bad Request)")
    print(f"   错误信息：{anthropic_response.text[:300]}")
    print("   这意味着 OpenRouter 只支持 OpenAI 格式")
    native_anthropic_support = False
    
else:
    print(f"⚠️  意外状态码：{anthropic_response.status_code}")
    print(f"   错误信息：{anthropic_response.text[:300]}")
    native_anthropic_support = False

print()

# 测试 2: 使用 OpenAI 格式（对照测试）
print("🚀 测试 2: 向 OpenRouter 发送 OpenAI 格式请求（对照）...")
print()

openai_response = requests.post(
    "https://openrouter.ai/api/v1/chat/completions",  # OpenAI 端点
    json={
        "model": "stepfun/step-3.5-flash:free",
        "messages": [{"role": "user", "content": "你好！请用中文回答，只用一句话介绍你自己"}],
        "max_tokens": 256
    },
    headers={
        "Content-Type": "application/json",
        "Authorization": "Bearer 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"
    },
    timeout=30
)

print(f"状态码：{openai_response.status_code}")

if openai_response.status_code == 200:
    data = openai_response.json()
    print("✅ OpenAI 格式请求成功（预期之内）")
    if data.get('choices') and len(data['choices']) > 0:
        content = data['choices'][0]['message'].get('content', '')
        if content:
            print(f"   响应：{content[:100]}...")
    openai_success = True
else:
    print(f"❌ OpenAI 格式请求失败：{openai_response.status_code}")
    openai_success = False

print()
print("=" * 80)
print("最终结论:")
print("=" * 80)

if not native_anthropic_support and openai_success:
    print("✅ OpenRouter 仅支持 OpenAI 格式，不支持 Anthropic 格式")
    print("✅ LiteLLM的格式转换是必需的")
    print()
    print("工作流程验证:")
    print("  Claude Code (Anthropic) → LiteLLM (必需转换) → OpenRouter (OpenAI)")
    print("                        ← LiteLLM (转回) ←")
elif native_anthropic_support:
    print("⚠️  OpenRouter 原生支持 Anthropic 格式！")
    print("   LiteLLM 可能不是必需的（但仍有价值作为代理层）")
else:
    print("⚠️  测试结果不明确，需要进一步调查")
