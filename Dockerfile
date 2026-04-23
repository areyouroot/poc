FROM python:3.12-slim

# Install system dependencies needed for native extensions (ChromaDB, MemPalace, etc.)
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    zstd \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
RUN pip install --no-cache-dir \
    chromadb \
    mcp \
    mempalace \
    requests \
    langchain-text-splitters \
    pydantic

# Copy project files
COPY . /app/

# Environment configurations
ENV OLLAMA_URL="http://ollama:11434/api/generate"
ENV PYTHONUNBUFFERED=1

# MCP servers typically run via stdio rather than an HTTP port,
# but the container will run as a persistent command or be invoked locally.
# Default command for the container to keep it alive or execute a test script
CMD ["tail", "-f", "/dev/null"]
