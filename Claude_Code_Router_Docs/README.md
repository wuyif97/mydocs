# Claude Code Router 中文文档

本目录包含 Claude Code Router 的完整中文文档和配置示例。

## 📚 文档内容

### 1. [官方文档完整版](./Claude_Code_Router_官方文档中文版.md)
- 完整的官方文档翻译
- 包含所有功能说明、配置选项和使用指南
- 905 行详细文档

**内容涵盖：**
- ✅ 简介与核心特性
- ✅ 快速开始指南
- ✅ 详细配置说明
- ✅ 路由系统详解
- ✅ CLI 命令手册
- ✅ 高级功能（Transformers、Plugins、Agents）
- ✅ 日志系统说明
- ✅ 故障排除指南
- ✅ 安全最佳实践

### 2. [配置示例](./config.example.json)
- 完整的配置文件示例
- 包含 8 个主流提供商配置
- 详细的中文注释说明
- 可直接使用或作为模板

**支持的提供商：**
- ✅ DeepSeek（深度求索）
- ✅ OpenRouter（多模型聚合）
- ✅ Google Gemini
- ✅ Ollama（本地部署）
- ✅ 火山引擎
- ✅ SiliconFlow（硅基流动）
- ✅ Groq
- ✅ 阿里云通义千问

### 3. [快速参考卡片](./快速参考卡片.md)
- 常用命令速查
- 配置要点总结
- 故障排除命令
- 成本优化策略
- 233 行精炼内容

## 🎯 快速上手

### 第一步：安装
```bash
npm install -g @anthropic-ai/claude-code
npm install -g @musistudio/claude-code-router
```

### 第二步：阅读文档
1. 先阅读 **快速参考卡片** 了解基本命令
2. 查看 **官方文档完整版** 的"快速开始"章节
3. 参考 **配置示例** 创建自己的配置

### 第三步：配置使用
```bash
# 方式 A：使用 Web UI（推荐新手）
ccr ui

# 方式 B：直接编辑配置文件
# 复制 config.example.json 到 ~/.claude-code-router/config.json
# 然后修改 API 密钥

# 启动服务
ccr start

# 使用 Claude Code
ccr code
```

## 📖 阅读建议

### 新手用户
1. 📋 快速参考卡片 → 常用命令
2. 📘 官方文档 → 快速开始章节
3. 🔧 配置示例 → 最小化配置
4. 🚀 开始使用

### 进阶用户
1. 📘 官方文档 → 完整阅读
2. 🔧 配置示例 → 参考高级配置
3. 🛠️ 尝试 Transformers 和 Plugins
4. 💡 自定义路由策略

### 特定需求

#### 想了解路由系统
- 📘 官方文档 → "路由系统" 章节
- 🔧 配置示例 → Router 配置部分

#### 想配置新提供商
- 📘 官方文档 → "提供商配置" 章节
- 🔧 配置示例 → 对应提供商配置

#### 遇到使用问题
- 📘 官方文档 → "故障排除" 章节
- 📋 快速参考卡片 → 故障排除命令

#### 想优化成本
- 📘 官方文档 → "适用场景" 章节
- 📋 快速参考卡片 → 成本优化策略

## 🌟 核心特性

### ⚡ 智能路由
根据任务类型自动选择最佳模型：
- 日常对话 → 经济模型
- 复杂推理 → 高性能模型
- 长文档处理 → 大上下文模型
- 后台任务 → 轻量模型

### 💰 成本优化
- 本地模型免费使用
- 简单任务用便宜模型
- 复杂任务用高端模型
- 成本可降低 10 倍

### 🔒 隐私保护
- 支持本地部署（Ollama）
- 敏感代码本地处理
- 必要时使用云端模型

### 🔄 灵活切换
- 命令行一键切换
- 会话中动态切换
- Web 界面可视化配置

## 🛠️ 使用场景

### 场景 1：个人开发者
**配置建议：**
- 默认：Ollama 本地模型（免费、快速）
- 思考：DeepSeek Reasoner（强大推理）
- 降级：备用本地模型

**优势：** 零成本开发，按需使用付费模型

### 场景 2：小团队
**配置建议：**
- 默认：DeepSeek Chat（性价比高）
- 后台：Ollama 本地
- 重要任务：Claude/Gemini Pro

**优势：** 平衡成本和质量

### 场景 3：企业用户
**配置建议：**
- 多提供商冗余
- 完整的降级链
- 严格的访问控制

**优势：** 高可用性、安全性

## 📊 文档结构

```
Claude_Code_Router_Docs/
├── README.md                           # 本文件（总览）
├── Claude_Code_Router_官方文档中文版.md  # 完整翻译（905 行）
├── config.example.json                 # 配置示例（158 行）
└── 快速参考卡片.md                      # 快速参考（233 行）
```

## 🔗 官方资源

- **GitHub**: https://github.com/musistudio/claude-code-router
- **官方文档**: https://musistudio.github.io/claude-code-router/
- **社区讨论**: https://github.com/musistudio/claude-code-router/discussions
- **NPM 包**: 
  - `@anthropic-ai/claude-code` (Claude Code)
  - `@musistudio/claude-code-router` (Router)

## 📝 文档版本

- **翻译版本**: 基于最新版本完整翻译
- **最后更新**: 2026 年 3 月
- **项目状态**: 活跃维护中（28,700+ stars）
- **许可证**: MIT License

## 💡 提示

### 环境变量管理
建议创建 `.env` 文件存储 API 密钥：
```bash
DEEPSEEK_API_KEY=sk-xxx
OPENROUTER_API_KEY=sk-xxx
GEMINI_API_KEY=xxx
```

### 配置备份
定期备份配置文件：
```bash
cp ~/.claude-code-router/config.json ./backup/config-$(date +%Y%m%d).json
```

### 日志查看
实时监控日志：
```bash
# Windows PowerShell
Get-Content ~/.claude-code-router/claude-code-router.log -Wait -Tail 50

# Linux/Mac
tail -f ~/.claude-code-router/claude-code-router.log
```

## 🤝 贡献

本文档为社区翻译版本，如有错误或遗漏，欢迎指正。

---

**祝你使用愉快！** 🎉

如有问题，请参考完整文档或查看官方资源。
