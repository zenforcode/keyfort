from typing import Optional
from pydantic import BaseModel

class Metadata():
    """Data model that implements the metadata for a secret."""

    def __init__(self, created_at: str, updated_at: str, is_active: bool, description: Optional[str] = ""):
        self.created_at = created_at
        self.updated_at = updated_at
        self.is_active = is_active
        self.description = description

    def __str__(self):
        return "metadata = created_at: {}, is_active: {}".format(self.created_at, self.is_active)

    def get_dto(self):
        return MetadataDTO(
            created_at=self.created_at,
            updated_at=self.updated_at,
            is_active=self.is_active,
            description=self.description
        )

class MetadataDTO(BaseModel):
    created_at: str
    updated_at: str
    is_active: bool
    description: Optional[str] = ""