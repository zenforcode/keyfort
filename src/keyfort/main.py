from fastapi import FastAPI
from .routers import secrets

from keyfort.models import (
    UpdateSecretPayload,
)

from keyfort.services import (
    secret_service
)

app = FastAPI()
app.include_router(
    secrets.router,
    prefix="/secret",
    tags=["secret"],
    # dependencies=[],
    responses={
        404: {
            "description": "Not found"
        }
    }
)


@app.put("/meta/update/{secret_id}")
def update_secret_meta(secret_id: str, payload: UpdateSecretPayload) -> str:
    return secret_service.update_secret_meta(secret_id, payload)
