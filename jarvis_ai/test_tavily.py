import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Ensure we can import from the backend
_here = Path(__file__).resolve().parent
_root = _here.parent
for _p in [str(_here), str(_root)]:
    if _p not in sys.path:
        sys.path.insert(0, _p)

load_dotenv(dotenv_path=_here / ".env", override=True)

try:
    from backend.tools.research.tavily_client import search
    from backend.tools.research.postprocessors import normalize_results
except ImportError as e:
    print(f"❌ Failed to import research tools: {e}")
    sys.exit(1)

def test_tavily_search():
    print("🔍 Testing Tavily Web Search Integration...")
    
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key or api_key == "your_tavily_api_key_here":
        print("❌ ERROR: TAVILY_API_KEY is not set in the .env file.")
        sys.exit(1)
        
    query = "What is the latest major breakthrough in Quantum Computing in 2025?"
    print(f"\n📡 Sending Query: '{query}'")
    
    try:
        raw_results = search(query=query, max_results=3)
        print("\n✅ Tavily API responded successfully!")
        
        normalized = normalize_results(query, raw_results)
        
        print("\n📝 Processed Results:")
        print("-" * 50)
        print(f"Summary Answer:\n{normalized.answer or 'No summary provided.'}\n")
        
        print(f"Sources ({len(normalized.snippets)}):")
        for i, snippet in enumerate(normalized.snippets, 1):
            print(f"  {i}. {snippet.title}")
            print(f"     URL: {snippet.url}")
            # Print a short snippet preview
            print(f"     Snippet: {snippet.summary[:150]}...\n")
            
    except Exception as e:
        print(f"\n❌ Error during Tavily search: {e}")

if __name__ == "__main__":
    test_tavily_search()
