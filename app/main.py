from fastapi.templating import Jinja2Templates
import os
from app.services.ai import client as openai_client 
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes.chat import router as chat_router

app = FastAPI(title="AI Log Analyzer")

# Подключение статических файлов
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")
# Убедитесь, что путь к шаблонам абсолютный
template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
templates = Jinja2Templates(directory=template_dir)
# Подключение роутера
app.include_router(chat_router)

#app.mount("/static", StaticFiles(directory="static"), name="static")

@app.on_event("startup")
async def startup():
    try:
        # Инициализируем клиенты при старте приложения
        ai_service.init_openai()
        ai_service.init_giga()
        print("AI services initialized successfully")
    except Exception as e:
        print(f"AI services initialization failed: {str(e)}")
        raise

@app.on_event("startup")
async def startup():
    try:
        secrets = get_secrets()
        print("Vault secrets loaded successfully")
        print("Available keys:", list(secrets.keys()))
    except Exception as e:
        print(f"Failed to load secrets: {str(e)}")
        raise

@app.on_event("startup")
async def startup():
    # Проверяем подключение к OpenAI
    try:
        models = openai_client.models.list()
        print("OpenAI connection successful")
    except Exception as e:
        print(f"OpenAI connection error: {str(e)}")

@app.get("/")
async def root():
    return {"message": "AI Log Analyzer is running"}

@app.on_event("startup")
async def startup_event():
    from app.services.logs import get_opensearch_client
    try:
        client = get_opensearch_client()
        if not client.ping():
            print("Warning: OpenSearch connection failed")
        else:
            print("OpenSearch connection successful")
    except Exception as e:
        print(f"OpenSearch connection error: {str(e)}")