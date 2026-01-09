# Health Outlook API (FastAPI)

Backend skeleton for collecting clinician-entered patient data, generating simple risk reports, and summarizing them via ChatGPT. Focused on local experimentation while remaining ready for containerization.

## Features
- FastAPI + Pydantic models for patients and risk reports.
- In-memory storage for rapid iteration (swap out for a database later).
- Rule-based risk scoring stub plus optional LLM summary (OpenAI ChatGPT).
- CORS enabled for connecting a local UI.
- Dockerfile included for k8s/cloud adaptation.

## Prerequisites
- Python 3.11+ recommended.
- `OPENAI_API_KEY` set in your shell to enable real LLM summaries (otherwise a deterministic fallback is used).

## Setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run locally
```bash
uvicorn app.main:app --reload
# API docs: http://127.0.0.1:8000/docs
```

## Example usage
Create a patient:
```bash
curl -X POST http://127.0.0.1:8000/api/patients \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Ada",
    "last_name": "Lovelace",
    "age": 67,
    "sex": "female",
    "conditions": ["hypertension"],
    "vitals": {"systolic_bp": 150, "diastolic_bp": 95}
  }'
```

Generate a report with LLM summary (set `OPENAI_API_KEY` to use ChatGPT):
```bash
curl -X POST http://127.0.0.1:8000/api/reports \
  -H "Content-Type: application/json" \
  -d '{"patient_id": "<patient-id-from-previous-response>", "summarize": true}'
```

Retrieve a report:
```bash
curl http://127.0.0.1:8000/api/reports/<report-id>
```

## Docker
```bash
docker build -t health-outlook-api .
docker run -p 8000:8000 -e OPENAI_API_KEY=$OPENAI_API_KEY health-outlook-api
```

## Notes
- Risk scoring is intentionally simple; replace `app/services/risk.py` with real clinical logic.
- LLM calls are best-effort: if the API key is missing or errors, a fallback summary is returned.
- Swap `app/storage.py` with a database-backed repository when ready for persistence.
