# LiteLLM 配置详解

> 原文: https://docs.litellm.ai/docs/proxy/configs

本文档详细介绍LiteLLM代理的config.yaml配置文件选项。

---

## 基础配置结构

```yaml
model_list:
  - model_name: gpt-4o
    litellm_params:
      model: openai/gpt-4o
      api_key: os.environ/OPENAI_API_KEY

litellm_settings:
  drop_params: true
  set_verbose: true

router_settings:
  routing_strategy: simple-shuffle

general_settings:
  master_key: sk-1234
```

---

## model_list - 模型列表

### 基础配置

```yaml
model_list:
  - model_name: gpt-4o
    litellm_params:
      model: azure/gpt-4o
      api_base: os.environ/AZURE_API_BASE
      api_key: os.environ/AZURE_API_KEY
      api_version: "2024-02-15-preview"
```

### 重要参数

| 参数 | 类型 | 说明 |
|------|------|------|
| model_name | string | 客户端使用的模型名称 |
| litellm_params.model | string | 实际调用的模型标识 |
| litellm_params.api_key | string | API密钥 |
| litellm_params.api_base | string | API基础URL |
| litellm_params.api_version | string | API版本 |

### 模型信息

```yaml
model_list:
  - model_name: gpt-4o
    litellm_params:
      model: openai/gpt-4o
    model_info:
      mode: chat  # chat, completion, embedding, image_generation
      supports_function_calling: true
      supports_vision: true
```

---

## litellm_settings - LiteLLM设置

### 通用设置

```yaml
litellm_settings:
  # 请求超时（秒）
  timeout: 600
  
  # 最大重试次数
  num_retries: 3
  
  # 重试延迟
  retry_delay: 0.5
  
  # 是否返回请求ID
  request_id: true
  
  # 自定义API基础URL
  base_url: http://localhost:8000
  
  # 代理设置
  proxy: http://proxy:8080
  
  # 雪花算法生成ID
  id_format: "litellm-{timestamp}-{model}-{role}"
```

### 请求修改

```yaml
litellm_settings:
  # 删除特定参数
  drop_params: true
  extra_body:
    key: value
    
  # 请求前/后钩子
  pre_call_rules:
    - field: messages
      action: replace
      value: "sensitive_word"
```

---

## router_settings - 路由设置

### 路由策略

```yaml
router_settings:
  # 路由策略选项:
  # - simple-shuffle: 简单轮询
  # - latency-based-routing: 基于延迟
  # - cost-based-routing: 基于成本
  # - usage-based-routing: 基于使用量
  routing_strategy: simple-shuffle
  
  # 允许连续失败次数
  allowed_fails: 3
  
  # 失败后冷却时间（秒）
  cooldown_time: 30
  
  # 启用健康检查
  enable_health_check: true
  
  # 健康检查间隔
  health_check_interval: 300
  
  # 启用超时检测
  enable_timeout_detection: true
```

### 速率限制

```yaml
router_settings:
  # 每分钟请求数限制
  rpm_limit: 60
  
  # 每分钟令牌数限制
  tpm_limit: 100000
  
  # 模型级别限制
  model_rpm_limits:
    gpt-4o: 100
    gpt-3.5-turbo: 1000
```

---

## key_management_settings - 密钥管理

### 基础设置

```yaml
key_management_settings:
  # 默认密钥有效期
  default_key_duration: "30d"
  
  # 默认预算
  default_max_budget: 1000
  
  # 默认速率限制
  default_rpm_limit: 60
  default_tpm_limit: 100000
  
  # 密钥存储
  store_in: "prisma"  # prisma, dynamodb, postgres
```

### 高级设置

```yaml
key_management_settings:
  # 启用多租户
  enable_multi tenancy: true
  
  # 密钥轮换
  auto_key_rotation: true
  key_rotation_interval: "90d"
  
  # 外部认证
  auth_mode: "basic"  # basic, jwt, external
```

---

## general_settings - 通用设置

### 基础设置

```yaml
general_settings:
  # 主密钥（必需）
  master_key: sk-admin-key-1234
  
  # 数据库连接
  database_url: postgresql://user:pass@localhost:5432/litellm
  
  # UI设置
  ui_access: true
  admin_ui: true
  
  # 域名限制
  allowed_domains:
    - example.com
    - app.example.com
```

### 环境变量

```yaml
general_settings:
  # 环境变量
  environment_variables:
    OPENAI_API_KEY: os.environ/OPENAI_API_KEY
    ANTHROPIC_API_KEY: os.environ/ANTHROPIC_API_KEY
    
  # 负载均衡器
  upstream_chunk_size: 100
  force_upstream_timeout: false
```

---

## 环境变量

### 必需的环境变量

```bash
# 主密钥
LITELLM_MASTER_KEY=sk-admin-key-1234

# 数据库（可选）
DATABASE_URL=postgresql://user:pass@localhost:5432/litellm

# 日志
LITELLM_LOG_LEVEL=INFO
```

### 可选环境变量

```bash
# 数据库
DATABASE_TYPE=postgres
DB_POOL_SIZE=10
DB_MAX_OVERFLOW=20

# Redis缓存
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=password

# 限流
GLOBAL_RATE_LIMIT=1000/1minute

# TLS/SSL
LITELLM_CERT_FILE=/path/to/cert.pem
LITELLM_KEY_FILE=/path/to/key.pem
```

---

## 完整配置示例

```yaml
model_list:
  - model_name: gpt-4o
    litellm_params:
      model: azure/azure-gpt-4o
      api_base: os.environ/AZURE_API_BASE
      api_key: os.environ/AZURE_API_KEY
      api_version: "2024-02-15-preview"
    model_info:
      mode: chat
      supports_function_calling: true
      
  - model_name: claude-3-opus
    litellm_params:
      model: anthropic/claude-3-opus-20240229
      api_key: os.environ/ANTHROPIC_API_KEY
    model_info:
      mode: chat
      supports_vision: true

litellm_settings:
  timeout: 600
  num_retries: 3
  retry_delay: 0.5

router_settings:
  routing_strategy: latency-based-routing
  allowed_fails: 3
  cooldown_time: 30
  rpm_limit: 100
  tpm_limit: 100000

key_management_settings:
  default_key_duration: "30d"
  default_max_budget: 500
  default_rpm_limit: 60

general_settings:
  master_key: sk-admin-key-1234
  database_url: postgresql://user:pass@localhost:5432/litellm
  ui_access: true
```

---

## 更多信息

- [快速开始](./LiteLLM_Docker快速开始_中文版.md)
- [虚拟密钥](./LiteLLM_虚拟密钥_认证_中文版.md)
- [部署指南](./LiteLLM_快速开始_部署_中文版.md)
