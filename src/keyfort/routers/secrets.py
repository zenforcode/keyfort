from fastapi import APIRouter, HTTPException

from keyfort.services import secret_service
from keyfort.models import (
    CreateSecretPayload,
    SecretDTO,
    MetadataDTO,
)
from keyfort.exceptions import NotCreatedException

router = APIRouter()


@router.post("/")
def create_secret(payload: CreateSecretPayload) -> SecretDTO:
    try:
        return secret_service.create_secret(payload)        
        
    except NotCreatedException as e:
        raise HTTPException(status_code=404, detail="Could not create secret")


@router.get("/{secret_id}")
def get_secret(secret_id: str, meta: bool = False) -> SecretDTO:
    secret = secret_service.get_secret(secret_id, meta)

    if not secret:
        raise HTTPException(status_code=404, detail="Could not retreive secret")
    
    return secret


@router.get("/{secret_id}/info")
def get_secret_info(secret_id: str) -> MetadataDTO:
    metadata = secret_service.get_secret_info(secret_id)

    if not metadata:
        raise HTTPException(status_code=404, detail="Could not retreive metadata")

    return metadata


@router.delete("/{secret_id}")
def invalidate_secret(secret_id: str) -> str:
    deleted = secret_service.invalidate_secret(secret_id)

    if deleted != "OK":
        raise HTTPException(status_code=404, detail="Could not invalidate secret")
    
    return "OK"
