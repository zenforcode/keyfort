"""Data Repository Pattern"""

from typing import Tuple, Optional, NoReturn
from models import Secret, Metadata, Version
from copy import deepcopy
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

    def get_secret_info(self, secret_id: str) -> Optional[Metadata]:
        """Get secret metadata

        Args:
            secret_id (str): Secret identifier

        Returns:
            Optional[Metadata]: Secret matadata.
        """
        secret = self.get_secret_meta(secret_id=secret_id)
        if secret:
            return secret.metadata
        return None

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

    def update_secret_by_id(
        self, old_secret_id: str, secret: Secret
    ) -> Tuple[bool, str]:
        """Update secret with a new one

        Args:
            old_secret (Secret): Old secret to update
            secret (Secret): New secret to update

        Returns:
            bool: False in case of error.
        """
        error, secret_id = self.get_secret(old_secret_id)
        if error:
            return True, "Not Found"
        else:
            secret.version = secret.version + 1
            IN_MEMORY_DB[secret_id] = secret
        return False, "OK"

    def invalidate_secret(self, secret_id: str) -> Tuple[bool, str]:
        """Invalidate the secret

        Args:
            secret_id (str): Secret identifier

        Returns:
            bool: True when the operation has success.
        """
        err, secret = self.get_secret(secret_id)
        if err:
            return False, "Not Found"
        else:
            secret.metadata.is_active = True
            IN_MEMORY_DB[secret_id] = secret
            return True, "OK"
