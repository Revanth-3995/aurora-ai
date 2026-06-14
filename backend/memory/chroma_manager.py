import os
import logging
import hashlib
from pathlib import Path
import chromadb
import google.generativeai as genai

# Append root to path internally for standalone testability
import sys
_here = Path(__file__).resolve().parent
_root = _here.parent.parent # agentic_ai_project
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

from backend.config.settings import GEMINI_API_KEY

logger = logging.getLogger(__name__)

class ChromaMemoryManager:
    """
    Manages long-term semantic persistence for AURORA utilizing ChromaDB 
    and Gemini embedding vectors for precision context retrieval.
    """
    def __init__(self):
        self.db_dir = _here / "chroma_db_v3"
        self.db_dir.mkdir(parents=True, exist_ok=True)
        self.active_embedding_model = None
        
        try:
            self.client = chromadb.PersistentClient(path=str(self.db_dir))
            
            # Auto-discover Google's currently active embedding model
            available_models = [m.name for m in genai.list_models() if 'embedContent' in m.supported_generation_methods]
            if not available_models:
                raise Exception("No Gemini embedding models are available for this API Key/Project!")
            self.active_embedding_model = available_models[0]
            logger.info("ChromaDB Memory Manager bound to embedding model: %s", self.active_embedding_model)
            
            self.collection = self.client.get_or_create_collection(
                name="user_personal_memory",
                metadata={"hnsw:space": "cosine"}
            )
            logger.info("ChromaDB Memory Manager initialized targeting %s", self.db_dir)
        except Exception as e:
            logger.error("Failed to boot ChromaDB Client: %s", e)
            self.client = None

    def _get_embedding(self, text: str) -> list[float]:
        # Fallback safeguard in case initialization bypassed auto-discovery
        model_name = self.active_embedding_model if self.active_embedding_model else "models/text-embedding-004"
        response = genai.embed_content(
            model=model_name,
            content=text
        )
        return response["embedding"]

    def save_memory(self, fact: str) -> str:
        """Saves a standalone factual string firmly into long-term personal memory."""
        if not self.client:
            return "Memory DB offline."
            
        fact_id = hashlib.md5(fact.encode('utf-8')).hexdigest()
        
        try:
            vector = self._get_embedding(fact)
            self.collection.upsert(
                documents=[fact],
                embeddings=[vector],
                ids=[fact_id],
                metadatas=[{"type": "user_preference"}]
            )
            logger.info("Deep-Memory Saved: %s", fact)
            return f"Successfully saved new long-term memory: '{fact}'"
        except Exception as e:
            logger.error("Failed to write fact to Chroma: %s", e)
            return f"Failed to save memory due to error: {str(e)}"

    def retrieve_related_memories(self, query: str, n_results: int = 4) -> list[str]:
        """Runs cosine semantic similarity against recent user queries to pull relevant facts."""
        if not self.client:
            return []
            
        try:
            # Count how many docs actually exist to avoid asking for more n_results than docs in the cluster
            doc_count = self.collection.count()
            if doc_count == 0:
                return []
                
            safe_n_results = min(n_results, doc_count)
            vector = self._get_embedding(query)
            
            results = self.collection.query(
                query_embeddings=[vector],
                n_results=safe_n_results
            )
            
            docs = results.get("documents", [])
            if docs and len(docs) > 0:
                return [str(doc) for doc in docs[0]]
            return []
        except Exception as e:
            logger.error("Retrieval Engine fault: %s", e)
            return []

# Singleton instance to expose directly
_instance = None
def get_memory_manager() -> ChromaMemoryManager:
    global _instance
    if _instance is None:
        _instance = ChromaMemoryManager()
    return _instance
