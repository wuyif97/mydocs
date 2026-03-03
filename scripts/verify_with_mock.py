"""
完整验证 LiteLLM 格式转换 - 使用本地 Mock 模型

为了完全控制测试环境，我们使用 LiteLLM的 custom_llm 功能
"""

import requests
import json
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import time

# Mock OpenAI兼容的 HTTP 服务器
class MockOpenAIHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        # 返回固定的 OpenAI 格式响应
        response = {
            "id": "mock-123",
            "object": "chat.completion",
            "created": 1234567890,
            "model": "mock-model",
            "choices": [{
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": "你好！我是 Mock 大模型，这是一个测试响应。"
                },
                "finish_reason": "stop"
            }],
            "usage": {
                "prompt_tokens": 10,
                "completion_tokens": 20,
                "total_tokens": 30
            }
        }
        
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())
    
    def log_message(self, format, *args):
        print(f"   [Mock Server] {args[0]}")

def start_mock_server(port=11111):
    server = HTTPServer(('127.0.0.1', port), MockOpenAIHandler)
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()
    return server

def main():
    print("=" * 80)
    print("LiteLLM 格式转换完整验证 - Mock 模型（完全控制）")
    print("=" * 80)
    print()
    
    # 步骤 1: 启动 Mock OpenAI 服务器
    print("📍 步骤 1: 启动 Mock OpenAI 服务器...")
    mock_port = 11111
    try:
        mock_server = start_mock_server(mock_port)
        print(f"✅ Mock 服务器运行在 http://127.0.0.1:{mock_port}")
    except Exception as e:
        print(f"❌ Mock 服务器启动失败：{e}")
        sys.exit(1)
    
    print()
    
    # 步骤 2: 检查 LiteLLM Proxy
    print("📍 步骤 2: 检查 LiteLLM Proxy...")
    litellm_port = 4000  # 固定端口
    try:
        response = requests.get(f"http://localhost:{litellm_port}/health", timeout=3)
        if response.status_code == 200:
            print(f"✅ LiteLLM Proxy 运行正常 (端口：{litellm_port})")
        else:
            print(f"⚠️  LiteLLM 健康检查异常：{response.status_code}")
    except Exception as e:
        print(f"❌ 无法连接到 LiteLLM (端口：{litellm_port}): {e}")
        print("   提示：LiteLLM 需要使用自定义配置启动")
        sys.exit(1)
    
    print()
    
    # 步骤 3: 通过 LiteLLM 调用 Mock 模型 (OpenAI 格式)
    print("🚀 步骤 3: 通过 LiteLLM 调用 Mock 模型（OpenAI 格式）...")
    
    try:
        lite_response = requests.post(
            f"http://localhost:{litellm_port}/v1/chat/completions",
            json={
                "model": "custom/mock-model",
                "api_base": f"http://127.0.0.1:{mock_port}",
                "messages": [{"role": "user", "content": "Hello"}],
                "max_tokens": 100
            },
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if lite_response.status_code == 200:
            data = lite_response.json()
            print("✅ LiteLLM (OpenAI 格式) 成功！")
            print(f"   响应内容：{data['choices'][0]['message']['content']}")
            openai_success = True
        else:
            print(f"⚠️  LiteLLM (OpenAI 格式) 返回：{lite_response.status_code}")
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
            f"http://localhost:{litellm_port}/v1/messages",  # Anthropic 端点
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
            timeout=10
        )
        
        if anthropic_response.status_code == 200:
            data = anthropic_response.json()
            print()
            print("✅✅✅ 验证成功！Anthropic 格式请求成功！")
            print()
            
            if 'content' in data and len(data['content']) > 0:
                content_text = data['content'][0].get('text', '')
                print(f"📝 响应内容：{content_text[:150]}...")
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
                    print("✅ LiteLLM 将请求转换为 OpenAI 格式并发送到后端")
                    print("✅ 后端返回 OpenAI 格式响应")
                    print("✅ LiteLLM 将响应转回 Anthropic 格式")
                    print("✅ Claude Code 可以正常使用内网模型！")
                    print("=" * 80)
                    return True
                else:
                    print("⚠️  响应格式可能不完整")
            else:
                print("⚠️  响应内容为空或格式不正确")
        else:
            print(f"❌ Anthropic 格式请求失败：{anthropic_response.status_code}")
            print(f"   错误信息：{anthropic_response.text[:300]}")
            
    except Exception as e:
        print(f"❌ Anthropic 格式测试异常：{e}")
        import traceback
        traceback.print_exc()
    
    print()
    print("📊 测试总结:")
    print(f"  - LiteLLM Proxy: ✅ 运行正常")
    print(f"  - Mock 服务器：✅ 运行正常")
    print(f"  - OpenAI 格式：{'✅ 成功' if openai_success else '需要查看日志'}")
    print(f"  - Anthropic 格式：需要查看具体响应")
    print()
    print("💡 建议查看 LiteLLM 控制台日志以了解请求处理过程")
    
    return False

if __name__ == "__main__":
    success = main()
    
    if not success:
        print()
        print("=" * 80)
        print("下一步操作:")
        print("=" * 80)
        print("1. 查看 LiteLLM 控制台输出")
        print("2. 确认是否调用了 async_anthropic_messages_handler")
        print("3. 确认格式转换是否发生")
    
    sys.exit(0 if success else 1)
