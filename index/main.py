from index.corpus import Corpus
from index.vectostore import VectorStore
from index.vector_db_manager import VectorDBManager
import argparse 

from dotenv import load_dotenv
load_dotenv()
import openai, os
openai.api_key = os.getenv("OPENAI_API_KEY")

def ingest_incremental(rebase: bool=False):
    corpus = Corpus()
    store = VectorStore()
    indexer = VectorDBManager(corpus, store)
    if rebase:
        store.clean_vs()
    indexer.upsert_folder(rebase)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--rebase",
        action="store_true",
        help="Delete the existing collection and build it from scratch.")
    
    args = parser.parse_args()

    ingest_incremental(args.rebase)

    store = VectorStore(persist_dir="./chroma_db")
    vs = store.load()
    print("Number of documents (chunks) in the vector store:", vs._collection.count())  
    


