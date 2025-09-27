# Demo1

mcp 的第一个 demo，用于展示如何使用 mcp 进行开发。

功能仅包含一个查询和一个计算两数加法的工具。

## 配置虚拟环境

We recommend using [uv](https://docs.astral.sh/uv/) to manage your Python projects.

Then add MCP to your project dependencies:

```bash
uv add "mcp[cli]"
```

Alternatively, for projects using pip for dependencies:

```bash
pip install "mcp[cli]"
```

## 使用

### 命令行启动方式

``` bash
# 命令行参数说明
```bash
python main.py \
  --transport {stdio|sse|streamable-http} \  # 传输协议，默认为sse
  --port PORT_NUMBER                        # 服务端口号，默认为8000
```

项目支持三种传输协议：

```bash
# 默认启动(stdio)
python main.py --transport stdio

# 使用SSE协议启动
python main.py --transport sse

# 使用streamable-http协议和自定义端口
python main.py --transport streamable-http --port 8080
```

#### 1. stdio (标准输入输出流)
- 适用于本地直接调用
- CherryStudio配置：
  - 类型选择 `标准输入/输出(stdio)`
  - 命令填写 `python`
  - 参数填写 `main.py`

#### 2. sse (服务器发送事件)
- 适用于远程调用
- 默认URL: `http://127.0.0.1:8000/sse`
- CherryStudio配置：
  - 类型选择 `服务器发送事件(sse)`
  - URL填写 `http://127.0.0.1:8000/sse` (IP根据实际情况修改)

#### 3. streamable-http (可流式传输的HTTP)
- 适用于远程调用
- 默认URL: `http://127.0.0.1:8000/mcp`
- CherryStudio配置：
  - 类型选择 `可流式传输的HTTP(streamableHttp)`
  - URL填写 `http://127.0.0.1:8000/mcp` (IP根据实际情况修改)

### JSON配置示例

#### stdio模式配置
```json
{
  "mcpServers": {
    "mcp-server-template": {
      "command": "python",
      "args": ["main.py", "--transport", "stdio"]
    }
  }
}
```

#### sse模式配置
```json
{
  "mcpServers": {
    "mcp-server-template": {
      "type": "sse",
      "url": "http://localhost:8000/sse",
      "port": 8000
    }
  }
}
```

#### streamableHttp模式配置
```json
{
  "mcpServers": {
    "mcp-server-template": {
      "type": "streamableHttp",
      "url": "http://localhost:8000/mcp",
      "port": 8000,
      "headers": {
        "Content-Type": "application/json"
      }
    }
  }
}
```

## Docker 部署

### 最佳实践配置

1. 创建`.env`文件(可选):
```bash
PORT=8000
TRANSPORT=sse
```

### 构建镜像
```bash
docker build -t mcp-server .
```

### 运行容器
```bash
# 基本运行
docker run -d -p 8000:8000 --name mcp-server mcp-server

# 自定义端口和传输协议
docker run -d -p 8080:8080 \
  -e PORT=8080 \
  -e TRANSPORT=streamable-http \
  --name mcp-server mcp-server
```

### 使用docker-compose
```bash
# 开发模式(带日志输出)
docker-compose up

# 生产模式(后台运行)
docker-compose up -d

# 查看日志
docker-compose logs -f
```

### 健康检查
```bash
docker inspect --format='{{json .State.Health}}' mcp-server
```

## 生产环境建议
1. 添加TLS证书
2. 配置资源限制
3. 设置日志轮转
4. 使用容器编排平台(K8s)

## 注意事项
1. 确保已安装所有依赖：`uv add "mcp[cli]"`
2. 项目要求Python版本 >= 3.10
3. 启动前请确认端口8000未被占用(对于sse和streamable-http模式)
4. JSON配置中的URL和端口可根据实际情况修改