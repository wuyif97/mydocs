# LiteLLM 路由与负载均衡

> 原文: https://docs.litellm.ai/docs/routing-load-balancing

LiteLLM代理提供强大的路由和负载均衡功能，优化LLM调用的性能和成本。

---

## 路由策略

### 1. 简单轮询 (Simple Shuffle)

```yaml
router_settings:
  routing_strategy: simple-shuffle
```

请求按顺序分发到各个模型。

### 2. 基于延迟的路由 (Latency-based)

```yaml
router_settings:
  routing_strategy: latency-based-routing
```

自动选择延迟最低的模型。

### 3. 基于成本的路由 (Cost-based)

```yaml
router_settings:
  routing_strategy: cost-based-routing
```

优先使用成本较低的模型。

### 4. 基于使用量的路由 (Usage-based)

```yaml
router_settings:
  routing_strategy: usage-based-routing
```

均匀分配请求到各个模型。

---

## 负载均衡配置

### 基础配置

```yaml
router_settings:
  # 允许连续失败次数
  allowed_fails: 3
  
  # 失败后冷却时间（秒）
  cooldown_time: 30
  
  # 启用健康检查
  enable_health_check: true
  
  # 健康检查间隔（秒）
  health_check_interval: 300
```

### 高级配置

```yaml
router_settings:
  # 路由策略
  routing_strategy: latency-based-routing
  
  # 模型超时检测
  enable_timeout_detection: true
  timeout_threshold: 60
  
  # 重试设置
  num_retries: 3
  retry_strategy: "exponential-backoff"
  
  # 失败转移
  fallback_models:
    - model_name: gpt-4o
      litellm_params:
        model: openai/gpt-4o
    - model_name: gpt-3.5-turbo
      litellm_params:
        model: openai/gpt-3.5-turbo
```

---

## 故障转移 (Failover)

### 自动故障转移

```yaml
router_settings:
  # 启用故障转移
  enable_fallbacks: true
  
  # 故障转移模型列表
  fallback_models:
    - model: openai/gpt-4o
    - model: anthropic/claude-3-opus
    - model: google/gemini-pro
```

### 手动故障转移

```python
from litellm import completion

response = completion(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello!"}],
    fallbacks=[
        {"model": "anthropic/claude-3-opus"},
        {"model": "google/gemini-pro"}
    ]
)
```

---

## 熔断机制

### 配置熔断

```yaml
router_settings:
  # 连续失败次数阈值
  allowed_fails: 5
  
  # 冷却时间
  cooldown_time: 60
  
  # 恢复时间
  recovery_time: 300
  
  # 启用熔断
  enable_circuit_breaker: true
```

---

## 流量分割

### A/B测试

```yaml
router_settings:
  # 流量分割
  traffic_split:
    gpt-4o: 70      # 70% 流量
    claude-3-opus: 30  # 30% 流量
```

### 流量镜像

```yaml
router_settings:
  # 流量镜像到备用模型
  traffic_mirroring:
    primary_model: gpt-4o
    mirror_model: gpt-3.5-turbo
    mirror_percentage: 10  # 镜像10%流量
```

---

## 性能优化

### 连接池

```yaml
router_settings:
  # 连接池大小
  max_parallel_requests: 100
  
  # 请求超时
  timeout: 60
  
  # 空闲连接超时
  idle_connection_timeout: 300
```

### 缓存

结合缓存使用可以大幅提升性能：

```yaml
router_settings:
  # 启用缓存
  cache: true
  
  cache_params:
    ttl: 300
```

---

## 监控

### 查看路由统计

```bash
curl -X GET 'http://localhost:4000/router/stats' \
  -H 'Authorization: Bearer sk-admin-key'
```

### 响应示例

```json
{
  "total_requests": 10000,
  "by_model": {
    "gpt-4o": {
      "requests": 6000,
      "avg_latency": 1.2,
      "failures": 10
    },
    "claude-3-opus": {
      "requests": 4000,
      "avg_latency": 0.8,
      "failures": 5
    }
  }
}
```

---

## 最佳实践

1. **选择合适的路由策略**
   - 生产环境：使用延迟或成本基础路由
   - 开发环境：使用简单轮询

2. **配置合理的故障转移**
   - 始终设置备用模型
   - 定期测试故障转移

3. **启用监控**
   - 跟踪延迟和失败率
   - 设置告警阈值

4. **使用缓存**
   - 对重复请求启用缓存
   - 合理设置TTL

---

## 更多信息

- [配置文档](./LiteLLM_Config配置.md)
- [缓存配置](./LiteLLM_缓存.md)
- [基准测试](./LiteLLM_基准测试.md)
