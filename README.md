# writing-assistant

Multi-agent “thinking assistant” for a Master’s thesis on Mergers & Acquisitions.

## Structure

- `backend/` FastAPI service with LangGraph orchestration and Chroma RAG memory.
- `frontend/` React UI with a markdown editor, agent tabs, and challenge box.

## Quick start

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

```bash
cd frontend
npm install
npm run dev
```
