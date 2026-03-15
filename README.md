# 🚀 AURORA-AI
### Autonomous Unified Reasoning & Orchestration AI

---

## 🧠 Overview

AURORA-AI is a multi-agent AI assistant designed to perform reasoning, planning, and task execution using Large Language Models (LLMs).

It integrates Google Calendar scheduling, web research, Python code execution, Retrieval-Augmented Generation (RAG), and memory systems to assist users with academic tasks, coding, research, and scheduling.

This project demonstrates a complete Agentic AI system using **Google Gemini's native tool-calling** for real-time tool execution, and **LangChain** for the RAG pipeline.

---

## 🆕 What's New (v2)

- ✅ Live **Google Calendar** integration via OAuth 2.0 — schedules real events directly
- ✅ **Tavily** web research tool — real-time information retrieval
- ✅ **Python code execution** tool — sandboxed execution with stdout/stderr
- ✅ Native `google-generativeai` SDK for tool-calling (no LangChain dependency for agents)
- ✅ Custom backend tool registry with feature flags via `.env`
- ✅ Automatic function calling via Gemini's built-in tool-use loop
- ✅ Rate-limit retry logic with exponential backoff

---

## ✨ Key Features

### 🤖 Agentic AI (Gemini Native Tool Use)
- Reason → Act (call tool) → Observe (tool result) → Respond
- Automatic function calling — no manual tool dispatch loop needed
- Tools declared as OpenAPI-style JSON schemas

### 📅 Google Calendar Integration
- Schedule events directly into Google Calendar
- Check availability within a time range
- OAuth 2.0 — one-time browser login, token cached for future runs
- Supports IST and any IANA timezone

### 🌐 Web Research (Tavily)
- Real-time web search and summarization
- Returns concise answers with source citations
- Optional long-term memory persistence

### 💻 Code Execution
- Execute Python snippets in a sandboxed environment
- Returns stdout, stderr, and success/failure status
- Configurable timeout and retry settings

### 📚 Retrieval-Augmented Generation (RAG)
- Query PDFs and personal notes via LangChain RetrievalQA
- Document ingestion pipeline (`rag/ingest.py`)
- Retriever for semantic search (`rag/retriever.py`)

### 🧠 Memory System
- Short-term: in-session conversation history
- Long-term: vector storage (FAISS / Chroma)

### 🎤 Voice Interaction *(Upcoming)*
- Speech-to-text and text-to-speech

---

## 🏗️ System Architecture

```
User (Text Input)
        ↓
app.py  →  genai.GenerativeModel (gemini-2.5-flash)
        ↓
Gemini Automatic Function Calling Loop
        ↓
tools_agent.py  →  get_gemini_tools()
        ↓
backend/tools/__init__.py  →  get_tool_registry()
   ├── calendar_google    (Google Calendar API)
   ├── code_advanced      (Python sandbox)
   └── research_advanced  (Tavily web search)
        ↓
LangChain RAG Layer (separate pipeline)
   ├── rag/ingest.py      (Document ingestion)
   └── rag/retriever.py   (Semantic search)
        ↓
Memory Layer
   ├── Short-term (chat history)
   └── Long-term  (FAISS / Chroma vector DB)
        ↓
Response to User
```

---

## 🛠️ Tech Stack

| Category       | Technology                                          |
|----------------|-----------------------------------------------------|
| Language       | Python 3.13                                         |
| LLM            | Google Gemini 2.5 Flash (`google-generativeai`)     |
| Agent Framework| Native Gemini tool-calling (no LangChain for agents)|
| RAG Framework  | LangChain RetrievalQA                               |
| Calendar       | Google Calendar API v3 + OAuth 2.0                  |
| Search         | Tavily API                                          |
| Vector DB      | FAISS / Chroma                                      |
| Code Execution | Sandboxed Python subprocess                         |
| Auth           | google-auth-oauthlib, google-auth-httplib2          |
| UI             | CLI (Streamlit — upcoming)                          |

---

## 📂 Project Structure

```
agentic_ai_project/
├── backend/
│   ├── config.py                   # Central settings (loads .env, feature flags)
│   ├── __init__.py
│   ├── memory/
│   │   └── hooks.py
│   └── tools/
│       ├── __init__.py             # Tool registry (get_tool_registry)
│       ├── types.py
│       ├── calendar/
│       │   ├── google_calendar_client.py
│       │   └── tool_calendar_google.py
│       ├── code/
│       │   └── tool_code_advanced.py
│       └── research/
│           └── tool_research_advanced.py
│
├── jarvis_ai/
│   ├── app.py                      # Main entry point
│   ├── tools_agent.py              # Gemini tool declarations + registry bridge
│   ├── credentials.json            # Google OAuth client secrets (not committed)
│   ├── token.json                  # Cached OAuth token (auto-generated)
│   ├── .env                        # API keys & feature flags (not committed)
│   ├── config/
│   │   └── settings.py
│   ├── agents/
│   ├── rag/
│   │   ├── ingest.py
│   │   └── retriever.py
│   ├── memory/
│   │   └── faiss_db/
│   ├── tools/
│   │   ├── calendar_tool.py
│   │   ├── code_tool.py
│   │   ├── file_tool.py
│   │   ├── rag_tool.py
│   │   └── search_tool.py
│   └── requirements.txt
│
└── tests/
    └── test_tools_basic.py
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/Revanth-3995/aurora-ai.git
cd aurora-ai
```

### 2. Create Virtual Environment

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Linux / Mac
```

### 3. Install Dependencies

```bash
pip install -r jarvis_ai/requirements.txt
```

### 4. Configure `.env`

Create `jarvis_ai/.env` with the following:

```env
GEMINI_API_KEY=your_gemini_api_key
TAVILY_API_KEY=your_tavily_api_key

# Feature flags
ENABLE_GOOGLE_CALENDAR=true
ENABLE_ADVANCED_CODE_TOOL=true
ENABLE_ADVANCED_RESEARCH_TOOL=true

# Google OAuth paths (files live in jarvis_ai/)
GOOGLE_CREDENTIALS_FILE=credentials.json
GOOGLE_TOKEN_FILE=token.json
```

### 5. Set Up Google Calendar OAuth

1. Go to [console.cloud.google.com](https://console.cloud.google.com) → Enable **Google Calendar API**
2. Create **OAuth 2.0 Client ID** (Desktop App) → download JSON
3. Save as `jarvis_ai/credentials.json`
4. Go to **OAuth consent screen → Test Users** → add your Gmail
5. First run opens a browser for authorization — `token.json` is saved automatically after login

### 6. Run AURORA

```bash
cd "C:\Users\<you>\agentic_ai_project"
.venv\Scripts\activate
python jarvis_ai\app.py
```

---

## 🧪 Phase Status

| Phase   | Description                              | Status           |
|---------|------------------------------------------|------------------|
| Phase 1 | Setup & LLM Connectivity                 | ✅ Completed      |
| Phase 2 | RAG Implementation (LangChain)           | ✅ Completed      |
| Phase 3 | Tool Integration (Calendar, Code, Research) | ✅ Completed   |
| Phase 4 | Multi-Agent System                       | 🔄 In Progress   |
| Phase 5 | Voice & Scheduling                       | ⏳ Pending        |
| Phase 6 | Streamlit UI Development                 | ⏳ Pending        |

---

## 🔍 Example Usage

### General Chat
```
You: My name is Revanth
AURORA: Nice to meet you, Revanth!

You: What is my name?
AURORA: Your name is Revanth.
```

### Google Calendar
```
You: Schedule a meeting called trial_meet on March 16 2026, 1pm to 2pm IST
AURORA: The event 'trial_meet' has been scheduled for March 16, 2026,
        from 1 PM to 2 PM IST.
```

### Web Research
```
You: Research the latest developments in agentic AI
AURORA: [calls research_advanced tool → returns summarized findings + sources]
```

### Code Execution
```
You: Write and run Python code to compute the first 10 Fibonacci numbers
AURORA: [calls code_advanced tool → returns stdout with results]
```

### RAG (Document Query)
```
You: Summarize the uploaded research paper on transformers
AURORA: [retrieves relevant chunks via LangChain RAG → generates summary]
```

---

## 🚀 Future Scope

- Full autonomous multi-agent task planning and execution
- Streamlit web UI
- Voice interaction (speech-to-text + text-to-speech)
- Real-time calendar notifications and reminders
- Multi-user support with per-user memory isolation
- Migration to `google-genai` (new Google SDK)

---

## 📌 Highlights

- Modular, scalable architecture with clean separation of concerns
- Native Gemini tool-calling for agents + LangChain for RAG (best of both)
- Feature-flag driven tool loading via `.env`
- Production-style monorepo project structure
- Real Google Calendar integration with OAuth 2.0
- Agentic AI with automatic function calling (Reason → Act → Observe → Respond)

---

## ⭐ Contribute / Feedback

Feel free to fork the project or suggest improvements!