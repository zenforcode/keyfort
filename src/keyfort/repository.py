"""Data Repository Pattern"""

import abc
from typing import Tuple, Dict, Optional, NoReturn
from copy import deepcopy

from keyfort.exceptions import NotCreatedException, DuplicateEntityException

from keyfort.models import Secret, Metadata


class SecretRepository(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def create(self, Secret: Secret) -> Tuple[bool, Optional[Secret]]:
        """Insert a secret

        Args:
            value (str): Value of the secret
            metadata (Optional[Metadata]): Metadata associated to the secret

        Raises:
            NotCreatedException: In case the DB later doesn't work with the secret.

        Returns:
            Secret: Secret inserted to the DB
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def find(self, secret_id: str, meta: bool = False) -> Optional[Secret]:
        """Get a secret.

        Args:
            secret_id (str): Secret identifier
            meta (bool): Should DB return metadata field

        Returns:
            Optional[Secret]: Secret found in DB or None
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def update(self, new_secret: Secret) -> Tuple[bool, str]:
        """Update secret with a new one

        Args:
            new_secret (Secret): Secret with updated values

        Returns:
            Tuple[bool, Optional[Secret]]: Tuple that indicates whether there is an error or not.
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def delete(self, secret_id: str) -> Tuple[bool, str]:
        """Invalidate the secret

        Args:
            secret_id (str): Secret identifier

        Returns:
            Tuple[bool, Optional[str]: Tuple that indicates whether there is an error or not.
        """
        raise NotImplementedError()


class InMemorySecretRepository(SecretRepository):
    """In memory Secret repository"""

    def __init__(self):
        super().__init__()
        self.IN_MEMORY_DB: Dict[str, Secret] = dict()

    def create(self, secret: Secret) -> Secret | NoReturn:
        duplicate = self.IN_MEMORY_DB.get(secret.secret_id)
        if duplicate:
            raise DuplicateEntityException("Secred with provided ID already exist!")

        self.IN_MEMORY_DB[secret.secret_id] = secret
        inserted = self.find(secret.secret_id)
        if not inserted:
            raise NotCreatedException()

        return deepcopy(secret)

    def find(self, secret_id: str, meta: bool = True) -> Optional[Secret]:
        secret = self.IN_MEMORY_DB.get(secret_id)
        if not secret:
            return None

        secret = deepcopy(secret)
        if not meta:
            secret.metadata = None

        return secret

    def update(self, secret_id: str, new_secret: str) -> Tuple[bool, str]:
        secret = self.find(secret_id)
        if not secret:
            return True, "Not Found"
        else:
            secret.value = new_secret
            secret.version.version_number += 1
            self.IN_MEMORY_DB[secret_id] = secret
        return False, "OK"

    def delete(self, secret_id: str) -> Tuple[bool, str]:
        secret = self.find(secret_id)
        if not secret:
            return True, "Not Found"
        else:
            secret.metadata.is_active = False
            self.IN_MEMORY_DB[secret_id] = secret
            return False, "OK"


# Example of another implementation
class SQLSecretRepository(SecretRepository):
    """SQL Secret repository"""

    def __init__(self):
        super().__init__()

    def find(self, secret_id: str) -> Tuple[bool, Optional[Secret]]:
        pass

    def create(self, value: str, metadata: Optional[Metadata]) -> Secret | NoReturn:
        pass

    def get_secret_info(self, secret_id: str) -> Optional[Metadata]:
        pass

    def get_secret_meta(self, secret_id: str, meta: bool = False) -> Optional[Secret]:
        pass

    def update_secret_by_id(
        self, old_secret_id: str, secret: Secret
    ) -> Tuple[bool, str]:
        pass

    def invalidate_secret(self, secret_id: str) -> Tuple[bool, str]:
        pass
