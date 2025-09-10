import os, hashlib
from config import DATA_DIR
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_core.documents import Document
from langchain.text_splitter import TokenTextSplitter


class Corpus():
    def __init__(self, data_dir=DATA_DIR):
        self.data_dir = data_dir

    def get_pdfs_paths(self, suffix:str=".pdf"):
        paths = [os.path.join(self.data_dir, filename) for filename in os.listdir(self.data_dir) if filename.endswith(suffix)]
        return sorted(paths)

    def hash_file(self, path:str)->str:
        h = hashlib.sha1()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(1<<20), b""): 
                h.update(chunk)
        return h.hexdigest()
    
    def load_pages(self, pdf_path:str)->list[Document]:
        pages = []
        for doc in PyMuPDFLoader(pdf_path).load():  #1 doc = 1 page
            doc.metadata.setdefault("source", os.path.relpath(pdf_path))
            pages.append(doc)
        return pages
    
    def chunk_pages(self,
                    pages=list[Document],
                    chunk_size:int=500,
                    chunk_overlap:int=60)->list[Document]:
        splitter = TokenTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        chunks = splitter.split_documents(pages)
        return chunks
        

    


