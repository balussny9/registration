# --- bootstrap so `python app/main.py` works ---
import sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]  # backend/
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# use absolute imports (important when running as a script)
from app.settings import settings
from app.db import engine, Base
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import uploads, assess, chat

app = FastAPI(title="Social Support Platform API (SQLite Local)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.BACKEND_CORS_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def _startup():
    Base.metadata.create_all(bind=engine)

app.include_router(uploads.router)
app.include_router(assess.router)
app.include_router(chat.router)

@app.get("/health")
def health():
    return {"ok": True}

# run uvicorn programmatically WITHOUT reload to avoid double import
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
