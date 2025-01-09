import unittest
from uuid import uuid4
from keyfort.models import Secret, Metadata, Version
from datetime import datetime
from keyfort.repository import InMemorySecretRepository
from keyfort.exceptions import DuplicateEntityException


SECRET_ID = "ca2f7ca0-1465-450c-acbe-51c8d165fb8f"


def create_test_secret(id=None) -> Secret:
    id = id if id is not None else SECRET_ID
    now = datetime.now()
    last_modified = now.strftime("%d%m%Y%H%M%S")
    version = Version(
        version_number=0,
        description="",
        last_modified=last_modified
    )
    metadata = Metadata(
        created_at=last_modified,
        updated_at=last_modified,
        description="",
        is_active=True,
    )
    return Secret(
        secret_id=id,
        value="test secret",
        version=version,
        metadata=metadata
    )


class RepositoryTest(unittest.TestCase):
    REPOSITORY = None

    @classmethod
    def setUpClass(cls):
        cls.REPOSITORY = InMemorySecretRepository()
        cls.REPOSITORY.IN_MEMORY_DB[SECRET_ID] = create_test_secret(SECRET_ID)

        return super().setUpClass()

    def test_successful_insert(self):
        # when
        test_secret = create_test_secret(uuid4())
        inserted = self.REPOSITORY.create(test_secret)

        # then
        assert inserted is not None

    def test_duplicated_insert(self):
        test_secret = create_test_secret(SECRET_ID)
        with self.assertRaises(DuplicateEntityException):
            self.REPOSITORY.create(test_secret)

    def test_successful_find(self):
        # when
        secret = self.REPOSITORY.find(SECRET_ID)

        # then
        # assert self.assertIsNotNone(secret) # It fails!
        assert secret is not None

    def test_unsuccessful_find(self):
        # when
        secret = self.REPOSITORY.find(uuid4())

        # then
        # assert self.assertIsNone(secret) # It fails!
        assert secret is None

    def test_successful_find_with_meta(self):
        # when
        secret = self.REPOSITORY.find(secret_id=SECRET_ID, meta=True)

        # then
        assert secret is not None
        assert secret.metadata is not None

    def test_successful_update(self):
        # when
        error, secret = self.REPOSITORY.update(SECRET_ID, "updated")
        found = self.REPOSITORY.find(SECRET_ID)

        # then
        assert not error
        assert secret == "OK"
        assert found.value == "updated"

    def test_successful_delete(self):
        # given
        uuid = uuid4()
        test_secret = create_test_secret(uuid)
        self.REPOSITORY.create(test_secret)

        # when
        error, secret = self.REPOSITORY.delete(uuid)
        found = self.REPOSITORY.find(uuid)

        # then
        assert not error
        assert secret == "OK"
        assert not found.metadata.is_active

    def test_unsuccessful_delete(self):
        # when
        error, secret = self.REPOSITORY.delete(uuid4())

        # then
        assert error
        assert secret == "Not Found"


if __name__ == '__main__':
    unittest.main()
