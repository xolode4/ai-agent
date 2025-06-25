from pydantic import BaseModel
from typing import Dict, List, Optional

class ChatRequest(BaseModel):
    question: str
    model: str
    environments: List[str] = []
    log_sources: List[str] = []

class ChatResponse(BaseModel):
    question: str
    answer: str
    model: str
    timestamp: float

class KnowledgeSource(BaseModel):
    repo_url: str
    branch: str
    token: Optional[str] = None

class LogEntry(BaseModel):
    message: str
    timestamp: str
    level: Optional[str] = None