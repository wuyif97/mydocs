# LiteLLM A2A 代理网关

> 原文: https://docs.litellm.ai/docs/a2a

A2A（Agent-to-Agent）协议网关允许您通过统一接口连接和管理多个AI代理。

---

## 什么是A2A？

A2A是一种代理间通信协议，允许不同的AI代理相互协作。它由Google等公司推动，旨在标准化代理之间的通信方式。

---

## 支持的代理提供商

- LangGraph
- Vertex AI Agent Engine
- Azure AI Foundry
- Bedrock AgentCore
- Pydantic AI

---

## 使用Python SDK

### 第一步：安装依赖

```bash
pip install litellm a2a
```

### 第二步：创建A2A客户端

```python
from litellm.a2a_protocol import A2AClient
from a2a.types import SendMessageRequest, MessageSendParams
from uuid import uuid4

client = A2AClient(base_url="http://localhost:10001")
```

### 第三步：发送消息

```python
request = SendMessageRequest(
    id=str(uuid4()),
    params=MessageSendParams(
        message={
            "role": "user",
            "parts": [{"kind": "text", "text": "Hello!"}],
            "messageId": uuid4().hex,
        }
    )
)

response = await client.send_message(request)
```

---

## 使用AI网关

### 第一步：添加代理到AI网关

在config.yaml中配置：

```yaml
a2a_agents:
  - agent_name: my-agent
    agent_address: http://localhost:10001
```

### 第二步：通过A2A SDK调用

```python
from a2a.client import A2ACardResolver, A2AClient
from a2a.types import MessageSendParams, SendMessageRequest
from uuid import uuid4
import httpx

base_url = "http://localhost:4000/a2a/my-agent"  # LiteLLM代理 + 代理名称
headers = {"Authorization": "Bearer sk-1234"}    # LiteLLM虚拟密钥

async with httpx.AsyncClient(headers=headers) as httpx_client:
    resolver = A2ACardResolver(httpx_client=httpx_client, base_url=base_url)
    agent_card = await resolver.get_agent_card()
    client = A2AClient(httpx_client=httpx_client, agent_card=agent_card)

    request = SendMessageRequest(
        id=str(uuid4()),
        params=MessageSendParams(
            message={
                "role": "user",
                "parts": [{"kind": "text", "text": "Hello!"}],
                "messageId": uuid4().hex,
            }
        )
    )
    response = await client.send_message(request)
```

---

## API端点

### 代理发现

```
GET /a2a/{agent_name}/agent-card
```

### 发送消息

```
POST /a2a/{agent_name}/messages/send
```

### 任务推送

```
POST /a2a/{agent_name}/tasks/push
```

---

## 更多信息

- [A2A协议规范](https://google.github.io/a2a-client/)
- [LiteLLM主文档](https://docs.litellm.ai/docs/)
