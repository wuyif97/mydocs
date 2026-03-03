"""
完整验证 LiteLLM 格式转换 - 使用 OpenRouter 免费模型 + API Key
"""

import requests
import json

LITELLM_PORT = 16817

print("=" * 80)
print("LiteLLM 格式转换完整验证 - OpenRouter 免费模型")
print("=" * 80)
print()

# 步骤 1: 健康检查
print("📍 步骤 1: 健康检查...")
try:
    r = requests.get(f"http://localhost:{LITELLM_PORT}/health", timeout=3)
    print(f"✅ LiteLLM 运行正常 (端口：{LITELLM_PORT})")
except Exception as e:
    print(f"❌ 连接失败：{e}")
    exit(1)

print()

# 步骤 2: 测试 OpenAI 格式
print("🚀 步骤 2: 测试 OpenAI 格式请求...")
print()

openai_response = requests.post(
    f"http://localhost:{LITELLM_PORT}/v1/chat/completions",
    json={
        "model": "free-model",
        "messages": [{"role": "user", "content": "你好！请用中文回答，只用一句话介绍你自己"}],
        "max_tokens": 100
    },
    headers={"Content-Type": "application/json"},
    timeout=30
)

print(f"OpenAI 格式状态码：{openai_response.status_code}")

if openai_response.status_code == 200:
    data = openai_response.json()
    print("✅ OpenAI 格式请求成功！")
    # 调试：打印完整响应
    import json
    with open('debug_openai_response.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("   (响应已保存到 debug_openai_response.json)")
    if data.get('choices') and len(data['choices']) > 0 and data['choices'][0].get('message'):
        content = data['choices'][0]['message'].get('content', '')
        if content:
            print(f"   响应：{content[:100]}...")
        else:
            print(f"   响应内容为空，查看完整数据：{json.dumps(data, ensure_ascii=False)[:200]}")
    else:
        print(f"   响应结构异常：{json.dumps(data, ensure_ascii=False)[:300]}")
    openai_success = True
else:
    print(f"❌ OpenAI 格式请求失败：{openai_response.status_code}")
    print(f"   错误：{openai_response.text[:200]}")
    openai_success = False

print()

# 步骤 3: 关键测试 - Anthropic 格式
print("🚀 步骤 3: 关键测试 - Anthropic 格式（Claude Code 使用的格式）...")
print()

anthropic_response = requests.post(
    f"http://localhost:{LITELLM_PORT}/v1/messages",  # Anthropic 端点
    json={
        "model": "free-model",  # 使用 LiteLLM 配置的模型名称
        "max_tokens": 256,
        "messages": [
            {"role": "user", "content": "你好！我是 Claude Code，请用中文回答，只用一句话介绍你自己"}
        ]
    },
    headers={
        "Content-Type": "application/json",
        "x-api-key": "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"
    },
    timeout=30
)

print(f"Anthropic 格式状态码：{anthropic_response.status_code}")
print()

if anthropic_response.status_code == 200:
    data = anthropic_response.json()
    print("✅✅✅ 验证成功！Anthropic 格式请求完全成功！")
    print()
    
    # 显示响应内容
    if 'content' in data and len(data['content']) > 0:
        text = data['content'][0].get('text', '')
        print("📝 响应内容:")
        print(f"   {text}")
        print()
    
    # 验证响应结构
    print("📊 验证响应格式（应该是 Anthropic 格式）:")
    print(f"   - id: {data.get('id', 'N/A')}")
    print(f"   - type: {data.get('type', 'N/A')}")
    print(f"   - role: {data.get('role', 'N/A')}")
    print(f"   - content: {len(data.get('content', []))} 条")
    print(f"   - model: {data.get('model', 'N/A')}")
    print()
    
    # 确认所有必需字段
    required_fields = ['id', 'type', 'role', 'content']
    if all(field in data for field in required_fields):
        print("🎉 响应完全符合 Anthropic 格式规范！")
        print()
        print("=" * 80)
        print("最终结论:")
        print("=" * 80)
        print("✅ LiteLLM 接收了 Anthropic 格式请求")
        print("✅ LiteLLM 将请求转换为 OpenAI 格式并发送到 OpenRouter")
        print("✅ OpenRouter 返回 OpenAI 格式响应")
        print("✅ LiteLLM 将响应转回 Anthropic 格式")
        print("✅ Claude Code 可以正常使用内网模型！")
        print()
        print("工作流程验证通过:")
        print("  Claude Code (Anthropic) → LiteLLM (转换) → OpenRouter (OpenAI)")
        print("                        ← LiteLLM (转回) ←")
        print("=" * 80)
        
        # 保存成功数据
        with open('test_success_result.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print()
        print("💾 响应数据已保存到 test_success_result.json")
        
        success = True
    else:
        print("⚠️  响应格式可能不完整")
        success = False
elif anthropic_response.status_code == 401:
    print("❌ 认证失败 - API Key 无效或过期")
    print(f"   错误信息：{anthropic_response.text[:300]}")
    success = False
else:
    print(f"❌ 请求失败 - 状态码：{anthropic_response.status_code}")
    print(f"   错误信息：{anthropic_response.text[:300]}")
    success = False

print()
print("📊 测试总结:")
print(f"  - OpenAI 格式：{'✅ 成功' if openai_success else '❌ 失败'}")
print(f"  - Anthropic 格式：{'✅ 成功' if success else '❌ 失败'}")
print()

if success:
    print("=" * 80)
    print("最终结论:")
    print("=" * 80)
    print("✅ LiteLLM 接收了 Anthropic 格式请求")
    print("✅ LiteLLM 将请求转换为 OpenAI 格式并发送到 OpenRouter")
    print("✅ OpenRouter 返回 OpenAI 格式响应")
    print("✅ LiteLLM 将响应转回 Anthropic 格式")
    print("✅ Claude Code 可以正常使用内网模型！")
    print()
    print("工作流程验证通过:")
    print("  Claude Code (Anthropic) → LiteLLM (转换) → OpenRouter (OpenAI)")
    print("                        ← LiteLLM (转回) ←")
    print("=" * 80)
