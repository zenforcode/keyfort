from typing import Type, Optional, Tuple
from copy import deepcopy

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, UUID4

from keyfort.models import Secret, Version, Metadata
from keyfort.repository import SecretRepository

app = FastAPI()


class NotCreatedException(Exception):
    def __init__(self):
        super().__init__("Error creating secret")


# TODO: is there anyway to inject?
secretRepository = SecretRepository()

class CreateSecretResponse(BaseModel):
    secret: Secret


class CreateSecretPayload(BaseModel):
    secret: str = Field(min_length=1, max_length=3000)


@app.post("/secret")
def create_secret(payload: CreateSecretPayload):
    try:
        if secretRepository.exists(payload.secret):
            raise HTTPException(status_code=400, detail="The secret exists")
        else:
            inserted_secret = secretRepository.insert_secret(secret_id=payload.secret.secret_id, value=payload.secret.value, metadata=payload.secret.metadata)
            if not inserted_secret:
                raise HTTPException(status_code=400, detail="Insertion failed")
    except NotCreatedException:
        raise HTTPException(status_code=404, detail="Could not create secret")


@app.get("/secret/{id}")
def get_secret(id: UUID4, meta: bool = False):
    try:
        return secretRepository.getSecret(id, meta)
    except NotFoundException:
        raise HTTPException(status_code=404, detail="Could not retreive secret")


@app.get("/secret/{id}/info")
def get_secret_info(id: UUID4):
    try:
        return secretRepository.getSecretInfo(id)
    except NotFoundException:
        raise HTTPException(
            status_code=404, detail="Could not retreive metadata for secret"
        )


class UpdateSecretPayload(BaseModel):
    secret: str


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
