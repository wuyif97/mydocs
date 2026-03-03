# Claude Code + LiteLLM - 快速参考卡片

## 🎯 一句话总结

**用 LiteLLM 作为桥梁，让 Claude Code 能够使用内网大模型。**

---

## ⚡ 30 秒快速上手

### 最简单方式（运行脚本）

```powershell
cd C:\Users\wyf\Desktop\ccr
.\start-claude-with-litellm.ps1
# 选择选项 "1"（标准模式）
```

自动完成：
1. ✅ 启动 LiteLLM Proxy
2. ✅ 设置环境变量
3. ✅ 启动 Claude Code

---

## 🔧 手动配置（3 步）

### 1️⃣ 启动 LiteLLM

```powershell
litellm --model openai/qwen-72b `
  --api_base http://192.168.1.100:8000/v1 `
  --api_key sk-local-key `
  --port 4000
```

### 2️⃣ 设置环境变量

```powershell
$env:ANTHROPIC_BASE_URL = "http://localhost:4000"
$env:ANTHROPIC_API_KEY = "sk-anthropic-key"
```

### 3️⃣ 启动 Claude Code

```powershell
claude
```

---

## 💻 实际使用示例

### 对话示例

```bash
# 启动后在 Claude Code 中输入
你好，请用 Python 写一个快速排序
```

### 文件操作

```bash
# 查看并修改文件
请帮我优化这个文件的代码性能
```

### 代码解释

```bash
# 请求解释代码
这段代码是什么意思？（附带代码）
```

---

## 🛠️ 常用命令速查

| 功能 | 命令 |
|------|------|
| **启动 LiteLLM** | `litellm --model openai/qwen-72b --api_base http://... --port 4000` |
| **设置环境变量** | `$env:ANTHROPIC_BASE_URL="http://localhost:4000"` |
| **启动 Claude Code** | `claude` |
| **测试连接** | `curl http://localhost:4000/health` |
| **停止服务** | `Ctrl+C` (LiteLLM) / 输入 `exit` (Claude Code) |

---

## 🔍 故障排查

| 问题 | 解决方案 |
|------|----------|
| ❌ Claude Code 无法连接 | 检查环境变量是否正确设置 |
| ❌ 返回格式错误 | 在 LiteLLM config 中添加 `drop_params: true` |
| ❌ 模型名称不对 | 确保使用正确的模型名称（如 `qwen-72b`） |
| ❌ 超时或无响应 | 增加 `request_timeout: 600` |
| ❌ 连接被拒绝 | 检查 LiteLLM 是否正常运行 |

---

## 📊 架构说明

```
用户输入
   ↓
Claude Code (Anthropic 格式)
   ↓
环境变量指向 LiteLLM (http://localhost:4000)
   ↓
LiteLLM 转换为 OpenAI 格式
   ↓
内网模型处理请求
   ↓
响应原路返回给 Claude Code
```

**关键点**：
- Claude Code 使用 Anthropic API 格式
- LiteLLM 负责双向协议转换
- 内网模型保持 OpenAI 格式不变

---

## 🎯 配置文件示例

### `config.yaml`（可选）

```yaml
model_list:
  - model_name: claude-qwen-72b
    litellm_params:
      model: openai/qwen-72b
      api_base: http://192.168.1.100:8000/v1
      api_key: sk-local-key

litellm_settings:
  drop_params: true
  # LiteLLM 自动处理协议转换，无需额外配置
```

启动：
```powershell
litellm --config config.yaml --port 4000
```

---

## 💡 实用技巧

### 技巧 1：永久环境变量（Windows）

```powershell
# 用户级别
[Environment]::SetEnvironmentVariable(
    "ANTHROPIC_BASE_URL", 
    "http://localhost:4000", 
    "User"
)
```

### 技巧 2：PowerShell 别名

在 `$PROFILE` 中添加：
```powershell
function Start-ClaudeLocal {
    $env:ANTHROPIC_BASE_URL = "http://localhost:4000"
    $env:ANTHROPIC_API_KEY = "sk-anthropic-key"
    claude
}
```

然后直接运行：
```powershell
Start-ClaudeLocal
```

### 技巧 3：后台运行

```powershell
# 后台启动 LiteLLM
Start-Job -ScriptBlock {
    litellm --model openai/qwen-72b `
      --api_base http://192.168.1.100:8000/v1 `
      --port 4000
}

# 设置环境变量
$env:ANTHROPIC_BASE_URL = "http://localhost:4000"

# 随时可以启动 Claude Code
claude
```

---

## 📋 支持的 Claude Code 功能

| 功能 | 支持状态 | 说明 |
|------|---------|------|
| **基本对话** | ✅ 完全支持 | 所有聊天功能正常 |
| **代码生成** | ✅ 完全支持 | 编程、调试、优化 |
| **文件读取** | ✅ 完全支持 | 查看和分析文件 |
| **文件修改** | ✅ 完全支持 | 编辑和保存更改 |
| **多轮对话** | ✅ 完全支持 | 上下文记忆正常 |
| **工具调用** | ⚠️ 部分支持 | 取决于内网模型能力 |

---

## 🆚 方案对比

### 方案 A：单独 LiteLLM ✅ 推荐新手
```powershell
litellm --model openai/qwen-72b --api_base ... --port 4000
$env:ANTHROPIC_BASE_URL = "http://localhost:4000"
claude
```
**优点**: 简单、快速  
**适用**: 个人使用、快速测试

### 方案 B：配置文件模式
```powershell
litellm --config config.yaml --port 4000
$env:ANTHROPIC_BASE_URL = "http://localhost:4000"
claude
```
**优点**: 支持多模型、高级功能  
**适用**: 生产环境、团队协作

### 方案 C：一键脚本 ⭐ 最推荐
```powershell
.\start-claude-with-litellm.ps1
# 选择选项 1
```
**优点**: 全自动、省心  
**适用**: 所有人

---

## 📁 相关文件

| 文件 | 用途 |
|------|------|
| [`start-claude-with-litellm.ps1`](start-claude-with-litellm.ps1) | 一键启动脚本 |
| [`LiteLLM_ClaudeCode 配置指南.md`](LiteLLM_ClaudeCode 配置指南.md) | 完整详细文档 |
| [`LiteLLM_独立使用_快速参考.md`](LiteLLM_独立使用_快速参考.md) | LiteLLM 通用参考 |

---

## 🔗 官方资源

- **Claude Code 文档**: https://docs.anthropic.com/claude-code/
- **LiteLLM 文档**: https://docs.litellm.ai/
- **GitHub Issues**: 
  - Claude Code: https://github.com/anthropics/claude-code
  - LiteLLM: https://github.com/BerriAI/litellm/issues

---

## 💬 常见问题

**Q: 需要安装 Claude Code Router 吗？**  
A: 不需要！只用 LiteLLM 就够了。

**Q: 支持哪些内网模型？**  
A: 任何提供 OpenAI兼容API的模型都支持。

**Q: 性能和原生 Claude 比如何？**  
A: 几乎一样，只多了 LiteLLM 的微小延迟（通常<10ms）。

**Q: 可以同时支持多个客户端吗？**  
A: 可以！LiteLLM 支持并发连接。

---

**开始使用吧！** 🎉

运行 `.\start-claude-with-litellm.ps1` 立即体验！
