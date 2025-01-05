from fastapi import APIRouter

from keyfort.services import secret_service
from keyfort.models import (
    CreateSecretPayload,
    SecretDTO,
    MetadataDTO,
)

router = APIRouter()


@router.post("/")
def create_secret(payload: CreateSecretPayload) -> SecretDTO:
    return secret_service.create_secret(payload)


@router.get("/{secret_id}")
def get_secret(secret_id: str, meta: bool = False) -> SecretDTO:
    return secret_service.get_secret(secret_id, meta)


@router.get("/{secret_id}/info")
def get_secret_info(secret_id: str) -> MetadataDTO:
    return secret_service.get_secret_info(secret_id)


@router.delete("/{secret_id}")
def invalidate_secret(secret_id: str) -> str:
    return secret_service.invalidate_secret(secret_id)
