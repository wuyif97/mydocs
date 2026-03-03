# Claude Code Router 官方文档（中文版）

## 目录

1. [简介](#简介)
2. [核心特性](#核心特性)
3. [快速开始](#快速开始)
4. [配置指南](#配置指南)
5. [路由系统](#路由系统)
6. [CLI 命令](#cli-命令)
7. [高级功能](#高级功能)
8. [故障排除](#故障排除)

---

## 简介

### 什么是 Claude Code Router？

Claude Code Router（CCR）是一个强大的中间件工具，作为 Claude Code CLI 与多个 AI 后端提供商之间的兼容层。它允许开发者：

- **动态切换模型**：在不同 AI 模型之间无缝切换
- **多提供商支持**：连接 OpenRouter、DeepSeek、Ollama、Gemini、Volcengine、SiliconFlow 等
- **智能路由**：根据任务类型自动路由到最合适的模型
- **成本优化**：为常规任务使用更经济的模型，复杂场景保留 Claude
- **隐私保护**：支持本地部署模型，同时按需使用云端模型

### 为什么需要 Claude Code Router？

⚡ **极速启动** - 只需一个命令，几分钟内即可开始使用，无需复杂配置

🎯 **智能路由** - 根据上下文长度、任务类型和自定义规则，自动将请求路由到最佳模型

🔌 **多提供商支持** - 支持 DeepSeek、Gemini、Groq、OpenRouter 等，易于扩展自定义转换器

💰 **成本效益** - 为常规任务使用更经济的模型，同时保持质量

🛠️ **Agent 系统** - 可扩展的 agent 架构，支持自定义工具和工作流，内置图像任务支持

🔧 **高度可定制** - 按项目配置路由，设置转换器，微调工作流的每个方面

---

## 核心特性

### 1. 模型路由
根据需求将请求路由到不同的模型（例如：后台任务、思考、长上下文）

### 2. 多提供商支持
支持各种模型提供商：
- OpenRouter
- DeepSeek
- Ollama（本地）
- Google Gemini
- Volcengine（火山引擎）
- SiliconFlow（硅基流动）
- Groq
- 阿里云通义千问

### 3. 请求/响应转换
使用 transformers 为不同提供商自定义请求和响应格式

### 4. 动态模型切换
在 Claude Code 中使用 `/model` 命令实时切换模型

### 5. CLI 模型管理
通过终端命令 `ccr model` 管理和配置模型及提供商

### 6. GitHub Actions 集成
在 CI/CD 工作流中触发 Claude Code 任务

### 7. 插件系统
通过自定义 transformers 扩展功能

### 8. Preset 系统
保存、分享和重用配置

---

## 快速开始

### 1. 安装

首先确保已安装 Claude Code：

```bash
npm install -g @anthropic-ai/claude-code
```

然后安装 Claude Code Router：

```bash
npm install -g @musistudio/claude-code-router
```

### 2. 配置

创建并配置 `~/.claude-code-router/config.json` 文件。

#### 配置方式 A：直接编辑配置文件

编辑 `~/.claude-code-router/config.json`：

```json
{
  "HOST": "0.0.0.0",
  "PORT": 8080,
  "Providers": [
    {
      "name": "openai",
      "api_base_url": "https://api.openai.com/v1/chat/completions",
      "api_key": "your-api-key-here",
      "models": ["gpt-4", "gpt-3.5-turbo"]
    }
  ],
  "Router": {
    "default": "openai,gpt-4"
  }
}
```

#### 配置方式 B：使用 Web UI

```bash
ccr ui
```

这将打开 Web 界面，可以可视化地配置提供商。

### 3. 启动路由器

```bash
ccr start
```

路由器将默认在 `http://localhost:8080` 上运行。

### 4. 使用 Claude Code

现在可以正常使用 Claude Code：

```bash
ccr code
```

你的请求将通过 Claude Code Router 路由到配置的提供商。

### 5. 配置更改后重启

如果修改了配置文件或通过 Web UI 进行了更改，需要重启服务：

```bash
ccr restart
```

或者直接在 Web UI 中重启。

---

## 配置指南

### 配置文件位置

```
~/.claude-code-router/config.json
```

该文件在首次运行 `ccr start` 或 `ccr code` 时自动创建。支持 JSON5 格式，允许注释和尾随逗号，便于编辑。

### 环境变量插值

Claude Code Router 支持在配置值中进行环境变量替换，允许将敏感数据（如 API 密钥）存储在配置文件之外。

#### 插值语法

支持两种语法：
1. `$VAR_NAME` - 简单变量引用
2. `${VAR_NAME}` - 括号变量引用（当变量名与其他文本相邻时使用）

#### 示例

环境变量：
```bash
export DEEPSEEK_API_KEY="sk-xxx"
export GEMINI_API_KEY="gemini-xxx"
```

配置文件：
```json
{
  "Providers": [
    {
      "name": "deepseek",
      "api_key": "$DEEPSEEK_API_KEY",
      "models": ["deepseek-chat"]
    },
    {
      "name": "gemini",
      "api_key": "${GEMINI_API_KEY}",
      "models": ["gemini-2.5-pro"]
    }
  ]
}
```

运行时会自动替换为实际的环境变量值。

### 全局配置选项

除了 Providers 和 Router，配置文件还支持多个全局设置：

#### 服务器设置

| 字段 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| HOST | string | "127.0.0.1" | 服务器绑定地址（如果未设置 APIKEY，则强制为 127.0.0.1） |
| PORT | number | 3456 | 服务器监听端口 |
| APIKEY | string | null | 可选的 API 访问认证密钥 |

#### 日志设置

| 字段 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| LOG | boolean | true | 启用/禁用文件日志 |
| LOG_LEVEL | string | "debug" | 日志级别：fatal, error, warn, info, debug, trace |

#### 网络设置

| 字段 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| PROXY_URL | string | null | 出站 API 请求的 HTTP 代理 |
| API_TIMEOUT_MS | number | 600000 | LLM API 调用超时（10 分钟） |

#### 自动化设置

| 字段 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| NON_INTERACTIVE_MODE | boolean | false | 为 CI/CD 环境（GitHub Actions、Docker）启用 |

### 提供商配置

Providers 数组中的每个提供商代表一个 LLM 服务端点。

#### 必需字段

| 字段 | 类型 | 描述 |
|------|------|------|
| name | string | 提供商的唯一标识符（用于路由引用） |
| api_base_url | string | 聊天完成的完整 API 端点 URL |
| api_key | string | 提供商的认证密钥（支持环境变量） |
| models | string[] | 该提供商可用的模型标识符数组 |

#### 可选字段

| 字段 | 类型 | 描述 |
|------|------|------|
| transformer | object | 定义请求/响应转换（见转换器配置） |

#### 提供商配置示例

**OpenRouter 配置：**
```json
{
  "name": "openrouter",
  "api_base_url": "https://openrouter.ai/api/v1/chat/completions",
  "api_key": "sk-xxx",
  "models": [
    "google/gemini-2.5-pro-preview",
    "anthropic/claude-sonnet-4",
    "anthropic/claude-3.5-sonnet"
  ],
  "transformer": {
    "use": ["openrouter"]
  }
}
```

**DeepSeek 配置：**
```json
{
  "name": "deepseek",
  "api_base_url": "https://api.deepseek.com/chat/completions",
  "api_key": "sk-xxx",
  "models": ["deepseek-chat", "deepseek-reasoner"],
  "transformer": {
    "use": ["deepseek"],
    "deepseek-chat": {
      "use": ["tooluse"]
    }
  }
}
```

**本地 Ollama 配置：**
```json
{
  "name": "ollama",
  "api_base_url": "http://localhost:11434/v1/chat/completions",
  "api_key": "ollama",
  "models": ["qwen2.5-coder:latest"]
}
```

**Google Gemini 配置：**
```json
{
  "name": "gemini",
  "api_base_url": "https://generativelanguage.googleapis.com/v1beta/models/",
  "api_key": "sk-xxx",
  "models": ["gemini-2.5-flash", "gemini-2.5-pro"],
  "transformer": {
    "use": ["gemini"]
  }
}
```

### 最小化配置示例

最简单的可用配置只需要一个提供商定义和一个默认路由：

```json
{
  "Providers": [
    {
      "name": "openai",
      "api_base_url": "https://api.openai.com/v1/chat/completions",
      "api_key": "sk-your-key",
      "models": ["gpt-4"]
    }
  ],
  "Router": {
    "default": "openai,gpt-4"
  }
}
```

此配置告诉 Claude Code Router 将所有请求路由到 openai 提供商的 gpt-4 模型。

### 完整配置示例

```json
{
  "APIKEY": "your-secret-key",
  "PROXY_URL": "http://127.0.0.1:7890",
  "LOG": true,
  "API_TIMEOUT_MS": 600000,
  "NON_INTERACTIVE_MODE": false,
  "Providers": [
    {
      "name": "openrouter",
      "api_base_url": "https://openrouter.ai/api/v1/chat/completions",
      "api_key": "sk-xxx",
      "models": [
        "google/gemini-2.5-pro-preview",
        "anthropic/claude-sonnet-4",
        "anthropic/claude-3.5-sonnet",
        "anthropic/claude-3.7-sonnet:thinking"
      ],
      "transformer": {
        "use": ["openrouter"]
      }
    },
    {
      "name": "deepseek",
      "api_base_url": "https://api.deepseek.com/chat/completions",
      "api_key": "sk-xxx",
      "models": ["deepseek-chat", "deepseek-reasoner"],
      "transformer": {
        "use": ["deepseek"],
        "deepseek-chat": {
          "use": ["tooluse"]
        }
      }
    },
    {
      "name": "ollama",
      "api_base_url": "http://localhost:11434/v1/chat/completions",
      "api_key": "ollama",
      "models": ["qwen2.5-coder:latest"]
    },
    {
      "name": "gemini",
      "api_base_url": "https://generativelanguage.googleapis.com/v1beta/models/",
      "api_key": "sk-xxx",
      "models": ["gemini-2.5-flash", "gemini-2.5-pro"],
      "transformer": {
        "use": ["gemini"]
      }
    },
    {
      "name": "volcengine",
      "api_base_url": "https://ark.cn-beijing.volces.com/api/v3/chat/completions",
      "api_key": "sk-xxx",
      "models": ["deepseek-v3-250324", "deepseek-r1-250528"],
      "transformer": {
        "use": ["deepseek"]
      }
    }
  ],
  "Router": {
    "default": "deepseek,deepseek-chat",
    "background": "ollama,qwen2.5-coder:latest",
    "think": "deepseek,deepseek-reasoner",
    "longContext": "openrouter,google/gemini-2.5-pro-preview",
    "longContextThreshold": 60000,
    "webSearch": "gemini,gemini-2.5-flash"
  }
}
```

此配置：
- 启用 APIKEY 认证
- 监听所有接口（0.0.0.0）
- 配置了 5 个提供商（OpenRouter、DeepSeek、Ollama、Gemini、火山引擎）
- 使用环境变量存储 API 密钥
- 为不同场景路由到合适的模型
- 提供完整的降级链

---

## 路由系统

### 基本路由结构

Router 对象定义了不同请求类型使用的模型。路由系统实现基于场景的路由，请求被分类并路由到适当的模型。

#### 路由字段

| 字段 | 必需 | 描述 | 默认 |
|------|------|------|------|
| default | 是 | 一般请求的主要模型 | - |
| background | 否 | 后台/轻量级任务的模型 | 使用 default |
| think | 否 | 重推理任务的模型 | 使用 default |
| longContext | 否 | 超过令牌阈值请求的模型 | 使用 default |
| longContextThreshold | 否 | longContext 路由的令牌计数阈值 | 60000 |
| webSearch | 否 | 网络搜索请求的模型 | 使用 default |
| image | 否 | 图像处理请求的模型 | 使用 default |
| fallback | 否 | 如果主要模型失败，有序的降级模型列表 | [] |

### 路由值格式

路由值使用格式：`"provider_name,model_name"`

- `provider_name`：必须匹配 Providers 数组中的 name 字段
- `model_name`：必须在该提供商的 models 数组中列出

示例：
```json
"default": "openai,gpt-4"
```

这引用了名为"openai"的提供商的"gpt-4"模型。

### 路由选择逻辑

系统根据以下规则自动选择路由：

1. **默认路由**：所有未特别指定的请求使用 `default`
2. **后台任务**：轻量级、非关键任务使用 `background`
3. **深度思考**：需要复杂推理的任务使用 `think`
4. **长上下文**：超过 `longContextThreshold`（默认 60000 令牌）的请求使用 `longContext`
5. **网络搜索**：涉及网络搜索的请求使用 `webSearch`
6. **图像处理**：包含图像的请求使用 `image`

### 动态模型切换

在 Claude Code 会话中，可以使用 `/model` 命令动态切换模型：

```
/model deepseek,deepseek-chat
/model openrouter,google/gemini-2.5-pro-preview
```

这允许在运行时根据需要切换到不同的模型。

---

## CLI 命令

### 命令概览

| 命令 | 描述 |
|------|------|
| `ccr start` | 启动路由器服务 |
| `ccr stop` | 停止路由器服务 |
| `ccr restart` | 重启路由器服务 |
| `ccr status` | 查看服务状态 |
| `ccr code` | 通过路由器启动 Claude Code |
| `ccr ui` | 打开 Web 配置界面 |
| `ccr model` | 交互式模型选择器 |
| `ccr preset` | Preset 管理命令 |

### 服务管理

#### 启动服务
```bash
ccr start
```

#### 停止服务
```bash
ccr stop
```

#### 重启服务
```bash
ccr restart
```

#### 查看状态
```bash
ccr status
```

### 代码命令

#### 启动 Claude Code
```bash
ccr code
```

这将通过路由器启动 Claude Code，所有请求将根据配置进行路由。

### 模型选择器

#### 交互式模型管理
```bash
ccr model
```

提供交互式界面来：
- 查看当前配置
- 查看所有已配置的模型（default、background、think、longContext、webSearch、image）
- 切换模型：快速更改每个路由类型使用的模型
- 添加新模型：向现有提供商添加模型
- 创建新提供商：设置完整的提供商配置

### Preset 命令

Preset 允许轻松保存、分享和重用配置。

#### 导出当前配置为 preset
```bash
ccr preset export my-preset
```

#### 带元数据导出
```bash
ccr preset export my-preset --description "我的 OpenAI 配置" --author "你的名字" --tags "openai,production"
```

#### 从本地目录安装 preset
```bash
ccr preset install /path/to/preset
```

#### 列出所有已安装的 preset
```bash
ccr preset list
```

#### 显示 preset 信息
```bash
ccr preset info my-preset
```

#### 删除 preset
```bash
ccr preset delete my-preset
```

#### Preset 特性

- **导出**：将当前配置保存为 preset 目录（包含 manifest.json）
- **安装**：从本地目录安装 preset
- **敏感数据处理**：API 密钥和其他敏感数据在导出时自动清理（标记为 `{{field}}` 占位符）
- **动态配置**：Presets 支持动态配置和 schema 验证

---

## 高级功能

### 转换器系统（Transformers）

转换器允许你为不同的提供商自定义请求和响应格式。

#### 内置转换器

- **openrouter**：适配 OpenRouter API 格式
- **deepseek**：适配 DeepSeek API 格式
- **gemini**：适配 Google Gemini API 格式
- **tooluse**：处理工具调用格式
- **maxtoken**：控制最大令牌数
- **enhancetool**：增强工具功能
- **reasoning**：处理推理模型特殊格式

#### 转换器配置示例

```json
{
  "name": "deepseek",
  "api_base_url": "https://api.deepseek.com/chat/completions",
  "api_key": "sk-xxx",
  "models": ["deepseek-chat", "deepseek-reasoner"],
  "transformer": {
    "use": ["deepseek"],
    "deepseek-chat": {
      "use": ["tooluse"]
    },
    "deepseek-reasoner": {
      "use": ["reasoning"]
    }
  }
}
```

#### 自定义转换器

你可以创建自定义转换器来处理特殊的 API 格式：

```javascript
// custom-transformer.js
module.exports = {
  transformRequest: (request) => {
    // 自定义请求转换逻辑
    return modifiedRequest;
  },
  transformResponse: (response) => {
    // 自定义响应转换逻辑
    return modifiedResponse;
  }
};
```

### 自定义路由脚本

通过 `CUSTOM_ROUTER_PATH` 配置项，可以使用自定义 JavaScript 函数来控制路由逻辑：

```json
{
  "CUSTOM_ROUTER_PATH": "/path/to/custom-router.js"
}
```

### Tokenizer 系统

Claude Code Router 支持多种 tokenizer：

- **Tiktoken**：OpenAI 风格的 tokenizer
- **HuggingFace**：HuggingFace 风格的 tokenizer
- **API Tokenizer**：通过 API 调用的 tokenizer

### Agent 系统

#### 图像 Agent
内置支持图像处理任务，可以自动路由到支持图像的模型。

#### 自定义 Agents
可以创建自定义 agent 来处理特殊任务类型。

### 插件系统

#### Token Speed 插件
优化令牌处理速度。

#### 自定义插件
通过插件系统扩展功能。

### 输出处理器

#### 状态行
自定义输出状态显示。

#### 主题
支持不同的显示主题。

### Web UI

通过 `ccr ui` 命令打开 Web 界面，提供：
- 配置管理
- 提供商管理
- Preset 管理
- 日志查看器

---

## 日志系统

Claude Code Router 使用两个独立的日志系统：

### 服务器级日志
- HTTP 请求、API 调用和服务器事件
- 使用 pino 记录
- 位置：`~/.claude-code-router/logs/`
- 文件名格式：`ccr-*.log`

### 应用级日志
- 路由决策和业务逻辑事件
- 位置：`~/.claude-code-router/claude-code-router.log`

### 日志级别

可用的日志级别：
- `fatal` - 致命错误
- `error` - 错误
- `warn` - 警告
- `info` - 信息
- `debug` - 调试
- `trace` - 跟踪

在配置文件中设置：
```json
{
  "LOG": true,
  "LOG_LEVEL": "debug"
}
```

---

## 配置备份系统

每次配置更新时（通过 API 或 UI），系统会自动创建备份：

### 备份位置
```
~/.claude-code-router/config.backup.{timestamp}.json
```

### 备份命名
```
config.backup.1704067200000.json  // 毫秒级 Unix 时间戳
```

### 恢复备份
```bash
cp ~/.claude-code-router/config.backup.1704067200000.json ~/.claude-code-router/config.json
ccr restart
```

---

## 配置生命周期

### 加载和验证

配置在服务启动时加载和验证。

### 配置更新流程

当配置被修改时（通过文件编辑或 Web UI），系统按以下步骤处理：

1. **创建备份**：原始配置备份到 `config.backup.{timestamp}.json`
2. **写入新配置**：新配置写入 `config.json`
3. **验证**：新配置在应用前进行验证
4. **需要重启**：服务器必须重启才能加载新配置（结构性更改不支持热重载）

### 重启方法

- 命令行：`ccr restart`
- Web UI：通过界面重启按钮

### 热重载限制

当前的配置系统不支持热重载。任何配置更改都需要完全重启服务。这影响：

- 提供商添加/删除
- 模型列表更改
- 路由规则修改
- 转换器配置
- 全局设置

---

## 故障排除

### 服务无法启动

**问题**：运行 `ccr start` 后服务没有响应

**解决方案**：
1. 检查配置文件语法是否正确（使用 JSON5 验证器）
2. 确认端口未被占用：`netstat -ano | findstr :3456`
3. 查看日志文件：`~/.claude-code-router/logs/ccr-*.log`
4. 尝试使用默认配置重新启动

### 提供商连接问题

**问题**：无法连接到配置的提供商

**解决方案**：
1. 验证 API 密钥是否正确
2. 检查网络连接和代理设置
3. 确认 `api_base_url` 是否正确
4. 测试 API 端点可达性：
   ```bash
   curl -X POST https://api.example.com/v1/chat/completions \
     -H "Authorization: Bearer YOUR_KEY" \
     -H "Content-Type: application/json"
   ```

### 路由问题

**问题**：请求未路由到预期的模型

**解决方案**：
1. 检查 Router 配置中的模型名称是否与 Providers 中的完全匹配
2. 确认格式为 `"provider_name,model_name"`
3. 查看应用日志了解路由决策
4. 使用 `ccr model` 检查当前配置

### 配置问题

**问题**：配置更改未生效

**解决方案**：
1. 确保已执行 `ccr restart`
2. 检查配置文件是否成功保存
3. 验证 JSON 语法（注意 JSON5 支持注释和尾随逗号）
4. 查看备份文件确认更改已应用

### 常见错误

#### 错误：端口已被占用
```bash
# 查找占用端口的进程
netstat -ano | findstr :3456
# 终止进程或使用不同端口
```

#### 错误：无效的 API 密钥
- 检查环境变量是否正确设置
- 确认配置文件中使用了正确的变量引用语法
- 验证 API 密钥未过期

#### 错误：模型不存在
- 确认模型名称在提供商的 models 数组中
- 检查拼写错误
- 验证模型对您的 API 密钥可用

---

## 安全最佳实践

### 1. API 密钥管理
- 始终使用环境变量存储 API 密钥
- 不要将包含真实密钥的配置文件提交到版本控制
- 定期轮换 API 密钥

### 2. 访问控制
- 设置 `APIKEY` 限制对路由器的访问
- 如果设置了 `APIKEY`，将 `HOST` 设置为 `127.0.0.1`
- 不要在公共网络上暴露路由器

### 3. 日志安全
- 定期清理日志文件
- 在生产环境中设置适当的 `LOG_LEVEL`
- 不要在日志中记录敏感信息

### 4. 网络安全
- 使用 `PROXY_URL` 通过代理进行 API 调用
- 配置防火墙规则限制访问
- 考虑使用 HTTPS（如果暴露在网络上）

---

## 适用场景

### 适合谁使用？

💰 **注重成本的开发者**
- 将 API 成本降低 10 倍，同时保持大多数任务的质量

🔒 **注重隐私的团队**
- 使用本地部署的模型保留代码，同时在需要时使用 Claude

🔄 **多模型工作流**
- 为不同任务使用不同模型，无需切换工具

⚡ **Claude Code 高级用户**
- 使用自定义提供商和路由策略扩展 Claude Code

---

## 资源链接

- **GitHub 仓库**：https://github.com/musistudio/claude-code-router
- **官方文档**：https://musistudio.github.io/claude-code-router/
- **社区讨论**：https://github.com/musistudio/claude-code-router/discussions
- **配置示例**：参考本文档中的完整配置示例

---

## 更新日志

本文档基于 Claude Code Router 最新版本，项目持续维护中，拥有超过 28,700 颗星标。

**许可证**：MIT License

**赞助商**：Z.ai - GLM CODING PLAN 订阅服务，每月仅需 3 美元起，可在 10+ 款流行 AI 编码工具中使用 GLM-4.7 模型。

---

*文档最后更新：2026 年 3 月*
