import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path, override=True)

from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS

# Constants
DATA_DIR = Path(__file__).parent.parent / "data" / "documents"
DB_DIR = Path(__file__).parent.parent / "memory" / "faiss_db"

def ingest_documents():
    """Reads PDFs from data/documents, chunks them, and stores in FAISS."""
    print(f"📂 Looking for PDFs in: {DATA_DIR}")
    
    # Ensure directories exist
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(DB_DIR, exist_ok=True)

    # 1. Load Documents
    loader = PyPDFDirectoryLoader(str(DATA_DIR))
    documents = loader.load()
    
    if not documents:
        print("⚠️ No PDF documents found. Add some PDFs to 'data/documents/' and run again.")
        return False

    print(f"📄 Loaded {len(documents)} document pages.")

    # 2. Split text into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
        add_start_index=True
    )
    chunks = text_splitter.split_documents(documents)
    print(f"✂️ Split documents into {len(chunks)} chunks.")

    # 3. Generate Embeddings using Gemini
    print("🧠 Generating embeddings with Gemini (models/gemini-embedding-001)...")
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

    # 4. Store in FAISS
    print("💾 Storing vectors in FAISS...")
    if os.path.exists(os.path.join(DB_DIR, "index.faiss")):
        # Load existing DB and add new chunks
        print("🔄 Updating existing FAISS index...")
        vector_db = FAISS.load_local(str(DB_DIR), embeddings, allow_dangerous_deserialization=True)
        vector_db.add_documents(chunks)
    else:
        # Create new DB
        print("✨ Creating new FAISS index...")
        vector_db = FAISS.from_documents(chunks, embeddings)
        
    vector_db.save_local(str(DB_DIR))
    print(f"✅ Ingestion complete! FAISS database saved to: {DB_DIR}")
    return True

if __name__ == "__main__":
    ingest_documents()
