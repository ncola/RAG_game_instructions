from index.corpus import Corpus
from index.vectostore import VectorStore
from index.vector_db_manager import VectorDBManager

from dotenv import load_dotenv
load_dotenv()
import openai, os
openai.api_key = os.getenv("OPENAI_API_KEY")

def ingest_incremental():
    corpus = Corpus()
    store = VectorStore()
    indexer = VectorDBManager(corpus, store)
    indexer.upsert_folder()

if __name__ == "__main__":
    ingest_incremental()

    store = VectorStore(persist_dir="./chroma_db")
    vs = store.load()

    print("Ilość dokumentów w bazie:", vs._collection.count())  
    


