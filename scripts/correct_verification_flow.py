"""
正确的验证流程：
1. 先测试 OpenAI格式（确认模型本身可用）
2. 再测试 Anthropic格式（验证 LiteLLM 转换能力）
3. 对比结果，确定问题根源
"""

import requests
import json

API_KEY = "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"
MODEL_ID = "google/gemma-2-9b-it:free"
LITELLM_PORT = 4000

print("=" * 80)
print("正确的验证流程：OpenAI格式 → Anthropic格式")
print("=" * 80)
print()

# ========== 步骤 1: 直接向 OpenRouter 发送 OpenAI格式请求 ==========
print("🚀 步骤 1: 直接向 OpenRouter 发送 OpenAI格式请求")
print(f"   模型：{MODEL_ID}")
print(f"   端点：https://openrouter.ai/api/v1/chat/completions")
print()

openai_direct_response = requests.post(
    "https://openrouter.ai/api/v1/chat/completions",
    json={
        "model": MODEL_ID,
        "messages": [{"role": "user", "content": "你好！请用中文回答，只用一句话"}],
        "max_tokens": 100
    },
    headers={
        "Content-Type": "application/json",
        "Authorization": f'Bearer {API_KEY}'
    },
    timeout=30
)

print(f"状态码：{openai_direct_response.status_code}")

if openai_direct_response.status_code == 200:
    data = openai_direct_response.json()
    print("✅ OpenRouter 支持此模型的 OpenAI格式")
    if data.get('choices') and len(data['choices']) > 0:
        content = data['choices'][0]['message'].get('content', '')
        if content:
            print(f"   响应：{content[:100]}...")
    model_available = True
else:
    print(f"❌ OpenRouter 不支持或模型不可用：{openai_direct_response.status_code}")
    print(f"   错误：{openai_direct_response.text[:200]}")
    model_available = False

print()

# ========== 步骤 2: 直接向 OpenRouter 发送 Anthropic格式请求 ==========
print("🚀 步骤 2: 直接向 OpenRouter 发送 Anthropic格式请求")
print(f"   模型：{MODEL_ID}")
print(f"   端点：https://openrouter.ai/api/v1/messages")
print()

anthropic_direct_response = requests.post(
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
    timeout=30
)

print(f"状态码：{anthropic_direct_response.status_code}")

if anthropic_direct_response.status_code == 200:
    data = anthropic_direct_response.json()
    if 'content' in data and isinstance(data['content'], list):
        print("✅ OpenRouter 原生支持此模型的 Anthropic格式")
        native_support = True
    else:
        print("⚠️  响应格式异常")
        native_support = False
elif anthropic_direct_response.status_code == 404:
    print("❌ OpenRouter 不支持此模型的 Anthropic格式 (404)")
    native_support = False
else:
    print(f"⚠️  其他错误：{anthropic_direct_response.text[:200]}")
    native_support = False

print()

# ========== 步骤 3: 通过 LiteLLM 发送 Anthropic格式请求 ==========
print("🚀 步骤 3: 通过 LiteLLM 发送 Anthropic格式请求")
print(f"   模型：gemma-free (LiteLLM 配置别名)")
print(f"   端点：http://localhost:{LITELLM_PORT}/v1/messages")
print()

litellm_response = requests.post(
    f"http://localhost:{LITELLM_PORT}/v1/messages",
    json={
        "model": "gemma-free",
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
    print("✅ LiteLLM 成功处理 Anthropic格式请求！")
    if 'content' in data and len(data['content']) > 0:
        text = data['content'][0].get('text', '')
        print(f"   响应：{text[:100]}...")
    litellm_success = True
else:
    print(f"❌ LiteLLM 失败：{litellm_response.status_code}")
    print(f"   错误信息：{litellm_response.text[:300]}")
    litellm_success = False

print()

# ========== 综合分析 ==========
print("=" * 80)
print("综合分析:")
print("=" * 80)
print()

if model_available and not native_support and litellm_success:
    print("✅ 完美验证！")
    print()
    print("结论:")
    print(f"  1. ✅ {MODEL_ID} 本身可用（OpenAI格式成功）")
    print(f"  2. ❌ OpenRouter 不原生支持Anthropic格式（404）")
    print(f"  3. ✅ LiteLLM 成功转换格式并返回正确响应")
    print()
    print("工作流程验证通过:")
    print("  Claude Code (Anthropic) → LiteLLM (转换) → OpenRouter (OpenAI) ← LiteLLM (转回) ←")
    
elif model_available and not native_support and not litellm_success:
    print("⚠️  关键发现！")
    print()
    print("分析:")
    print(f"  1. ✅ {MODEL_ID} 本身可用（OpenAI格式成功）")
    print(f"  2. ❌ OpenRouter 不原生支持Anthropic格式（404）")
    print(f"  3. ❌ LiteLLM 也失败了（{litellm_response.status_code}）")
    print()
    print("可能的原因:")
    print("  - LiteLLM 配置错误（模型别名不匹配）")
    print("  - LiteLLM 版本过旧，不支持格式转换")
    print("  - LiteLLM 没有正确透传请求到后端")
    print()
    print("解决方案:")
    print("  1. 检查 LiteLLM 配置文件中的模型名称")
    print("  2. 查看 LiteLLM 服务端日志")
    print("  3. 更新 LiteLLM 到最新版本")
    
elif not model_available:
    print("⚠️  模型本身不可用")
    print()
    print("分析:")
    print(f"  1. ❌ {MODEL_ID} 在 OpenRouter 上不可用或需要付费")
    print(f"  2. 无法判断 OpenRouter 是否支持Anthropic格式")
    print(f"  3. LiteLLM 失败是因为后端模型不可用")
    print()
    print("建议:")
    print("  - 换一个可用的免费模型重新测试")
    print("  - 检查 OpenRouter API Key 是否有足够额度")
    
elif native_support:
    print("⚠️  此模型原生支持Anthropic格式")
    print()
    print("分析:")
    print(f"  1. ✅ {MODEL_ID} 本身可用")
    print(f"  2. ✅ OpenRouter 原生支持Anthropic格式")
    print(f"  3. LiteLLM 的转换不是必需的（但仍有价值）")
    print()
    print("建议:")
    print("  - 选择不支持Anthropic格式的模型重新测试（如 Llama-3、Mistral 等）")
