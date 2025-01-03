from typing import Optional
from pydantic import BaseModel, Field


class Metadata(BaseModel):
    """Data model that implements the metadata for a secret."""

    created_at: str
    updated_at: str
    is_active: bool
    description: Optional[str] = ""


class Version(BaseModel):
    """Each secret changes version to any modification."""

    version_number: int = 0
    last_modified: str
    description: Optional[str] = ""

    def __add__(self, number: int):
        """Operator overriding"""
        if not isinstance(number, int):
            raise ValueError("Invalid operator type")
        self.version_number = self.version_number + number


class Secret(BaseModel):
    """Model that contains the secret."""

    secret_id: str
    value: str
    version: Version
    description: Optional[str] = ""
    metadata: Optional[Metadata] = None


class CreateSecretResponse(BaseModel):
    secret: Secret


class CreateSecretPayload(BaseModel):
    secret: str = Field(min_length=1, max_length=3000)
    value: str
    metadata: Optional[Metadata] = None


class UpdateSecretPayload(BaseModel):
    secret: Secret
    new_secret: Secret
