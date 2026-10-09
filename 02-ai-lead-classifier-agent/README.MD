# Lead classifier

HTTP service that classifies a sales lead and returns a route plus an action.

## Run locally

```bash
py -3.12 -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload

`POST /leads/classify` with `name`, `email` and `message`. Response: `classification` (`route`, `score`, `reason`) and `action` (`notify_sales`, `enroll_sequence`, `archive`).