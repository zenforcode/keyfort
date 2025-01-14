from typing import Optional
from pydantic import BaseModel, Field


class Metadata:
    """Data model that implements the metadata for a secret."""

    def __init__(
        self,
        created_at: str,
        updated_at: str,
        is_active: bool,
        description: Optional[str] = "",
    ):
        self.created_at = created_at
        self.updated_at = updated_at
        self.is_active = is_active
        self.description = description

    def __str__(self):
        return "metadata = created_at: {}, is_active: {}".format(
            self.created_at, self.is_active
        )

    def get_dto(self):
        return MetadataDTO(
            created_at=self.created_at,
            updated_at=self.updated_at,
            is_active=self.is_active,
            description=self.description,
        )


class MetadataDTO(BaseModel):
    created_at: str
    updated_at: str
    is_active: bool
    description: Optional[str] = ""


class Version:
    """Each secret changes version to any modification."""

    def __init__(
        self,
        last_modified: str,
        version_number: int = 0,
        description: Optional[str] = "",
    ):
        self.version_number = version_number
        self.last_modified = last_modified
        self.description = description

    def __add__(self, number: int):
        """Operator overriding"""
        if not isinstance(number, int):
            raise ValueError("Invalid operator type")
        self.version_number = self.version_number + number

    def get_dto(self):
        return VersionDTO(
            version_number=self.version_number,
            last_modified=self.last_modified,
            description=self.description,
        )


class VersionDTO(BaseModel):
    version_number: int
    last_modified: str
    description: Optional[str]


class Secret:
    """Model that contains the secret."""

    def __init__(
        self,
        secret_id: str,
        value: str,
        version: Version,
        description: Optional[str] = "",
        metadata: Optional[Metadata] = None,
    ):
        self.secret_id = secret_id
        self.value = value
        self.version = version
        self.description = description
        self.metadata = metadata

    def __str__(self):
        return "secret = id: {}, value: {}".format(self.secret_id, self.value)

    def get_dto(self):
        return SecretDTO(
            secret_id=self.secret_id,
            value=self.value,
            version=self.version.get_dto(),
            description=self.description,
            metadata=(self.metadata.get_dto() if self.metadata else None),
        )


class SecretDTO(BaseModel):
    secret_id: str
    value: str
    version: VersionDTO
    description: str
    metadata: Optional[MetadataDTO] = None


class CreateSecretPayload(BaseModel):
    secret: str = Field(min_length=1, max_length=3000)
    metadata: Optional[MetadataDTO] = None


class UpdateSecretPayload(BaseModel):
    secret: str
