from pydantic import BaseModel, ConfigDict, Field

class WebhookPayload(BaseModel):
    model_config = ConfigDict(
        strict=True,
        extra="forbid",
        str_strip_whitespace=True,
    )

    message: str = Field(min_length=1, max_length=4096)