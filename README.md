# AI-Driven Autonomous Research Agent (v2)

**An Agentic RAG system designed for deep scientific discovery using Google Gemini 3 Pro.**

## 🚀 Features
* **Persistent Memory:** Resumes research where you left off (no more amnesia).
* **Autonomous Planning:** Creates and executes multi-step research plans.
* **Interactive Mode:** Asks for follow-up questions after completing tasks.
* **Deep Reading:** Reads up to 500 full papers at once using Gemini's long context.

## 📂 Setup
1.  **Install:** `pip install -r requirements.txt`
2.  **Keys:** Open `.env` and add your `GOOGLE_API_KEY`.
3.  **Data:** Put your PDF files in `data/raw_pdfs/`.

## ▶️ Workflow
**Step 1: The Refinery (One-time setup)**
Convert your PDFs into clean Markdown:
`python preprocess.py`

**Step 2: The Agent (Daily driver)**
Start the interactive research loop:
`python main.py`

## 👨‍🔬 Author
**Yang Cheng** - *Postdoctoral Scholar, UCLA Device Research Lab*
cheng991@g.ucla.edu
