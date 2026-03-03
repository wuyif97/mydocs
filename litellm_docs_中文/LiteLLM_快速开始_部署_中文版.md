# LiteLLM 快速开始与部署

> 原文: https://docs.litellm.ai/docs/proxy/quick_start

本文档介绍LiteLLM代理的多种部署方式和快速开始指南。

---

## 安装方式

### 方式一：pip安装

```bash
# 安装Python包
pip install 'litellm[proxy]'

# 验证安装
litellm --version
```

### 方式二：Docker

```bash
# 拉取最新镜像
docker pull docker.litellm.ai/berriai/litellm:main-latest

# 运行容器
docker run \
  -e LITELLM_MASTER_KEY=sk-1234 \
  -e DATABASE_URL=postgresql://user:pass@db:5432/litellm \
  -p 4000:4000 \
  docker.litellm.ai/berriai/litellm:main-latest
```

### 方式三：Docker Compose（推荐）

```bash
# 获取docker-compose文件
curl -O https://raw.githubusercontent.com/BerriAI/litellm/main/docker-compose.yml

# 编辑配置文件
nano .env

# 启动所有服务
docker compose up -d
```

---

## 环境配置

### 必需的环境变量

```bash
# 主密钥（必需）
LITELLM_MASTER_KEY=sk-your-master-key-here

# 可选：数据库连接
DATABASE_URL=postgresql://user:password@localhost:5432/litellm
```

### 常用环境变量

```bash
# 日志级别
LITELLM_LOG_LEVEL=INFO

# 端口
LITELLM_PORT=4000
LITELLM_HOST=0.0.0.0

# 数据库
DATABASE_TYPE=postgres
DB_HOST=localhost
DB_PORT=5432
DB_NAME=litellm
DB_USER=postgres
DB_PASSWORD=password

# Redis缓存（可选）
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=password

# TLS/SSL
LITELLM_CERT_FILE=/path/to/cert.pem
LITELLM_KEY_FILE=/path/to/key.pem
```

---

## 启动服务

### 快速启动（单模型）

```bash
litellm \
  --model gpt-4o \
  --port 4000
```

### 使用配置文件启动

```bash
litellm --config config.yaml
```

### Docker启动

```bash
# 基础启动
docker run -d \
  -p 4000:4000 \
  -v $(pwd)/config.yaml:/app/config.yaml \
  -e LITELLM_MASTER_KEY=sk-1234 \
  docker.litellm.ai/berriai/litellm:main-latest \
  --config /app/config.yaml --port 4000
```

---

## 配置示例

### 基础config.yaml

```yaml
model_list:
  - model_name: gpt-4o
    litellm_params:
      model: openai/gpt-4o
      api_key: os.environ/OPENAI_API_KEY

general_settings:
  master_key: sk-1234
```

### 多模型配置

```yaml
model_list:
  - model_name: gpt-4o
    litellm_params:
      model: openai/gpt-4o
      api_key: os.environ/OPENAI_API_KEY
      
  - model_name: claude-3-opus
    litellm_params:
      model: anthropic/claude-3-opus-20240229
      api_key: os.environ/ANTHROPIC_API_KEY
      
  - model_name: azure-gpt-4
    litellm_params:
      model: azure/azure-gpt-4
      api_base: os.environ/AZURE_API_BASE
      api_key: os.environ/AZURE_API_KEY
      api_version: "2024-02-15-preview"

litellm_settings:
  num_retries: 3
  timeout: 600

router_settings:
  routing_strategy: latency-based-routing
  rpm_limit: 100

general_settings:
  master_key: sk-1234
  database_url: postgresql://user:pass@localhost:5432/litellm
```

---

## 验证部署

### 健康检查

```bash
curl http://localhost:4000/health
```

### 获取模型列表

```bash
curl http://localhost:4000/v1/models \
  -H "Authorization: Bearer sk-1234"
```

### 测试API调用

```bash
curl http://localhost:4000/v1/chat/completions \
  -H "Authorization: Bearer sk-1234" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4o",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

---

## 管理界面

启动后访问 http://localhost:4000/ui

功能包括：
- 查看所有密钥
- 管理用户
- 监控使用量
- 配置模型
- 查看日志

---

## 生产环境部署

### 使用Nginx反向代理

```nginx
server {
    listen 443 ssl http2;
    server_name litellm.yourcompany.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    location / {
        proxy_pass http://localhost:4000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

### 使用Systemd

```ini
[Unit]
Description=LiteLLM Proxy
After=network.target

[Service]
Type=simple
User=litellm
WorkingDirectory=/opt/litellm
ExecStart=/usr/local/bin/litellm --config /opt/litellm/config.yaml
Restart=always
Environment=LITELLM_MASTER_KEY=sk-1234

[Install]
WantedBy=multi-user.target
```

### 使用Kubernetes

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: litellm-proxy
spec:
  replicas: 3
  selector:
    matchLabels:
      app: litellm-proxy
  template:
    metadata:
      labels:
        app: litellm-proxy
    spec:
      containers:
      - name: litellm
        image: docker.litellm.ai/berriai/litellm:main-latest
        ports:
        - containerPort: 4000
        env:
        - name: LITELLM_MASTER_KEY
          value: "sk-1234"
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: litellm-secrets
              key: database-url
```

---

## 故障排除

### 常见问题

1. **连接被拒绝**
   - 检查端口是否正确
   - 检查防火墙设置

2. **认证失败**
   - 确认主密钥正确
   - 检查请求头格式

3. **模型调用失败**
   - 验证API密钥
   - 检查网络连接
   - 查看日志

### 日志查看

```bash
# Docker日志
docker logs litellm

# Systemd日志
journalctl -u litellm -f
```

---

## 更多信息

- [配置详解](./LiteLLM_Config配置_中文版.md)
- [虚拟密钥](./LiteLLM_虚拟密钥_认证_中文版.md)
- [监控与日志](./LiteLLM_Admin管理界面_中文版.md)
