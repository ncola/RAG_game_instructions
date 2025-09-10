from index.corpus import Corpus
from index.vectostore import VectorStore
from config import MANIFEST_FILE
import os, json

class VectorDBManager():
    def __init__(self, corpus: Corpus, vectorstore: VectorStore):
        self.corpus=corpus
        self.vectorstore=vectorstore
        self.manifest_path=os.path.join(vectorstore.persist_dir, MANIFEST_FILE)
        self.manifest=self._load_manifest()

    def _load_manifest(self)->dict:
        """Load manifest.json which tracks changes in data """
        if os.path.exists(self.manifest_path):
            with open(self.manifest_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}
    
    def _save_manifest(self)->None:
        """Save manifest.json which tracks changes in data"""
        os.makedirs(self.vectorstore.persist_dir, exist_ok=True)
        with open(self.manifest_path, 'w', encoding='utf-8') as f:
            json.dump(self.manifest, f, ensure_ascii=False, indent=2)
    
    def _chunk_ids(self, doc_hash:str, chunks:list)->list:
        """Give unique values to chunks"""
        ids = []
        for i, chunk in enumerate(chunks):
            page = chunk.metadata.get("page")
            ids.append(f"{doc_hash}:{page}:{i}")
        return ids
    
    def upsert_folder(self)->None:
        """Main flow: add/update new/changed and delete disappeared files from vectorstore.
        Checking the contents of the entire data folder each time"""
        self.vectorstore.ensure_loaded()
        pdfs = self.corpus.get_pdfs_paths()
        seen = {}

        # for each PDF check the hash and do an upsert only if changed/new
        for pdf in pdfs:
            new_hash = self.corpus.hash_file(pdf)
            seen[pdf] = new_hash

            old_hash = self.manifest.get(pdf)
            if old_hash is not None:
                if old_hash == new_hash: #if hash is the same = no chages in file
                    print(f"Bez zmian: {pdf}")
                    continue
                else: #if hash is not the same delete old chunks of that document
                    self.store.delete_by_doc_id(old_hash)
                    print(f"Usunięto starą wersję: {os.path.basename(pdf)}")
        
            pages:list = self.corpus.load_pages(pdf)

            for page in pages:
                page.metadata['doc_id'] = new_hash

            chunks:list = self.corpus.chunk_pages(pages, chunk_size = 500,chunk_overlap = 60)

            #create and ids for every chunk 
            ids = []
            for i, chunk in enumerate(chunks):
                page_no = chunk.metadata.get("page")
                ids.append(f"{new_hash}:{page_no}:{i}")
            
            self.vectorstore.add_chunks(chunks, ids)

            #update the manifts file
            self.manifest[pdf] = new_hash
            print(f"Zaktualizowano: {os.path.basename(pdf)} ({len(chunks)} chunków)")

        
        # delete pdfs that are no longer in data folder
        for pdf in list(self.manifest.keys()):
            if pdf not in seen:
                old_hash = self.manifest[pdf]
                self.vectorstore.delete_by_doc_id(old_hash)
                del self.manifest[pdf]
                print(f"Usunięto wpisy po znikniętym pliku: {os.path.basename(pdf)}")

        self._save_manifest()
        print("✅ Vector database creation/update completed")












