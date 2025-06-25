from fastapi import Depends
from app.config import settings
from app.services.vault import get_secrets
from app.services.ai import get_ai_provider
from app.services.logs import get_opensearch_client
from app.services.knowledge import load_knowledge_sources

async def get_secrets_dep():
    return get_secrets()

async def get_ai_provider_dep(model: str, secrets: dict = Depends(get_secrets_dep)):
    return get_ai_provider(model, secrets)

async def get_opensearch_dep():
    return get_opensearch_client()

async def get_knowledge_sources_dep():
    return load_knowledge_sources()