# Web AI Agent - 使用手册

## 项目简介

Web AI Agent 是一个基于 AI 的网页自动化工具，能够自动学习网页结构并生成可复用的操作技能。通过自然语言指令即可控制浏览器执行各种网页操作。

## 核心功能

- **自动学习网页**: 自动分析网页元素，识别可交互组件
- **AI 生成技能**: 使用大语言模型自动生成高频操作技能
- **自然语言执行**: 使用自然语言指令执行自动化任务
- **技能复用**: 学习一次，多次复用

## 系统要求

- Python 3.8+
- Windows 操作系统
- Chrome/Edge 浏览器
- Ollama 本地大模型服务

## 快速开始

### 1. 项目安装

```bash
# 克隆或下载项目
cd web-ai-agent

# 安装依赖
pip install -r requirements.txt
```

### 2. 环境配置

编辑 `.env` 文件，配置你的 API 信息：

```env
GLM_TOKEN=ollama
GLM_BASE_URL=http://127.0.0.1:11434/v1
GLM_MODEL=qwen2.5:32b
SKILL_DIR=./skills
```

### 3. 启动 Ollama 服务

确保本地 Ollama 服务正在运行：

```bash
# 启动 Ollama
ollama serve

# 下载模型（如果还没有）
ollama pull qwen2.5:32b
```

## 使用方法

### 模式一：学习网页

自动学习网页结构并生成技能：

```bash
python web_agent.py learn --url "https://www.baidu.com/"
```

**输出示例：**
```
[INFO] 正在打开网页: https://www.baidu.com/
[INFO] 页面元素已提取，ID: e81c1f57
[SUCCESS] AI 已生成 3 个技能，保存至: skills\e81c1f57
```

学习完成后，会在 `skills/` 目录下生成对应页面ID的文件夹，包含：
- `elements.json` - 页面元素数据
- `skills.yaml` - AI 生成的技能文件

### 模式二：执行技能

使用自然语言指令执行自动化任务：

```bash
python web_agent.py run --page_id e81c1f57 --intent "搜索"
```

**支持的指令类型：**
- 搜索相关：搜索、search、查询
- 导航相关：导航、访问、跳转
- 登录相关：登录、注册
- 其他自定义技能

## 技能文件格式

`skills.yaml` 文件结构：

```yaml
skills:
  - description: 在百度搜索框输入关键词并点击搜索按钮
    intent_keywords:
      - 搜索
      - search
      - 查询
    skill_id: search_baidu
    steps:
      - action: input
        target_selector: '#kw'
        value: '{search_text}'
      - action: click
        target_selector: '#su'
```

## 支持的操作类型

| 操作类型 | 说明 | 示例 |
|---------|------|------|
| `input` | 输入文本 | 在搜索框输入内容 |
| `click` | 点击元素 | 点击按钮或链接 |
| `wait` | 等待加载 | 等待页面加载完成 |
| `select` | 选择选项 | 从下拉框选择 |

## 高级用法

### 自定义技能

手动编辑 `skills.yaml` 文件，添加自定义技能：

```yaml
skills:
  - description: 登录网站
    intent_keywords:
      - 登录
      - login
    skill_id: login_site
    steps:
      - action: input
        target_selector: '#username'
        value: '{username}'
      - action: input
        target_selector: '#password'
        value: '{password}'
      - action: click
        target_selector: '#login-btn'
```

### 参数替换

在技能中使用参数占位符，程序会自动替换：

```yaml
value: '{search_text}'  # 会被替换为实际搜索内容
```

支持的默认参数：
- `username`: test
- `password`: 123456
- `search_text`: AI

## 故障排除

### 问题 1：元素未找到

**错误信息：**
```
[ERROR] 元素未找到: #kw
```

**解决方案：**
- 检查页面是否完全加载
- 验证选择器是否正确
- 尝试增加超时时间

### 问题 2：点击失败

**错误信息：**
```
[WARNING] 点击失败: 该元素没有位置及大小
```

**解决方案：**
- 程序会自动尝试使用 JavaScript 点击
- 检查元素是否可见和可交互

### 问题 3：AI 生成技能失败

**错误信息：**
```
[ERROR] AI 生成失败: Connection error
```

**解决方案：**
- 检查 Ollama 服务是否运行
- 验证 API 配置是否正确
- 检查网络连接

## 项目结构

```
web-ai-agent/
├── .env                  # 配置文件
├── web_agent.py          # 核心程序
├── requirements.txt      # 依赖清单
├── skills/               # 技能库目录
│   └── {page_id}/       # 页面技能文件夹
│       ├── elements.json # 页面元素数据
│       └── skills.yaml   # 生成的技能
└── README.md             # 使用手册
```

## 技术栈

- **DrissionPage**: 浏览器自动化
- **OpenAI SDK**: AI 接口调用
- **PyYAML**: 配置文件解析
- **Ollama**: 本地大模型服务

## 注意事项

1. **浏览器兼容性**: 建议使用最新版本的 Chrome 或 Edge
2. **网络连接**: 首次学习网页需要网络连接
3. **模型选择**: 根据电脑配置选择合适的模型大小
4. **技能质量**: AI 生成的技能可能需要手动调整优化

## 常见问题

**Q: 支持哪些网页？**
A: 支持大部分基于 HTML 的网页，包括单页应用。

**Q: 可以同时学习多个网页吗？**
A: 可以，每个网页会生成独立的技能文件。

**Q: 技能可以分享吗？**
A: 可以，直接复制 `skills/` 目录下的对应文件夹即可。

**Q: 如何调试技能执行过程？**
A: 程序会输出详细的执行日志，包括每个步骤的执行结果。

## 更新日志

### v1.0.0 (2026-04-28)
- 初始版本发布
- 支持网页学习和技能生成
- 支持自然语言指令执行
- 集成 Ollama 本地模型

## 许可证

MIT License

## 联系方式

如有问题或建议，请提交 Issue。
