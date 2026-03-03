"""
对比验证：Qwen-2（不支持 Anthropic API）通过 LiteLLM 转换

测试流程：
1. 直接向 OpenRouter 发送 Anthropic 格式请求（预期失败）
2. 通过 LiteLLM 发送 Anthropic 格式请求（预期成功）
3. 证明 LiteLLM 的格式转换价值
"""

import requests
import json

API_KEY = "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"
MODEL_ID = "mistralai/mistral-7b-instruct:free"
LITELLM_PORT = 4000

print("=" * 80)
print("对比验证：LiteLLM 格式转换的必要性")
print("=" * 80)
print()

# ========== 测试 1: 直接连接 OpenRouter（不经过 LiteLLM）==========
print("🚀 测试 1: 直接向 OpenRouter 发送 Anthropic 格式请求")
print(f"   模型：{MODEL_ID}")
print(f"   端点：https://openrouter.ai/api/v1/messages")
print()

direct_response = requests.post(
    "https://openrouter.ai/api/v1/messages",
    json={
        "model": MODEL_ID,
        "max_tokens": 100,
        "messages": [{"role": "user", "content": "你好！请用中文回答，只用一句话"}]
    },
    headers={
        "Content-Type": "application/json",
        "Authorization": f'Bearer {API_KEY}'
    },
    timeout=15
)

print(f"状态码：{direct_response.status_code}")

if direct_response.status_code == 200:
    data = direct_response.json()
    if 'content' in data and isinstance(data['content'], list):
        print("✅ OpenRouter 原生支持此模型的 Anthropic 格式")
        native_support = True
    else:
        print("⚠️  响应格式异常")
        native_support = False
elif direct_response.status_code == 404:
    print("❌ OpenRouter 不支持此模型的 Anthropic 格式 (404)")
    print("   这意味着必须通过格式转换器才能使用 Claude Code")
    native_support = False
else:
    print(f"⚠️  其他错误：{direct_response.text[:200]}")
    native_support = False

print()

# ========== 测试 2: 通过 LiteLLM 连接 ==========
print("🚀 测试 2: 通过 LiteLLM 发送 Anthropic 格式请求")
print(f"   模型：qwen-free (配置别名)")
print(f"   端点：http://localhost:{LITELLM_PORT}/v1/messages")
print()

litellm_response = requests.post(
    f"http://localhost:{LITELLM_PORT}/v1/messages",
    json={
        "model": "mistral-free",  # LiteLLM 配置的模型别名
        "max_tokens": 100,
        "messages": [{"role": "user", "content": "你好！请用中文回答，只用一句话"}]
    },
    headers={
        "Content-Type": "application/json",
        "x-api-key": "sk-test"
    },
    timeout=30
)

print(f"状态码：{litellm_response.status_code}")

if litellm_response.status_code == 200:
    data = litellm_response.json()
    print("✅ LiteLLM 成功处理 Anthropic 格式请求！")
    print()
    
    # 显示响应内容
    if 'content' in data and len(data['content']) > 0:
        text = data['content'][0].get('text', '')
        print(f"📝 响应内容：{text}")
        print()
    
    # 验证响应格式
    print("📊 响应结构验证:")
    print(f"   - id: {data.get('id', 'N/A')}")
    print(f"   - type: {data.get('type', 'N/A')}")
    print(f"   - role: {data.get('role', 'N/A')}")
    print(f"   - content: {len(data.get('content', []))} 条")
    
    litellm_success = True
    
elif litellm_response.status_code == 400:
    print(f"❌ LiteLLM 返回 400 错误")
    print(f"   错误信息：{litellm_response.text[:300]}")
    litellm_success = False
else:
    print(f"❌ LiteLLM 请求失败：{litellm_response.status_code}")
    print(f"   错误信息：{litellm_response.text[:300]}")
    litellm_success = False

print()

# ========== 总结 ==========
print("=" * 80)
print("最终结论:")
print("=" * 80)

if not native_support and litellm_success:
    print("✅ 验证成功！")
    print()
    print("关键发现:")
    print(f"  1. ❌ {MODEL_ID} 不支持原生 Anthropic 格式")
    print(f"  2. ✅ LiteLLM 成功转换格式并返回正确响应")
    print()
    print("工作流程验证:")
    print("  Claude Code (Anthropic)")
    print("    ↓")
    print("  LiteLLM (必需！格式转换)")
    print("    ↓")
    print(f"  {MODEL_ID} (OpenAI 格式)")
    print("    ↓")
    print("  LiteLLM (转回 Anthropic)")
    print("    ↓")
    print("  Claude Code (正常接收)")
    print()
    print("💡 这就是为什么内网模型需要 LiteLLM！")
    print()
    
    # 保存完整响应
    with open('litellm_conversion_proof.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("💾 响应数据已保存到 litellm_conversion_proof.json")
    
elif native_support:
    print("⚠️  此模型原生支持 Anthropic 格式，无法证明 LiteLLM 的必要性")
    print("   请选择不支持 Anthropic 格式的模型（如 Qwen-2、Mistral 等）")
    
elif not litellm_success:
    print("❌ LiteLLM 转换失败，需要检查配置或日志")
