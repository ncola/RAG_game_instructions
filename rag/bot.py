from config import PURPOSE, RULES, EXAMPLES
from models.models import BotConfig, LLMConfig
import rag.utils as u

from rag.llm import LLMClient
from index.vectostore import VectorStore

SYSTEM_PROMPT = (
    f"{PURPOSE}\n\n"
    f"ZASADY:\n{RULES}\n"
    "Zawsze podaj źródła (plik + strona) na końcu.\n"
)

class Bot():
    def __init__(self, cfg: BotConfig, api_key=None):
        self.cfg = cfg
        self.vectorstore = VectorStore()      
        self.vectorstore.load()                
        self.retriever = self.vectorstore.vector_retriever(k=cfg.k, score_threshold=cfg.score_threshold)
        self.llm = LLMClient(LLMConfig, api_key=api_key)

    def _retrieve(self, question:str):
        return self.retriever.get_relevant_documents(question)
    
    def answer(self, question, history=None):
        docs = self._retrieve(question)
        ctx = u.format_docs(docs, max_docs=self.cfg.max_ctx_docs)
        messages = u.build_messages(SYSTEM_PROMPT, history or [], question, ctx)
        answer = self.llm.generate(messages)
        sources = u.sources_line(docs)
        return answer, sources
    
    