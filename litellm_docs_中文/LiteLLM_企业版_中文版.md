# LiteLLM 企业版

> 原文: https://docs.litellm.ai/docs/proxy/enterprise

LiteLLM企业版为大型组织提供高级功能、安全性和支持服务。

---

## 企业版功能

### 高级安全特性

- **单点登录 (SSO)**
  - SAML 2.0
  - OIDC
  - OAuth 2.0

- **审计日志**
  - 完整的API调用记录
  - 用户操作追踪
  - 合规性报告

- **数据驻留**
  - 区域数据存储
  - GDPR合规
  - HIPAA支持

### 高级管理功能

- **多团队/多租户**
  - 组织层级管理
  - 团队隔离
  - 跨团队报告

- **高级分析**
  - 自定义仪表板
  - API使用分析
  - 成本优化建议

---

## 部署选项

### 自托管

```bash
# 使用企业版Docker镜像
docker pull docker.litellm.ai/berriai/litellm:main-latest
```

### 云托管

访问 [LiteLLM Cloud](https://www.litellm.ai/cloud) 获取托管服务

---

## 成本追踪

### 详细支出报告

```bash
# 获取详细支出报告
curl -X GET 'http://localhost:4000/spend/report' \
  -H 'Authorization: Bearer sk-admin-key' \
  -d '{
    "start_date": "2024-01-01",
    "end_date": "2024-01-31",
    "group_by": "model"  # model, team, user
  }'
```

### 响应示例

```json
{
  "total_spend": 10000.00,
  "by_model": {
    "gpt-4o": 5000.00,
    "claude-3-opus": 3000.00,
    "gemini-pro": 2000.00
  },
  "by_team": {
    "engineering": 6000.00,
    "marketing": 4000.00
  }
}
```

### 预算告警

```yaml
general_settings:
  alert_settings:
    webhook_url: "https://your-company.com/alerts"
    channels:
      - type: email
        recipients: ["admin@company.com"]
      - type: slack
        webhook: "https://slack.com/..."
      - type: pagerduty
        key: "..."
```

---

## SLA保证

| 功能 | 标准版 | 企业版 |
|------|--------|--------|
| 上线时间 | 99.5% | 99.9% |
| 支持响应 | 48小时 | 4小时 |
| 专属客户经理 | ❌ | ✅ |
| 定制开发 | ❌ | ✅ |
| 安全审计 | 基础 | 完整 |

---

## 定价

请联系销售团队获取定制报价：

- [预约演示](https://calendly.com/d/cx9p-5yf-2nm/litellm-introductions)
- 邮箱: ishaan@berri.ai

---

## 更多信息

- [联系销售](https://www.litellm.ai/enterprise)
- [标准版文档](./LiteLLM_AI_Gateway_代理_中文版.md)
