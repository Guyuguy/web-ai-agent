# OpenCode 快速使用指南

## 一键启动项目

### 步骤 1：创建项目目录

```bash
mkdir web-ai-agent
cd web-ai-agent
```

### 步骤 2：创建配置文件

**创建 `.env` 文件：**
```env
GLM_TOKEN=ollama
GLM_BASE_URL=http://127.0.0.1:11434/v1
GLM_MODEL=qwen2.5:32b
SKILL_DIR=./skills
```

### 步骤 3：创建依赖文件

**创建 `requirements.txt`：**
```
DrissionPage>=4.1.0
openai>=1.30.0
pyyaml>=6.0
python-dotenv>=1.0.0
```

### 步骤 4：创建核心程序

创建 `web_agent.py` 文件，内容见项目源码。

### 步骤 5：安装依赖

```bash
pip install -r requirements.txt
```

## OpenCode 执行指令

### 学习新网页

```bash
# 学习百度首页
python web_agent.py learn --url "https://www.baidu.com/"

# 学习其他网站
python web_agent.py learn --url "https://www.example.com/"
```

### 执行技能

```bash
# 搜索功能
python web_agent.py run --page_id e81c1f57 --intent "搜索"

# 导航功能
python web_agent.py run --page_id e81c1f57 --intent "导航"

# 登录功能
python web_agent.py run --page_id e81c1f57 --intent "登录"
```

## 完整使用流程

### 1. 环境准备

```bash
# 启动 Ollama 服务
ollama serve

# 下载模型（如果需要）
ollama pull qwen2.5:32b
```

### 2. 学习网页

```bash
# 学习目标网页
python web_agent.py learn --url "https://www.baidu.com/"
```

### 3. 查看生成的技能

```bash
# 查看技能文件
cat skills/e81c1f57/skills.yaml
```

### 4. 执行自动化任务

```bash
# 执行搜索任务
python web_agent.py run --page_id e81c1f57 --intent "搜索"
```

## 快速测试命令

```bash
# 一键测试（假设已安装）
python web_agent.py learn --url "https://www.baidu.com/" && python web_agent.py run --page_id e81c1f57 --intent "搜索"
```

## 自定义技能模板

```yaml
skills:
  - description: 你的技能描述
    intent_keywords:
      - 关键词1
      - 关键词2
    skill_id: your_skill_id
    steps:
      - action: input
        target_selector: '#input-id'
        value: '{param}'
      - action: click
        target_selector: '#button-id'
```

## 常用场景示例

### 场景 1：自动登录

```bash
# 学习登录页面
python web_agent.py learn --url "https://example.com/login"

# 执行登录
python web_agent.py run --page_id <page_id> --intent "登录"
```

### 场景 2：数据抓取

```bash
# 学习数据页面
python web_agent.py learn --url "https://example.com/data"

# 导航并抓取
python web_agent.py run --page_id <page_id> --intent "导航"
```

### 场景 3：表单填写

```bash
# 学习表单页面
python web_agent.py learn --url "https://example.com/form"

# 填写表单
python web_agent.py run --page_id <page_id> --intent "提交"
```

## 故障排除指令

```bash
# 检查 Ollama 服务
curl http://127.0.0.1:11434/api/tags

# 检查 Python 版本
python --version

# 检查依赖安装
pip list | grep -E "DrissionPage|openai|pyyaml"

# 测试 API 连接
python -c "from openai import OpenAI; client = OpenAI(base_url='http://127.0.0.1:11434/v1', api_key='ollama'); print(client.chat.completions.create(model='qwen2.5:32b', messages=[{'role':'user','content':'test'}]).choices[0].message.content)"
```

## 性能优化建议

1. **使用较小的模型**（如果内存有限）：
   ```env
   GLM_MODEL=qwen2.5:1.5b
   ```

2. **减少页面元素数量**：
   修改 `EXTRACT_JS` 中的 `slice(0, 50)` 为更小的值

3. **增加超时时间**：
   修改代码中的 `timeout` 参数

## 项目文件结构

```
web-ai-agent/
├── .env                  # 配置文件
├── web_agent.py          # 主程序
├── requirements.txt      # 依赖
├── skills/               # 技能库
│   └── {page_id}/       # 页面ID
│       ├── elements.json # 元素数据
│       └── skills.yaml   # 技能定义
├── README.md             # 详细手册
└── OPENCODE_GUIDE.md     # 本指南
```

## 下一步

- 阅读详细使用手册：`README.md`
- 查看技能文件格式：`skills/{page_id}/skills.yaml`
- 自定义技能：编辑 `skills.yaml` 文件
- 扩展功能：修改 `web_agent.py` 源码

## 技术支持

如遇到问题，请检查：
1. Ollama 服务是否正常运行
2. Python 环境和依赖是否正确安装
3. `.env` 配置是否正确
4. 网络连接是否正常
