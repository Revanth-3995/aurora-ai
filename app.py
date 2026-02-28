import os
import sys
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path, override=True)
from config.settings import GEMINI_API_KEY

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage

def main():
    print("Initializing AURORA Basic Chat...")
    
    if not GEMINI_API_KEY or GEMINI_API_KEY == "your_gemini_api_key_here":
        print("ERROR: Please set your GEMINI_API_KEY in the .env file.")
        sys.exit(1)
        
    try:
        # Initialize Gemini via LangChain
        # Using gemini-2.5-flash based on i.py success
        llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=GEMINI_API_KEY)
    except Exception as e:
        print(f"Failed to initialize LLM: {e}")
        sys.exit(1)
        
    print("AURORA is ready. Type 'exit' or 'quit' to stop.")
    
    # Simple chat loop (no memory yet)
    chat_history = [
        SystemMessage(content="You are AURORA, an Autonomous Unified Reasoning & Orchestration AI. You are helpful and concise.")
    ]
    
    while True:
        try:
            user_input = input("\nYou: ")
            if user_input.lower() in ['exit', 'quit']:
                print("AURORA shutting down...")
                break
                
            if not user_input.strip():
                continue
                
            # Add user input
            chat_history.append(HumanMessage(content=user_input))
            
            # Get response
            print("AURORA is thinking...")
            response = llm.invoke(chat_history)
            
            # Print response and add to history
            print(f"\nAURORA: {response.content}")
            chat_history.append(response)
            
        except KeyboardInterrupt:
            print("\nAURORA shutting down...")
            break
        except Exception as e:
            print(f"Error during chat: {e}")

if __name__ == "__main__":
    main()
