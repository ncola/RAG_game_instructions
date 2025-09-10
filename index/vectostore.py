from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from config import PERSIST_DIR, EMBED_MODEL

class VectorStore():
    def __init__(self, persist_dir=PERSIST_DIR, embed_model=EMBED_MODEL):
        self.persist_dir=persist_dir
        self.emb=OpenAIEmbeddings(model=embed_model)
        self.vs: Chroma | None = None #Chroma vector database object
    
    def load(self)->Chroma:
        self.vs=Chroma(persist_directory=self.persist_dir, embedding_function=self.emb)
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
    
    def vector_retriever(self, k:int=5, mmr:bool=True, lambda_mult:float=0.5):
        """
        Returns a vector retriever (Chroma). Method: MMR (Max Marginal Relevance) - provides more context variety
        """
        vs = self.ensure_loaded()
        kwargs = {"k": k}
        if mmr:
            kwargs.update({"search_type": "mmr", "lambda_mult": lambda_mult})
        return vs.as_retriever(search_kwargs=kwargs)


 