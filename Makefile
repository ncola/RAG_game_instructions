install:
	@echo "📦 Installing dependencies..."
	pip install -r requirements.txt

app:
	@echo "🚀 Starting RAG-based Board Games Chatbot application... (on http://localhost:8505)"
	streamlit run app.py --server.port 8505 --server.headless true
