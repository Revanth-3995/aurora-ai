import os
import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path('jarvis_ai/.env'), override=True)
import google.generativeai as genai
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

try:
    print(genai.embed_content(
        model='models/embedding-001',
        content='test',
        task_type='retrieval_document'
    ))
except Exception as e:
    print(repr(e))
