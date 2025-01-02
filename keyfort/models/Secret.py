from uuid import uuid4

from .Metadata import Metadata


class Secret():
    def __init__(self, secret: str):
        self.id = uuid4()
        self.value = secret
        self.metadata = Metadata()

    def removeMeta(self):
        del self.metadata
        return self

    def updateSecret(self, secret: str):
        self.value = secret
        self.metadata.updateTimestamp()
        return self

    def deactivate(self):
        self.metadata.deactivate()
        return self

    def __str__(self):
        return "id:" + str(self.id) + "\nvalue:" + self.value

    def __repr__(self):
        return "id:" + str(self.id) + "\nvalue:" + self.value
