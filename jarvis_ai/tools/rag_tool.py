from langchain_core.tools import tool
from rag.retriever import get_rag_chain

@tool
def query_knowledge_base(query: str) -> str:
    """Useful to search for information inside the user's uploaded documents/PDFs/notes."""
    rag_chain = get_rag_chain()
    if not rag_chain:
        return "Error: RAG System not initialized. Cannot search documents. Please upload documents and run ingestion first."
    try:
        response = rag_chain.invoke(query)
        return response
    except Exception as e:
        return f"Error retrieving from knowledge base: {e}"
