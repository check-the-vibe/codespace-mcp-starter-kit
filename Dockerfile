FROM python:3.11-slim

WORKDIR /app

# Install basic OS deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements if present at repo root (template expects it)
COPY ../requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy template code
COPY . /app

ENV PYTHONUNBUFFERED=1
ENV MCP_HTTP_HOST=0.0.0.0
ENV MCP_HTTP_PORT=8000
ENV MCP_HTTP_PATH=/mcp
ENV MCP_SNIPPETS_ROOT=/data

EXPOSE 8000

CMD ["python3", "server_http.py"]
