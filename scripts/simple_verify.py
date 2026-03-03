"""
超简单验证 - 直接向 LiteLLM 发送 Anthropic 格式请求
"""

import requests

# LiteLLM 实际运行端口
LITELLM_PORT = 41996

print("=" * 80)
print("LiteLLM 格式转换验证")
print("=" * 80)
print()

# 步骤 1: 健康检查
print("📍 健康检查...")
try:
    r = requests.get(f"http://localhost:{LITELLM_PORT}/health", timeout=3)
    print(f"✅ LiteLLM 运行正常 (端口：{LITELLM_PORT})")
except Exception as e:
    print(f"❌ 连接失败：{e}")
    exit(1)

print()

# 步骤 2: 关键测试 - Anthropic 格式
print("🚀 测试：Anthropic 格式 → LiteLLM → OpenRouter 免费模型")
print()

response = requests.post(
    f"http://localhost:{LITELLM_PORT}/v1/messages",
    json={
        "model": "free-model",
        "max_tokens": 100,
        "messages": [
            {"role": "user", "content": "你好！请用中文回答，只用一句话"}
        ]
    },
    headers={
        "Content-Type": "application/json",
        "x-api-key": "sk-test"
    },
    timeout=30
)

print(f"状态码：{response.status_code}")
print()

if response.status_code == 200:
    data = response.json()
    print("✅✅✅ 成功！Anthropic 格式请求被接受并处理！")
    print()
    print("📝 响应内容:")
    if 'content' in data and len(data['content']) > 0:
        text = data['content'][0].get('text', '')
        print(f"   {text}")
    print()
    
    print("📊 响应结构验证:")
    print(f"   - id: {data.get('id', 'N/A')}")
    print(f"   - type: {data.get('type', 'N/A')}")
    print(f"   - role: {data.get('role', 'N/A')}")
    print(f"   - content: {len(data.get('content', []))} 条")
    print()
    
    # 确认所有必需字段
    required_fields = ['id', 'type', 'role', 'content']
    if all(field in data for field in required_fields):
        print("🎉 响应完全符合 Anthropic 格式规范！")
        print()
        print("=" * 80)
        print("最终结论:")
        print("=" * 80)
        print("✅ Claude Code (Anthropic 格式) → LiteLLM → 内网模型 (OpenAI 格式)")
        print("✅ 格式自动转换已验证通过！")
        print("=" * 80)
    else:
        print("⚠️  响应格式可能不完整")
        
elif response.status_code == 401:
    print("❌ 认证失败 - OpenRouter 需要 API Key")
    print("   错误信息:", response.text[:200])
else:
    print(f"❌ 请求失败 - 状态码：{response.status_code}")
    print("   错误信息:", response.text[:300])
