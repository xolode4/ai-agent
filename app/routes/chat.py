from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
import json
from app.services.knowledge import load_combined_knowledge
from app.services.logs import search_logs
from app.services.ai import ai_service

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def chat_ui(request: Request):
    prompts_path = Path(__file__).parent.parent / "prompts.json"
    with open(prompts_path, "r", encoding="utf-8") as f:
        prompts = json.load(f)
    
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "prompts": prompts,
            "selected_prompt": "default"
        }
    )

@router.post("/ask", response_class=HTMLResponse)
async def ask_question(
    request: Request,
    question: str = Form(...),
    model: str = Form(...),
    prompt_key: str = Form("default"),
    environments: list = Form([]),
    log_sources: list = Form([])
):
    prompts_path = Path(__file__).parent.parent / "prompts.json"
    with open(prompts_path, "r", encoding="utf-8") as f:
        prompts = json.load(f)
    
    knowledge = load_combined_knowledge(environments)
    logs = search_logs(question) if "security-auditlog" in log_sources else []
    
    answer = await ai_service.generate_response(
        model=model,
        question=question,
        knowledge=knowledge,
        logs=logs,
        system_prompt=prompts.get(prompt_key, prompts["default"])["prompt"]
    )
    
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "question": question,
            "answer": answer,
            "model": model,
            "prompts": prompts,
            "selected_prompt": prompt_key
        }
    )