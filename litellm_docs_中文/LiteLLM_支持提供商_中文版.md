# LiteLLM 支持的提供商

> 原文: https://docs.litellm.ai/docs/providers

LiteLLM支持100+大语言模型提供商，包括：

---

## 支持的API端点

| 端点 | 说明 |
|------|------|
| `/chat/completions` | 聊天完成 |
| `/responses` | 响应 |
| `/embeddings` | 向量嵌入 |
| `/image/generations` | 图像生成 |
| `/audio/transcriptions` | 语音转文字 |
| `/audio/speech` | 文字转语音 |
| `/moderations` | 内容审核 |
| `/batches` | 批量处理 |
| `/rerank` | 重排序 |

---

## 主要提供商列表

### OpenAI
- GPT-4o, GPT-4o-mini
- GPT-4 Turbo
- GPT-4
- GPT-3.5 Turbo
- Embeddings (text-embedding-3-small, text-embedding-3-large)
- DALL-E 3

### Anthropic
- Claude 4 (Sonnet, Opus, Haiku)
- Claude 3.5 Sonnet
- Claude 3 Opus
- Claude 3 Haiku

### Google
- Gemini 2.0 Pro/Flash
- Gemini 1.5 Pro/Flash
- Vertex AI
- PaLM

### Microsoft Azure
- Azure OpenAI
- Azure AI Studio

### Amazon
- Bedrock (Claude, Titan, Llama, Mistral)
- SageMaker

### 开源模型
- Llama 3.1/3/2
- Mistral
- Phi
- Gemma
- Qwen
- DeepSeek
- Yi

### 其他提供商
- Cohere (Command, Embed)
- Groq
- Together AI
- Replicate
- Hugging Face
- Ollama (本地部署)
- LM Studio (本地部署)

---

## 使用示例

### OpenAI

```python
from litellm import completion

response = completion(
    model="openai/gpt-4o",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

### Anthropic

```python
response = completion(
    model="anthropic/claude-sonnet-4-20250514",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

### Azure

```python
response = completion(
    model="azure/gpt-4o",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

### Ollama (本地)

```python
response = completion(
    model="ollama/llama2",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

---

## 环境变量配置

每个提供商需要设置相应的API密钥：

```bash
# OpenAI
OPENAI_API_KEY=sk-...

# Anthropic
ANTHROPIC_API_KEY=sk-ant-...

# Azure
AZURE_API_KEY=...
AZURE_API_BASE=https://your-resource.openai.azure.com/
AZURE_API_VERSION=2024-02-15-preview

# Google
GOOGLE_API_KEY=...

# Cohere
COHERE_API_KEY=...
```

---

## 更多信息

- [完整端点文档](https://docs.litellm.ai/docs/supported_endpoints)
- [模型价格](https://models.litellm.ai/)
- [详细配置](./LiteLLM_Config配置.md)
