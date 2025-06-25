from openai import OpenAI
from typing import Dict, List
import json
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_gigachat.chat_models import GigaChat
from app.services.vault import get_secrets
class AIService:
    def __init__(self):
        self._openai_client = None
        self._giga_client = None
    
    def init_openai(self):
        secrets = get_secrets()
        self._openai_client = OpenAI(api_key=secrets["OPENAI_API_KEY"])
    
    def init_giga(self):
        secrets = get_secrets()
        self._giga_client = GigaChat(
            credentials=secrets["GIGACHAT_TOKEN"],
            verify_ssl_certs=False
        )
    
    async def generate_response(
        self,
        model: str,
        question: str,
        knowledge: Dict[str, str],
        logs: List[Dict],
        system_prompt: str
    ) -> str:
        context = "\n".join([f"{k}: {v}" for k, v in knowledge.items()])
        if logs:
            context += f"\n\n[Logs]\n" + "\n".join(str(log) for log in logs)
        
        full_prompt = f"{context}\n\nQuestion: {question}\nAnswer:"
        
        if model == "openai":
            if self._openai_client is None:
                self.init_openai()
            try:
                response = self._openai_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": full_prompt}
                    ]
                )
                return response.choices[0].message.content
            except Exception as e:
                return f"OpenAI error: {str(e)}"
        
        elif model == "gigachat":
            if self._giga_client is None:
                self.init_giga()
            try:
                response = self._giga_client([
                    SystemMessage(content=system_prompt),
                    HumanMessage(content=full_prompt)
                ])
                return response.content
            except Exception as e:
                return f"GigaChat error: {str(e)}"
        
        elif model == "opensearch":
            return json.dumps(logs, ensure_ascii=False, indent=2)
        
        return "Unsupported model"

# Инициализируем сервис при импорте
ai_service = AIService()