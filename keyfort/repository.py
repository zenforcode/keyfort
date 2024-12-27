from typing import Tuple, Optional, NoReturn
from models import Secret, Metadata, Version
from copy import deepcopy
from uuid import uuid4
from time import strftime
from datetime import datetime

IN_MEMORY_DB = dict()


class NotCreatedException(Exception):
    def __init__(self):
        super().__init__("Error creating secret")


class SecretRepository:
    """Secret repository"""

    def get_secret(self, secret_id: str) -> Tuple[bool, Optional[Secret]]:
        """Get a secret.

        Args:
            secret_id (str): Identifier of the secret

        Returns:
            Tuple[bool, Optional[Secret]]: Tuple that indicates whether there is an error or not.
        """
        secret = IN_MEMORY_DB.get(secret_id)
        if not secret:
            return False, None
        return True, deepcopy(secret)

    def insert_secret(
        self, secret_id: str, value: str, metadata: Optional[Metadata]
    ) -> Secret | NoReturn:
        """Insert a secret

        Args:
            secret_id (str): Secret Identifier
            value (str): Value of the secret
            metadata (Optional[Metadata]): Metadata associated to the secret

        Raises:
            NotCreatedException: In case the db later doesn't work with the secret.

        Returns:
            Secret | NoReturn: Secret Value or NotCreatedException
        """
        now = datetime.now()
        last_modified = now.strftime("%d%m%Y%H%M%S")
        version = Version(version_number=0, description="", last_modified=last_modified)
        newSecret = Secret(
            secret_id=secret_id, value=value, version=version, metadata=metadata
        )
        IN_MEMORY_DB[newSecret.id] = newSecret
        error, secret = self.get_secret(newSecret.secret_id)
        if error:
            raise NotCreatedException()
        return secret

    def get_secret_meta(self, secret_id: str, meta: bool = False) -> Optional[Secret]:
        """Get secret with or without metadata

        Args:
            secret_id (str): Identifier of the sectret
            meta (bool, optional): Metadata of the secret. Defaults to False.

        Returns:
            Optional[Secret]: A secret value.
        """

        error, secret = self.get_secret(secret_id)
        if error:
            return None
        if not meta:
            secret.meta = None
        return secret

    def updateSecret(self, old_secret: Secret, secret: Secret):
        secret_id = self.get_secret(old_secret.secret_id)
        secret.version = secret.version + 1 
        IN_MEMORY_DB[secret_id] = secret

    def invalidateSecret(self, secret_id: str) -> bool:
        err, secret = self.get_secret(secret_id)
        if err:
            return False
        else:
            secret.metadata.is_active = True
            IN_MEMORY_DB[secret_id] = secret
            return True
