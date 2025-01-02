from typing import Type, Optional, Tuple, NoReturn
from copy import deepcopy

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, UUID4

from keyfort.models import (
    Secret,
    Version,
    Metadata,
    CreateSecretPayload,
    UpdateSecretPayload,
)
from keyfort.repository import SecretRepository

app = FastAPI()


class NotCreatedException(Exception):
    def __init__(self):
        super().__init__("Error creating secret")


# TODO: is there anyway to inject?
secretRepository = SecretRepository()


@app.post("/secret")
def create_secret(payload: CreateSecretPayload):
    try:
        inserted_secret: Secret = secretRepository.insert_secret(
            secret_id=payload.secret, value=payload.value, metadata=payload.metadata
        )
        # it might fail if exists.
        if not inserted_secret:
            raise HTTPException(status_code=400, detail="Insertion failed")
    except NotCreatedException as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/secret/{id}")
def get_secret(secret_id: str, meta: bool = False):
    secret = secretRepository.get_secret_meta(secret_id=secret_id, meta=meta)
    if secret:
        return secret
    else:
        raise HTTPException(status_code=404, detail="Could not retreive secret")


@app.get("/secret/{id}/info")
def get_secret_info(secret_id: str) -> Secret | NoReturn:
    err, secret = secretRepository.get_secret(secret_id=secret_id)
    if err:
        raise HTTPException(
            status_code=404, detail="Could not retreive metadata for secret"
        )
    return secret


@app.put("/meta/update/{id}")
def update_secret_meta(id: UUID4, payload: UpdateSecretPayload):
    print(id)
    try:
        return secretRepository.updateSecret(id, payload.secret)
    except NotFoundException:
        raise HTTPException(status_code=404, detail="Could not retreive secret")


@app.delete("/secret/invalidate/{id}")
def invalidate_secret(id: UUID4):
    try:
        return secretRepository.invalidateSecret(id)
    except NotFoundException:
        raise HTTPException(status_code=404, detail="Could not retreive secret")
