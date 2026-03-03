# LiteLLM Admin 管理界面

> 原文: https://docs.litellm.ai/docs/proxy/ui

LiteLLM提供功能强大的Admin管理界面，用于监控和管理代理服务。

---

## 访问管理界面

启动后访问: http://localhost:4000/ui

使用主密钥登录后即可使用完整功能。

---

## 主要功能

### 1. 仪表板概览

- 总请求数
- 活跃密钥数
- 今日支出
- 错误率统计

### 2. 密钥管理

- 查看所有虚拟密钥
- 创建新密钥
- 编辑密钥权限
- 删除密钥
- 查看密钥使用统计

### 3. 用户管理

- 创建用户
- 设置用户预算
- 分配模型权限
- 查看用户活动

### 4. 模型配置

- 添加新模型
- 配置模型参数
- 设置速率限制
- 监控模型使用

### 5. 日志查看

- 实时请求日志
- 错误日志
- 审计日志
- 日志导出

---

## API访问

### 获取使用统计

```bash
curl -X GET 'http://localhost:4000/global/spend' \
  -H 'Authorization: Bearer sk-admin-key'
```

### 获取活跃请求

```bash
curl -X GET 'http://localhost:4000/requests/status' \
  -H 'Authorization: Bearer sk-admin-key'
```

---

## 最佳实践

1. **定期检查仪表板** - 监控服务健康状态
2. **设置告警** - 及时发现异常
3. **审计日志** - 定期审查操作日志
4. **密钥管理** - 定期轮换密钥

---

## 更多信息

- [配置文档](./LiteLLM_Config配置.md)
- [虚拟密钥](./LiteLLM_虚拟密钥_认证_中文版.md)
