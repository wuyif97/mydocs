# LiteLLM AI 网关（代理）

> 原文: https://docs.litellm.ai/docs/simple_proxy

LiteLLM AI网关（LLM代理）是一个OpenAI代理服务器（LLM网关），用于：
- 以统一接口调用100+大语言模型
- 跟踪支出
- 为虚拟密钥/用户设置预算

---

## 核心功能

### 📄 入门教程
LiteLLM代理的端到端教程，包括：
- 添加Azure OpenAI模型
- 进行成功的/chat/completion调用
- 生成虚拟密钥
- 设置虚拟密钥的RPM限制

### 🔗 A2A 代理网关
支持A2A（Agent-to-Agent）协议连接多个代理服务

### 🔗 MCP 网关
支持MCP（Model Context Protocol）服务器连接

### 🗃️ Config.yaml
配置文件相关设置（3个项目）

### 🗃️ 设置与部署
部署和配置相关指南（10个项目）

### 🗃️ 管理界面
Admin UI管理界面相关（6个项目）

### 🗃️ 架构
系统架构说明（10个项目）

### ✨ 企业版功能
获取许可证请联系

### 🗃️ 认证
虚拟密钥和认证相关（9个项目）

### 🗃️ 预算和速率限制
用户预算和速率限制设置（10个项目）

### 📄 缓存
OpenAI/Anthropic提示缓存相关

### 🔗 Guardrails
内容安全护栏

### 🔗 策略
安全策略配置

### 🗃️ 创建自定义插件
修改请求、响应等

### 📄 LiteLLM代理CLI
litellm-proxy命令行工具用于管理LiteLLM代理

### 🔗 负载均衡、路由、回退
负载均衡和故障转移配置

---

## 快速开始

### 使用Docker

```bash
# 拉取最新镜像
docker pull docker.litellm.ai/berriai/litellm:main-latest
```

### 使用Python

```bash
pip install 'litellm[proxy]'
```

### 启动代理

```bash
litellm --model gpt-4o
```

### 通过API调用

```python
import openai

client = openai.OpenAI(
    api_key="anything",
    base_url="http://0.0.0.0:4000"
)

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

---

## 主要特性

1. **统一接口** - 一个API端点访问100+大语言模型
2. **虚拟密钥** - 为不同用户/项目生成独立的API密钥
3. **预算管理** - 按密钥/用户设置支出限额
4. **速率限制** - RPM/TPM限制控制
5. **日志记录** - 完整的请求和响应日志
6. **监控** - Admin仪表板实时监控

---

## 更多信息

- [完整文档](https://docs.litellm.ai/docs/)
- [GitHub](https://github.com/BerriAI/litellm)
- [Discord社区](https://discord.gg/wuPM9dRgDw)
