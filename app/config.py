from pydantic_settings import BaseSettings
from pydantic import SecretStr, Field
from typing import List

class Settings(BaseSettings):
    # Настройки Vault (обязательные поля)
    vault_url: str = Field(default="https://vault.home.lcl:8200")
    vault_secret_path: str = Field(default="secret/data/ai-agent")  # Полный путь в Vault
    vault_token: SecretStr  # Убрали default=None, теперь поле обязательно
    vault_refresh_seconds: int = Field(default=3600)
    vault_secret_path: str = Field(default="ai-agent")
    vault_ssl_verify: bool = Field(default=False)
    
    # Настройки OpenSearch
    opensearch_host: str = Field(default="http://localhost:9200")
    opensearch_ssl_verify: bool = Field(default=False)
    
    # Настройки приложения
    excluded_paths: List[str] = Field(default=[".git", "__pycache__", "tmp"])
    include_extensions: List[str] = Field(default=[])
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"
    
    @property
    def secrets(self):
        from app.services.vault import get_secrets
        return get_secrets()

settings = Settings()
