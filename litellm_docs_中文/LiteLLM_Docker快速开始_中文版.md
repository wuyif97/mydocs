# LiteLLM Docker 快速开始教程

> 原文: https://docs.litellm.ai/docs/proxy/docker_quick_start

这是一个LiteLLM代理的端到端教程，教你如何：
- 添加Azure OpenAI模型
- 进行成功的/chat/completion调用
- 生成虚拟密钥
- 设置虚拟密钥的RPM限制

---

## 前置要求

### 方式一：使用Docker

安装Docker后，运行：

```bash
docker pull docker.litellm.ai/berriai/litellm:main-latest
```

### 方式二：使用Docker Compose（代理+数据库）

```bash
# 获取docker compose文件
curl -O https://raw.githubusercontent.com/BerriAI/litellm/main/docker-compose.yml

# 添加主密钥 - 可以在设置后更改
echo 'LITELLM_MASTER_KEY="sk-1234"' > .env

# 添加litellm salt密钥 - 添加模型后无法更改
# 用于加密/解密您的LLM API密钥凭据
echo 'LITELLM_SALT_KEY="sk-1234"' >> .env

# 启动
docker compose up
```

### 方式三：使用LiteLLM CLI

```bash
pip install 'litellm[proxy]'
```

---

## 步骤1：添加模型

使用config.yaml文件控制LiteLLM代理。

### config.yaml 示例 - Azure模型

```yaml
model_list:
  - model_name: gpt-4o
    litellm_params:
      model: azure/my_azure_deployment
      api_base: os.environ/AZURE_API_BASE
      api_key: "os.environ/AZURE_API_KEY"
      api_version: "2025-01-01-preview"
```

### 重要参数说明

| 参数 | 类型 | 说明 |
|------|------|------|
| model_name | str | 接收到的模型名称 |
| model | str | 发送到后端的模型标识符 |
| api_key | str | 认证用的API密钥 |
| api_base | str | Azure部署的API基础URL |
| api_version | str | Azure OpenAI API版本 |

---

## 步骤2：发起请求

### 使用cURL

```bash
curl http://localhost:4000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer sk-1234" \
  -d '{
    "model": "gpt-4o",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

### 使用Python

```python
import openai

client = openai.OpenAI(
    api_key="sk-1234",
    base_url="http://localhost:4000"
)

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello!"}]
)

print(response.choices[0].message.content)
```

---

## 步骤3：生成虚拟密钥

### 通过Admin API

```bash
curl -X POST 'http://localhost:4000/key/generate' \
  -H 'Authorization: Bearer sk-1234' \
  -H 'Content-Type: application/json' \
  -d '{
    "key_alias": "my-key",
    "duration": "30d"
  }'
```

### 响应示例

```json
{
  "key": "sk-1234-xxxxx",
  "expires": "2024-12-31T23:59:59Z"
}
```

---

## 步骤4：设置速率限制

在config.yaml中设置RPM（每分钟请求数）限制：

```yaml
model_list:
  - model_name: gpt-4o
    litellm_params:
      model: azure/my_azure_deployment
      api_base: os.environ/AZURE_API_BASE
      api_key: "os.environ/AZURE_API_KEY"

litellm_settings:
  num_retries: 3
  timeout: 60

router_settings:
  routing_strategy: latency-based-routing
  allowed_fails: 5
  cooldown_time: 30

key_management_settings:
  default_key_duration: "30d"
```

---

## 管理界面

启动后访问 http://localhost:4000/ui 使用Admin界面管理：
- 查看密钥
- 管理用户
- 监控使用情况
- 配置模型

---

## 更多信息

- [完整配置文档](./LiteLLM_Config配置.md)
- [虚拟密钥认证](./LiteLLM_虚拟密钥_认证.md)
- [用户和预算](./LiteLLM_用户_预算_限速.md)
