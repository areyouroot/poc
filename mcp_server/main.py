import json
import logging
import asyncio
from mcp.server import Server, NotificationOptions
from mcp.server.stdio import stdio_server
from mcp.server.models import InitializationOptions
import mcp.types as types
import requests

from mcp_server.memory_manager import memory_manager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mcp_server")

server = Server("Architecture_Router")

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5-coder:3b"

# Global exchange counter
exchange_index = 0

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """List available tools."""
    return [
        types.Tool(
            name="classify_intent",
            description="Route a user prompt to the correct specialist and retrieve augmented context.",
            inputSchema={
                "type": "object",
                "properties": {
                    "prompt": {"type": "string", "description": "The user prompt to classify"}
                },
                "required": ["prompt"],
            },
        )
    ]


@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """Handle tool execution requests."""
    global exchange_index
    if name != "classify_intent":
        raise ValueError(f"Unknown tool: {name}")

    if not arguments or "prompt" not in arguments:
        raise ValueError("Missing prompt argument")

    prompt = arguments["prompt"]

    sys_prompt = '''You are an intent classifier. Categorize the user's prompt into one of the following categories:
- "Testing": tasks related to unit tests, UI testing, writing test code.
- "Architecture": tasks related to system design, routing, high-level planning.
- "Coding": tasks related to writing functional code, implementing features.
Return ONLY valid JSON in the format: {"category": "category_name", "confidence": 0.95}'''

    try:
        response = requests.post(OLLAMA_URL, json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "system": sys_prompt,
            "format": "json",
            "stream": False
        }, timeout=30)

        response.raise_for_status()
        result_json = response.json()
        llm_response = json.loads(result_json["response"])

        category = llm_response.get("category", "Coding")
        confidence = llm_response.get("confidence", 0.0)

        logger.info(f"Classified prompt as {category} with confidence {confidence}")

        # Load profile
        profile_path = f"mcp_server/profiles/{category.lower()}_specialist.md"
        try:
            with open(profile_path, "r", encoding="utf-8") as f:
                profile_content = f.read()
        except FileNotFoundError:
            profile_content = f"You are a specialist for {category}. Follow standard coding practices."

        # Fetch short-term memory
        recent_exchanges = memory_manager.get_recent_exchanges(n=5)

        # Fetch procedural memory
        procedural_memory = memory_manager.get_procedural_memory()

        response_text = (f"Category: {category}\nConfidence: {confidence}\n\n"
                         f"Profile Context:\n{profile_content}\n\n"
                         f"Procedural Memory:\n{procedural_memory}\n\n"
                         f"Recent Conversational Context:\n{recent_exchanges}")

        # Save exchange
        memory_manager.add_exchange(user_msg=prompt, agent_msg=response_text, chunk_index=exchange_index)
        exchange_index += 1

        return [types.TextContent(type="text", text=response_text)]

    except Exception as e:
        logger.error(f"Error during tool execution: {e}")
        return [types.TextContent(type="text", text=f"Error: {e}")]


async def main():
    logger.info("Starting Architecture_Router MCP server over stdio...")
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="Architecture_Router",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())
