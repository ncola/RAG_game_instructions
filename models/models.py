from dataclasses import dataclass
from config import PERSIST_DIR, EMBED_MODEL, MODEL_NAME


@dataclass
class BotConfig:
    persist_dir: str = PERSIST_DIR                
    embed_model: str = EMBED_MODEL   
    k: int = 6
    score_threshold: float = 0.75 
    max_ctx_docs = 8

@dataclass
class LLMConfig:
    model: str = MODEL_NAME
    temperature: float = 0.7
