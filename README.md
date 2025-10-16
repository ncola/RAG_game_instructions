# 🎲 Game Instructions RAG 🎲
A Retrieval-Augmented Generation (RAG) system preloaded with board game rulebooks in PDF format, capable of answering questions about gameplay rules.  
The bot retrieves relevant rule fragments, passes them as context to an LLM, and returns an answer along with cited sources.

## Tech stack 
- Python 3.10+
- LangChain – RAG pipeline orchestration
- ChromaDB – vector database for rulebook embeddings
- PyMuPDF – PDF parsing 
- OpenAI GPT – language model for generating responses
- Streamlit – lightweight chat UI
- python-dotenv – API key management via `.env`

## Architecture 
**data/** – stores board game rulebooks (PDF)

**index/** – indexing module: loads documents, splits them into chunks, creates embeddings, and saves/updates them in ChromaDB

**rag/** – RAG module: retrieves relevant chunks, builds prompts, calls the LLM, and returns answers with sources

**models/** – bot and model configuration (e.g., retriever parameters, temperature)

**config.py** – project settings and system prompt definitions

**app.py** – Streamlit app providing a simple chat interface

**chroma_db/** – persistent vector database for embeddings

## Makefile commands

To simplify running the project, a small **Makefile** is included. Usage:

```bash
make install   # install dependencies
make app       # run the Streamlit chatbot on http://localhost:8505 and have fun! 
```

## 💬 Example questions
- “How do you score roads in Carcassonne?”  
- “What’s the objective in Dobble?”

## Features
- Loads game rulebooks from PDF files and builds a ChromaDB vector store  
- Retrieves relevant fragments and provides them as context to the LLM  
- Answers **strictly based on context** (no hallucinations)  
- Displays **sources** (file and page) for each answer  
- Streamlit-based **chat UI**  
- Supports **API key** from `.env` or manual entry within the app

## Next steps 
- Text cleaning before chunking and improved metadata  
- Token streaming (live answer generation)  
- Better conversation history management ✅  
- Add Dockerfile for easy deployment

## Sources 
Rulebooks sourced from:
[https://am76.pl/instrukcje](https://am76.pl/instrukcje)




