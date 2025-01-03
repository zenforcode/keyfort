"""Data Repository Pattern"""

from typing import Tuple, Optional, NoReturn
from keyfort.models import Secret, Metadata, Version
from copy import deepcopy
from datetime import datetime

IN_MEMORY_DB = dict()


class NotCreatedException(Exception):
    def __init__(self):
        super().__init__("Error creating secret")


class SecretRepository:
    """Secret repository"""

    def get_secret(self, secret: str) -> Tuple[bool, Optional[Secret]]:
        """Get a secret.

        Args:
            secret (str): Secret name

        Returns:
            Tuple[bool, Optional[Secret]]: Tuple that indicates whether there is an error or not.
        """
        secret_data = IN_MEMORY_DB.get(secret)
        print(IN_MEMORY_DB)
        if not secret_data:
            return False, None
        return True, deepcopy(secret_data)

    def insert_secret(
        self, secret: str, value: str, metadata: Optional[Metadata]
    ) -> Secret | NoReturn:
        """Insert a secret

        Args:
            secret (str): Secret Name
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
        newSecret = Secret(name=secret, value=value, version=version, metadata=metadata)
        IN_MEMORY_DB[secret] = newSecret
        return secret

    def get_secret_info(self, secret: str) -> Optional[Metadata]:
        """Get secret metadata

        Args:
            secret (str): Secret identifier

        Returns:
            Optional[Metadata]: Secret matadata.
        """
        secret_data = self.get_secret_meta(secret=secret)
        if secret_data:
            return secret_data.metadata
        return None

    def get_secret_meta(self, secret: str, meta: bool = False) -> Optional[Secret]:
        """Get secret with or without metadata

        Args:
            secret_id (str): Identifier of the sectret
            meta (bool, optional): Metadata of the secret. Defaults to False.

        Returns:
            Optional[Secret]: A secret value.
        """

        error, secret_data = self.get_secret(secret)
        if error:
            return None
        if not meta:
            secret_data.meta = None
        return secret_data

    def update_secret(self, old_secret: str, secret_data: Secret) -> Tuple[bool, str]:
        """Update secret with a new one

        Args:
            old_secret (Secret): Old secret to update
            secret (Secret): New secret to update

        Returns:
            bool: False in case of error.
        """
        error, secret_data = self.get_secret(old_secret)
        if error:
            return True, "Not Found"
        else:
            secret_data.version = secret_data.version + 1
            IN_MEMORY_DB[old_secret] = secret_data
        return False, "OK"

    def invalidate_secret(self, secret: str) -> Tuple[bool, str]:
        """Invalidate the secret

        Args:
            secret (str): Secret name

        Returns:
            bool: True when the operation has success.
        """
        err, secret_data = self.get_secret(secret)
        if err:
            return False, "Not Found"
        else:
            secret_data.metadata.is_active = True
            IN_MEMORY_DB[secret] = secret_data
            return True, "OK"
