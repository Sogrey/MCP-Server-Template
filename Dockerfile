# 构建阶段
FROM python:3.11-slim as builder

WORKDIR /app
COPY pyproject.toml .

RUN pip install --no-cache-dir ".[cli]"

# 运行阶段
FROM python:3.11-slim

WORKDIR /app
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY . .

ENV PATH="/usr/local/bin:${PATH}"

# 确保脚本可执行
RUN chmod +x main.py

# 添加用户
RUN useradd -m mcpuser && \
    chown -R mcpuser:mcpuser /app
USER mcpuser

ENV PATH=/root/.local/bin:$PATH \
    PYTHONUNBUFFERED=1 \
    PORT=8000

EXPOSE $PORT

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:$PORT/sse || exit 1

CMD ["python", "main.py", "--transport", "sse", "--port", "$PORT"]