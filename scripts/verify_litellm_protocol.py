"""
验证 LiteLLM 格式转换能力 - 使用模拟响应

由于免费模型需要 API Key，我们直接测试 LiteLLM 的协议转换能力
"""

import requests
import json

def test_litellm_conversion():
    """测试 LiteLLM 是否能正确处理 Anthropic 格式请求"""
    
    print("=" * 60)
    print("LiteLLM 格式转换验证 - 测试协议层")
    print("=" * 60)
    print()
    
    # 测试 1: 检查 LiteLLM 是否运行
    print("📍 步骤 1: 检查 LiteLLM Proxy...")
    try:
        response = requests.get("http://localhost:4000/health", timeout=3)
        if response.status_code == 200:
            print("✅ LiteLLM Proxy 运行正常")
        else:
            print(f"❌ 健康检查失败：{response.status_code}")
            return
    except Exception as e:
        print(f"❌ 无法连接到 LiteLLM: {e}")
        return
    
    print()
    
    # 测试 2: 发送 OpenAI 格式请求（应该成功）
    print("🚀 步骤 2: 测试 OpenAI 格式...")
    try:
        openai_response = requests.post(
            "http://localhost:4000/v1/chat/completions",
            json={
                "model": "groq/llama-3.1-8b-instant",
                "messages": [{"role": "user", "content": "Hello"}],
                "max_tokens": 50
            },
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if openai_response.status_code == 200:
            print("✅ OpenAI 格式请求成功")
            data = openai_response.json()
            print(f"   响应：{json.dumps(data, indent=2)[:200]}...")
        else:
            print(f"⚠️  OpenAI 格式返回错误：{openai_response.status_code}")
            print(f"   {openai_response.text[:200]}")
    except Exception as e:
        print(f"❌ OpenAI 格式测试失败：{e}")
    
    print()
    
    # 测试 3: 发送 Anthropic 格式请求（关键测试！）
    print("🚀 步骤 3: 测试 Anthropic 格式 (关键!)...")
    print("   如果 LiteLLM 支持自动转换，应该能处理这个请求")
    
    try:
        anthropic_response = requests.post(
            "http://localhost:4000/v1/messages",  # Anthropic 端点
            json={
                "model": "claude-3-sonnet-20240229",
                "max_tokens": 1024,
                "messages": [
                    {"role": "user", "content": "Hello from Claude Code!"}
                ]
            },
            headers={
                "Content-Type": "application/json",
                "x-api-key": "sk-test"
            },
            timeout=10
        )
        
        if anthropic_response.status_code == 200:
            print("✅ Anthropic 格式请求成功!")
            data = anthropic_response.json()
            print(f"   响应类型：{type(data)}")
            print(f"   响应内容：{json.dumps(data, indent=2)[:300]}...")
            
            # 验证响应格式
            if "content" in data and isinstance(data["content"], list):
                print()
                print("🎉 验证成功！")
                print()
                print("结论:")
                print("  ✅ LiteLLM 接收了 Anthropic 格式请求")
                print("  ✅ LiteLLM 将请求转换为 OpenAI 格式")
                print("  ✅ LiteLLM 将响应转回 Anthropic 格式")
                print("  ✅ 格式双向转换功能正常!")
                return True
            else:
                print("⚠️  响应格式可能不正确")
        else:
            print(f"❌ Anthropic 格式请求失败：{anthropic_response.status_code}")
            print(f"   错误信息：{anthropic_response.text[:300]}")
            print()
            print("这可能意味着:")
            print("  1. LiteLLM 不支持 /v1/messages 端点")
            print("  2. 需要配置 passthrough 模式")
            print("  3. 当前模型不支持 Anthropic 格式")
            
    except Exception as e:
        print(f"❌ Anthropic 格式测试异常：{e}")
        import traceback
        traceback.print_exc()
    
    print()
    print("📊 总结:")
    print("  虽然实际模型调用失败（需要 API Key），但我们可以查看 LiteLLM 日志")
    print("  来确认它是否尝试进行格式转换")
    
    return False

if __name__ == "__main__":
    success = test_litellm_conversion()
    
    if not success:
        print()
        print("💡 建议:")
        print("  1. 查看 LiteLLM 控制台输出，了解请求处理过程")
        print("  2. 使用 --debug 参数启动 LiteLLM 查看详细日志")
        print("  3. 参考官方文档配置正确的模型和认证")
