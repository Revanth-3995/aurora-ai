import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path, override=True)

from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

DB_DIR = Path(__file__).parent.parent / "memory" / "faiss_db"

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def get_rag_chain():
    """Initializes the FAISS DB and returns an LCEL RAG chain to answer queries based on PDF context."""
    
    if not os.path.exists(os.path.join(DB_DIR, "index.faiss")):
        print("⚠️ FAISS database not found. Please run 'python rag/ingest.py' first.")
        return None

    # Load Embeddings and DB
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    try:
        vector_db = FAISS.load_local(str(DB_DIR), embeddings, allow_dangerous_deserialization=True)
    except Exception as e:
        print(f"❌ Error loading FAISS DB: {e}")
        return None

    # We retrieve the top 3 most relevant chunks
    retriever = vector_db.as_retriever(search_kwargs={"k": 3})

    # Initialize Gemini
    api_key = os.getenv("GEMINI_API_KEY")
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=api_key)

    # Prepare prompt
    template = """You are AURORA, a helpful assistant. Use the following pieces of retrieved context to answer the question. 
If you don't know the answer based on the context, just say that you don't know. Keep the answer concise and relevant.

Context: {context}

Question: {question}

Answer:"""
    
    prompt = ChatPromptTemplate.from_template(template)

    # Create full LCEL RAG chain
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return rag_chain

def query_documents(query: str):
    """Utility function to test the RAG chain standalone."""
    rag_chain = get_rag_chain()
    if not rag_chain:
        return "Error: RAG System not initialized."
    
    response = rag_chain.invoke(query)
    return response

if __name__ == "__main__":
    # Test execution
    test_query = "Summarize the key points of the loaded documents."
    print(f"Query: {test_query}")
    print("-" * 30)
    answer = query_documents(test_query)
    print(answer)
