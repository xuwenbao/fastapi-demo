# Fastapi Demo

> 注意：本项目中的Dockerfile与Docker compose还未测试完成

这是Fastapi Demo项目，包含使用Fastapi与Sqlmodel库实现web程序的样例。

## 环境准备

### 步骤1，安装poetry（Python依赖管理工具）

> 将poetry安装在系统默认Python环境中，推荐使用Python3.10版本, 本样例使用的Python 3.10.14。
> 更多高级用法请参照poetry官方文档: https://python-poetry.org/docs/

```shell
pip install poetry
```

### 步骤2，安装Python虚拟环境

以下命令会在项目根目录下创建一个`.venv`文件夹，其中是Python虚拟环境，同时安装已定义的Python依赖库。
其他使用虚拟环境的方式，如使用已有Python环境，请参照poetry官方文档。

```shell
poetry install
```

### 步骤3，添加新的依赖库（可选）

需要安装新的依赖库时，执行以下命令：

```shell
poetry add <package name>
```

### 步骤4，查看已安装的Python依赖库

使用以下命令查看已安装的Python依赖库

```shell
poetry show --tree

fastapi 0.115.5 FastAPI framework, high performance, easy to learn, fast to code, ready for production
├── pydantic >=1.7.4,<1.8 || >1.8,<1.8.1 || >1.8.1,<2.0.0 || >2.0.0,<2.0.1 || >2.0.1,<2.1.0 || >2.1.0,<3.0.0
│   ├── annotated-types >=0.6.0
│   ├── pydantic-core 2.23.4
│   │   └── typing-extensions >=4.6.0,<4.7.0 || >4.7.0
│   ├── typing-extensions >=4.12.2 (circular dependency aborted here)
│   └── typing-extensions >=4.6.1 (circular dependency aborted here)
├── starlette >=0.40.0,<0.42.0
│   └── anyio >=3.4.0,<5
│       ├── exceptiongroup >=1.0.2
│       ├── idna >=2.8
│       ├── sniffio >=1.1
│       └── typing-extensions >=4.1
└── typing-extensions >=4.8.0
sqlmodel 0.0.22 SQLModel, SQL databases in Python, designed for simplicity, compatibility, and robustness.
├── pydantic >=1.10.13,<3.0.0
│   ├── annotated-types >=0.6.0
│   ├── pydantic-core 2.23.4
│   │   └── typing-extensions >=4.6.0,<4.7.0 || >4.7.0
│   ├── typing-extensions >=4.12.2 (circular dependency aborted here)
│   └── typing-extensions >=4.6.1 (circular dependency aborted here)
└── sqlalchemy >=2.0.14,<2.1.0
    ├── greenlet !=0.4.17
    └── typing-extensions >=4.6.0

... 省略后续内容
```

## 项目结构说明

```
.
├── Dockerfile                # Docker构建文件
├── README.md                 # 项目说明文档
├── docker-compose.yml        # Docker Compose编排配置文件
├── fastapi_demo/             # 主程序包目录
│   ├── api/                  # API接口目录
│   │   ├── __init__.py
│   │   ├── router.py         # API路由配置
│   │   └── v1/               # V1版本API接口
│   │       ├── __init__.py
│   │       └── diocese.py    # 教区相关API实现
│   ├── main.py               # 应用程序入口
│   ├── models/               # 数据模型目录
│   │   └── diocese.py        # 教区数据模型定义
│   └── services/             # 业务服务层目录
│       ├── __init__.py
│       ├── base.py           # 基础服务类
│       ├── config.py         # 配置管理
│       ├── db.py             # 数据库连接管理
│       └── diocese.py        # 教区业务逻辑实现
├── poetry.lock               # Poetry依赖版本锁定文件
├── poetry.toml               # Poetry配置文件
├── pyproject.toml            # 项目依赖配置文件
└── tests/                    # 测试用例目录
```

该项目采用典型的三层架构:
- API层 (`api/`): 处理HTTP请求和响应
- 服务层 (`services/`): 实现核心业务逻辑
- 数据层 (`models/`): 定义数据模型和数据库交互

## 本地运行

> 在本地运行前，建议先通过docker compose启动mysql服务器

首先，在项目根目录下执行如下命令进入Python虚拟环境：

```shell
poetry shell
```

然后, 在项目根目录下执行如下命令启动开发服务器：

```shell
python fastapi_demo/main.py

2024-11-13 21:31:27.724 | INFO     | fastapi_demo.services.db:create_db_and_tables:12 - creating tables ...
2024-11-13 21:31:27.725 | DEBUG    | fastapi_demo.services.config:load:45 - 未发现配置文件在：`/Users/xuwenbao/.config.yml`
2024-11-13 21:31:27.725 | DEBUG    | fastapi_demo.services.config:load:45 - 未发现配置文件在：`/Users/xuwenbao/Dropbox/projects/demos/fastapi-demo/fastapi_demo/config.yml`
2024-11-13 21:31:27.725 | DEBUG    | fastapi_demo.services.config:load:45 - 未发现配置文件在：`/Users/xuwenbao/Dropbox/projects/demos/fastapi-demo/fastapi_demo/config/config.yml`
2024-11-13 21:31:27.726 | INFO     | fastapi_demo.services.config:get_settings:64 - ============================================================
2024-11-13 21:31:27.726 | INFO     | fastapi_demo.services.config:get_settings:65 - settings:
2024-11-13 21:31:27.726 | INFO     | fastapi_demo.services.config:get_settings:66 - testing: False
2024-11-13 21:31:27.727 | INFO     | fastapi_demo.services.config:get_settings:68 - mysql host: 127.0.0.1
2024-11-13 21:31:27.727 | INFO     | fastapi_demo.services.config:get_settings:69 - mysql port: 3306
2024-11-13 21:31:27.727 | INFO     | fastapi_demo.services.config:get_settings:70 - mysql database: demo
2024-11-13 21:31:27.727 | INFO     | fastapi_demo.services.config:get_settings:71 - mysql user: root
2024-11-13 21:31:27.727 | INFO     | fastapi_demo.services.config:get_settings:72 - mysql password: 1234
2024-11-13 21:31:27.727 | INFO     | fastapi_demo.services.config:get_settings:73 - ============================================================
INFO:     Started server process [73874]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:7860 (Press CTRL+C to quit)  <-- 看到此内容代表启动成功
```

访问`http://127.0.0.1:7860/docs`可查看swagger接口文档.

## 接口示例

以下使用一套管理教学区域的Restful接口为例。

- API层 (`api/v1/diocese.py`): 处理HTTP请求和响应
- 服务层 (`services/diocese.py`): 实现核心业务逻辑
- 数据层 (`models/diocese.py`): 定义数据模型和数据库交互

### 创建教区

```shell
curl -X 'POST' \
  'http://localhost:7860/api/v1/dioceses/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "test"
}'
```

### 查询教区

```shell
curl -X 'GET' \
  'http://localhost:7860/api/v1/diocese/1' \
  -H 'accept: application/json'
```

### 查询教区列表

```shell
curl -X 'GET' \
  'http://localhost:7860/api/v1/dioceses' \
  -H 'accept: application/json'
```

### 删除教区

```shell
curl -X 'DELETE' \
  'http://localhost:7860/api/v1/dioceses/1' \
  -H 'accept: application/json'
```
