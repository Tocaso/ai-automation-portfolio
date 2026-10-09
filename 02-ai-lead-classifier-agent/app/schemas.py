from enum import Enum

from pydantic import BaseModel, Field


class Route(str, Enum):
    SALES = "sales"
    NURTURE = "nurture"
    DISCARD = "discard"


class LeadIn(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    email: str = Field(min_length=3, max_length=254)
    message: str = Field(min_length=1, max_length=4000)
    source: str = Field(default="web", max_length=64)


class LeadClassification(BaseModel):
    route: Route
    score: int = Field(ge=0, le=100)
    reason: str = Field(min_length=1, max_length=500)

class LeadDecision(BaseModel):
    classification: LeadClassification
    action: str