# 在 OpenCode 上快速使用 Web AI Agent

## 快速开始指南

### 方式一：直接复制项目文件

如果你已经有项目文件，直接复制到工作目录即可。

### 方式二：使用 OpenCode 指令创建

在 OpenCode 中按顺序执行以下指令：

#### 1. 创建项目结构
```bash
mkdir web-ai-agent
cd web-ai-agent
mkdir skills
```

#### 2. 创建配置文件
创建 `.env` 文件：
```env
GLM_TOKEN=ollama
GLM_BASE_URL=http://127.0.0.1:11434/v1
GLM_MODEL=qwen2.5:32b
SKILL_DIR=./skills
```

#### 3. 创建依赖文件
创建 `requirements.txt`：
```
DrissionPage>=4.1.0
openai>=1.30.0
pyyaml>=6.0
python-dotenv>=1.0.0
```

#### 4. 创建核心程序
创建 `web_agent.py` 文件（需要提供完整代码，见项目源码）

#### 5. 安装依赖
```bash
pip install -r requirements.txt
```

## OpenCode 必备指令

### 基础测试指令
```bash
# 测试 API 连接
python -c "from openai import OpenAI; client = OpenAI(base_url='http://127.0.0.1:11434/v1', api_key='ollama'); print(client.chat.completions.create(model='qwen2.5:32b', messages=[{'role':'user','content':'test'}]).choices[0].message.content)"
```

### 学习网页指令
```bash
# 学习百度首页
python web_agent.py learn --url "https://www.baidu.com/"

# 学习 Google
python web_agent.py learn --url "https://www.google.com/"
```

### 执行技能指令
```bash
# 搜索功能
python web_agent.py run --page_id e81c1f57 --intent "搜索"

# 导航功能
python web_agent.py run --page_id e81c1f57 --intent "导航"
```

## 一键启动命令

### 完整自动化流程
```bash
# 一键学习并执行
python web_agent.py learn --url "https://www.baidu.com/" && python web_agent.py run --page_id e81c1f57 --intent "搜索"
```

### 环境检查
```bash
# 检查所有环境
python --version && pip list | grep -E "DrissionPage|openai" && curl -s http://127.0.0.1:11434/api/tags
```

## OpenCode 使用技巧

### 1. 批量操作
```bash
# 学习多个网站
for site in "https://www.baidu.com/" "https://www.google.com/" "https://github.com/"; do
    python web_agent.py learn --url "$site"
    sleep 2
done
```

### 2. 错误处理
```bash
# 带错误处理的执行
python web_agent.py learn --url "https://www.baidu.com/" || echo "学习失败，请检查配置"
```

### 3. 日志记录
```bash
# 记录执行日志
python web_agent.py learn --url "https://www.baidu.com/" 2>&1 | tee output.log
```

## 常见 OpenCode 操作

### 查看项目结构
```bash
ls -la
ls -la skills/
```

### 查看技能文件
```bash
cat skills/e81c1f57/skills.yaml
```

### 编辑技能文件
```bash
# 使用编辑器修改技能
# 可以手动优化 AI 生成的技能
```

### 清理和重置
```bash
# 清理所有技能
rm -rf skills/*

# 重新开始
python web_agent.py learn --url "https://www.baidu.com/"
```

## OpenCode 完整工作流程

### 步骤 1：准备环境
```bash
# 确认 Ollama 运行
curl http://127.0.0.1:11434/api/tags

# 确认 Python 环境
python --version
```

### 步骤 2：学习网页
```bash
# 学习目标网页
python web_agent.py learn --url "https://www.baidu.com/"
```

### 步骤 3：查看结果
```bash
# 查看生成的技能
cat skills/e81c1f57/skills.yaml
```

### 步骤 4：执行任务
```bash
# 执行自动化任务
python web_agent.py run --page_id e81c1f57 --intent "搜索"
```

### 步骤 5：验证结果
```bash
# 检查执行日志
# 观察浏览器操作
```

## OpenCode 快速命令参考

| 功能 | 命令 |
|------|------|
| 学习网页 | `python web_agent.py learn --url "URL"` |
| 执行技能 | `python web_agent.py run --page_id "ID" --intent "指令"` |
| 查看技能 | `cat skills/{page_id}/skills.yaml` |
| 检查环境 | `python --version && pip list` |
| 清理技能 | `rm -rf skills/*` |

## 故障排除

### 问题：依赖未安装
```bash
# 解决方案
pip install -r requirements.txt
```

### 问题：API 连接失败
```bash
# 检查 Ollama 服务
curl http://127.0.0.1:11434/api/tags

# 重启 Ollama
# 在另一个终端运行：ollama serve
```

### 问题：元素未找到
```bash
# 重新学习网页
python web_agent.py learn --url "https://www.baidu.com/"
```

## 性能优化

### 使用小模型
```bash
# 修改 .env 文件
echo "GLM_MODEL=qwen2.5:1.5b" > .env
```

### 减少学习时间
```bash
# 修改代码中的元素数量限制
# 将 slice(0, 50) 改为更小的值
```

## 扩展功能

### 添加自定义技能
```bash
# 编辑 skills.yaml 文件
# 添加自定义技能定义
```

### 批量处理
```bash
# 创建脚本处理多个网页
# 参考 COMMANDS.md 中的批量脚本
```

## 文档参考

- **详细使用手册**: `README.md`
- **OpenCode 指南**: `OPENCODE_GUIDE.md`
- **命令参考**: `COMMANDS.md`

## 下一步

1. 阅读详细文档了解所有功能
2. 学习不同的网页类型
3. 自定义和优化技能
4. 集成到自动化工作流

## 技术支持

如遇到问题，请：
1. 检查环境配置
2. 查看错误日志
3. 阅读故障排除部分
4. 参考文档和示例

---

**提示**: 在 OpenCode 中使用时，建议先测试简单的网页（如百度首页），然后再尝试复杂的网站。
