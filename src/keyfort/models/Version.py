from typing import Optional
from pydantic import BaseModel

class Version():
    """Each secret changes version to any modification."""

    def __init__(self, last_modified: str, version_number: int = 0, description: Optional[str] = ""):
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
            description=self.description
        )

class VersionDTO(BaseModel):
    version_number: int
    last_modified: str
    description: Optional[str]