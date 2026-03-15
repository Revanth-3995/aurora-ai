import os
from pathlib import Path
from langchain_core.tools import tool

DATA_DIR = Path(__file__).parent.parent / "data"

@tool
def list_available_files() -> str:
    """List all files in the user's data directory."""
    try:
        if not os.path.exists(DATA_DIR):
            return "Data directory does not exist or is empty."
        
        files = []
        for root, dirs, filenames in os.walk(DATA_DIR):
            for filename in filenames:
                full_path = Path(root) / filename
                rel_path = full_path.relative_to(DATA_DIR.parent)
                files.append(str(rel_path))
                
        if not files:
            return "No files found."
        return "\n".join(files)
    except Exception as e:
        return f"Error listing files: {e}"

@tool
def read_file_content(relative_path: str) -> str:
    """Read the text content of a file given its relative path (e.g., 'data/documents/info.txt')."""
    file_path = Path(__file__).parent.parent / relative_path
    
    if not os.path.exists(file_path):
        return f"Error: File '{relative_path}' not found."
        
    try:
        if file_path.suffix.lower() == '.pdf':
            from pypdf import PdfReader
            reader = PdfReader(str(file_path))
            text = "".join(page.extract_text() for page in reader.pages)
            return text
        else:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
    except Exception as e:
        return f"Error reading file: {e}"
