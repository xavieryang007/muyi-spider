# News Server

基于Python的新闻采集系统

## 功能特性

- 浏览器自动化采集（使用Playwright）- 分布式任务处理（Celery）
- 网页内容解析工具
- 基于LLM的内容解析引擎（LangChain集成）
- 支持多种大模型接口：  - OpenAI兼容API
  - Ollama本地模型
  - 最低支持7B参数模型（如DeepSeek-r1:7b）
- 网页自动化防检测机制（集成playwright-stealth）
- 可视化任务管理界面（Streamlit）

## 环境要求

- Python 3.9+
- Playwright浏览器
- 支持CUDA的GPU（可选，用于加速LLM推理）
- 内存建议：至少8GB（使用本地LLM时建议16GB+）

## 快速开始
 
1. 安装依赖：
```bash
pip install -r requirements-3.in
playwright install
```

2. 创建.env配置文件：
   
   在项目根目录新建.env文件，内容如下：
```ini
# 大语言模型配置
MODEL_TYPE=ollama
MODEL=deepseek-r1:8b
OPENAI_API_KEY=
BASE_URL=http://localhost:11434  # Ollama默认地址

# 分布式任务队列
REDIS_URL=redis://127.0.0.1:6379/0
```

3. 启动主服务：
```bash
./start.bat
```

4. 启动爬虫工作进程：
```bash
./start_worker.bat
```

5. 启动Web管理界面：
```bash
streamlit run webui.py
```

## 项目结构

```
├── app/
│   ├── api/            # API接口模块
│   ├── core/           # 核心功能
│   ├── utils/          # 工具函数
│   └── router/         # 路由配置
├── tests/              # 单元测试
├── main.py             # 主入口
├── worker.py           # Celery worker
└── webui.py            # Web管理界面
```

## 依赖管理

使用requirements-3.in管理依赖，生成虚拟环境：
```bash
python -m venv .venv
```

## 文档

详细文档见docs目录（待完成）

## 许可协议

本项目采用 MIT 许可证 - 详情请见 LICENSE 文件

## 贡献指南

欢迎提交Pull Request。请确保：
1. 遵守PEP8编码规范
2. 添加对应的单元测试
3. 更新相关文档
