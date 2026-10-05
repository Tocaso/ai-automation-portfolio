import httpx
from fastapi import FastAPI, HTTPException, status

from app.config import Settings
from app.schemas import WebhookPayload


settings = Settings()

app = FastAPI(
    title="Telegram Automation API",
    description="Microservicio para enviar notificaciones a Telegram.",
    version="1.0.0",
)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/v1/webhook", status_code=status.HTTP_200_OK)
async def webhook(payload: WebhookPayload) -> dict[str, str]:
    token = settings.TELEGRAM_BOT_TOKEN.get_secret_value()
    url = f"https://api.telegram.org/bot{token}/sendMessage"

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                url,
                json={
                    "chat_id": settings.TELEGRAM_CHAT_ID,
                    "text": payload.message,
                },
            )

        response.raise_for_status()
        data = response.json()

        if not isinstance(data, dict) or data.get("ok") is not True:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Telegram no confirmó el envío del mensaje.",
            )

    except httpx.HTTPError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No se pudo enviar el mensaje a Telegram.",
        ) from None

    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Telegram devolvió una respuesta inválida.",
        ) from None

    return {"status": "ok", "detail": "Mensaje enviado a Telegram."}