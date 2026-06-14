from backend.memory.chroma_manager import get_memory_manager

def execute_memory_save(payload: dict) -> str:
    """
    Saves a specific string fact directly into the ChromaDB memory persistence layer.
    """
    fact = payload.get("fact")
    if not fact:
        return "Error: Missing required parameter 'fact'."
        
    manager = get_memory_manager()
    return manager.save_memory(fact)
