import os, hashlib, re
from config import DATA_DIR
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_core.documents import Document
from langchain.text_splitter import TokenTextSplitter


class Corpus():
    def __init__(self, data_dir=DATA_DIR):
        self.data_dir = data_dir

    def get_pdfs_paths(self, suffix:str=".pdf") -> list[str]:
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
            doc.page_content = (doc.page_content.encode("latin-1", errors="ignore").decode("cp1250", errors="ignore"))
            doc.metadata.setdefault("source", os.path.relpath(pdf_path))
            pages.append(doc)
        return pages

    def chunk_pages(self,
                    pages=list[Document],
                    chunk_size:int=1000,
                    chunk_overlap:int=100)->list[Document]:
        splitter = TokenTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        chunks = splitter.split_documents(pages)
        return chunks
    
    def clean_text(self, raw:str):
        text = raw.strip()
        text = re.sub(r"\n{3,}", "\n\n", text)
        text = re.sub(r"[ \t]+", " ", text)         
        text = re.sub(r"(?<!\n)\n(?!\n)", " ", text)
        text = re.sub(r"[\x00-\x1F\x7F]", "", text)
        return text

    def get_game_name(self, pdf_path):
        filename = os.path.basename(pdf_path)
        name, _ = os.path.splitext(filename)
        game_family = name.split("---")[0]
        game_name = (name
                 .replace('---', ': ')
                 .replace('_', ' ')
                 .strip())

        return game_name, game_family

    


