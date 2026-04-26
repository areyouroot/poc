import asyncio
from mcp_server.main import handle_call_tool

async def test_classifier():
    result = await handle_call_tool("classify_intent", {"prompt": "Write unit tests for the login function using playwright."})
    print(result[0].text)

if __name__ == "__main__":
    asyncio.run(test_classifier())
