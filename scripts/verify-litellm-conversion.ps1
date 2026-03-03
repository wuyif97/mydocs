# LiteLLM 格式转换验证脚本

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "LiteLLM 格式转换能力验证" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 步骤 1：启动 LiteLLM Proxy（模拟 Anthropic 服务端）
Write-Host "📋 测试方案:" -ForegroundColor Yellow
Write-Host "  1. 启动 LiteLLM Proxy (使用 Ollama 作为后端)" -ForegroundColor White
Write-Host "  2. 用 Anthropic SDK 连接 LiteLLM" -ForegroundColor White
Write-Host "  3. 验证是否能正常对话" -ForegroundColor White
Write-Host ""

Write-Host "🚀 第一步：检查 Ollama 是否可用..." -ForegroundColor Yellow

# 检查 Ollama
try {
    $ollamaResponse = Invoke-RestMethod -Uri "http://localhost:11434/api/tags" -Method Get -TimeoutSec 5 -ErrorAction Stop
    Write-Host "✅ Ollama 运行正常" -ForegroundColor Green
    $ollamaModels = $ollamaResponse.models | ForEach-Object { $_.name }
    Write-Host "   可用模型：$($ollamaModels -join ', ')" -ForegroundColor Cyan
    
    if ($ollamaModels.Count -eq 0) {
        Write-Host "⚠️  Ollama 没有可用模型，需要先拉取模型" -ForegroundColor Yellow
        Write-Host "   运行：ollama pull qwen2.5-coder:latest" -ForegroundColor White
        exit 1
    }
    
    $testModel = $ollamaModels[0]
    Write-Host "   将使用模型：$testModel" -ForegroundColor Cyan
} catch {
    Write-Host "❌ Ollama 未运行或无法访问" -ForegroundColor Red
    Write-Host "   错误：$_" -ForegroundColor Red
    Write-Host ""
    Write-Host "💡 替代方案：使用真实的 OpenAI API 测试" -ForegroundColor Yellow
    Write-Host "   需要设置 OPENAI_API_KEY 环境变量" -ForegroundColor White
    exit 1
}

Write-Host ""
Write-Host "🚀 第二步：启动 LiteLLM Proxy..." -ForegroundColor Yellow

# 停止旧的 LiteLLM 进程
Get-Job | Where-Object { $_.Name -like "*litellm*" } | ForEach-Object {
    Write-Host "🛑 停止旧进程：$($_.Name)" -ForegroundColor Yellow
    Stop-Job $_
    Remove-Job $_
}

# 启动 LiteLLM（后台）
$litellmJob = Start-Job -ScriptBlock {
    param($model, $port)
    Write-Host "Starting LiteLLM with model: $model on port $port..."
    litellm --model "ollama/$model" --port $port --set_verbose
} -ArgumentList $testModel, 4000 -Name "LiteLLM-Test"

Write-Host "⏳ 等待 LiteLLM 启动..." -ForegroundColor Yellow
Start-Sleep -Seconds 8

# 验证 LiteLLM 是否运行
try {
    $health = Invoke-RestMethod -Uri "http://localhost:4000/health" -Method Get -TimeoutSec 5 -ErrorAction Stop
    Write-Host "✅ LiteLLM Proxy 运行正常" -ForegroundColor Green
} catch {
    Write-Host "❌ LiteLLM Proxy 启动失败" -ForegroundColor Red
    Write-Host "   错误：$_" -ForegroundColor Red
    Write-Host ""
    Write-Host "📝 查看日志:" -ForegroundColor Yellow
    Get-Job -Id $litellmJob.Id | Receive-Job
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "选择验证方式:" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "1. 使用 OpenAI SDK 测试 (验证基本功能)"
Write-Host "2. 使用 Anthropic SDK 测试 (验证格式转换) ⭐"
Write-Host "3. 使用 cURL 测试 (原始 HTTP)"
Write-Host "4. 退出"
Write-Host ""

$choice = Read-Host "请输入选项 (1-4)"

switch ($choice) {
    "1" {
        # 测试 1：OpenAI SDK
        Write-Host ""
        Write-Host "🧪 使用 OpenAI SDK 测试..." -ForegroundColor Yellow
        
        $testCode = @"
from openai import OpenAI

client = OpenAI(
    api_key="sk-test",
    base_url="http://localhost:4000"
)

print("正在发送请求...")
response = client.chat.completions.create(
    model="ollama/$testModel",
    messages=[{"role": "user", "content": "你好，请用一句话介绍你自己"}],
    max_tokens=100
)

print("✅ 收到响应!")
print(f"内容：{response.choices[0].message.content}")
"@
        
        $testCode | Out-File -FilePath "$PSScriptRoot\test_openai.py" -Encoding utf8
        Write-Host "📝 测试脚本已创建：test_openai.py" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "🚀 运行测试..." -ForegroundColor Green
        python "$PSScriptRoot\test_openai.py"
    }
    
    "2" {
        # 测试 2：Anthropic SDK
        Write-Host ""
        Write-Host "🧪 使用 Anthropic SDK 测试 (关键测试!)..." -ForegroundColor Yellow
        Write-Host "这将验证 LiteLLM 是否能将 Anthropic 格式转换为 OpenAI 格式" -ForegroundColor Cyan
        Write-Host ""
        
        # 检查是否安装了 anthropic
        Write-Host "🔍 检查 Anthropic SDK..." -ForegroundColor Yellow
        try {
            $null = python -c "import anthropic" 2>&1
            Write-Host "✅ Anthropic SDK 已安装" -ForegroundColor Green
        } catch {
            Write-Host "⚠️  Anthropic SDK 未安装" -ForegroundColor Yellow
            Write-Host "正在安装..." -ForegroundColor Yellow
            pip install anthropic
        }
        
        $testCode = @"
import anthropic

# 配置客户端连接到 LiteLLM Proxy
client = anthropic.Anthropic(
    api_key="sk-test-key",
    base_url="http://localhost:4000"
)

print("🚀 正在发送 Anthropic 格式请求到 LiteLLM...")
print("   如果 LiteLLM 能自动转换格式，应该能收到 OpenAI 后端的响应")
print("")

try:
    message = client.messages.create(
        model="$testModel",  # LiteLLM 会识别这个模型名
        max_tokens=1024,
        messages=[
            {"role": "user", "content": "你好，请用一句话介绍你自己"}
        ]
    )
    print("✅ 成功收到响应!")
    print(f"内容：{message.content[0].text}")
except Exception as e:
    print(f"❌ 请求失败：{e}")
    import traceback
    traceback.print_exc()
"@
        
        $testCode | Out-File -FilePath "$PSScriptRoot\test_anthropic.py" -Encoding utf8
        Write-Host "📝 测试脚本已创建：test_anthropic.py" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "🚀 运行测试..." -ForegroundColor Green
        python "$PSScriptRoot\test_anthropic.py"
        
        Write-Host ""
        Write-Host "📊 测试结果分析:" -ForegroundColor Cyan
        Write-Host "  ✅ 如果成功 → LiteLLM 确实能自动转换格式!" -ForegroundColor Green
        Write-Host "  ❌ 如果失败 → 可能需要额外配置或 Transformer" -ForegroundColor Yellow
    }
    
    "3" {
        # 测试 3：cURL
        Write-Host ""
        Write-Host "🧪 使用 cURL 测试..." -ForegroundColor Yellow
        
        Write-Host "`n--- OpenAI 格式测试 ---" -ForegroundColor Cyan
        curl http://localhost:4000/v1/chat/completions `
          -H "Content-Type: application/json" `
          -d '{
            "model": "ollama/$testModel",
            "messages": [{"role": "user", "content": "Hello"}],
            "max_tokens": 50
          }'
        
        Write-Host "`n`n--- Anthropic 格式测试 ---" -ForegroundColor Cyan
        # Anthropic /v1/messages 端点
        curl http://localhost:4000/v1/messages `
          -X POST `
          -H "Content-Type: application/json" `
          -H "x-api-key: sk-test" `
          -d '{
            "model": "$testModel",
            "max_tokens": 1024,
            "messages": [{"role": "user", "content": "Hello"}]
          }'
    }
    
    "4" {
        Write-Host "👋 再见!" -ForegroundColor Yellow
        exit
    }
    
    default {
        Write-Host "❌ 无效选项" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "清理提示:" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "测试完成后，可以运行以下命令停止 LiteLLM:" -ForegroundColor White
Write-Host "  Stop-Job -Id $($litellmJob.Id); Remove-Job -Id $($litellmJob.Id)" -ForegroundColor Gray
Write-Host ""
