import httpx

from app.config import settings
from app.schemas import LeadClassification, LeadIn

URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    f"{settings.gemini_model}:generateContent"
)

SCHEMA = {
    "type": "object",
    "properties": {
        "route": {"type": "string", "enum": ["sales", "nurture", "discard"]},
        "score": {"type": "integer", "minimum": 0, "maximum": 100},
        "reason": {"type": "string"},
    },
    "required": ["route", "score", "reason"],
}


def classify(lead: LeadIn) -> LeadClassification:
    prompt = (
        "Classify this sales lead. "
        "sales = ready to buy or asking for a demo. "
        "nurture = interested but not ready. "
        "discard = spam, student, or no commercial intent.\n"
        f"name: {lead.name}\nemail: {lead.email}\nsource: {lead.source}\n"
        f"message: {lead.message}"
    )
    body = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "responseMimeType": "application/json",
            "responseJsonSchema": SCHEMA,
        },
    }
    response = httpx.post(
        URL,
        headers={"x-goog-api-key": settings.gemini_api_key},
        json=body,
        timeout=30,
    )
    response.raise_for_status()
    text = response.json()["candidates"][0]["content"]["parts"][0]["text"]
    return LeadClassification.model_validate_json(text)