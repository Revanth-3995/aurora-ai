# 🚀 AURORA-AI

**Autonomous Unified Reasoning & Orchestration AI**

---

## 🧠 Overview

AURORA-AI is a **multi-agent AI assistant** designed to perform **reasoning, planning, and task execution** using Large Language Models (LLMs).

It integrates **voice interaction, Retrieval-Augmented Generation (RAG), memory systems, and tool-based automation** to assist users with academic tasks, coding, research, and scheduling.

This project demonstrates a complete **Agentic AI system** using LangChain.

---

## ✨ Key Features

* 🤖 **Multi-Agent Architecture**

  * Intent detection
  * Task planning
  * Tool execution

* 🧠 **Agentic AI (ReAct Pattern)**

  * Reason → Act → Observe → Respond

* 📚 **Retrieval-Augmented Generation (RAG)** *(Upcoming)*

  * Query PDFs and personal notes

* 🧠 **Memory System**

  * Short-term conversation memory
  * Long-term vector storage *(Chroma / FAISS)*

* 🌐 **Web Research Tool** *(Upcoming)*

  * Real-time information retrieval

* 💻 **Coding Assistant** *(Upcoming)*

  * Code generation, explanation, debugging

* 📅 **Scheduling System** *(Upcoming)*

  * Study plans and task management

* 🎤 **Voice Interaction** *(Upcoming)*

  * Speech-to-text and text-to-speech

---

## 🏗️ System Architecture

```
User (Voice/Text)
        ↓
LLM (Gemini)
        ↓
LangChain Agent System
        ↓
ReAct Loop (Reason → Act → Observe)
        ↓
Tools Layer
   ├── RAG Tool
   ├── Code Tool
   ├── Search Tool
   ├── Calendar Tool
        ↓
Memory Layer
   ├── Short-term (Conversation)
   ├── Long-term (Vector DB)
        ↓
Response
```

---

## 🛠️ Tech Stack

* **Language:** Python
* **Framework:** LangChain
* **LLM:** Google Gemini API
* **Search API:** Tavily
* **Vector Database:** FAISS / Chroma
* **RAG:** LangChain RetrievalQA
* **Voice:** SpeechRecognition, pyttsx3
* **UI:** Streamlit *(Upcoming)*

---

## 📂 Project Structure

```
aurora-ai/
│
├── agents/          # AI agents (planner, executor, etc.)
├── tools/           # Tools (RAG, search, calendar, etc.)
├── rag/             # RAG pipeline
├── memory/          # Vector database
├── config/          # Settings & environment
├── data/            # Documents & datasets
├── logs/            # Logs & debugging
│
├── app.py           # Main application
├── requirements.txt
├── .env             # API keys (not committed)
└── README.md
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/Revanth-3995/aurora-ai.git
cd aurora-ai
```

---

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate    # Linux / Mac
venv\Scripts\activate       # Windows
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Setup Environment Variables

Create a `.env` file:

```
GEMINI_API_KEY=your_api_key
TAVILY_API_KEY=your_api_key
```

---

### 5. Run the Application

```bash
python app.py
```

---

## 🧪 Phase Status

| Phase   | Description              | Status         |
| ------- | ------------------------ | -------------- |
| Phase 1 | Setup & LLM Connectivity | ✅ Completed    |
| Phase 2 | RAG Implementation       | ✅ Completed    |
| Phase 3 | Tool Integration         | ⏳ Pending      |
| Phase 4 | Multi-Agent System       | ⏳ Pending      |
| Phase 5 | Voice & Scheduling       | ⏳ Pending      |
| Phase 6 | UI Development           | ⏳ Pending      |

---

## 🔍 Example Usage

```
You: My name is Revanth  
AURORA: Nice to meet you, Revanth!

You: What is my name?  
AURORA: Your name is Revanth.
```

---

## 🚀 Future Scope

* Full autonomous task execution
* Google Calendar integration
* Real-time notifications
* Multi-user support

---

## 📌 Highlights

* Modular, scalable architecture
* Agentic AI implementation (ReAct pattern)
* Clean separation of tools and agents
* Production-style project structure


---

## ⭐ Contribute / Feedback

Feel free to fork the project or suggest improvements!

---
