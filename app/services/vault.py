import hvac
from app.config import settings
from typing import Dict

_secrets_cache = None

def get_secrets() -> Dict[str, str]:
    global _secrets_cache
    if _secrets_cache is not None:
        return _secrets_cache
        
    try:
        client = hvac.Client(
            url=settings.vault_url,
            token=settings.vault_token.get_secret_value(),
            verify=settings.vault_ssl_verify
        )
        
        if not client.is_authenticated():
            raise Exception("Vault authentication failed")
        
        response = client.secrets.kv.v2.read_secret_version(
            path=settings.vault_secret_path.replace("secret/data/", "")
        )
        
        _secrets_cache = response['data']['data']
        return _secrets_cache
        
    except Exception as e:
        raise Exception(f"Failed to fetch secrets from Vault: {str(e)}")