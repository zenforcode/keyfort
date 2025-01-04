from uuid import uuid4
from datetime import datetime
from fastapi import HTTPException

from ..models import (
    CreateSecretPayload,
    UpdateSecretPayload,
    Secret,
    SecretDTO,
    Version,
    Metadata,
    MetadataDTO
)

from ..exceptions import (
    NotCreatedException,
)

from ..repository import (
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

    try:
        inserted_secret: Secret = secretRepository.create(secret)

        if not inserted_secret:
            raise HTTPException(status_code=400, detail="Insertion failed")
        
        return inserted_secret.get_dto()
        
    except NotCreatedException as e:
        raise HTTPException(status_code=404, detail=str(e))
    
def get_secret(secret_id: str, meta: bool) -> SecretDTO:
    secret = secretRepository.find(secret_id=secret_id, meta=meta)

    if secret:
        return secret.get_dto()
    else:
        raise HTTPException(
            status_code=404, detail="Could not retreive secret")

def get_secret_info(secret_id: str) -> MetadataDTO:
    secret = secretRepository.find(secret_id)

    if not secret or not secret.metadata:
        raise HTTPException(
            status_code=404, detail="Could not retreive metadata for secret"
        )

    metadata = secret.metadata
    print("metadata:", metadata.get_dto())
    return metadata.get_dto()

def update_secret_meta(secret_id: str, payload: UpdateSecretPayload):
    err, res = secretRepository.update(secret_id, payload.secret)
    if err:
        raise HTTPException(status_code=404, detail=res)
    return res

def invalidate_secret(secret_id: str) -> str:
    err, res = secretRepository.delete(secret_id)
    if err:
        raise HTTPException(status_code=404, detail=res)
    return res