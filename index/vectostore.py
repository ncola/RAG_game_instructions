from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from config import PERSIST_DIR, EMBED_MODEL
from chromadb.errors import NotFoundError

from datetime import datetime

class VectorStore():
    def __init__(self, persist_dir=PERSIST_DIR, embed_model=EMBED_MODEL):
        self.persist_dir=persist_dir
        self.emb=OpenAIEmbeddings(model=embed_model)
        self.vs: Chroma | None = None #Chroma vector database object
    
    def load(self)->Chroma:
        self.vs=Chroma(collection_name="game_instructions", 
                       persist_directory=self.persist_dir, 
                       embedding_function=self.emb, 
                       collection_metadata={
                           "description": "Vector database storing text chunks from board game rulebooks",
                           "created": str(datetime.now())
                       })
        return self.vs
    
    def ensure_loaded(self)->Chroma:
        return self.vs if self.vs is not None else self.load()
    
    def add_chunks(self, chunks:list[Document], ids:list[str])->None:
        vs = self.ensure_loaded()
        vs.add_documents(documents=chunks, ids=ids)
        vs.persist() #permanent record PERSIST_DIR

    def delete_by_doc_id(self, doc_id:str)->None:
        vs = self.ensure_loaded()
        vs.delete(where={"doc_id": doc_id})
        vs.persist() 
    
    def vector_retriever(self, k:int=5, score_threshold:float=0.8):
        """
        Returns a vector retriever (Chroma). Method: MMR (Max Marginal Relevance) - provides more context variety
        """
        vs = self.ensure_loaded()
        kwargs = {"k": k, "score_threshold": score_threshold}

        return vs.as_retriever(search_type="mmr", search_kwargs=kwargs)
    
    def clean_vs(self):
        try:
            vs = self.ensure_loaded()
            vs.delete_collection()
        except NotFoundError:
            print("Collection not found. Skipping deletion.")
        except Exception as e:
            print(f"Unexpected error while deleting collection: {e}")
        finally:
            self.vs = None



 