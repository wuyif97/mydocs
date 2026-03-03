# 🚅 LiteLLM 中文文档

<p align="center">
    <p align="center">调用100+大语言模型，使用OpenAI格式。[Bedrock、Azure、OpenAI、VertexAI、Anthropic、Groq等]</p>
    <p align="center">
        <a href="https://render.com/deploy?repo=https://github.com/BerriAI/litellm" target="_blank" rel="nofollow">部署到Render</a>
        <a href="https://railway.app/template/HLP0Ub?referralCode=jch2ME">部署到Railway</a>
    </p>
</p>

<h4 align="center">
    <a href="https://docs.litellm.ai/docs/simple_proxy" target="_blank">LiteLLM代理服务器（AI网关）</a> | 
    <a href="https://docs.litellm.ai/docs/enterprise#hosted-litellm-proxy" target="_blank">托管代理</a> | 
    <a href="https://docs.litellm.ai/docs/enterprise"target="_blank">企业版</a>
</h4>

<h4 align="center">
    <a href="https://pypi.org/project/litellm/" target="_blank">PyPI版本</a> | 
    <a href="https://www.ycombinator.com/companies/berriai">Y Combinator W23</a> | 
    <a href="https://discord.gg/wuPM9dRgDw">Discord</a> | 
    <a href="https://www.litellm.ai/support">Slack</a>
</h4>

---

## LiteLLM的用途

<details open>
<summary><b>大语言模型</b> - 调用100+大语言模型（Python SDK + AI网关）</summary>

[**所有支持的端点**](https://docs.litellm.ai/docs/supported_endpoints) - `/chat/completions`、`/responses`、`/embeddings`、`/images`、`/audio`、`/batches`、`/rerank`、`/a2a`、`/messages` 等。

### Python SDK

```bash
pip install litellm
```

```python
from litellm import completion
import os

os.environ["OPENAI_API_KEY"] = "your-openai-key"
os.environ["ANTHROPIC_API_KEY"] = "your-anthropic-key"

# OpenAI
response = completion(model="openai/gpt-4o", messages=[{"role": "user", "content": "Hello!"}])

# Anthropic  
response = completion(model="anthropic/claude-sonnet-4-20250514", messages=[{"role": "user", "content": "Hello!"}])
```

### AI网关（代理服务器）

[**入门 - 端到端教程**](https://docs.litellm.ai/docs/proxy/docker_quick_start) - 设置虚拟密钥，发起第一个请求

```bash
pip install 'litellm[proxy]'
litellm --model gpt-4o
```

```python
import openai

client = openai.OpenAI(api_key="anything", base_url="http://0.0.0.0:4000")
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

[**文档：LLM提供商**](https://docs.litellm.ai/docs/providers)

</details>

<details>
<summary><b>代理（Agents）</b> - 调用A2A代理（Python SDK + AI网关）</summary>

[**支持的提供商**](https://docs.litellm.ai/docs/a2a#add-a2a-agents) - LangGraph、Vertex AI Agent Engine、Azure AI Foundry、Bedrock AgentCore、Pydantic AI

### Python SDK - A2A协议

```python
from litellm.a2a_protocol import A2AClient
from a2a.types import SendMessageRequest, MessageSendParams
from uuid import uuid4

client = A2AClient(base_url="http://localhost:10001")

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

### AI网关（代理服务器）

**第一步。** [将您的代理添加到AI网关](https://docs.litellm.ai/docs/a2a#adding-your-agent)

**第二步。** 通过A2A SDK调用代理

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

[**文档：A2A代理网关**](https://docs.litellm.ai/docs/a2a)

</details>

<details>
<summary><b>MCP工具</b> - 将MCP服务器连接到任何LLM（Python SDK + AI网关）</summary>

### Python SDK - MCP桥接

```python
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from litellm import experimental_mcp_client
import litellm

server_params = StdioServerParameters(command="python", args=["mcp_server.py"])

async with stdio_client(server_params) as (read, write):
    async with ClientSession(read, write) as session:
        await session.initialize()

        # 以OpenAI格式加载MCP工具
        tools = await experimental_mcp_client.load_mcp_tools(session=session, format="openai")

        # 与任何LiteLLM模型一起使用
        response = await litellm.acompletion(
            model="gpt-4o",
            messages=[{"role": "user", "content": "What's 3 + 5?"}],
            tools=tools
        )
```

### AI网关 - MCP网关

**第一步。** [将您的MCP服务器添加到AI网关](https://docs.litellm.ai/docs/mcp#adding-your-mcp)

**第二步。** 通过`/chat/completions`调用MCP工具

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

### 与Cursor IDE一起使用

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

[**文档：MCP网关**](https://docs.litellm.ai/docs/mcp)

</details>

---

## 如何使用LiteLLM

您可以通过代理服务器或Python SDK使用LiteLLM。两者都为您提供统一的界面来访问多个LLM（100+大语言模型）。选择最适合您需求的选项：

| | **LiteLLM AI网关** | **LiteLLM Python SDK** |
|---|---|---|
| **用例** | 访问多个LLM的中心服务（LLM网关） | 在Python代码中直接使用LiteLLM |
| **谁在使用？** | 生成式AI赋能/ML平台团队 | 开发LLM项目的开发者 |
| **主要特点** | 集中式API网关，具有认证和授权、多租户成本跟踪和每项目/用户支出管理、每项目定制（日志、护栏、缓存）、用于安全访问控制的虚拟密钥、用于监控和管理的Admin仪表板UI | 直接Python库集成到您的代码库中、带有跨多个部署重试/回退逻辑的路由器（如Azure/OpenAI）、应用级负载均衡和成本跟踪、具有OpenAI兼容错误的可观测性回调（Lunary、MLflow、Langfuse等） |

LiteLLM性能：**8ms P95延迟**，1k RPS（[查看基准测试](https://docs.litellm.ai/docs/benchmarks)）

[**跳转到LiteLLM代理（LLM网关）文档**](https://docs.litellm.ai/docs/simple_proxy)  
[**跳转到支持的LLM提供商**](https://docs.litellm.ai/docs/providers)

**稳定版本：** 使用带有`-stable`标签的Docker镜像。这些都经过12小时负载测试后才发布。[了解更多发布周期信息](https://docs.litellm.ai/docs/proxy/release_cycle)

支持更多提供商。缺少提供商或LLM平台，请提交[功能请求](https://github.com/BerriAI/litellm/issues/new?assignees=&labels=enhancement&projects=&template=feature_request.yml&title=%5BFeature%5D%3A+)。

## 开源采用者

Netflix、Google ADK、Stripe、Greptile、OpenHands、OpenAI Agents SDK

## 支持的提供商

| 提供商 | `/chat/completions` | `/messages` | `/responses` | `/embeddings` | `/image/generations` | `/audio/transcriptions` | `/audio/speech` | `/moderations` | `/batches` | `/rerank` |
|---|---|---|---|---|---|---|---|---|---|---|
| Abliteration | ✅ | | | | | | | | | |
| AI/ML API | ✅ | ✅ | ✅ | ✅ | ✅ | | | | | |
| AI21 | ✅ | ✅ | ✅ | | | | | | | |
| Aleph Alpha | ✅ | ✅ | ✅ | | | | | | | |
| Amazon Nova | ✅ | ✅ | ✅ | | | | | | | |
| Anthropic | ✅ | ✅ | ✅ | | | | | ✅ | | |
| Anyscale | ✅ | ✅ | ✅ | | | | | | | |
| AssemblyAI | ✅ | ✅ | ✅ | | | ✅ | | | | |
| Auto Router | ✅ | ✅ | ✅ | | | | | | | |
| AWS - Bedrock | ✅ | ✅ | ✅ | ✅ | | | | | | ✅ |
| AWS - Sagemaker | ✅ | ✅ | ✅ | ✅ | | | | | | |
| Azure | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | |
| Azure AI | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | |
| Baseten | ✅ | ✅ | ✅ | | | | | | | |
| Cerebras | ✅ | ✅ | ✅ | | | | | | | |
| Clarifai | ✅ | ✅ | ✅ | | | | | | | |
| Cloudflare AI Workers | ✅ | ✅ | ✅ | | | | | | | |
| Codestral | ✅ | ✅ | ✅ | | | | | | | |
| Cohere | ✅ | ✅ | ✅ | ✅ | | | | | | ✅ |
| CometAPI | ✅ | ✅ | ✅ | ✅ | | | | | | |
| Custom | ✅ | ✅ | ✅ | | | | | | | |
| Custom OpenAI | ✅ | ✅ | ✅ | | | ✅ | ✅ | ✅ | ✅ | |
| Dashscope | ✅ | ✅ | ✅ | | | | | | | |
| Databricks | ✅ | ✅ | ✅ | | | | | | | |
| Deepgram | ✅ | ✅ | ✅ | | | ✅ | | | | |
| DeepInfra | ✅ | ✅ | ✅ | | | | | | | |
| Deepseek | ✅ | ✅ | ✅ | | | | | | | |
| ElevenLabs | ✅ | ✅ | ✅ | | | ✅ | ✅ | | | |
| Fal AI | ✅ | ✅ | ✅ | | ✅ | | | | | |
| Fireworks AI | ✅ | ✅ | ✅ | | | | | | | |
| FriendliAI | ✅ | ✅ | ✅ | | | | | | | |
| GitHub Copilot | ✅ | ✅ | ✅ | ✅ | | | | | | |
| GitHub Models | ✅ | ✅ | ✅ | | | | | | | |
| Google - PaLM | ✅ | ✅ | ✅ | | | | | | | |
| Google - Vertex AI | ✅ | ✅ | ✅ | ✅ | ✅ | | | | | |
| Google AI Studio - Gemini | ✅ | ✅ | ✅ | | | | | | | |
| GradientAI | ✅ | ✅ | ✅ | | | | | | | |
| Groq AI | ✅ | ✅ | ✅ | | | | | | | |
| Heroku | ✅ | ✅ | ✅ | | | | | | | |
| Hosted VLLM | ✅ | ✅ | ✅ | | | | | | | |
| Huggingface | ✅ | ✅ | ✅ | ✅ | | | | | | ✅ |
| Hyperbolic | ✅ | ✅ | ✅ | | | | | | | |
| IBM - Watsonx.ai | ✅ | ✅ | ✅ | ✅ | | | | | | |
| Infinity | | | | ✅ | | | | | | |
| Jina AI | | | | ✅ | | | | | | |
| Lambda AI | ✅ | ✅ | ✅ | | | | | | | |
| Lemonade | ✅ | ✅ | ✅ | | | | | | | |
| LiteLLM Proxy | ✅ | ✅ | ✅ | ✅ | ✅ | | | | | |
| Llamafile | ✅ | ✅ | ✅ | | | | | | | |
| LM Studio | ✅ | ✅ | ✅ | | | | | | | |
| Maritalk | ✅ | ✅ | ✅ | | | | | | | |
| Meta - Llama API | ✅ | ✅ | ✅ | | | | | | | |
| Mistral AI API | ✅ | ✅ | ✅ | ✅ | | | | | | |
| Moonshot | ✅ | ✅ | ✅ | | | | | | | |
| Morph | ✅ | ✅ | ✅ | | | | | | | |
| Nebius AI Studio | ✅ | ✅ | ✅ | ✅ | | | | | | |
| NLP Cloud | ✅ | ✅ | ✅ | | | | | | | |
| Novita AI | ✅ | ✅ | ✅ | | | | | | | |
| Nscale | ✅ | ✅ | ✅ | | | | | | | |
| Nvidia NIM | ✅ | ✅ | ✅ | | | | | | | |
| OCI | ✅ | ✅ | ✅ | | | | | | | |
| Ollama | ✅ | ✅ | ✅ | ✅ | | | | | | |
| Oobabooga | ✅ | ✅ | ✅ | | | ✅ | ✅ | ✅ | ✅ | |
| OpenAI | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | |
| OpenAI-like | | | | ✅ | | | | | | |
| OpenRouter | ✅ | ✅ | ✅ | | | | | | | |
| OVHCloud AI Endpoints | ✅ | ✅ | ✅ | | | | | | | |
| Perplexity AI | ✅ | ✅ | ✅ | | | | | | | |
| Petals | ✅ | ✅ | ✅ | | | | | | | |
| Predibase | ✅ | ✅ | ✅ | | | | | | | |
| Recraft | | | | | ✅ | | | | | |
| Replicate | ✅ | ✅ | ✅ | | | | | | | |
| Sambanova | ✅ | ✅ | ✅ | | | | | | | |
| Snowflake | ✅ | ✅ | ✅ | | | | | | | |
| Text Completion Codestral | ✅ | ✅ | ✅ | | | | | | | |
| Text Completion OpenAI | ✅ | ✅ | ✅ | | | ✅ | ✅ | ✅ | ✅ | |
| Together AI | ✅ | ✅ | ✅ | | | | | | | |
| Topaz | ✅ | ✅ | ✅ | | | | | | | |
| Triton | ✅ | ✅ | ✅ | | | | | | | |
| V0 | ✅ | ✅ | ✅ | | | | | | | |
| Vercel AI Gateway | ✅ | ✅ | ✅ | | | | | | | |
| VLLM | ✅ | ✅ | ✅ | | | | | | | |
| Volcengine | ✅ | ✅ | ✅ | | | | | | | |
| Voyage AI | | | | ✅ | | | | | | |
| WandB Inference | ✅ | ✅ | ✅ | | | | | | | |
| xAI | ✅ | ✅ | ✅ | | | | | | | |
| Xinference | | | | ✅ | | | | | | |

[**阅读文档**](https://docs.litellm.ai/docs/)

## 开发者模式运行

### 服务
1. 在根目录设置.env文件
2. 运行依赖服务 `docker-compose up db prometheus`

### 后端
1. （在根目录）创建虚拟环境 `python -m venv .venv`
2. 激活虚拟环境 `source .venv/bin/activate`
3. 安装依赖 `pip install -e ".[all]"`
4. `pip install prisma`
5. `prisma generate`
6. 启动代理后端 `python litellm/proxy/proxy_cli.py`

### 前端
1. 进入 `ui/litellm-dashboard`
2. 安装依赖 `npm install`
3. 运行 `npm run dev` 启动仪表板

# 企业版

需要更好安全性、用户管理和专业支持的公司

[与创始人联系](https://calendly.com/d/cx9p-5yf-2nm/litellm-introductions)

这包括：
- ✅ **LiteLLM商业许可证下的功能**
- ✅ **功能优先级**
- ✅ **自定义集成**
- ✅ **专业支持 - 专用discord + slack**
- ✅ **自定义SLA**
- ✅ **单点登录安全访问**

# 贡献

我们欢迎为LiteLLM做出贡献！无论是修复错误、添加功能还是改进文档，我们都很感谢您的帮助。

## 贡献者快速入门

这需要安装poetry。

```bash
git clone https://github.com/BerriAI/litellm.git
cd litellm
make install-dev    # 安装开发依赖
make format         # 格式化代码
make lint           # 运行所有linting检查
make test-unit      # 运行单元测试
make format-check   # 仅检查格式化
```

有关详细的贡献指南，请参阅[CONTRIBUTING.md](CONTRIBUTING.md)。

## 代码质量/Linting

LiteLLM遵循[Google Python风格指南](https://google.github.io/styleguide/pyguide.html)。

我们的自动化检查包括：
- **Black** 用于代码格式化
- **Ruff** 用于linting和代码质量
- **MyPy** 用于类型检查
- **循环导入检测**
- **导入安全检查**

所有这些检查必须通过才能合并您的PR。

# 支持/与创始人交流

- [安排演示](https://calendly.com/d/4mp-gd3-k5k/berriai-1-1-onboarding-litellm-hosted-version)
- [社区Discord](https://discord.gg/wuPM9dRgDw)
- [社区Slack](https://www.litellm.ai/support)
- 我们的电话：+1 (770) 8783-106 / +1 (412) 618-6238
- 我们的邮箱：ishaan@berri.ai / krrish@berri.ai

# 为什么我们构建了这个

- **简单性的需求**：我们的代码在管理和翻译Azure、OpenAI和Cohere之间的调用时变得极其复杂。

# 贡献者

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->
<!-- ALL-CONTRIBUTORS-LIST:END -->
