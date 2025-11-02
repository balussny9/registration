# Social Support Platform — Local (SQLite, no Docker)

This project includes:
- **FastAPI** backend (Python 3.11)
- **Next.js** frontend
- **SQLite** database (default)
- **OpenAI Responses API**
- **Postman** collection & environment
- **Sample documents** to test uploads

## 1) Prerequisites
- Python 3.11+
- Node.js 18+
- An OpenAI API key

## 2) Configure environment
From the project root:
```bash
cp .env.example .env
# open .env and set your real OPENAI_API_KEY
```
The defaults use SQLite at `backend/app/data/ssp.db` and uploads under `./uploads`.

## 3) Run the backend (FastAPI + SQLite)
```bash
cd backend
python3 -m venv .venv
# macOS/Linux:
source .venv/bin/activate
# Windows PowerShell:
# .venv\Scripts\Activate.ps1

pip install -r requirements.txt

# IMPORTANT: run from the backend folder so the SQLite relative path works
uvicorn app.main:app --reload --port 8000
```
- API docs: http://127.0.0.1:8000/docs
- Health: http://127.0.0.1:8000/health

## 4) Run the frontend (Next.js)
```bash
cd ../frontend
echo "NEXT_PUBLIC_BACKEND_URL=http://127.0.0.1:8000" > .env.local
npm install
npm run dev
```
Open http://localhost:3000

## 5) Test flow in the UI
1. Fill applicant details (income, employment history, family size, wealth, demographics).
2. Upload sample docs from `sample_data/` (resume.docx, assets.xlsx, bank_statement.txt, id_front.png).
3. Click **Create Application** → shows an application ID.
4. Click **Run Eligibility Assessment** → decision, confidence, reasons, criteria.
5. Click **Get Enablement Recommendations** → upskilling, job matches, counseling.
6. Use the **Chatbot** to ask status/next steps (linked to the application).

## 6) Test with Postman
- Import: `SSP_API_v2.postman_collection.json` and `SSP_Local.postman_environment.json`.
- Ensure the environment has `BASE=http://127.0.0.1:8000`.
- Run in order:
  1) **Create Application (multipart)** — attach files from `sample_data/`
  2) **Assess** — `{ "application_id": <ID> }`
  3) **Recommend** — `{ "application_id": <ID> }`
  4) **Chat** — `{ "application_id": <ID>, "message":"What is my status?" }`

## Notes
- We pin `httpx==0.27.2` to avoid an old `proxies` incompatibility with the OpenAI SDK.
- `.env` is loaded explicitly in the backend via `load_dotenv(override=True)`.
- If you switch to Postgres later, set `DATABASE_URL` accordingly (e.g., `postgresql+psycopg://user:pass@localhost:5432/db`).

Happy testing!
