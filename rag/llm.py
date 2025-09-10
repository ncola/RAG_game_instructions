from models.models import LLMConfig
from openai import OpenAI

class LLMClient:
    def __init__(self, cfg: LLMConfig, api_key=None):
        self.cfg = cfg
        self.client = OpenAI(api_key=api_key) if api_key else OpenAI() 

    def generate(self, messages):
        completion = self.client.chat.completions.create(
            model = self.cfg.model,
            messages = messages,
            temperature = self.cfg.temperature
        )
        return completion.choices[0].message.content