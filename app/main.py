from typing import Type
from copy import deepcopy

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, UUID4

from models import Secret


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


IN_MEMORY_DB = dict()


class NotFoundException(Exception):
    def __init__(self):
        super().__init__("Secret with provided ID does not exist")


class NotCreatedException(Exception):
    def __init__(self):
        super().__init__("Error creating secret")


class SecretRepository:
    def getSecretOrEexception(self, id):
        secret = IN_MEMORY_DB.get(id)
        if not secret:
            raise NotFoundException()

        return deepcopy(secret)

    def insertSecret(self, secret: str) -> Type[Secret]:
        try:
            newSecret = Secret(secret)
            IN_MEMORY_DB[newSecret.id] = newSecret

            return self.getSecretOrEexception(newSecret.id)
        except NotFoundException:
            raise NotCreatedException()

    def getSecret(self, id: UUID4, meta: bool = False):
        try:
            secret = self.getSecretOrEexception(id)
            if meta:
                return secret
            return secret.removeMeta()

        except NotFoundException as err:
            raise err

    def getSecretInfo(self, id: UUID4):
        pass

    def updateSecret(self, id: UUID4, secret: str):
        try:
            oldSecret = self.getSecretOrEexception(id)
            IN_MEMORY_DB[id] = oldSecret.updateSecret(secret)
            return self.getSecretOrEexception(id)
        except NotFoundException as err:
            raise err

    def invalidateSecret(self, id: UUID4):
        try:
            secret = self.getSecretOrEexception(id)
            secret.deactivate()
            IN_MEMORY_DB[secret.id] = secret
            return "OK"
        except NotFoundException as err:
            raise err


secretRepository = SecretRepository()


class CreateSecretResponse(BaseModel):
    id: UUID4
    secret: str


class CreateSecretPayload(BaseModel):
    secret: str = Field(min_length=1, max_length=3000)


@app.post("/secret")
def create_secret(payload: CreateSecretPayload):
    try:
        return secretRepository.insertSecret(payload.secret)
    except NotCreatedException:
        raise HTTPException(status_code=404, detail="Could not create secret")


@app.get("/secret/{id}")
def get_secret(id: UUID4, meta: bool = False):
    try:
        return secretRepository.getSecret(id, meta)
    except NotFoundException:
        raise HTTPException(
            status_code=404, detail="Could not retreive secret")


@app.get("/secret/{id}/info")
def get_secret_info(id: UUID4):
    try:
        return secretRepository.getSecretInfo(id)
    except NotFoundException:
        raise HTTPException(
            status_code=404, detail="Could not retreive metadata for secret")


class UpdateSecretPayload(BaseModel):
    secret: str


@app.put("/meta/update/{id}")
def update_secret_meta(id: UUID4, payload: UpdateSecretPayload):
    print(id)
    try:
        return secretRepository.updateSecret(id, payload.secret)
    except NotFoundException:
        raise HTTPException(
            status_code=404, detail="Could not retreive secret")


@app.delete("/secret/invalidate/{id}")
def invalidate_secret(id: UUID4):
    try:
        return secretRepository.invalidateSecret(id)
    except NotFoundException:
        raise HTTPException(
            status_code=404, detail="Could not retreive secret")
