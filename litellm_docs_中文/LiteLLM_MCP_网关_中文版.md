# LiteLLM MCP 网关

> 原文: https://docs.litellm.ai/docs/mcp

MCP（Model Context Protocol）网关允许您将MCP服务器连接到任何LLM。

---

## 什么是MCP？

MCP（模型上下文协议）是一种标准化协议，允许AI模型与外部工具和服务进行交互。它类似于OpenAI的函数调用，但提供了一个更通用的标准。

---

## 使用Python SDK

### 安装依赖

```bash
pip install litellm mcp
```

### 桥接MCP工具到OpenAI格式

```python
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from litellm import experimental_mcp_client
import litellm

server_params = StdioServerParameters(
    command="python", 
    args=["mcp_server.py"]
)

async with stdio_client(server_params) as (read, write):
    async with ClientSession(read, write) as session:
        await session.initialize()

        # 以OpenAI格式加载MCP工具
        tools = await experimental_mcp_client.load_mcp_tools(
            session=session, 
            format="openai"
        )

        # 与任何LiteLLM模型一起使用
        response = await litellm.acompletion(
            model="gpt-4o",
            messages=[{"role": "user", "content": "What's 3 + 5?"}],
            tools=tools
        )
```

---

## 使用AI网关

### 第一步：添加MCP服务器到AI网关

在config.yaml中配置：

```yaml
mcp_servers:
  - server_name: github_mcp
    server_path: /path/to/github/mcp/server
    env: {}
```

### 第二步：通过/chat/completions调用

```bash
curl -X POST 'http://0.0.0.0:4000/v1/chat/completions' \
  -H 'Authorization: Bearer sk-1234' \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "gpt-4o",
    "messages": [{"role": "user", "content": "Summarize the latest open PR"}],
    "tools": [{
      "type": "mcp",
      "server_url": "litellm_proxy/mcp/github",
      "server_label": "github_mcp",
      "require_approval": "never"
    }]
  }'
```

---

## 与Cursor IDE集成

```json
{
  "mcpServers": {
    "LiteLLM": {
      "url": "http://localhost:4000/mcp/",
      "headers": {
        "x-litellm-api-key": "Bearer sk-1234"
      }
    }
  }
}
```

---

## 支持的MCP服务器

- GitHub MCP
- Filesystem MCP
- PostgreSQL MCP
- Slack MCP
- Puppeteer MCP
- 以及任何兼容MCP协议的服务器

---

## 常用MCP命令

### 列出可用工具

```python
tools = await session.list_tools()
for tool in tools:
    print(f"- {tool.name}: {tool.description}")
```

### 调用特定工具

```python
result = await session.call_tool(
    "tool_name", 
    {"param1": "value1"}
)
```

---

## 更多信息

- [MCP协议文档](https://modelcontextprotocol.io/)
- [LiteLLM主文档](https://docs.litellm.ai/docs/)
