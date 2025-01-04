from typing import Optional
from pydantic import BaseModel, Field

from .Metadata import MetadataDTO


class CreateSecretPayload(BaseModel):
    secret: str = Field(min_length=1, max_length=3000)
    metadata: Optional[MetadataDTO] = None


class UpdateSecretPayload(BaseModel):
    secret: str
