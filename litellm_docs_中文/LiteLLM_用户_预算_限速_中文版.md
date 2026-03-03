# LiteLLM 用户、预算与速率限制

> 原文: https://docs.litellm.ai/docs/proxy/users

LiteLLM代理提供完整的用户管理、预算控制和速率限制功能。

---

## 用户管理

### 创建用户

```bash
curl -X POST 'http://localhost:4000/user/new' \
  -H 'Authorization: Bearer sk-admin-key' \
  -H 'Content-Type: application/json' \
  -d '{
    "user_id": "user-123",
    "user_email": "user@example.com",
    "metadata": {"team": "engineering"}
  }'
```

### 获取用户信息

```bash
curl -X GET 'http://localhost:4000/user/info?user_id=user-123' \
  -H 'Authorization: Bearer sk-admin-key'
```

### 列出所有用户

```bash
curl -X GET 'http://localhost:4000/user/list' \
  -H 'Authorization: Bearer sk-admin-key'
```

---

## 预算管理

### 设置用户预算

```bash
curl -X POST 'http://localhost:4000/user/budget' \
  -H 'Authorization: Bearer sk-admin-key' \
  -H 'Content-Type: application/json' \
  -d '{
    "user_id": "user-123",
    "budget_duration": "30d",
    "max_budget": 1000
  }'
```

### 预算参数说明

| 参数 | 类型 | 说明 |
|------|------|------|
| budget_duration | string | 预算周期 (如 "30d", "1m") |
| max_budget | float | 预算上限（美元） |
| max_parallel_requests | int | 最大并发请求数 |
| tpm_limit | int | 每分钟令牌数限制 |
| rpm_limit | int | 每分钟请求数限制 |

### 在config.yaml中设置默认预算

```yaml
key_management_settings:
  default_max_budget: 500        # 默认预算 500美元
  default_budget_duration: "30d"  # 默认30天
  
router_settings:
  default_rpm_limit: 60          # 默认每分钟60请求
  default_tpm_limit: 100000      # 默认每分钟100K令牌
```

---

## 速率限制

### 请求速率限制 (RPM)

```bash
# 为特定密钥设置RPM限制
curl -X POST 'http://localhost:4000/key/generate' \
  -H 'Authorization: Bearer sk-admin-key' \
  -H 'Content-Type: application/json' \
  -d '{
    "key_alias": "rate-limited-key",
    "rpm_limit": 100
  }'
```

### 令牌速率限制 (TPM)

```bash
# 为特定密钥设置TPM限制
curl -X POST 'http://localhost:4000/key/generate' \
  -H 'Authorization: Bearer sk-admin-key' \
  -H 'Content-Type: application/json' \
  -d '{
    "key_alias": "token-limited-key",
    "tpm_limit": 100000
  }'
```

### 高级速率限制配置

```yaml
router_settings:
  # 路由策略
  routing_strategy: latency-based-routing  # 基于延迟的路由
  
  # 失败后冷却时间
  cooldown_time: 30
  
  # 允许连续失败次数
  allowed_fails: 3
  
  # 启用熔断
  enable_budgeting: true
  
  # 启用速率限制
  enable_rate_limiting: true
```

---

## 使用量追踪

### 获取用户支出

```bash
curl -X GET 'http://localhost:4000/user/spend?user_id=user-123' \
  -H 'Authorization: Bearer sk-admin-key'
```

### 获取密钥支出

```bash
curl -X GET 'http://localhost:4000/key/spend?key=sk-1234' \
  -H 'Authorization: Bearer sk-admin-key'
```

### 响应示例

```json
{
  "total_spend": 150.50,
  "key": "sk-1234",
  "models": {
    "gpt-4o": {
      "spend": 100.00,
      "requests": 500,
      "tokens": 1000000
    }
  },
  "start_date": "2024-01-01",
  "end_date": "2024-01-31"
}
```

---

## 预算告警

### 配置告警阈值

```yaml
general_settings:
  # 达到预算百分比时发送告警
  alert_settings:
    webhook_url: "https://your-webhook.com/alerts"
    alert_types:
      - "budget_threshold_80"   # 达到80%预算
      - "budget_threshold_100"   # 达到100%预算
      - "key_expiry"             # 密钥即将过期
```

---

## 成本控制策略

### 按模型设置成本

```yaml
model_list:
  - model_name: gpt-4o
    litellm_params:
      model: openai/gpt-4o
    model_info:
      mode: chat
      input_cost_per_second: 0.0001
      output_cost_per_second: 0.0001
      
  - model_name: gpt-3.5-turbo
    litellm_params:
      model: openai/gpt-3.5-turbo
    model_info:
      mode: chat
      input_cost_per_second: 0.00001
      output_cost_per_second: 0.00002
```

---

## 最佳实践

1. **设置合理的预算** - 根据实际使用情况设置预算
2. **启用速率限制** - 防止滥用和意外超额
3. **监控使用量** - 定期检查支出报告
4. **设置告警** - 在接近预算限制时收到通知
5. **定期审计** - 定期检查用户和密钥使用情况

---

## 更多信息

- [虚拟密钥认证](./LiteLLM_虚拟密钥_认证_中文版.md)
- [配置文档](./LiteLLM_Config配置.md)
- [成本追踪](./LiteLLM_企业版.md)
