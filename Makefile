.PHONY: install upsert upsert-vs rebase rebase-vs app full-start

# === ENVIRONMENT ===
# Installs all required Python packages listed in requirements.txt
install:
	@echo "📦 Installing dependencies..."
	pip install -r requirements.txt


# === VECTOR STORE ===
# Adds or updates embedded game rule documents in Chroma vectorstore from data/ folder
upsert-vs: 
	@echo "📚 Creating/updating vectorstore..."
	python3 -m index.main
upsert: upsert-vs

# Deletes the existing Chroma vectorstore and recreates it from scratch
rebase-vs:
	@echo "🧹📚 Creating/updating vectorstore..."
	python3 -m index.main --rebase 
rebase: rebase-vs


# === APP ===
# Launches the RAG-based Board Games Chatbot on localhost:8505
app:
	@echo "🚀 Starting RAG-based Board Games Chatbot application... (on http://localhost:8505)"
	streamlit run app.py --server.port 8505 --server.headless true


# === FULL START PIPELINE ===
# Installs dependencies, creates/updates the vectorstore, and runs the chatbot app
full-start: 
	@echo "📦 Installing dependencies..."
	pip install -r requirements.txt
	@echo "📚 Creating/updating vectorstore..."
	python3 -m index.main
	@echo "🚀 Starting RAG-based Board Games Chatbot application... (on http://localhost:8505)"
	streamlit run app.py --server.port 8505 --server.headless true
