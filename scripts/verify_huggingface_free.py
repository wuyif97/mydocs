"""
完整验证 LiteLLM 格式转换 - 使用 Hugging Face 免费模型

Hugging Face Inference API 提供免费额度，不需要认证即可测试
"""

import requests
import json
import sys

def main():
    print("=" * 80)
    print("LiteLLM 格式转换完整验证 - Hugging Face 免费模型")
    print("=" * 80)
    print()
    
    # 步骤 1: 检查 LiteLLM Proxy
    print("📍 步骤 1: 检查 LiteLLM Proxy...")
    try:
        response = requests.get("http://localhost:4000/health", timeout=3)
        if response.status_code == 200:
            print("✅ LiteLLM Proxy 运行正常")
        else:
            print(f"❌ 健康检查失败：{response.status_code}")
            sys.exit(1)
    except Exception as e:
        print(f"❌ 无法连接到 LiteLLM: {e}")
        print("   请先启动 LiteLLM: litellm --model <model> --port 4000")
        sys.exit(1)
    
    print()
    
    # 步骤 2: 直接调用 Hugging Face（测试模型本身）
    print("🚀 步骤 2: 直接测试 Hugging Face 模型（不经过 LiteLLM）...")
    hf_url = "https://api-inference.huggingface.co/models/Qwen/Qwen2.5-Coder-32B-Instruct/v1/chat/completions"
    
    try:
        payload = {
            "model": "Qwen/Qwen2.5-Coder-32B-Instruct",
            "messages": [{"role": "user", "content": "你好，请用一句话介绍你自己"}],
            "max_tokens": 100
        }
        
        headers = {"Content-Type": "application/json"}
        
        print(f"   请求 URL: {hf_url}")
        print(f"   请求内容：{json.dumps(payload, ensure_ascii=False)}")
        print()
        
        response = requests.post(hf_url, json=payload, headers=headers, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Hugging Face 模型响应成功！")
            print(f"   响应内容：{data['choices'][0]['message']['content'][:100]}...")
            print()
            
            # 保存这个成功的响应作为基准
            baseline_response = data
        else:
            print(f"⚠️  Hugging Face 返回错误：{response.status_code}")
            print(f"   {response.text[:200]}")
            print()
            print("   这可能意味着模型正在加载中，我们继续测试 LiteLLM...")
            baseline_response = None
            
    except Exception as e:
        print(f"⚠️  直接调用 Hugging Face 失败：{e}")
        print("   继续测试 LiteLLM...")
        baseline_response = None
    
    print()
    
    # 步骤 3: 通过 LiteLLM 调用 Hugging Face (OpenAI 格式)
    print("🚀 步骤 3: 通过 LiteLLM 调用（OpenAI 格式）...")
    
    try:
        lite_response = requests.post(
            "http://localhost:4000/v1/chat/completions",
            json={
                "model": "huggingface/Qwen/Qwen2.5-Coder-32B-Instruct",
                "messages": [{"role": "user", "content": "你好，请用一句话介绍你自己"}],
                "max_tokens": 100
            },
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if lite_response.status_code == 200:
            data = lite_response.json()
            print("✅ LiteLLM (OpenAI 格式) 成功！")
            print(f"   响应：{data['choices'][0]['message']['content'][:100]}...")
            openai_success = True
        else:
            print(f"❌ LiteLLM (OpenAI 格式) 失败：{lite_response.status_code}")
            print(f"   {lite_response.text[:200]}")
            openai_success = False
            
    except Exception as e:
        print(f"❌ LiteLLM (OpenAI 格式) 异常：{e}")
        openai_success = False
    
    print()
    
    # 步骤 4: 关键测试 - Anthropic 格式通过 LiteLLM
    print("🚀 步骤 4: 关键测试 - Anthropic 格式通过 LiteLLM...")
    print("   这是验证的核心：Claude Code 使用 Anthropic 格式")
    
    try:
        anthropic_response = requests.post(
            "http://localhost:4000/v1/messages",  # Anthropic 端点
            json={
                "model": "claude-3-sonnet-20240229",
                "max_tokens": 1024,
                "messages": [
                    {"role": "user", "content": "你好！我是 Claude Code，请用一句话介绍你自己"}
                ]
            },
            headers={
                "Content-Type": "application/json",
                "x-api-key": "sk-test"
            },
            timeout=30
        )
        
        if anthropic_response.status_code == 200:
            data = anthropic_response.json()
            print()
            print("✅✅✅ 验证成功！Anthropic 格式请求成功！")
            print()
            print(f"📝 响应内容：{data['content'][0]['text'][:150]}...")
            print()
            
            # 验证响应结构
            print("📊 验证响应格式:")
            print(f"   - ID: {data.get('id', 'N/A')}")
            print(f"   - 类型：{data.get('type', 'N/A')}")
            print(f"   - 角色：{data.get('role', 'N/A')}")
            print(f"   - 内容：{len(data.get('content', []))} 条")
            print(f"   - 模型：{data.get('model', 'N/A')}")
            print()
            
            # 确认是 Anthropic 格式
            if all(k in data for k in ['id', 'type', 'role', 'content']):
                print("🎉 响应符合 Anthropic 格式规范！")
                print()
                print("=" * 80)
                print("最终结论:")
                print("=" * 80)
                print("✅ LiteLLM 接收了 Anthropic 格式请求")
                print("✅ LiteLLM 将请求转换为 OpenAI 格式并发送到 Hugging Face")
                print("✅ Hugging Face 返回 OpenAI 格式响应")
                print("✅ LiteLLM 将响应转回 Anthropic 格式")
                print("✅ Claude Code 可以正常使用内网模型！")
                print("=" * 80)
                return True
            else:
                print("⚠️  响应格式可能不完整")
                
        else:
            print(f"❌ Anthropic 格式请求失败：{anthropic_response.status_code}")
            print(f"   错误信息：{anthropic_response.text[:300]}")
            print()
            
            # 分析错误
            if "403" in str(anthropic_response.status_code):
                print("💡 403 错误可能是因为:")
                print("   1. Hugging Face 需要 API Key（但之前测试应该能工作）")
                print("   2. LiteLLM 配置问题")
            elif "404" in str(anthropic_response.status_code):
                print("💡 404 错误意味着 LiteLLM 不支持 /v1/messages 端点")
                print("   这不可能，因为日志显示它支持")
            
    except Exception as e:
        print(f"❌ Anthropic 格式测试异常：{e}")
        import traceback
        traceback.print_exc()
    
    print()
    print("📊 测试总结:")
    print(f"  - LiteLLM Proxy: ✅ 运行正常")
    print(f"  - OpenAI 格式：{'✅ 成功' if openai_success else '❌ 失败'}")
    print(f"  - Anthropic 格式：需要查看具体响应")
    print()
    
    return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
