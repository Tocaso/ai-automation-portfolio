from fastapi import FastAPI

from app.agent import classify
from app.router import next_action
from app.schemas import LeadClassification, LeadDecision, LeadIn
from app.database import save_lead

app = FastAPI(title="Lead classifier")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/leads/classify", response_model=LeadDecision)
def classify_lead(lead: LeadIn) -> LeadDecision:
    result = classify(lead)
    action = next_action(result)
    decision = LeadDecision(classification=result, action=action)
    save_lead(lead, decision)
    return decision
