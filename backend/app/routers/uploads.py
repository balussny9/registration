from fastapi import APIRouter, UploadFile, File, Form, Depends
from sqlalchemy.orm import Session
from pathlib import Path
from typing import List, Optional
from ..db import get_db, engine, Base
from ..models import Applicant, Application, Document
from ..settings import settings
from ..extractors import extract_text_generic
import json

router = APIRouter(prefix="/api", tags=["uploads"])

# Create tables automatically on import
Base.metadata.create_all(bind=engine)

@router.post("/applications/create")
async def create_application(
    name: str = Form(...),
    email: str = Form(...),
    phone: Optional[str] = Form(None),
    form_json: Optional[str] = Form("{}"),
    files: List[UploadFile] = File(default=[]),
    db: Session = Depends(get_db),
):
    applicant = db.query(Applicant).filter(Applicant.email == email).first()
    if not applicant:
        applicant = Applicant(name=name, email=email, phone=phone or "")
        db.add(applicant)
        db.flush()

    app = Application(applicant_id=applicant.id, form_data=json.loads(form_json))
    db.add(app)
    db.flush()

    updir = Path(settings.UPLOAD_DIR) / f"app_{app.id}"
    updir.mkdir(parents=True, exist_ok=True)

    texts = []
    for f in files or []:
        dest = updir / f.filename
        with dest.open("wb") as out:
            out.write(await f.read())
        text = extract_text_generic(dest)
        db.add(Document(application_id=app.id, filename=f.filename, filetype=dest.suffix.lower(), path=str(dest), text=text))
        if text:
            texts.append(text)

    app.extracted_text = "\n\n".join(texts)[:500000]
    db.commit()
    return {"application_id": app.id, "uploaded": [d.filename for d in app.documents]}
