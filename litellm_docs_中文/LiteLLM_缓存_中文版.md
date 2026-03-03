# LiteLLM 缓存配置

> 原文: https://docs.litellm.ai/docs/proxy/caching

LiteLLM代理支持多种缓存策略来提高性能和降低成本。

---

## 缓存类型

### Redis缓存

```yaml
router_settings:
  redis_host: localhost
  redis_port: 6379
  redis_password: password
  # 可选：使用TLS
  # redis_ssl: true
  # redis_db: 0
```

### 内存缓存

```yaml
router_settings:
  # 内存缓存设置
  cache: true
  max_cache_size: 1000
```

---

## 缓存策略

### 请求缓存

```yaml
router_settings:
  cache_params:
    # 缓存时间（秒）
    ttl: 3600
    
    # 缓存键前缀
    cache_key_prefix: "litellm"
    
    # 缓存命中时返回
    cache_keywords:
      - messages
      - model
```

### 供应商缓存

#### OpenAI 提示缓存

```yaml
model_list:
  - model_name: gpt-4o
    litellm_params:
      model: openai/gpt-4o-1106-preview
      caching: "prompt"  # 启用提示缓存
```

#### Anthropic 提示缓存

```yaml
model_list:
  - model_name: claude-3-opus
    litellm_params:
      model: anthropic/claude-3-opus-20240229
      caching: "prompt"  # 启用提示缓存
```

---

## 缓存配置示例

### 完整Redis配置

```yaml
router_settings:
  # Redis连接
  redis_host: localhost
  redis_port: 6379
  redis_password: your-password
  
  # 缓存设置
  cache: true
  cache_params:
    ttl: 3600
    cache_key_prefix: "litellm"
    
  # 缓存排除
  cache_excluded_keys:
    - "admin"
    - "internal"
```

### 多Redis实例

```yaml
router_settings:
  # 主Redis（缓存）
  redis_host: cache.example.com
  redis_port: 6379
  
  # 用于速率限制的Redis
  rate_limit_redis:
    host: ratelimit.example.com
    port: 6379
```

---

## 缓存API

### 查看缓存状态

```bash
curl -X GET 'http://localhost:4000/cache/status' \
  -H 'Authorization: Bearer sk-admin-key'
```

### 清除缓存

```bash
# 清除所有缓存
curl -X POST 'http://localhost:4000/cache/flush' \
  -H 'Authorization: Bearer sk-admin-key'

# 清除特定模型的缓存
curl -X POST 'http://localhost:4000/cache/flush' \
  -H 'Authorization: Bearer sk-admin-key' \
  -H 'Content-Type: application/json' \
  -d '{"model": "gpt-4o"}'
```

---

## 缓存策略最佳实践

### 1. 选择合适的TTL

| 使用场景 | 推荐TTL |
|---------|---------|
| 聊天应用 | 60-300秒 |
| 文档生成 | 300-3600秒 |
| 嵌入向量 | 86400秒（24小时） |

### 2. 缓存键设计

```yaml
router_settings:
  cache_params:
    # 基于这些参数生成缓存键
    cache_params:
      - messages
      - model
      - temperature
      - max_tokens
    # 排除的参数
    cache_ignore_params:
      - user_id
      - request_id
```

### 3. 缓存失效

```yaml
router_settings:
  # 当请求失败时不缓存
  cache_on_failure: false
  
  # 强制刷新
  always_refresh_cache: false
```

---

## 性能优化

### 缓存命中示例

```python
# 第一次请求 - 未命中缓存
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "什么是量子计算？"}]
)
# 请求发送到OpenAI

# 相同请求 - 命中缓存
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "什么是量子计算？"}]
)
# 直接从缓存返回，无需API调用
```

### 成本节省

使用缓存可以显著降低API成本：
- 重复请求无需再次调用LLM
- 减少延迟（缓存响应即时返回）
- 节省API调用配额

---

## 更多信息

- [配置文档](./LiteLLM_Config配置.md)
- [性能基准](./LiteLLM_基准测试.md)
- [路由配置](./LiteLLM_路由_负载均衡.md)
