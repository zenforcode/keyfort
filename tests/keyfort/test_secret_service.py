import unittest
from uuid import uuid4
from keyfort.models import (
    SecretDTO,  MetadataDTO, CreateSecretPayload, UpdateSecretPayload
)
import keyfort.services.secret_service as SECRET_SERVICE


class RepositoryTest(unittest.TestCase):
    test_secret_service = None
    SEEDED_SECRET_ID = None

    @classmethod
    def setUpClass(cls):
        cls.test_secret_service = SECRET_SERVICE
        secret_dto = CreateSecretPayload(secret="this is my secret")
        created_secret = cls.test_secret_service.create_secret(secret_dto)
        cls.SEEDED_SECRET_ID = created_secret.secret_id

        return super().setUpClass()

    def test_create_secret_success(self):
        # when
        createSecretPayload = CreateSecretPayload(secret="test secret")
        created = self.test_secret_service.create_secret(createSecretPayload)

        # then
        assert created.secret_id is not None

    def test_get_secret_success(self):
        # when
        secret: SecretDTO = self.test_secret_service.get_secret(
            secret_id=self.SEEDED_SECRET_ID)

        # then
        assert secret.value == "this is my secret"

    def test_get_secret_info_success(self):
        # when
        secret: MetadataDTO = self.test_secret_service.get_secret_info(
            secret_id=self.SEEDED_SECRET_ID)

        # then
        assert secret is not None
        assert isinstance(secret, MetadataDTO)

    def test_update_secret_meta_success(self):
        # given
        createSecretPayload = CreateSecretPayload(secret="test secret")
        created = self.test_secret_service.create_secret(createSecretPayload)

        # when
        secret = self.test_secret_service.update_secret_meta(
            secret_id=created.secret_id,
            payload=UpdateSecretPayload(secret="updated secret")
        )

        # then
        assert secret == "OK"

    def test_update_secret_meta_failure(self):
        # when
        secret = self.test_secret_service.update_secret_meta(
            secret_id=uuid4(),
            payload=UpdateSecretPayload(secret="updated secret")
        )

        # then
        assert secret == "Not Found"

    def test_invalidate_secret_meta_success(self):
        # given
        createSecretPayload = CreateSecretPayload(secret="test secret")
        created = self.test_secret_service.create_secret(createSecretPayload)

        # when
        secret = self.test_secret_service.invalidate_secret(
            secret_id=created.secret_id
        )

        # then
        assert secret == "OK"

    def test_invalidate_secret_meta_failure(self):
        # when
        secret = self.test_secret_service.invalidate_secret(
            secret_id=uuid4()
        )

        # then
        assert secret == "Not Found"


if __name__ == '__main__':
    unittest.main()
