# LiteLLM 虚拟密钥与认证

> 原文: https://docs.litellm.ai/docs/proxy/virtual_keys

LiteLLM代理提供强大的虚拟密钥认证系统，支持API密钥生成、权限管理和访问控制。

---

## 核心概念

### 虚拟密钥（Virtual Keys）
- 为不同用户/项目生成独立的API密钥
- 每个密钥可以设置不同的访问权限
- 支持设置过期时间

### 主密钥（Master Key）
- 管理员使用的密钥
- 拥有完全访问权限
- 在部署时设置

---

## 密钥管理API

### 生成密钥

```bash
curl -X POST 'http://localhost:4000/key/generate' \
  -H 'Authorization: Bearer sk-admin-key' \
  -H 'Content-Type: application/json' \
  -d '{
    "key_alias": "my-project-key",
    "duration": "30d",
    "models": ["gpt-4o", "claude-3-opus"],
    "metadata": {"team": "engineering"}
  }'
```

### 响应示例

```json
{
  "key": "sk-1234-abcdefgh",
  "expires": "2024-12-31T23:59:59.000Z",
  "created_at": "2024-01-01T00:00:00.000Z"
}
```

### 列出所有密钥

```bash
curl -X GET 'http://localhost:4000/key/info' \
  -H 'Authorization: Bearer sk-admin-key'
```

### 删除密钥

```bash
curl -X DELETE 'http://localhost:4000/key/delete' \
  -H 'Authorization: Bearer sk-admin-key' \
  -H 'Content-Type: application/json' \
  -d '{"key": "sk-1234-abcdefgh"}'
```

### 更新密钥

```bash
curl -X POST 'http://localhost:4000/key/update' \
  -H 'Authorization: Bearer sk-admin-key' \
  -H 'Content-Type: application/json' \
  -d '{
    "key": "sk-1234-abcdefgh",
    "duration": "60d",
    "models": ["gpt-4o"]
  }'
```

---

## 密钥权限配置

### 在config.yaml中设置

```yaml
key_management_settings:
  # 默认密钥有效期
  default_key_duration: "30d"
  
  # 允许的模型列表
  allowed_model_region: ["us-east-1", "eu-west-1"]
  
  # 启用/禁用密钥
  default_key_status: "active"
```

### 按密钥设置预算

```yaml
key_management_settings:
  default_max_budget: 1000  # 美元
```

### 密钥级别限制

```yaml
model_list:
  - model_name: gpt-4o
    litellm_params:
      model: openai/gpt-4o
    model_info:
      mode: chat
      
key_generation:
  - key_alias: "premium-user"
    max_budget: 5000
    rpm_limit: 1000
    tpm_limit: 100000
```

---

## 认证方式

### Bearer Token认证

```bash
curl -X GET 'http://localhost:4000/v1/models' \
  -H 'Authorization: Bearer sk-1234-abcdefgh'
```

### API Key认证

```bash
curl -X GET 'http://localhost:4000/v1/models' \
  -H 'x-api-key: sk-1234-abcdefgh'
```

### 自定义Header

```yaml
general_settings:
  master_key: "sk-admin-key"
  
key_management_settings:
  store_in: "dynamodb"  # 支持dynamodb存储
  auth_mode: "basic"   # basic, jwt, external
```

---

## JWT认证

### 配置JWT验证

```yaml
auth_settings:
  jwt_auth: true
  jwt_public_key: |
    -----BEGIN PUBLIC KEY-----
    ... your public key ...
    -----END PUBLIC KEY-----
  jwt_algorithm: "RS256"
  jwt_issuer: "your-issuer"
  jwt_audience: "your-audience"
```

### JWT包含的信息

```python
import jwt

token = jwt.encode(
    {
        "sub": "user123",
        "models": ["gpt-4o", "claude-3"],
        "budget": 1000,
        "exp": datetime.datetime.utcnow() + timedelta(days=30)
    },
    "your-private-key",
    algorithm="RS256"
)
```

---

## 高级功能

### 密钥轮换

```bash
# 自动轮换密钥
curl -X POST 'http://localhost:4000/key/rotate' \
  -H 'Authorization: Bearer sk-admin-key' \
  -H 'Content-Type: application/json' \
  -d '{"key": "sk-1234-abcdefgh"}'
```

### 密钥使用统计

```bash
curl -X GET 'http://localhost:4000/key/spend?key=sk-1234-abcdefgh' \
  -H 'Authorization: Bearer sk-admin-key'
```

### 速率限制

```yaml
router_settings:
  routing_strategy: latency-based-routing
  
  # 每个密钥的速率限制
  rpm_limit: 100
  tpm_limit: 10000
```

---

## 安全最佳实践

1. **定期轮换密钥** - 定期更换主密钥和虚拟密钥
2. **最小权限原则** - 只授予必要的模型访问权限
3. **设置预算限制** - 防止意外超额使用
4. **监控使用情况** - 定期检查密钥使用统计
5. **使用HTTPS** - 生产环境必须使用TLS

---

## 更多信息

- [用户与预算管理](./LiteLLM_用户_预算_限速.md)
- [配置文档](./LiteLLM_Config配置.md)
- [Admin界面](./LiteLLM_Admin管理界面.md)
