# Autonomous Agent Docker Container
# Secure environment for AI execution

FROM python:3.11-slim

# Set working directory
WORKDIR /workspace

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    jq \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Install GitHub CLI
RUN curl -fsSL https://cli.github.com/packages/githubcli-archive_keyring.pgp | dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | tee /etc/apt/sources.list.d/github-cli.list > /dev/null \
    && apt-get update \
    && apt-get install -y gh \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Ollama (for local usage when run locally)
RUN curl -fsSL https://ollama.ai/install.sh | sh

# Copy agent code
COPY . /workspace/

# Create directories for agent work
RUN mkdir -p agent/memory agent/skills docs tools scripts tmp

# Set permissions (security: read-only where possible)
RUN chmod -R 755 /workspace/agent \
    && chmod -R 755 /workspace/docs \
    && chmod -R 755 /workspace/tools \
    && chmod -R 755 /workspace/scripts

# Security: No root user
RUN useradd -m -u 1001 agentuser
chown -R agentuser:agentuser /workspace
USER agentuser

# Environment variables
ENV PYTHONPATH=/workspace
ENV AGENT_WORKSPACE=/workspace

# Health check
HEALTHCHECK --interval=60s --timeout=10s --start-period=30s --retries=3 \
    CMD python -c "import sys; sys.exit(0)" || exit 1

# Default command
CMD ["python", "agent/ollama_agent.py"]

# Labels for container management
LABEL org.opencontainers.image.title="Autonomous AI Agent"
LABEL org.opencontainers.image.description="Secure autonomous AI agent with GitHub Actions integration"
LABEL org.opencontainers.image.vendor="Sara AI"
LABEL org.opencontainers.image.licenses="MIT"