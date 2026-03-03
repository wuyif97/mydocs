# LiteLLM 独立使用 - 快速启动脚本
# 不使用 Claude Code Router，仅用 LiteLLM

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "LiteLLM 独立模式启动脚本" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# ============================================
# 配置区域（请根据实际情况修改）
# ============================================
$MODEL_NAME = "qwen-72b"                      # 模型名称
$API_BASE = "http://192.168.1.100:8000/v1"   # 内网模型 API 地址
$API_KEY = "sk-local-key"                     # API Key
$PORT = 4000                                  # 代理端口
# ============================================

Write-Host "📋 配置信息:" -ForegroundColor Yellow
Write-Host "  模型：$MODEL_NAME"
Write-Host "  API 地址：$API_BASE"
Write-Host "  API Key: $API_KEY"
Write-Host "  端口：$PORT"
Write-Host ""

# 检查 Python
Write-Host "🔍 检查 Python 环境..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python 未安装或未添加到 PATH" -ForegroundColor Red
    exit 1
}

# 检查 LiteLLM
Write-Host "🔍 检查 LiteLLM 安装..." -ForegroundColor Yellow
try {
    $litellmVersion = litellm --version 2>&1
    Write-Host "✅ LiteLLM: $litellmVersion" -ForegroundColor Green
} catch {
    Write-Host "⚠️  LiteLLM 未安装" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "正在安装 LiteLLM..." -ForegroundColor Yellow
    pip install 'litellm[proxy]'
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ LiteLLM 安装成功" -ForegroundColor Green
    } else {
        Write-Host "❌ 安装失败，请手动执行：pip install 'litellm[proxy]'" -ForegroundColor Red
        exit 1
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "选择启动模式:" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "1. 前台启动（适合测试）"
Write-Host "2. 后台启动（推荐）"
Write-Host "3. 测试连接"
Write-Host "4. 停止后台服务"
Write-Host "5. 退出"
Write-Host ""

$choice = Read-Host "请输入选项 (1-5)"

switch ($choice) {
    "1" {
        # 前台启动
        Write-Host ""
        Write-Host "🚀 启动 LiteLLM代理（前台模式）..." -ForegroundColor Green
        Write-Host "监听地址：http://0.0.0.0:$PORT" -ForegroundColor Cyan
        Write-Host "按 Ctrl+C 停止服务" -ForegroundColor Yellow
        Write-Host ""
        
        litellm `
          --model $MODEL_NAME `
          --api_base $API_BASE `
          --api_key $API_KEY `
          --port $PORT
    }
    
    "2" {
        # 后台启动
        Write-Host ""
        Write-Host "🚀 启动 LiteLLM代理（后台模式）..." -ForegroundColor Green
        
        # 检查是否已有进程在运行
        $existingJob = Get-Job | Where-Object { $_.Name -like "*litellm*" }
        if ($existingJob) {
            Write-Host "⚠️  检测到已有 LiteLLM 进程，先停止..." -ForegroundColor Yellow
            Stop-Job $existingJob
            Remove-Job $existingJob
        }
        
        # 后台启动
        $litellmJob = Start-Job -ScriptBlock {
            param($model, $apiBase, $apiKey, $port)
            Write-Host "Starting LiteLLM..."
            litellm --model $model --api_base $apiBase --api_key $apiKey --port $port
        } -ArgumentList $MODEL_NAME, $API_BASE, $API_KEY, $PORT -Name "LiteLLM-$PORT"
        
        Write-Host "⏳ 等待服务启动..." -ForegroundColor Yellow
        Start-Sleep -Seconds 5
        
        # 检查服务状态
        if ((Get-Job -Id $litellmJob.Id).State -eq "Running") {
            Write-Host "✅ LiteLLM 已在后台启动" -ForegroundColor Green
            Write-Host ""
            Write-Host "💡 使用方式:" -ForegroundColor Cyan
            Write-Host "  Python 示例:" -ForegroundColor White
            Write-Host "  from openai import OpenAI" -ForegroundColor Gray
            Write-Host "  client = OpenAI(api_key='$API_KEY', base_url='http://localhost:$PORT')" -ForegroundColor Gray
            Write-Host "  response = client.chat.completions.create(model='$MODEL_NAME', messages=[{'role': 'user', 'content': '你好'}])" -ForegroundColor Gray
            Write-Host ""
            Write-Host "  cURL 示例:" -ForegroundColor White
            Write-Host "  curl http://localhost:$PORT/v1/chat/completions -d '{`"model`": `"$MODEL_NAME`", `"messages`": [{`"role`": `"user`", `"content`": `"你好`"}]}'" -ForegroundColor Gray
            Write-Host ""
            Write-Host "🛠️  管理命令:" -ForegroundColor Cyan
            Write-Host "  查看日志：Get-Job -Id $($litellmJob.Id) | Receive-Job" -ForegroundColor White
            Write-Host "  停止服务：Stop-Job -Id $($litellmJob.Id); Remove-Job -Id $($litellmJob.Id)" -ForegroundColor White
        } else {
            Write-Host "❌ 启动失败，请检查配置和日志" -ForegroundColor Red
            Write-Host "日志：" -ForegroundColor Yellow
            Get-Job -Id $litellmJob.Id | Receive-Job
        }
    }
    
    "3" {
        # 测试连接
        Write-Host ""
        Write-Host "🧪 测试内网模型连接..." -ForegroundColor Yellow
        Write-Host "目标：$API_BASE" -ForegroundColor Cyan
        Write-Host ""
        
        try {
            $response = Invoke-RestMethod `
              -Uri "$API_BASE/chat/completions" `
              -Method Post `
              -Headers @{
                "Content-Type" = "application/json"
                "Authorization" = "Bearer $API_KEY"
              } `
              -Body (@{
                model = $MODEL_NAME
                messages = @(@{role = "user"; content = "Hello" })
                max_tokens = 50
              } | ConvertTo-Json) `
              -TimeoutSec 10
            
            Write-Host "✅ 直连成功！" -ForegroundColor Green
            Write-Host "响应预览：" -ForegroundColor Yellow
            $jsonResponse = $response | ConvertTo-Json -Depth 3
            Write-Host $jsonResponse.Substring(0, [Math]::Min(300, $jsonResponse.Length))
        } catch {
            Write-Host "❌ 直连失败" -ForegroundColor Red
            Write-Host "错误：$_" -ForegroundColor Red
            Write-Host ""
            Write-Host "请检查:" -ForegroundColor Yellow
            Write-Host "  1. 内网模型服务是否运行" -ForegroundColor White
            Write-Host "  2. API 地址是否正确" -ForegroundColor White
            Write-Host "  3. 网络连通性" -ForegroundColor White
            Write-Host "  4. 防火墙设置" -ForegroundColor White
        }
        
        Write-Host ""
        Write-Host "🧪 测试 LiteLLM代理..." -ForegroundColor Yellow
        
        # 尝试启动临时 LiteLLM 实例测试
        $testJob = Start-Job -ScriptBlock {
            param($model, $base, $key, $port)
            litellm --model $model --api_base $base --api_key $key --port $port
        } -ArgumentList $MODEL_NAME, $API_BASE, $API_KEY, ($PORT + 1000)
        
        Start-Sleep -Seconds 5
        
        try {
            $healthCheck = Invoke-RestMethod `
              -Uri "http://localhost:$($PORT + 1000)/health" `
              -Method Get `
              -TimeoutSec 5
            
            Write-Host "✅ LiteLLM代理正常" -ForegroundColor Green
        } catch {
            Write-Host "⚠️  LiteLLM 测试中..." -ForegroundColor Yellow
        } finally {
            Stop-Job $testJob
            Remove-Job $testJob
        }
    }
    
    "4" {
        # 停止服务
        Write-Host ""
        Write-Host "🛑 查找并停止 LiteLLM 服务..." -ForegroundColor Yellow
        
        $jobs = Get-Job | Where-Object { $_.Name -like "*litellm*" -or $_.Name -like "*LiteLLM*" }
        
        if ($jobs) {
            foreach ($job in $jobs) {
                Write-Host "停止作业：$($job.Name) (ID: $($job.Id))" -ForegroundColor Yellow
                Stop-Job $job
                Remove-Job $job
            }
            Write-Host "✅ 所有服务已停止" -ForegroundColor Green
        } else {
            Write-Host "ℹ️  未发现运行中的 LiteLLM 服务" -ForegroundColor Cyan
        }
        
        # 也检查是否有残留进程
        $processes = Get-Process | Where-Object { $_.ProcessName -like "*python*" -and $_.CommandLine -like "*litellm*" }
        if ($processes) {
            Write-Host "⚠️  发现残留进程，建议手动结束" -ForegroundColor Yellow
            $processes | ForEach-Object {
                Write-Host "  PID: $($_.Id) - $($_.ProcessName)"
            }
        }
    }
    
    "5" {
        Write-Host "👋 再见！" -ForegroundColor Yellow
        exit
    }
    
    default {
        Write-Host "❌ 无效选项" -ForegroundColor Red
    }
}
