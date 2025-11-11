FROM mcr.microsoft.com/devcontainers/python:3.11

WORKDIR /app

# Install dependencies for GitHub CLI
RUN apt-get update && apt-get install -y \
    curl \
    ca-certificates \
    gnupg \
    lsb-release \
    git \
    && rm -rf /var/lib/apt/lists/*

# Add the GitHub CLI official GPG key and repository
RUN curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | tee /usr/share/keyrings/githubcli-archive-keyring.gpg > /dev/null \
    && chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | tee /etc/apt/sources.list.d/github-cli.list > /dev/null

# Install GitHub CLI
RUN apt-get update && apt-get install -y gh \
    && rm -rf /var/lib/apt/lists/*

# Verify installation
RUN gh --version

# Copy requirements if present at repo root (template expects it)
COPY requirements.txt /app/requirements.txt
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
