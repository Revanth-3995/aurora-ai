import os
import sys
import time
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path, override=True)
from config.settings import GEMINI_API_KEY

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_core.chat_history import InMemoryChatMessageHistory

def main():
    print("Initializing AURORA Basic Chat...")
    
    if not GEMINI_API_KEY or GEMINI_API_KEY == "your_gemini_api_key_here":
        print("❌ ERROR: Please set your GEMINI_API_KEY in the .env file.")
        sys.exit(1)
        
    try:
        # Initialize Gemini via LangChain
        # Using gemini-2.5-flash based on i.py success
        llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=GEMINI_API_KEY)
    except Exception as e:
        print(f"❌ Failed to initialize LLM: {e}")
        sys.exit(1)
        
    print("✅ AURORA is ready. Type 'exit' or 'quit' to stop.")
    
    # 1. Conversation Memory (Short-Term Memory)
    chat_history = InMemoryChatMessageHistory()
    
    # We maintain a system message that acts as the core LLM instruction
    system_msg = SystemMessage(content="You are AURORA, an Autonomous Unified Reasoning & Orchestration AI. You are helpful and concise.")
    
    while True:
        try:
            # 2. Input Validation
            user_input = input("\nYou: ").strip()
            
            # Ignore empty inputs and prompt again
            if not user_input:
                print("AURORA: Please enter a valid message. (Input cannot be empty)")
                continue
                
            if user_input.lower() in ['exit', 'quit']:
                print("AURORA shutting down...")
                break
                
            print("AURORA is thinking...")
            
            # Combine System Message + Chat History + Current Input
            messages = [system_msg] + chat_history.messages
            messages.append(HumanMessage(content=user_input))
            
            # 3. Error Handling & Robustness (Retry Logic)
            max_retries = 3
            retry_delay = 2
            success = False
            
            for attempt in range(max_retries):
                try:
                    # Get response
                    response = llm.invoke(messages)
                    
                    # Print response
                    print(f"\nAURORA: {response.content}")
                    
                    # Save context to short-term memory
                    chat_history.add_user_message(user_input)
                    chat_history.add_ai_message(response.content)
                    success = True
                    break # Success, break out of retry loop
                    
                except Exception as api_error:
                    error_msg = str(api_error).lower()
                    if "429" in error_msg or "quota" in error_msg or "exhausted" in error_msg:
                        print(f"⚠️ Rate limit hit. Retrying in {retry_delay} seconds... (Attempt {attempt+1}/{max_retries})")
                        time.sleep(retry_delay)
                        retry_delay *= 2 # Exponential backoff
                    else:
                        print(f"❌ Unable to connect to LLM. Please check API key or Network. Error: {api_error}")
                        break # Break on non-retryable errors
                        
            if not success and attempt == max_retries - 1:
                 print("❌ Failed after maximum retries. Please check your API limits or network connection.")
            
        except KeyboardInterrupt:
            print("\nAURORA shutting down...")
            break
        except Exception as e:
            print(f"❌ Unexpected Error during chat: {e}")

if __name__ == "__main__":
    main()
