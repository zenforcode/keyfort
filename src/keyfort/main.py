from fastapi import FastAPI, HTTPException
from fastapi_versioning import version
from keyfort.models import (
    Secret,
    CreateSecretPayload,
    UpdateSecretPayload,
)
from keyfort.repository import SecretRepository


class NotCreatedException(Exception):
    def __init__(self):
        super().__init__("Error creating secret")


app = FastAPI()

# Assuming `secretRepository` is an instance of `SecretRepository`
secretRepository = SecretRepository()


@app.post("/secret")
@version(1)
def create_secret(payload: CreateSecretPayload):
    try:
        inserted_secret: Secret = secretRepository.insert_secret(
            secret_id=payload.secret, value=payload.value, metadata=payload.metadata
        )
        if not inserted_secret:
            raise HTTPException(
                status_code=400, detail="Secret already exists or insertion failed."
            )
        return inserted_secret
    except NotCreatedException as e:
        raise HTTPException(status_code=400, detail=f"Insertion failed: {str(e)}")


@app.get("/secret/{secret_id}")
@version(1)
def get_secret(secret_id: str, meta: bool = False) -> Secret:
    try:
        secret = secretRepository.get_secret_meta(secret_id=secret_id, meta=meta)
        if not secret:
            raise HTTPException(status_code=404, detail="Secret not found.")
        return secret
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@app.get("/secret/{secret_id}/info")
@version(1)
def get_secret_info(secret_id: str) -> Secret:
    try:
        err, secret = secretRepository.get_secret(secret_id=secret_id)
        if err or not secret:
            raise HTTPException(
                status_code=404, detail="Could not retrieve metadata for secret."
            )
        return secret
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@app.put("/secret/{secret_id}/meta")
@version(1)
def update_secret_meta(secret_id: str, payload: UpdateSecretPayload) -> Secret:
    try:
        err, res = secretRepository.update_secret_by_id(secret_id, payload)
        if err:
            raise HTTPException(status_code=404, detail=res)
        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@app.delete("/secret/{secret_id}")
@version(1)
def invalidate_secret(secret_id: str):
    try:
        err, res = secretRepository.invalidate_secret(secret_id)
        if err:
            raise HTTPException(status_code=404, detail=res)
        return {"message": "Secret invalidated successfully.", "details": res}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
