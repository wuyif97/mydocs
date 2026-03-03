# ============================================
# Claude Code + LiteLLM 一键启动脚本
# ============================================

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Claude Code + LiteLLM 启动脚本" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# ============================================
# 配置区域（请根据实际情况修改）
# ============================================
$MODEL_NAME = "qwen-72b"                      # 模型名称
$API_BASE = "http://192.168.1.100:8000/v1"   # 内网模型 API 地址
$API_KEY = "sk-local-key"                     # API Key
$LITELLM_PORT = 4000                          # LiteLLM 端口
# ============================================

Write-Host "📋 配置信息:" -ForegroundColor Yellow
Write-Host "  模型：$MODEL_NAME"
Write-Host "  API 地址：$API_BASE"
Write-Host "  API Key: $API_KEY"
Write-Host "  LiteLLM 端口：$LITELLM_PORT"
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

# 检查 Claude Code
Write-Host "🔍 检查 Claude Code 安装..." -ForegroundColor Yellow
try {
    $claudeVersion = claude --version 2>&1
    Write-Host "✅ Claude Code: $claudeVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Claude Code 未安装" -ForegroundColor Red
    Write-Host ""
    Write-Host "请先安装 Claude Code:" -ForegroundColor Yellow
    Write-Host "  npm install -g @anthropic-ai/claude-code" -ForegroundColor White
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "选择启动模式:" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "1. 标准模式（推荐）"
Write-Host "2. 后台模式（适合长时间使用）"
Write-Host "3. 测试连接"
Write-Host "4. 停止服务"
Write-Host "5. 退出"
Write-Host ""

$choice = Read-Host "请输入选项 (1-5)"

switch ($choice) {
    "1" {
        # 标准模式：前台启动 LiteLLM
        
        Write-Host ""
        Write-Host "🚀 启动流程:" -ForegroundColor Green
        Write-Host "  1. 启动 LiteLLM Proxy" -ForegroundColor White
        Write-Host "  2. 设置环境变量" -ForegroundColor White
        Write-Host "  3. 启动 Claude Code" -ForegroundColor White
        Write-Host ""
        
        # 清理旧进程
        Get-Job | Where-Object { $_.Name -like "*litellm*" } | ForEach-Object {
            Write-Host "🛑 停止旧进程：$($_.Name)" -ForegroundColor Yellow
            Stop-Job $_
            Remove-Job $_
        }
        
        # 启动 LiteLLM（后台 Job）
        Write-Host "🚀 启动 LiteLLM Proxy..." -ForegroundColor Green
        $litellmJob = Start-Job -ScriptBlock {
            param($model, $base, $key, $port)
            litellm --model $model --api_base $base --api_key $key --port $port
        } -ArgumentList $MODEL_NAME, $API_BASE, $API_KEY, $LITELLM_PORT -Name "LiteLLM-Claude"
        
        Write-Host "⏳ 等待服务启动..." -ForegroundColor Yellow
        Start-Sleep -Seconds 5
        
        # 验证服务
        try {
            $health = Invoke-RestMethod -Uri "http://localhost:$LITELLM_PORT/health" -Method Get -ErrorAction Stop
            Write-Host "✅ LiteLLM 运行正常" -ForegroundColor Green
        } catch {
            Write-Host "⚠️  LiteLLM 可能还在启动中..." -ForegroundColor Yellow
        }
        
        # 设置环境变量（当前进程）
        Write-Host ""
        Write-Host "🔧 设置环境变量..." -ForegroundColor Yellow
        $env:ANTHROPIC_BASE_URL = "http://localhost:$LITELLM_PORT"
        $env:ANTHROPIC_API_KEY = "sk-anthropic-key"
        
        Write-Host "  ANTHROPIC_BASE_URL=http://localhost:$LITELLM_PORT" -ForegroundColor Cyan
        Write-Host "  ANTHROPIC_API_KEY=sk-anthropic-key" -ForegroundColor Cyan
        
        # 启动 Claude Code
        Write-Host ""
        Write-Host "🚀 启动 Claude Code..." -ForegroundColor Green
        Write-Host "💡 在 Claude Code 中使用模型：$MODEL_NAME" -ForegroundColor Yellow
        Write-Host "🛑 按 Ctrl+C 退出 Claude Code，然后会询问是否停止 LiteLLM" -ForegroundColor Yellow
        Write-Host ""
        
        # 启动 Claude Code
        claude
        
        # Claude Code 退出后，询问是否停止 LiteLLM
        Write-Host ""
        $stopLiteLLM = Read-Host "是否停止 LiteLLM Proxy? (y/n)"
        if ($stopLiteLLM -eq 'y' -or $stopLiteLLM -eq 'Y') {
            Write-Host "🛑 停止 LiteLLM..." -ForegroundColor Yellow
            Stop-Job $litellmJob
            Remove-Job $litellmJob
            Write-Host "✅ 已停止所有服务" -ForegroundColor Green
        } else {
            Write-Host "ℹ️  LiteLLM 仍在后台运行" -ForegroundColor Cyan
            Write-Host "   运行 '.\start-claude-with-litellm.ps1' 选择选项 4 来停止" -ForegroundColor White
        }
    }
    
    "2" {
        # 后台模式：完全后台运行
        
        Write-Host ""
        Write-Host "🚀 启动后台模式..." -ForegroundColor Green
        
        # 清理旧进程
        Get-Job | Where-Object { $_.Name -like "*litellm*" } | ForEach-Object {
            Write-Host "🛑 停止旧进程：$($_.Name)" -ForegroundColor Yellow
            Stop-Job $_
            Remove-Job $_
        }
        
        # 启动 LiteLLM
        $litellmJob = Start-Job -ScriptBlock {
            param($model, $base, $key, $port)
            litellm --model $model --api_base $base --api_key $key --port $port
        } -ArgumentList $MODEL_NAME, $API_BASE, $API_KEY, $LITELLM_PORT -Name "LiteLLM-Claude-Background"
        
        Write-Host "⏳ 等待服务启动..." -ForegroundColor Yellow
        Start-Sleep -Seconds 5
        
        # 验证
        try {
            $health = Invoke-RestMethod -Uri "http://localhost:$LITELLM_PORT/health" -Method Get -ErrorAction Stop
            Write-Host "✅ LiteLLM 已在后台启动" -ForegroundColor Green
        } catch {
            Write-Host "⚠️  服务可能还在启动中..." -ForegroundColor Yellow
        }
        
        # 设置永久环境变量（当前会话）
        Write-Host ""
        Write-Host "🔧 设置环境变量..." -ForegroundColor Yellow
        [Environment]::SetEnvironmentVariable("ANTHROPIC_BASE_URL", "http://localhost:$LITELLM_PORT", "Process")
        [Environment]::SetEnvironmentVariable("ANTHROPIC_API_KEY", "sk-anthropic-key", "Process")
        
        Write-Host "  ANTHROPIC_BASE_URL=http://localhost:$LITELLM_PORT" -ForegroundColor Cyan
        Write-Host "  ANTHROPIC_API_KEY=sk-anthropic-key" -ForegroundColor Cyan
        
        Write-Host ""
        Write-Host "✅ 全部启动完成！" -ForegroundColor Green
        Write-Host ""
        Write-Host "💡 使用方式:" -ForegroundColor Cyan
        Write-Host "  - 直接运行 'claude' 即可使用" -ForegroundColor White
        Write-Host "  - 查看日志：Get-Job -Id $($litellmJob.Id) | Receive-Job" -ForegroundColor White
        Write-Host "  - 停止服务：Stop-Job -Id $($litellmJob.Id); Remove-Job -Id $($litellmJob.Id)" -ForegroundColor White
        Write-Host ""
    }
    
    "3" {
        # 测试连接
        
        Write-Host ""
        Write-Host "🧪 测试完整连接..." -ForegroundColor Yellow
        Write-Host ""
        
        # 1. 测试内网模型直连
        Write-Host "1️⃣ 测试内网模型直连..." -ForegroundColor Cyan
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
            
            Write-Host "   ✅ 内网模型连接成功" -ForegroundColor Green
        } catch {
            Write-Host "   ❌ 内网模型连接失败" -ForegroundColor Red
            Write-Host "      错误：$_" -ForegroundColor Red
            Write-Host ""
            Write-Host "   请检查:" -ForegroundColor Yellow
            Write-Host "     - 内网模型服务是否运行" -ForegroundColor White
            Write-Host "     - API 地址是否正确" -ForegroundColor White
            Write-Host "     - 网络连通性" -ForegroundColor White
        }
        
        # 2. 测试 LiteLLM
        Write-Host ""
        Write-Host "2️⃣ 启动临时 LiteLLM 实例测试..." -ForegroundColor Cyan
        
        $testPort = $LITELLM_PORT + 1000
        $testJob = Start-Job -ScriptBlock {
            param($model, $base, $key, $port)
            litellm --model $model --api_base $base --api_key $key --port $port
        } -ArgumentList $MODEL_NAME, $API_BASE, $API_KEY, $testPort
        
        Start-Sleep -Seconds 5
        
        try {
            $health = Invoke-RestMethod -Uri "http://localhost:$testPort/health" -Method Get -TimeoutSec 5
            Write-Host "   ✅ LiteLLM代理正常" -ForegroundColor Green
            
            # 测试模型列表
            $models = Invoke-RestMethod -Uri "http://localhost:$testPort/v1/models" -Method Get -TimeoutSec 5
            Write-Host "   📦 可用模型：" -ForegroundColor Yellow
            $models.data | ForEach-Object {
                Write-Host "      - $($_.id)" -ForegroundColor White
            }
        } catch {
            Write-Host "   ⚠️  LiteLLM 测试中..." -ForegroundColor Yellow
        } finally {
            Stop-Job $testJob
            Remove-Job $testJob
        }
        
        # 3. 总结
        Write-Host ""
        Write-Host "📊 测试总结:" -ForegroundColor Cyan
        Write-Host "  如果上面都成功，可以运行选项 1 或 2 启动服务" -ForegroundColor White
    }
    
    "4" {
        # 停止服务
        
        Write-Host ""
        Write-Host "🛑 停止所有 LiteLLM 服务..." -ForegroundColor Yellow
        
        $jobs = Get-Job | Where-Object { $_.Name -like "*litellm*" -or $_.Name -like "*LiteLLM*" }
        
        if ($jobs) {
            foreach ($job in $jobs) {
                Write-Host "停止作业：$($job.Name) (ID: $($job.Id))" -ForegroundColor Yellow
                Stop-Job $job
                Remove-Job $job
            }
            Write-Host "✅ 所有 LiteLLM 服务已停止" -ForegroundColor Green
        } else {
            Write-Host "ℹ️  未发现运行中的 LiteLLM 服务" -ForegroundColor Cyan
        }
        
        # 清除环境变量
        Write-Host ""
        Write-Host "🧹 清除环境变量..." -ForegroundColor Yellow
        Remove-Item Env:\ANTHROPIC_BASE_URL -ErrorAction SilentlyContinue
        Remove-Item Env:\ANTHROPIC_API_KEY -ErrorAction SilentlyContinue
        Write-Host "✅ 环境变量已清除" -ForegroundColor Green
    }
    
    "5" {
        Write-Host "👋 再见！" -ForegroundColor Yellow
        exit
    }
    
    default {
        Write-Host "❌ 无效选项" -ForegroundColor Red
    }
}
