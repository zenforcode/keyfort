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


# @app.post("/secret")
# def create_secret(payload: CreateSecretPayload) -> SecretDTO:
#     return secret_service.create_secret(payload)
#
#
# @app.get("/secret/{secret_id}")
# def get_secret(secret_id: str, meta: bool = False) -> SecretDTO:
#     return secret_service.get_secret(secret_id, meta)
#
#
# @app.get("/secret/{secret_id}/info")
# def get_secret_info(secret_id: str) -> MetadataDTO:
#     return secret_service.get_secret_info(secret_id)
#
#
# @app.delete("/secret/invalidate/{secret_id}")
# def invalidate_secret(secret_id: str) -> str:
#     return secret_service.invalidate_secret(secret_id)


@app.put("/meta/update/{secret_id}")
def update_secret_meta(secret_id: str, payload: UpdateSecretPayload) -> str:
    return secret_service.update_secret_meta(secret_id, payload)
