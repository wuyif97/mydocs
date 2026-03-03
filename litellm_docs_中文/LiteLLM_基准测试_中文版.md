# LiteLLM 性能基准测试

> 原文: https://docs.litellm.ai/docs/benchmarks

本文档展示LiteLLM代理的性能基准测试结果。

---

## 性能指标

### 延迟 (Latency)

| 场景 | P50延迟 | P95延迟 | P99延迟 |
|------|---------|---------|---------|
| 简单请求 | 5ms | 8ms | 15ms |
| 复杂请求 | 10ms | 25ms | 50ms |
| 流式响应 | 8ms | 20ms | 40ms |

### 吞吐量 (Throughput)

- **单节点**: 最高 1,000 RPS (每秒请求数)
- **集群**: 最高 10,000+ RPS

---

## 测试环境

### 硬件配置

- CPU: 8核
- 内存: 16GB
- 网络: 10Gbps

### 软件配置

- LiteLLM版本: main-latest
- 数据库: PostgreSQL
- 缓存: Redis

---

## 测试结果

### 单模型性能

| 模型 | 请求/秒 | 平均延迟 | 错误率 |
|------|---------|---------|--------|
| gpt-4o | 500 | 12ms | 0.1% |
| gpt-3.5-turbo | 800 | 8ms | 0.05% |
| claude-3-opus | 450 | 15ms | 0.1% |

### 多模型负载均衡

| 配置 | 请求/秒 | 平均延迟 | 错误率 |
|------|---------|---------|--------|
| 2模型 | 900 | 10ms | 0.1% |
| 5模型 | 850 | 12ms | 0.15% |
| 10模型 | 750 | 15ms | 0.2% |

---

## 优化建议

### 1. 使用缓存

```yaml
router_settings:
  redis_host: localhost
  redis_port: 6379
  cache: true
  cache_params:
    ttl: 300
```

### 2. 启用连接池

```yaml
router_settings:
  max_parallel_requests: 500
  timeout: 60
```

### 3. 选择合适的路由策略

```yaml
router_settings:
  routing_strategy: latency-based-routing
```

### 4. 启用健康检查

```yaml
router_settings:
  enable_health_check: true
  health_check_interval: 60
```

---

## 负载测试工具

### 使用locust进行测试

```python
from locust import HttpUser, task, between

class LLMUser(HttpUser):
    wait_time = between(0.1, 0.5)
    
    @task
    def chat_completion(self):
        self.client.post("/v1/chat/completions", json={
            "model": "gpt-4o",
            "messages": [{"role": "user", "content": "Hello!"}]
        })
```

运行测试：

```bash
locust -f locustfile.py --host=http://localhost:4000
```

---

## 监控指标

### 关键指标

1. **请求延迟** - P50, P95, P99
2. **吞吐量** - RPS
3. **错误率** - 4xx, 5xx
4. **资源使用** - CPU, 内存, 网络

### 查看监控数据

```bash
curl -X GET 'http://localhost:4000/metrics' \
  -H 'Authorization: Bearer sk-admin-key'
```

---

## 最佳实践

1. **预估容量** - 根据峰值流量预留足够资源
2. **启用监控** - 实时跟踪性能指标
3. **设置告警** - 及时发现异常
4. **定期测试** - 周期性进行负载测试

---

## 更多信息

- [配置文档](./LiteLLM_Config配置.md)
- [路由配置](./LiteLLM_路由_负载均衡.md)
- [缓存配置](./LiteLLM_缓存.md)
