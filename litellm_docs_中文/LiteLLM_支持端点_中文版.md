# LiteLLM 支持的API端点

> 原文: https://docs.litellm.ai/docs/supported_endpoints

LiteLLM支持多种API端点，覆盖各种大语言模型使用场景。

---

## 聊天完成 (Chat Completions)

### 标准请求

```bash
curl -X POST 'http://localhost:4000/v1/chat/completions' \
  -H 'Authorization: Bearer sk-1234' \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "gpt-4o",
    "messages": [
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": "Hello!"}
    ],
    "temperature": 0.7,
    "max_tokens": 1000
  }'
```

### 流式响应

```bash
curl -X POST 'http://localhost:4000/v1/chat/completions' \
  -H 'Authorization: Bearer sk-1234' \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "gpt-4o",
    "messages": [{"role": "user", "content": "Hello!"}],
    "stream": true
  }'
```

---

## 嵌入 (Embeddings)

```bash
curl -X POST 'http://localhost:4000/v1/embeddings' \
  -H 'Authorization: Bearer sk-1234' \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "text-embedding-3-small",
    "input": "The quick brown fox jumps over the lazy dog"
  }'
```

---

## 图像生成 (Image Generation)

```bash
curl -X POST 'http://localhost:4000/v1/images/generations' \
  -H 'Authorization: Bearer sk-1234' \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "dall-e-3",
    "prompt": "A beautiful sunset over the ocean",
    "n": 1,
    "size": "1024x1024"
  }'
```

---

## 语音转文字 (Audio Transcription)

```bash
curl -X POST 'http://localhost:4000/v1/audio/transcriptions' \
  -H 'Authorization: Bearer sk-1234' \
  -F 'file=@audio.mp3' \
  -F 'model="whisper-1"'
```

---

## 文字转语音 (Audio Speech)

```bash
curl -X POST 'http://localhost:4000/v1/audio/speech' \
  -H 'Authorization: Bearer sk-1234' \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "tts-1",
    "input": "Hello, world!",
    "voice": "alloy"
  }'
```

---

## 审核 (Moderations)

```bash
curl -X POST 'http://localhost:4000/v1/moderations' \
  -H 'Authorization: Bearer sk-1234' \
  -H 'Content-Type: application/json' \
  -d '{
    "input": "I want to hurt someone"
  }'
```

---

## 批量处理 (Batches)

```bash
curl -X POST 'http://localhost:4000/v1/batches' \
  -H 'Authorization: Bearer sk-1234' \
  -H 'Content-Type: application/json' \
  -d '{
    "input_file_id": "file-xxx",
    "endpoint": "/v1/chat/completions",
    "completion_window": "24h"
  }'
```

---

## 重排序 (Rerank)

```bash
curl -X POST 'http://localhost:4000/v1/rerank' \
  -H 'Authorization: Bearer sk-1234' \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "cohere-rerank-3",
    "query": "What is the capital of France?",
    "documents": ["Paris is the capital of France.", "London is the capital of England."],
    "top_n": 1
  }'
```

---

## 支持的模型类型

| 端点 | 支持的模型 |
|------|------------|
| /chat/completions | GPT-4, Claude, Gemini, Llama等 |
| /embeddings | text-embedding-3, Cohere等 |
| /images/generations | DALL-E, Stable Diffusion |
| /audio/transcriptions | Whisper |
| /audio/speech | TTS-1 |
| /moderations | OpenAI Moderation |
| /batches | GPT-4, Claude |
| /rerank | Cohere Rerank |

---

## 更多信息

- [提供商列表](./LiteLLM_支持提供商_中文版.md)
- [配置文档](./LiteLLM_Config配置.md)
