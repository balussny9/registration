from pydantic import BaseModel
from typing import Optional, Any, Dict

class ApplicantCreate(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None

class ApplicationOut(BaseModel):
    id: int
    status: str
    decision_json: Dict[str, Any] = {}
    class Config:
        from_attributes = True

class ChatRequest(BaseModel):
    application_id: Optional[int] = None
    message: str

class ChatResponse(BaseModel):
    reply: str

class AssessRequest(BaseModel):
    application_id: int

class RecommendRequest(BaseModel):
    application_id: int
