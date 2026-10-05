\# FastAPI Telegram Webhook



Microservicio en Python que recibe un mensaje mediante HTTP,

valida su contenido y envía una notificación a Telegram.



Proyecto de portafolio orientado a AI Automation Engineering.

Este servicio implementa la capa de notificaciones; no incluye un modelo de IA.



\## Funcionamiento



Una aplicación o automatización envía un JSON a

POST /api/v1/webhook. FastAPI valida los datos con Pydantic

y utiliza la API de Telegram para enviar el texto al chat configurado.



Este endpoint recibe eventos de otras aplicaciones.

No implementa el formato de actualizaciones entrantes de Telegram

ni registra un webhook mediante setWebhook.



\## Tecnologías



\- Python 3.12

\- FastAPI y Uvicorn

\- Pydantic v2 y Pydantic Settings

\- HTTPX con llamadas asincrónicas

\- Telegram Bot API

\- Docker



\## Organización



\- app/\_\_init\_\_.py: identifica el paquete de Python.

\- app/config.py: carga y valida la configuración.

\- app/schemas.py: define el payload y su validación estricta.

\- app/main.py: define los endpoints y el envío a Telegram.

\- requirements.txt: dependencias.

\- .env.example: plantilla de configuración.

\- .gitignore: exclusiones de Git.

\- .dockerignore: exclusiones del contexto de Docker.

\- Dockerfile: construcción y arranque de la imagen.

\- README.md: documentación.



\## Configuración



Crea un bot con @BotFather y obtén su token.

Inicia una conversación con el bot y obtén el chat ID de destino.



Copia .env.example a .env y configura:



```dotenv

TELEGRAM\_BOT\_TOKEN=REEMPLAZAR\_CON\_TOKEN\_REAL

TELEGRAM\_CHAT\_ID=123456789

```



Sustituye ambos valores por los reales.

No publiques .env ni incluyas credenciales en el código.



\## Ejecución local: Windows PowerShell



Desde la carpeta del proyecto:



```powershell

python -m venv .venv

.\\.venv\\Scripts\\Activate.ps1

python -m pip install -r requirements.txt

```



Si todavía no tienes .env:



```powershell

Copy-Item .env.example .env

notepad .env

```



Configura los valores reales antes de arrancar:



```powershell

python -m uvicorn app.main:app --reload

```



Swagger UI: http://127.0.0.1:8000/docs



\## Endpoints



| Método | Ruta | Función |

|---|---|---|

| GET | /health | Comprueba que la aplicación responde. |

| POST | /api/v1/webhook | Valida un mensaje y lo envía a Telegram. |



/health no verifica la disponibilidad de Telegram.



\### Petición válida



```json

{

&#x20; "message": "Nueva notificación desde FastAPI"

}

```



message debe ser texto de entre 1 y 4096 caracteres.

Se eliminan espacios al inicio y al final.

Se rechazan campos adicionales.



\### Respuesta de envío exitoso: 200



```json

{

&#x20; "status": "ok",

&#x20; "detail": "Mensaje enviado a Telegram."

}

```



\### Errores



\- 422: el payload no cumple las reglas de validación.

\- 500: error de conexión, rechazo de Telegram o respuesta inválida.



\## Ejecución con Docker



Requiere Docker funcionando y un archivo .env configurado.



Construye la imagen:



```powershell

docker build -t fastapi-telegram-webhook:1.0 .

```



Detén cualquier servidor que esté utilizando el puerto 8000.

Después ejecuta:



```powershell

docker run --rm --name telegram-api --env-file .env -p 127.0.0.1:8000:8000 fastapi-telegram-webhook:1.0

```



Abre http://127.0.0.1:8000/docs para probar la API.



Docker recibe la configuración mediante variables de entorno.

El archivo .env no se copia a la imagen.



Para detener el contenedor desde otra terminal:



```powershell

docker stop telegram-api

```



El contenedor se elimina al detenerse por usar --rm.

La imagen permanece disponible.



\## Validación manual



\- Envío local: 200 y mensaje recibido en Telegram.

\- Payload con message numérico: 422.

\- Arranque en Docker: /health responde con status ok.

\- Envío desde Docker: 200 y mensaje recibido en Telegram.



\## Alcance actual



Versión de demostración para ejecución local.



El endpoint no tiene autenticación, límites de peticiones

ni de duplicación. Cada petición válida intenta un nuevo envío.

Antes de exponerlo públicamente, se deben incorporar esos controles.



La configuración del token y del chat ID es obligatoria al arrancar.

