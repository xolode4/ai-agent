from opensearchpy import OpenSearch, ConnectionError
from app.config import settings
import time
from typing import List, Dict

def get_opensearch_client(max_retries: int = 3) -> OpenSearch:
    for attempt in range(max_retries):
        try:
            return OpenSearch(
                hosts=[settings.opensearch_host],
                http_compress=True,
                verify_certs=settings.opensearch_ssl_verify,
                timeout=30,
                max_retries=3,
                retry_on_timeout=True
            )
        except ConnectionError:
            if attempt == max_retries - 1:
                raise
            time.sleep(1)

def search_logs(query: str, time_range: str = "1h", size: int = 5) -> List[Dict]:
    try:
        client = get_opensearch_client()
        
        query_body = {
            "query": {
                "multi_match": {
                    "query": query,
                    "fields": ["message", "exception"],
                    "operator": "AND"
                }
            },
            "size": size,
            "sort": [{"@timestamp": "desc"}]
        }
        
        response = client.search(
            index="logstash-*",
            body=query_body,
            request_timeout=45  # Увеличили таймаут
        )
        
        return [hit["_source"] for hit in response["hits"]["hits"]]
    
    except Exception as e:
        print(f"OpenSearch error: {str(e)}")
        return []