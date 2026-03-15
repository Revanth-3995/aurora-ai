import os
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.tools import tool

@tool
def web_search(query: str) -> str:
    """Useful to search the web for real-time information and current events."""
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key or api_key == "your_tavily_api_key_here":
        return "Error: TAVILY_API_KEY is not set in the .env. Please set it to search the web."
    
    try:
        search = TavilySearchResults(max_results=3)
        results = search.invoke({"query": query})
        return str(results)
    except Exception as e:
        return f"Error performing web search: {e}"
