# POC: Hierarchical MCP Agent System Initialization

This repository serves as a proof-of-concept (POC) for a multi-agent orchestration system using the **Model Context Protocol (MCP)**.

The system acts as a hierarchical router:
1. **Ollama Intent Classification**: Uses a small local LLM (`qwen2.5-coder:3b`) to classify user prompts (e.g. Testing, Architecture, Coding).
2. **Vector Retrieval**: Automatically pulls the correct specialist profile markdown documentation based on the intent.
3. **MemPalace Memory Unit**:
    - **Short-term Memory**: Uses `MemPalace` to record and retrieve the last 5 conversational exchanges from a local ChromaDB instance (`.chroma_data`).
    - **Long-term Procedural Memory**: Records approved tool strategies to a local `procedural_memory.json` file to inform future interactions.
4. **GitHub Copilot Integration**: By registering this tool via `.vscode/settings.json`, GitHub Copilot automatically routes complex tasks through this "Brain" via the MCP.

---

## 🚀 Deployment Guide (Docker)

To run the full stack (Ollama + MCP Server Router) locally using Docker, use the provided Docker Compose configuration.

### Prerequisites
* Docker and Docker Compose installed on your system.

### Steps to Deploy

1. **Start the containers**
   From the root of the repository, run:
   ```bash
   docker-compose up -d
   ```
   *This will start two services:*
   - `ollama`: The local LLM engine.
   - `mcp_router`: The Python environment containing MemPalace, ChromaDB, and the official MCP SDK.

2. **Wait for the Model to Pull**
   The `mcp_router` container is configured to automatically pull the `qwen2.5-coder:3b` model into the Ollama container. This may take a few minutes depending on your internet connection. You can watch the logs using:
   ```bash
   docker-compose logs -f mcp_router
   ```

3. **Verify the Index (Optional but Recommended)**
   If you want to manually build the Knowledge Base Vector Index in ChromaDB, you can run the indexing script inside the container:
   ```bash
   docker exec -it mcp_router python scripts/build_index.py
   ```

4. **Test the Setup**
   Test if the classifier and memory buffer are working by running the test script:
   ```bash
   docker exec -it mcp_router python test_classifier.py
   ```

### 🛑 Stopping the System
```bash
docker-compose down
```

---

## 💻 Integration with GitHub Copilot

Because MCP operates over `stdio`, you configure your IDE (like VS Code) to spin up the Python server directly on your host machine (or inside a DevContainer if you prefer).

The repository includes a `.vscode/settings.json` that registers the server:
```json
{
  "mcp.servers": {
    "Architecture_Router": {
      "command": "python",
      "args": [
        "${workspaceFolder}/mcp_server/main.py"
      ]
    }
  }
}
```
**Note:** For Copilot to access this locally, you must ensure your local host has the Python dependencies installed (`pip install -r requirements.txt` or manually installing `mcp chromadb mempalace requests`). See `DEVELOPER.md` for local testing.
