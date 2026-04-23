import json
import logging
from mempalace.miner import add_drawer
from mempalace.searcher import search_memories
from mempalace.palace import get_collection

logger = logging.getLogger("memory_manager")

class MemoryManager:
    def __init__(self, db_path="./.chroma_data"):
        self.db_path = db_path
        self.collection = get_collection(db_path, create=True)
        self.procedural_memory_path = "mcp_server/procedural_memory.json"

        # Initialize procedural memory file if it doesn't exist
        try:
            with open(self.procedural_memory_path, "r") as f:
                pass
        except FileNotFoundError:
            with open(self.procedural_memory_path, "w") as f:
                json.dump({"patterns": []}, f)

    def add_exchange(self, user_msg: str, agent_msg: str, chunk_index: int):
        """Add short term exchange to MemPalace buffer"""
        content = f"User: {user_msg}\nAgent: {agent_msg}"
        try:
            add_drawer(self.collection, wing="session", room="buffer", content=content, source_file="mcp_session", chunk_index=chunk_index, agent="mcp_router")
            logger.info("Saved exchange to MemPalace.")
        except Exception as e:
            logger.error(f"Failed to add drawer to MemPalace: {e}")

    def get_recent_exchanges(self, n=5):
        """Retrieve recent exchanges from MemPalace session buffer."""
        try:
            results = search_memories(query="User", palace_path=self.db_path, wing="session", room="buffer", n_results=n)

            # search_memories returns a dict with 'results' array
            exchanges = []
            if "results" in results:
                for res in results["results"]:
                    if "text" in res:
                        exchanges.append(res["text"])
            return "\n\n".join(exchanges)
        except Exception as e:
            logger.error(f"Failed to search MemPalace: {e}")
            return ""

    def record_successful_pattern(self, task_type: str, successful_context: str):
        """Append approved code structures or user preferences to long-term JSON memory."""
        try:
            with open(self.procedural_memory_path, "r") as f:
                memory = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            memory = {"patterns": []}

        memory["patterns"].append({
            "task_type": task_type,
            "context": successful_context
        })

        with open(self.procedural_memory_path, "w") as f:
            json.dump(memory, f, indent=4)
        logger.info(f"Recorded procedural memory for {task_type}")

    def get_procedural_memory(self):
        """Load procedural memory to inject into specialist context."""
        try:
            with open(self.procedural_memory_path, "r") as f:
                memory = json.load(f)
                return json.dumps(memory, indent=2)
        except (FileNotFoundError, json.JSONDecodeError):
            return ""

memory_manager = MemoryManager()
