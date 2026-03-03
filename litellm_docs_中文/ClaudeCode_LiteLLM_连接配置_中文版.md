# Claude Code CLI 通过 LiteLLM 连接 OpenAI 模型 - 完整指南

> 根据LiteLLM官方文档，LiteLLM支持`/v1/messages`端点，可以直接接收Anthropic格式请求！

## 架构概述

```
Claude Code CLI (Anthropic格式 /v1/messages)
        ↓
        LiteLLM 代理 (端口4000)
        ↓
OpenAI 兼容模型 (如 Ollama, Azure OpenAI, 本地模型等)
```

**好消息：不需要CCR中间层！**

## 实现步骤

### 步骤 1：安装 LiteLLM

```bash
# 安装 LiteLLM
pip install 'litellm[proxy]'
```

### 步骤 2：配置 LiteLLM

创建 `config.yaml` 文件：

```yaml
model_list:
  # 配置 Ollama 本地模型
  - model_name: llama3
    litellm_params:
      model: ollama/llama3
      api_base: http://localhost:11434

  # 或者配置 Azure OpenAI
  - model_name: azure-gpt4o
    litellm_params:
      model: azure/azure-gpt-4o
      api_base: https://your-resource.openai.azure.com/
      api_key: os.environ/AZURE_API_KEY

general_settings:
  master_key: sk-123456789
```

### 步骤 3：启动 LiteLLM

```bash
litellm --config config.yaml
```

### 步骤 4：配置 Claude Code

设置环境变量，让 Claude Code 连接到 LiteLLM 的 `/v1/messages` 端点：

```bash
# Linux/Mac
export ANTHROPIC_API_KEY="sk-123456789"
export ANTHROPIC_API_URL="http://localhost:4000/v1/messages"

# Windows PowerShell
$env:ANTHROPIC_API_KEY="sk-123456789"
$env:ANTHROPIC_API_URL="http://localhost:4000/v1/messages"
```

### 步骤 5：验证连接

```bash
# 测试 LiteLLM /v1/messages 端点
curl http://localhost:4000/v1/messages \
  -H "Authorization: Bearer sk-123456789" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama3",
    "messages": [{"role": "user", "content": "Hello!"}],
    "max_tokens": 100
  }'
```

## 关键点

| 端点 | 地址 | 说明 |
|------|------|------|
| `/v1/messages` | http://localhost:4000/v1/messages | **Anthropic格式** (Claude Code使用) |
| `/v1/chat/completions` | http://localhost:4000/v1/chat/completions | OpenAI格式 |

**LiteLLM自动完成格式转换**：Anthropic格式 → 目标模型格式

## 故障排除

1. **认证失败**
   - 确认 `ANTHROPIC_API_KEY` 与 `master_key` 一致
   
2. **模型未找到**
   - 确认模型已在 `config.yaml` 中配置
   - 确认 Ollama 已启动并运行

3. **端口占用**
   - 检查4000端口：`netstat -ano | findstr 4000`

## 总结

✅ **可以直接连接！**
- 只需要设置 `ANTHROPIC_API_URL=http://localhost:4000/v1/messages`
- LiteLLM会自动将Anthropic格式转换为目标模型格式
- 不需要额外的CCR中间层
