# 更正说明：关于 anthropic_mocking_enabled 参数

## ❌ 错误声明

在之前的文档中，我错误地提到了 `anthropic_mocking_enabled: true` 这个参数。

**这是错误的！该参数不是 LiteLLM 官方参数。**

---

## ✅ 正确配置

### LiteLLM 自动处理协议转换

LiteLLM 会**自动**在 Anthropic 格式和 OpenAI 格式之间转换，**无需任何额外配置**。

正确的配置只需要：

```yaml
model_list:
  - model_name: claude-qwen-72b
    litellm_params:
      model: openai/qwen-72b
      api_base: http://192.168.1.100:8000/v1
      api_key: sk-local-key

litellm_settings:
  drop_params: true    # 可选：丢弃不支持的参数
  set_verbose: true    # 可选：启用详细日志
  num_retries: 3       # 可选：重试次数
  request_timeout: 600 # 可选：超时时间（秒）
```

**不需要** `anthropic_mocking_enabled` 参数！

---

## 🔍 为什么会出错

我在之前的文档中混淆了以下概念：

1. **LiteLLM的 Passthrough 功能** - 允许直接调用 Anthropic 原生 API
2. **自动格式转换** - LiteLLM 自动处理 Anthropic ↔ OpenAI 格式转换

实际上，**LiteLLM 默认就会自动处理格式转换**，不需要特殊配置。

---

## 📚 官方文档参考

根据 LiteLLM 官方文档：

- **Anthropic 支持**: https://docs.litellm.ai/docs/providers/anthropic
- **Passthrough 模式**: https://litellm.vercel.app/docs/pass_through/anthropic_completion

LiteLLM 支持：
- ✅ 自动格式转换（Anthropic ↔ OpenAI）
- ✅ 所有主流参数（stream, temperature, max_tokens 等）
- ✅ 结构化输出
- ✅ 工具调用
- ✅ 流式响应

---

## ✅ 已更正的文件

以下文件已更新，移除了错误的参数：

1. [`LiteLLM_ClaudeCode 配置指南.md`](LiteLLM_ClaudeCode 配置指南.md)
   - ✅ 第 130 行：添加说明"LiteLLM 自动处理 Anthropic 格式转换，无需额外配置"
   - ✅ 第 287 行：移除错误参数，改为"LiteLLM 会自动处理协议转换"

2. [`ClaudeCode_LiteLLM_快速参考.md`](ClaudeCode_LiteLLM_快速参考.md)
   - ✅ 第 94 行：故障排查改为"添加 `drop_params: true`"
   - ✅ 第 138 行：添加注释"无需额外配置"

---

## 💡 正确的使用方式

### 最简单配置（推荐）

```powershell
# 一行命令启动
litellm --model openai/qwen-72b `
  --api_base http://192.168.1.100:8000/v1 `
  --api_key sk-local-key `
  --port 4000

# 设置环境变量
$env:ANTHROPIC_BASE_URL = "http://localhost:4000"
$env:ANTHROPIC_API_KEY = "sk-anthropic-key"

# 启动 Claude Code
claude
```

### 配置文件模式

```yaml
model_list:
  - model_name: claude-qwen-72b
    litellm_params:
      model: openai/qwen-72b
      api_base: http://192.168.1.100:8000/v1
      
litellm_settings:
  drop_params: true  # 仅此而已！
```

---

## 🎯 总结

### ❌ 错误做法
```yaml
litellm_settings:
  anthropic_mocking_enabled: true  # ❌ 这不是官方参数！
```

### ✅ 正确做法
```yaml
litellm_settings:
  drop_params: true  # ✅ 这样就够了
```

### 核心原理

```
Claude Code (Anthropic 格式)
    ↓
LiteLLM (自动转换)
    ↓
内网模型 (OpenAI 格式)
```

**LiteLLM 会自动处理所有格式转换工作！**

---

## 🙏 致歉

对于之前文档中的错误信息给大家造成的困扰，我深表歉意。

我会继续学习和验证，确保提供准确的信息。

感谢你的理解和耐心！🙏

---

## 📖 相关资源

- **LiteLLM 官方文档**: https://docs.litellm.ai/
- **Anthropic 集成**: https://docs.litellm.ai/docs/providers/anthropic
- **GitHub Issues**: https://github.com/BerriAI/litellm/issues

如有任何疑问，欢迎查看官方文档或提出讨论。
