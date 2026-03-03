"""
验证 LiteLLM 是否能自动转换 Anthropic 格式到 OpenAI 格式

测试架构:
Anthropic SDK → LiteLLM Proxy → OpenAI兼容模型
"""

import sys
import time
import subprocess
import threading
from pathlib import Path

def print_banner(text):
    print("\n" + "=" * 60)
    print(text.center(60))
    print("=" * 60 + "\n")

def check_installation():
    """检查必要的包是否已安装"""
    print_banner("步骤 1: 检查环境")
    
    # 检查 litellm
    try:
        import litellm
        print(f"✅ LiteLLM 已安装")
    except ImportError:
        print("❌ LiteLLM 未安装")
        print("   运行：pip install 'litellm[proxy]'")
        return False
    
    # 检查 openai
    try:
        import openai
        print(f"✅ OpenAI SDK 已安装")
    except ImportError:
        print("❌ OpenAI SDK 未安装")
        print("   运行：pip install openai")
        return False
    
    # 检查 anthropic
    try:
        import anthropic
        print(f"✅ Anthropic SDK 已安装")
    except ImportError:
        print("⚠️  Anthropic SDK 未安装 (可选，用于测试格式转换)")
        print("   如要测试格式转换，运行：pip install anthropic")
    
    return True

def start_litellm_proxy():
    """启动 LiteLLM Proxy（使用模拟模式）"""
    print_banner("步骤 2: 启动 LiteLLM Proxy")
    
    # 使用 gpt-3.5-turbo 作为测试模型（LiteLLM 会模拟）
    cmd = [
        "litellm",
        "--model", "gpt-3.5-turbo",
        "--port", "4000",
        "--set_verbose"
    ]
    
    print("🚀 启动命令:", " ".join(cmd))
    print("⏳ 等待服务启动...")
    
    # 后台启动进程
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # 等待 5 秒让服务启动
    time.sleep(5)
    
    # 检查是否成功启动
    import requests
    try:
        response = requests.get("http://localhost:4000/health", timeout=3)
        if response.status_code == 200:
            print("✅ LiteLLM Proxy 启动成功!")
            print(f"   监听地址：http://localhost:4000")
            return process
        else:
            print(f"❌ 健康检查失败：{response.status_code}")
            return None
    except Exception as e:
        print(f"❌ 无法连接到 LiteLLM Proxy: {e}")
        return None

def test_openai_format(process):
    """测试 1: 使用 OpenAI SDK"""
    print_banner("测试 1: OpenAI SDK (标准格式)")
    
    from openai import OpenAI
    
    client = OpenAI(
        api_key="sk-test",
        base_url="http://localhost:4000"
    )
    
    try:
        print("📤 发送 OpenAI 格式请求...")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "你好"}],
            max_tokens=50
        )
        print("✅ OpenAI 格式测试成功!")
        print(f"   响应：{response.choices[0].message.content[:100]}...")
        return True
    except Exception as e:
        print(f"❌ OpenAI 格式测试失败：{e}")
        return False

def test_anthropic_format(process):
    """测试 2: 使用 Anthropic SDK (验证格式转换)"""
    print_banner("测试 2: Anthropic SDK (验证格式转换) ⭐")
    
    try:
        import anthropic
    except ImportError:
        print("⚠️  Anthropic SDK 未安装，跳过此测试")
        return False
    
    # 配置客户端连接到 LiteLLM
    client = anthropic.Anthropic(
        api_key="sk-test-key",
        base_url="http://localhost:4000"
    )
    
    try:
        print("📤 发送 Anthropic 格式请求到 LiteLLM...")
        print("   如果 LiteLLM 能自动转换，应该能收到响应")
        
        message = client.messages.create(
            model="claude-3-sonnet-20240229",  # 使用 Claude 模型名
            max_tokens=1024,
            messages=[
                {"role": "user", "content": "你好，请用一句话介绍你自己"}
            ]
        )
        
        print("✅ Anthropic 格式测试成功!")
        print(f"   响应：{message.content[0].text[:100]}...")
        return True
        
    except Exception as e:
        print(f"❌ Anthropic 格式测试失败：{e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主函数"""
    print_banner("LiteLLM 格式转换能力验证")
    
    # 检查环境
    if not check_installation():
        print("\n❌ 环境检查失败，请先安装必要组件")
        return
    
    # 启动 LiteLLM Proxy
    litellm_process = start_litellm_proxy()
    
    if not litellm_process:
        print("\n❌ LiteLLM Proxy 启动失败")
        return
    
    try:
        # 测试 1: OpenAI 格式
        openai_success = test_openai_format(litellm_process)
        
        # 测试 2: Anthropic 格式
        anthropic_success = test_anthropic_format(litellm_process)
        
        # 总结
        print_banner("测试结果总结")
        print(f"OpenAI 格式测试：  {'✅ 成功' if openai_success else '❌ 失败'}")
        print(f"Anthropic 格式测试:{'✅ 成功' if anthropic_success else '❌ 失败'}")
        print("")
        
        if anthropic_success:
            print("🎉 结论：LiteLLM 确实能自动转换 Anthropic 格式到 OpenAI 格式!")
        else:
            print("⚠️  结论：Anthropic 格式测试失败，可能需要额外配置")
            print("   这可能是因为:")
            print("   1. LiteLLM 不支持自动转换到这个端点")
            print("   2. 需要配置特定的 transformer")
            print("   3. 需要使用 passthrough 模式")
            
    finally:
        # 清理
        print_banner("清理")
        print("🛑 停止 LiteLLM Proxy...")
        litellm_process.terminate()
        litellm_process.wait()
        print("✅ 已停止服务")

if __name__ == "__main__":
    main()
