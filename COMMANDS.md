# OpenCode 执行指令集合

## 基础操作指令

### 1. 项目初始化
```bash
# 创建项目目录
mkdir web-ai-agent
cd web-ai-agent

# 创建 .env 配置文件
echo "GLM_TOKEN=ollama" > .env
echo "GLM_BASE_URL=http://127.0.0.1:11434/v1" >> .env
echo "GLM_MODEL=qwen2.5:32b" >> .env
echo "SKILL_DIR=./skills" >> .env

# 创建 requirements.txt
echo "DrissionPage>=4.1.0" > requirements.txt
echo "openai>=1.30.0" >> requirements.txt
echo "pyyaml>=6.0" >> requirements.txt
echo "python-dotenv>=1.0.0" >> requirements.txt

# 安装依赖
pip install -r requirements.txt
```

### 2. 网页学习指令
```bash
# 学习百度首页
python web_agent.py learn --url "https://www.baidu.com/"

# 学习谷歌首页
python web_agent.py learn --url "https://www.google.com/"

# 学习 GitHub
python web_agent.py learn --url "https://github.com/"

# 学习任意网站
python web_agent.py learn --url "https://your-website.com/"
```

### 3. 技能执行指令
```bash
# 百度搜索
python web_agent.py run --page_id e81c1f57 --intent "搜索"

# 页面导航
python web_agent.py run --page_id e81c1f57 --intent "导航"

# 登录操作
python web_agent.py run --page_id e81c1f57 --intent "登录"

# 查询功能
python web_agent.py run --page_id e81c1f57 --intent "查询"
```

## 高级操作指令

### 4. 批量学习多个网页
```bash
# 学习多个常用网站
python web_agent.py learn --url "https://www.baidu.com/" &
python web_agent.py learn --url "https://www.google.com/" &
python web_agent.py learn --url "https://github.com/" &
wait
```

### 5. 自动化测试流程
```bash
# 完整的自动化测试流程
echo "开始自动化测试..."
python web_agent.py learn --url "https://www.baidu.com/"
echo "学习完成，开始执行..."
python web_agent.py run --page_id e81c1f57 --intent "搜索"
echo "测试完成"
```

### 6. 清理和重置
```bash
# 清理所有技能
rm -rf skills/*

# 重新学习
python web_agent.py learn --url "https://www.baidu.com/"
```

## 环境检查指令

### 7. 系统环境检查
```bash
# 检查 Python 版本
python --version

# 检查依赖安装
pip list | grep -E "DrissionPage|openai|pyyaml|python-dotenv"

# 检查 Ollama 服务
curl http://127.0.0.1:11434/api/tags

# 测试 API 连接
python -c "from openai import OpenAI; client = OpenAI(base_url='http://127.0.0.1:11434/v1', api_key='ollama'); print('API连接正常' if client else 'API连接失败')"
```

### 8. 项目文件检查
```bash
# 查看项目结构
ls -la

# 查看技能目录
ls -la skills/

# 查看特定技能文件
cat skills/e81c1f57/skills.yaml

# 查看元素数据
cat skills/e81c1f57/elements.json | head -20
```

## 调试和故障排除

### 9. 调试模式
```bash
# 启用详细日志（修改代码后）
python web_agent.py learn --url "https://www.baidu.com/" 2>&1 | tee debug.log

# 查看日志
cat debug.log
```

### 10. 性能测试
```bash
# 测试学习速度
time python web_agent.py learn --url "https://www.baidu.com/"

# 测试执行速度
time python web_agent.py run --page_id e81c1f57 --intent "搜索"
```

## 自定义和扩展

### 11. 修改配置
```bash
# 使用不同的模型
echo "GLM_MODEL=qwen2.5:1.5b" > .env

# 使用不同的 API 端点
echo "GLM_BASE_URL=https://your-api-endpoint.com/v1" >> .env

# 使用不同的技能目录
echo "SKILL_DIR=./my_skills" >> .env
```

### 12. 创建自定义技能
```bash
# 编辑技能文件
nano skills/e81c1f57/skills.yaml

# 或使用其他编辑器
vim skills/e81c1f57/skills.yaml
code skills/e81c1f57/skills.yaml
```

## 一键执行脚本

### 13. 完整自动化脚本
```bash
#!/bin/bash

# Web AI Agent 一键启动脚本

echo "=== Web AI Agent 自动化脚本 ==="

# 检查环境
echo "检查环境..."
python --version || { echo "Python 未安装"; exit 1; }
curl -s http://127.0.0.1:11434/api/tags > /dev/null || { echo "Ollama 服务未运行"; exit 1; }

# 学习网页
echo "学习网页..."
python web_agent.py learn --url "https://www.baidu.com/"

# 执行技能
echo "执行技能..."
python web_agent.py run --page_id e81c1f57 --intent "搜索"

echo "=== 执行完成 ==="
```

### 14. 批量测试脚本
```bash
#!/bin/bash

# 批量测试多个网站

sites=(
    "https://www.baidu.com/"
    "https://www.google.com/"
    "https://github.com/"
)

for site in "${sites[@]}"; do
    echo "学习网站: $site"
    python web_agent.py learn --url "$site"
    echo "等待 3 秒..."
    sleep 3
done

echo "批量学习完成"
```

## 维护和更新

### 15. 依赖更新
```bash
# 更新所有依赖
pip install --upgrade -r requirements.txt

# 更新特定包
pip install --upgrade DrissionPage
pip install --upgrade openai
```

### 16. 项目备份
```bash
# 备份技能文件
tar -czf skills_backup_$(date +%Y%m%d).tar.gz skills/

# 备份整个项目
tar -czf web_ai_agent_backup_$(date +%Y%m%d).tar.gz .
```

## 监控和日志

### 17. 日志管理
```bash
# 创建日志目录
mkdir -p logs

# 运行并记录日志
python web_agent.py learn --url "https://www.baidu.com/" 2>&1 | tee logs/learn_$(date +%Y%m%d_%H%M%S).log
python web_agent.py run --page_id e81c1f57 --intent "搜索" 2>&1 | tee logs/run_$(date +%Y%m%d_%H%M%S).log
```

### 18. 实时监控
```bash
# 监控技能目录变化
watch -n 1 'ls -la skills/'

# 监控日志文件
tail -f logs/*.log
```

## 快速参考

### 常用命令速查
```bash
# 学习网页
python web_agent.py learn --url "URL"

# 执行技能
python web_agent.py run --page_id "ID" --intent "指令"

# 查看技能
cat skills/{page_id}/skills.yaml

# 清理技能
rm -rf skills/*

# 检查环境
python --version && pip list
```

### 页面 ID 获取
学习网页后，程序会输出页面 ID，例如：
```
[INFO] 页面元素已提取，ID: e81c1f57
```
使用这个 ID 来执行对应的技能。

## 注意事项

1. 确保 Ollama 服务在运行
2. 首次使用需要下载模型
3. 网络连接影响学习速度
4. 技能文件可以手动编辑优化
5. 建议定期备份技能文件

## 获取帮助

```bash
# 查看帮助信息
python web_agent.py --help

# 查看项目文档
cat README.md
cat OPENCODE_GUIDE.md
```

## 更新日志

- 2026-04-28: 初始版本创建
- 包含所有常用指令和操作
- 支持自动化脚本
