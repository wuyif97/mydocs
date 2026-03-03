"""
验证 LiteLLM 格式转换能力 - 使用真实免费模型

架构：Anthropic SDK → LiteLLM Proxy → Groq (OpenAI兼容免费模型)
"""

import os
from anthropic import Anthropic

def main():
    print("=" * 60)
    print("LiteLLM 格式转换验证 - 使用 Groq 免费模型")
    print("=" * 60)
    print()
    
    # 配置 LiteLLM Proxy 地址
    ANTHROPIC_BASE_URL = "http://localhost:4000"
    API_KEY = "sk-test-key"  # 任意值即可
    
    print(f"📍 LiteLLM Proxy 地址：{ANTHROPIC_BASE_URL}")
    print(f"🔑 API Key: {API_KEY}")
    print()
    
    # 创建 Anthropic 客户端（连接到 LiteLLM）
    client = Anthropic(
        api_key=API_KEY,
        base_url=ANTHROPIC_BASE_URL
    )
    
    print("🚀 测试 1: 使用 Anthropic SDK 发送请求...")
    print("   如果 LiteLLM 能自动转换格式，应该收到响应")
    print()
    
    try:
        # 发送 Anthropic 格式的请求
        message = client.messages.create(
            model="llama-3.1-8b-instant",  # Groq 的免费模型
            max_tokens=1024,
            messages=[
                {
                    "role": "user", 
                    "content": "你好！请用一句话介绍你自己。"
                }
            ]
        )
        
        print("✅ 成功收到响应!")
        print(f"📝 内容：{message.content[0].text}")
        print()
        
        # 验证响应格式
        print("📊 验证响应对象结构:")
        print(f"   - 类型：{type(message)}")
        print(f"   - ID: {getattr(message, 'id', 'N/A')}")
        print(f"   - 角色：{message.role if hasattr(message, 'role') else 'N/A'}")
        print(f"   - 内容长度：{len(message.content)}")
        print()
        
        print("🎉 验证成功！LiteLLM 确实能自动转换格式!")
        print()
        print("结论:")
        print("  ✅ Anthropic SDK 可以连接 LiteLLM Proxy")
        print("  ✅ LiteLLM 将 Anthropic 格式转换为 OpenAI 格式")
        print("  ✅ Groq 接收 OpenAI 格式并返回响应")
        print("  ✅ LiteLLM 将响应转回 Anthropic 格式")
        
    except Exception as e:
        print(f"❌ 请求失败：{e}")
        print()
        print("可能的原因:")
        print("  1. LiteLLM Proxy 未启动或端口不对")
        print("  2. 模型名称不匹配")
        print("  3. LiteLLM 配置问题")
        print()
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
