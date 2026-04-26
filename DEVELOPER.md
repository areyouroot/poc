# Developer Guide

Welcome to the POC for the Hierarchical MCP Agent System. This document outlines how to test, write code, deploy, and debug the MCP server and MemPalace integration.

## 🏗️ Architecture Overview

The codebase is split into three main parts:
1. **Knowledge Base Generation** (`scripts/build_index.py`): Parses markdown documents in `/docs` and stores them via ChromaDB in `.chroma_data`.
2. **Memory Manager** (`mcp_server/memory_manager.py`): Wraps MemPalace for short-term conversation storage (also hitting `.chroma_data`) and manages a long-term procedural memory JSON.
3. **MCP Router Server** (`mcp_server/main.py`): The core server implementing the Model Context Protocol. It exposes the `classify_intent` tool.

---

## 🛠️ Local Development Setup

If you are developing locally (outside of Docker), you need the following:

1. **Install Local Dependencies**
   Run the provided bash script to install Python tools and the local Ollama instance:
   ```bash
   ./scripts/setup_env.sh
   ```

2. **Verify Database Creation**
   Run the index build script to populate the ChromaDB:
   ```bash
   python scripts/build_index.py
   ```

3. **Run the Test Script**
   To test the intent routing without starting the full MCP stdio loop, you can run:
   ```bash
   python test_classifier.py
   ```

## 🐳 Docker Development Setup

To test how the system runs inside containers (e.g. to ensure URL routing to Ollama works):

1. **Start the environment**
   ```bash
   docker-compose up -d --build
   ```

2. **Run commands inside the container**
   ```bash
   docker exec -it mcp_router bash
   # Inside the container:
   python test_classifier.py
   ```

3. **Check Logs for Debugging**
   If the LLM classifier is failing, check if the Ollama container downloaded the model:
   ```bash
   docker-compose logs ollama
   ```
   Or check the initialization script in the router:
   ```bash
   docker-compose logs mcp_router
   ```

---

## 🐛 Debugging Guide

### 1. `classify_intent` Tool Fails or Times Out
**Symptom**: VS Code / Copilot hangs or the MCP server returns an error.
**Fix**: Ensure `OLLAMA_URL` is correct. If running locally, it defaults to `http://localhost:11434`. If using Docker compose, it should be `http://ollama:11434`.

### 2. MemPalace Search Errors
**Symptom**: `Failed to search MemPalace: search_memories() got an unexpected keyword argument...`
**Fix**: MemPalace's programmatic API expects specific parameters. In `mcp_server/memory_manager.py`, we use:
```python
search_memories(query="...", palace_path=self.db_path, wing="session", room="buffer", n_results=5)
```
Check the MemPalace library version installed. This POC was built using MemPalace `3.3.2`.

### 3. Copilot Not Detecting the Server
**Symptom**: You ask Copilot a prompt, but the Orchestrator doesn't fire.
**Fix**:
- Ensure `.vscode/settings.json` has `mcp.servers` properly configured.
- Try reloading the VS Code window (`Cmd+Shift+P` -> `Reload Window`).
- Check the VS Code Output panel, switch to the `GitHub Copilot Chat` or `MCP` logs to see if the Python process failed to start over stdio.
