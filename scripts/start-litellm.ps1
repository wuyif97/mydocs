# ============================================
# LiteLLM + 内网大模型快速启动脚本
# ============================================

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "LiteLLM + 内网大模型启动脚本" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# ============================================
# 配置区域（请根据实际情况修改）
# ============================================
$LOCAL_MODEL_NAME = "qwen-72b"                    # 你的模型名称
$LOCAL_MODEL_API_BASE = "http://192.168.1.100:8000/v1"  # 内网模型 API 地址
$LOCAL_MODEL_API_KEY = "sk-local-key"            # API Key（如无认证可随意填写）
$LITELLM_PORT = 4000                              # LiteLLM代理端口
# ============================================

Write-Host "📋 配置信息:" -ForegroundColor Yellow
Write-Host "  模型名称：$LOCAL_MODEL_NAME"
Write-Host "  API 地址：$LOCAL_MODEL_API_BASE"
Write-Host "  API Key: $LOCAL_MODEL_API_KEY"
Write-Host "  LiteLLM 端口：$LITELLM_PORT"
Write-Host ""

# 检查是否安装了 LiteLLM
Write-Host "🔍 检查 LiteLLM 安装..." -ForegroundColor Yellow
try {
    $litellmVersion = litellm --version 2>&1
    Write-Host "✅ LiteLLM 已安装：$litellmVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ LiteLLM 未安装" -ForegroundColor Red
    Write-Host ""
    Write-Host "正在安装 LiteLLM..." -ForegroundColor Yellow
    pip install 'litellm[proxy]'
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ LiteLLM 安装成功" -ForegroundColor Green
    } else {
        Write-Host "❌ LiteLLM 安装失败，请先手动安装：pip install 'litellm[proxy]'" -ForegroundColor Red
        exit 1
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "选择启动模式:" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "1. 仅启动 LiteLLM代理"
Write-Host "2. 启动 LiteLLM + Claude Code Router"
Write-Host "3. 测试内网模型连接"
Write-Host "4. 退出"
Write-Host ""

$choice = Read-Host "请输入选项 (1-4)"

switch ($choice) {
    "1" {
        # 模式 1：仅启动 LiteLLM
        Write-Host ""
        Write-Host "🚀 启动 LiteLLM代理..." -ForegroundColor Green
        Write-Host "监听地址：http://0.0.0.0:$LITELLM_PORT" -ForegroundColor Cyan
        Write-Host "按 Ctrl+C 停止服务" -ForegroundColor Yellow
        Write-Host ""
        
        litellm `
          --model "openai/$LOCAL_MODEL_NAME" `
          --api_base $LOCAL_MODEL_API_BASE `
          --api_key $LOCAL_MODEL_API_KEY `
          --port $LITELLM_PORT
    }
    
    "2" {
        # 模式 2：启动 LiteLLM + CCR
        
        Write-Host ""
        Write-Host "📝 正在创建 CCR 配置文件..." -ForegroundColor Yellow
        
        $configPath = "$env:APPDATA\.claude-code-router"
        if (!(Test-Path $configPath)) {
            New-Item -ItemType Directory -Force -Path $configPath | Out-Null
        }
        
        $configJson = @"
{
  "Providers": [
    {
      "name": "litellm-proxy",
      "api_base_url": "http://localhost:$LITELLM_PORT/v1/chat/completions",
      "api_key": "$LOCAL_MODEL_API_KEY",
      "models": ["openai/$LOCAL_MODEL_NAME"]
    }
  ],
  
  "Router": {
    "default": "litellm-proxy,openai/$LOCAL_MODEL_NAME",
    "background": "litellm-proxy,openai/$LOCAL_MODEL_NAME",
    "think": "litellm-proxy,openai/$LOCAL_MODEL_NAME",
    "fallback": [
      "litellm-proxy,openai/$LOCAL_MODEL_NAME"
    ]
  }
}
"@
        
        $configJson | Out-File -FilePath "$configPath\config.json" -Encoding utf8
        Write-Host "✅ 配置文件已创建：$configPath\config.json" -ForegroundColor Green
        
        Write-Host ""
        Write-Host "🚀 启动 LiteLLM代理（后台运行）..." -ForegroundColor Green
        
        # 后台启动 LiteLLM
        $litellmJob = Start-Job -ScriptBlock {
            param($model, $apiBase, $apiKey, $port)
            litellm --model $model --api_base $apiBase --api_key $apiKey --port $port
        } -ArgumentList "openai/$LOCAL_MODEL_NAME", $LOCAL_MODEL_API_BASE, $LOCAL_MODEL_API_KEY, $LITELLM_PORT
        
        Write-Host "⏳ 等待 LiteLLM 启动..." -ForegroundColor Yellow
        Start-Sleep -Seconds 5
        
        # 测试 LiteLLM 是否正常
        Write-Host ""
        Write-Host "🧪 测试 LiteLLM 连接..." -ForegroundColor Yellow
        try {
            $response = Invoke-RestMethod `
              -Uri "http://localhost:$LITELLM_PORT/health" `
              -Method Get `
              -ErrorAction Stop
            
            Write-Host "✅ LiteLLM 运行正常" -ForegroundColor Green
        } catch {
            Write-Host "⚠️  LiteLLM 可能还在启动中..." -ForegroundColor Yellow
        }
        
        Write-Host ""
        Write-Host "🚀 启动 Claude Code Router..." -ForegroundColor Green
        ccr start
        
        Write-Host ""
        Write-Host "✅ 全部启动完成！" -ForegroundColor Green
        Write-Host ""
        Write-Host "💡 使用提示:" -ForegroundColor Cyan
        Write-Host "  - 使用 'ccr code' 启动 Claude Code" -ForegroundColor White
        Write-Host "  - 使用 'Stop-Job `$litellmJob' 停止 LiteLLM" -ForegroundColor White
        Write-Host "  - 使用 'ccr stop' 停止 CCR" -ForegroundColor White
        Write-Host ""
    }
    
    "3" {
        # 模式 3：测试内网模型连接
        
        Write-Host ""
        Write-Host "🧪 测试内网模型连接..." -ForegroundColor Yellow
        Write-Host "目标地址：$LOCAL_MODEL_API_BASE" -ForegroundColor Cyan
        Write-Host ""
        
        try {
            $testResponse = Invoke-RestMethod `
              -Uri "$LOCAL_MODEL_API_BASE/chat/completions" `
              -Method Post `
              -Headers @{
                "Content-Type" = "application/json"
                "Authorization" = "Bearer $LOCAL_MODEL_API_KEY"
              } `
              -Body (@{
                model = $LOCAL_MODEL_NAME
                messages = @(@{role = "user"; content = "Hello" })
                max_tokens = 50
              } | ConvertTo-Json) `
              -TimeoutSec 10
            
            Write-Host "✅ 连接成功！" -ForegroundColor Green
            Write-Host "响应预览：" -ForegroundColor Yellow
            Write-Host ($testResponse | ConvertTo-Json -Depth 3).Substring(0, [Math]::Min(200, ($testResponse | ConvertTo-Json -Depth 3).Length))
        } catch {
            Write-Host "❌ 连接失败" -ForegroundColor Red
            Write-Host "错误信息：$_" -ForegroundColor Red
            Write-Host ""
            Write-Host "请检查:" -ForegroundColor Yellow
            Write-Host "  1. 内网模型服务是否运行" -ForegroundColor White
            Write-Host "  2. API 地址是否正确" -ForegroundColor White
            Write-Host "  3. 网络是否连通" -ForegroundColor White
            Write-Host "  4. 防火墙设置" -ForegroundColor White
        }
    }
    
    "4" {
        Write-Host "👋 再见！" -ForegroundColor Yellow
        exit
    }
    
    default {
        Write-Host "❌ 无效选项" -ForegroundColor Red
    }
}
