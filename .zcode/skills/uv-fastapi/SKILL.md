---
name: uv-fastapi
description: FastAPI + uv 项目初始化。使用此技能当：用户需要创建 FastAPI 项目、初始化 Python 项目、使用 uv 管理依赖、配置 Python 开发环境、从 pip 迁移到 uv、或询问 uv/FastAPI 相关问题。
---

# uv + FastAPI 项目初始化

快速创建和配置 FastAPI 项目，使用 uv 作为包管理工具（比 pip 快 10-100 倍）。

## 安装 uv

### Windows
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### macOS/Linux
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

验证安装：
```bash
uv --version
```

## 快速启动（原型开发）

```bash
mkdir my-fastapi-app && cd my-fastapi-app
uv init
uv add fastapi uvicorn python-dotenv

cat > main.py << 'EOF'
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}
EOF

uv run uvicorn main:app --reload
```

访问接口文档：`http://127.0.0.1:8000/docs`

## 完整项目结构（生产）

```bash
mkdir my-fastapi-app && cd my-fastapi-app
uv init
uv add fastapi uvicorn python-dotenv
uv add --dev pytest httpx ruff
```

项目结构：
```
my-fastapi-app/
├── pyproject.toml      # 项目配置和依赖
├── .venv/              # 虚拟环境（自动创建）
├── .env                # 环境变量
└── app/
    ├── __init__.py
    ├── main.py         # 应用入口
    ├── config.py       # 配置管理
    ├── routers/        # 路由模块
    └── models/         # 数据模型
```

## 常用命令

### 依赖管理
```bash
uv sync              # 安装所有依赖
uv add fastapi       # 添加生产依赖
uv add --dev pytest  # 添加开发依赖
uv remove fastapi    # 删除依赖
uv sync --upgrade    # 更新依赖
```

### 运行命令
```bash
uv run python main.py
uv run uvicorn main:app --reload
uv run pytest
uv run ruff check .
uv run ruff format .
```

### 虚拟环境
```bash
uv venv                           # 创建虚拟环境
.venv\Scripts\activate           # Windows 激活
source .venv/bin/activate        # Linux/Mac 激活
deactivate                       # 退出
```

## 配置镜像源（中国用户）

在 `pyproject.toml` 末尾添加：

```toml
[[tool.uv.index]]
url = "https://pypi.tuna.tsinghua.edu.cn/simple"
default = true
```

或阿里云：
```toml
[[tool.uv.index]]
url = "https://mirrors.aliyun.com/pypi/simple"
default = true
```

## pyproject.toml 示例

```toml
[project]
name = "my-fastapi-app"
version = "0.1.0"
requires-python = ">=3.10"
dependencies = [
    "fastapi>=0.115.0",
    "uvicorn[standard]>=0.32.0",
    "pydantic>=2.9.0",
    "python-dotenv>=1.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.3.0",
    "httpx>=0.27.0",
    "ruff>=0.7.0",
]

[tool.ruff]
line-length = 100
target-version = "py310"
```

## app/main.py 示例

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="My API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
```

## 从 pip 迁移到 uv

```bash
uv init
uv add -r requirements.txt
rm requirements.txt
```

## 指定 Python 版本

```bash
uv init --python 3.11
# 或在 pyproject.toml 中修改
requires-python = ">=3.11"
```

## Docker 部署

```dockerfile
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app
COPY pyproject.toml ./
RUN uv sync --no-dev
COPY app/ ./app/

EXPOSE 8000
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 参考链接

- [uv 官方文档](https://docs.astral.sh/uv/)
- [FastAPI 官方文档](https://fastapi.tiangolo.com/)
- [PyPI 清华镜像](https://mirrors.tuna.tsinghua.edu.cn/help/pypi/)