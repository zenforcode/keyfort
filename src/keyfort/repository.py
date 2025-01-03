"""Data Repository Pattern"""

from typing import Tuple, Optional, NoReturn
from keyfort.models import Secret, Metadata, Version
from datetime import datetime
from dbm import open as open_db
import msgpack


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
        with open_db("secretstore.db", flag="c", mode=0o666) as db:
            secret_data_binary = db.get(secret.encode())
            if not secret_data_binary:
                return True, None
            secret_data = msgpack.unpackb(secret_data_binary, raw=False)
            return False, Secret(**secret_data)
        return True, None

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
        with open_db("secretstore.db", flag="c", mode=0o666) as db:
            db.update(secret.encode(), msgpack.packb(newSecret.model_dump()))
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
            return Secret(*secret_data).metadata
        return None

    def get_secret_meta(self, secret: str, meta: bool = True) -> Optional[Secret]:
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
            secret_data.metadata = None
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
            now = datetime.now()
            last_modified = now.strftime("%d%m%Y%H%M%S")
            version = Version(
                version_number=secret_data.version.version_number + 1,
                description=secret_data.description,
                last_modified=last_modified,
            )
            secret_data.version = version
            with open_db("secretstore.db", flag="c", mode=0o666) as db:
                db.update(old_secret.encode(), msgpack.packb(secret_data.model_dump()))
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
            return True, "Not Found"
        else:
            secret_data.metadata.is_active = True
            with open_db("secretstore.db", flag="w", mode=0o666) as db:
                db.update(secret.encode(), msgpack.packb(secret_data.model_dump()))
            return False, "OK"
