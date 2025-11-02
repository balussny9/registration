from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db
from ..models import Application, ChatMessage
from ..schemas import ChatRequest, ChatResponse
from ..llm import chat_text

router = APIRouter(prefix="/api", tags=["chat"])

@router.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest, db: Session = Depends(get_db)):
    context = ""
    if req.application_id:
        app = db.query(Application).get(req.application_id)
        if not app:
            raise HTTPException(404, "Application not found")
        context = f"Application status: {app.status}. Decision: {app.decision_json}"
    reply = chat_text(context + "\n\nUser: " + req.message)
    db.add(ChatMessage(application_id=req.application_id, role="user", content=req.message))
    db.add(ChatMessage(application_id=req.application_id, role="assistant", content=reply))
    db.commit()
    return {"reply": reply}
