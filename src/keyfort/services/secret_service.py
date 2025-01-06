from uuid import uuid4
from datetime import datetime
from fastapi import HTTPException
from typing import Optional

from keyfort.models import (
    CreateSecretPayload,
    UpdateSecretPayload,
    Secret,
    SecretDTO,
    Version,
    Metadata,
    MetadataDTO
)

from keyfort.exceptions import (
    NotCreatedException,
)

from keyfort.repository import (
    SecretRepository,
    InMemorySecretRepository,
    SQLSecretRepository
)


ENV = "DEV"
secretRepository: SecretRepository = InMemorySecretRepository()

if ENV != "DEV":
    secretRepository = SQLSecretRepository()


def create_secret(payload: CreateSecretPayload) -> SecretDTO:
    now = datetime.now()
    last_modified = now.strftime("%d%m%Y%H%M%S")
    version = Version(
        version_number=0, 
        description="",
        last_modified=last_modified
    )
    metadata = Metadata(
        created_at=last_modified,
        updated_at=last_modified,
        description="",
        is_active=True,
    )
    secret = Secret(
        secret_id=str(uuid4()), 
        value=payload.secret, 
        version=version, 
        metadata=metadata
    )

    inserted_secret: Secret = secretRepository.create(secret)

    if not inserted_secret:
        raise NotCreatedException()
    
    return inserted_secret.get_dto()

    
def get_secret(secret_id: str, meta: bool = False) -> Optional[SecretDTO]:
    secret = secretRepository.find(secret_id=secret_id, meta=meta)

    if secret:
        return secret.get_dto()

    return None

def get_secret_info(secret_id: str) -> Optional[MetadataDTO]:
    secret = secretRepository.find(secret_id)

    if secret:
        return secret.metadata.get_dto()

    return None

def update_secret_meta(secret_id: str, payload: UpdateSecretPayload) -> str:
    err, res = secretRepository.update(secret_id, payload.secret)

    return res

def invalidate_secret(secret_id: str) -> str:
    err, res = secretRepository.delete(secret_id)

    return res