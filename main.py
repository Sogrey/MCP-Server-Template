# server.py
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("mcp-server-template")

# Add an addition tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """
    两数相加工具
    
    Args:
        a (int): 第一个加数
        b (int): 第二个加数
        
    Returns:
        int: 两数之和
        
    Example:
        >>> add(2, 3)
        5
        >>> add(10, -5)
        5
    """
    logger.info(f"调用add工具，参数: a={a}, b={b}")
    result = a + b
    logger.info(f"add工具返回结果: {result}")
    return result

# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """
    获取个性化问候语
    
    Args:
        name (str): 要问候的人名
        
    Returns:
        str: 个性化问候字符串
        
    Example:
        >>> get_greeting("John")
        'Hello, John!'
        >>> get_greeting("Alice")
        'Hello, Alice!'
        
    URL调用示例:
        greeting://John
        greeting://Alice
    """
    logger.info(f"调用get_greeting资源，参数: name={name}")
    result = f"Hello, {name}!"
    logger.info(f"get_greeting返回结果: {result}")
    return result

# Run the server
if __name__ == "__main__":
    import argparse
    import logging
    
    # 配置日志
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)
    
    # 创建参数解析器
    parser = argparse.ArgumentParser(description='MCP服务器启动参数')
    parser.add_argument('--transport', type=str, default='sse',
                       choices=['stdio', 'sse', 'streamable-http'],
                       help='传输协议类型: stdio|sse(默认)|streamable-http')
    parser.add_argument('--port', type=int, default=8000,
                       help='服务端口号 (默认: 8000)')
    
    args = parser.parse_args()
    
    logger.info(f"启动MCP服务器，传输协议: {args.transport}, 端口: {args.port}")
    
    # 检查端口是否被占用
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind(("127.0.0.1", args.port))
        sock.close()
    except OSError as e:
        if e.errno == 10048:  # 端口被占用错误码
            logger.error(f"端口 {args.port} 已被占用，请使用其他端口")
            exit(1)
        raise
    
    # 显示连接信息
    if args.transport == "stdio":
        logger.info("""
stdio模式已启动，等待标准输入...
调用方式：需要通过其他程序通过标准输入输出流调用
        """)
    elif args.transport == "sse":
        logger.info(f"""
SSE模式已启动
访问URL: http://127.0.0.1:{args.port}/sse
测试命令: curl http://127.0.0.1:{args.port}/sse
        """)
    elif args.transport == "streamable-http":
        logger.info(f"""
Streamable-HTTP模式已启动
访问URL: http://127.0.0.1:{args.port}/mcp
测试命令: curl http://127.0.0.1:{args.port}/mcp
        """)
    
    try:
        # 根据MCP库的实际API调整端口配置方式
        if args.transport in ['sse', 'streamable-http']:
            # 对于HTTP类传输，通过环境变量设置端口
            import os
            os.environ['MCP_PORT'] = str(args.port)
        
        mcp.run(transport=args.transport)
        logger.info(f"MCP服务器已启动，端口: {args.port}")
    except Exception as e:
        logger.error(f"启动MCP服务器失败: {str(e)}")
    except KeyboardInterrupt:
        logger.info("MCP服务器已停止")
