from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..db import get_db
from ..models import Application
from ..schemas import AssessRequest, RecommendRequest
from ..llm import assess_json, recs_json
import json

router = APIRouter(prefix="/api", tags=["assessment"])

@router.post("/assess")
def assess(req: AssessRequest, db: Session = Depends(get_db)):
    app = db.query(Application).get(req.application_id)
    if not app:
        raise HTTPException(404, "Application not found")
    payload = json.dumps({
        "form_data": app.form_data,
        "extracted_text": app.extracted_text[:20000]
    })
    out = assess_json(payload)
    try:
        app.decision_json = json.loads(out)
        app.status = "assessed"
        db.commit()
    except Exception:
        raise HTTPException(500, f"Model output not JSON: {out[:500]}")
    return {"application_id": app.id, "decision": app.decision_json}

@router.post("/recommend")
def recommend(req: RecommendRequest, db: Session = Depends(get_db)):
    app = db.query(Application).get(req.application_id)
    if not app:
        raise HTTPException(404, "Application not found")
    out = recs_json(json.dumps({"profile": app.form_data, "decision": app.decision_json}))
    try:
        recs = json.loads(out)
        return {"application_id": app.id, "recommendations": recs}
    except Exception:
        raise HTTPException(500, f"Model output not JSON: {out[:400]}")
