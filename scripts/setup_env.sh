#!/bin/bash

# Update and install dependencies
sudo apt-get update
sudo apt-get install -y curl

# Install Python dependencies
pip install chromadb mcp mempalace requests langchain-text-splitters pydantic

# Install Ollama
curl -fsSL https://ollama.com/install.sh | bash

# Start Ollama in the background
ollama serve > ollama.log 2>&1 &
sleep 5 # Wait for Ollama to start

# Pull a 4B class model suitable for tools/coding (Qwen 2.5 Coder 3B)
ollama pull qwen2.5-coder:3b
