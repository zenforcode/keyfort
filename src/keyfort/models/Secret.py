from typing import Optional
from pydantic import BaseModel

from .Metadata import Metadata, MetadataDTO
from .Version import Version, VersionDTO

class Secret():
    """Model that contains the secret."""

    def __init__(self, secret_id: str, value: str, version: Version, 
                 description: Optional[str] = "", metadata: Optional[Metadata] = None):
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
            metadata=self.metadata.get_dto()
        )

class SecretDTO(BaseModel):
    secret_id: str
    value: str
    version: VersionDTO
    description: str
    metadata: Optional[MetadataDTO]
