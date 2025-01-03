import pytest
from unittest.mock import MagicMock, patch
from keyfort.models import Secret, Metadata, Version
from datetime import datetime
import msgpack
from keyfort.repository import SecretRepository

class FakeDB:
    def __init__(self, data_dict: dict):
        self._storage = data_dict
    def get(self, key):
        return self._storage.get(key)
    def update(self, key, value):
        self._storage[key] = value
    def close(self):
        pass
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

@pytest.fixture
def secret_repo():
    return SecretRepository()


@pytest.fixture
def test_secret():
    metadata = Metadata(created_at=str(datetime.now()), is_active=True)
    return Secret(
        name="test_secret",
        value="test_value",
        version=Version(
            version_number=0,
            description="",
            last_modified=str(datetime.now())
        ),
        metadata=metadata
    )
@pytest.fixture
def test_fake_db(test_secret):
    return FakeDB({'test_secret'.encode(): msgpack.packb(test_secret.model_dump())})
@patch('keyfort.repository.open_db')
def test_get_secret_success(mock_db, secret_repo, test_secret, test_fake_db):
    mock_db.return_value = test_fake_db
    result, secret = secret_repo.get_secret(test_secret.name)
    assert result is True
    assert secret['name'] == test_secret.name

@patch('keyfort.repository.open_db')
def test_get_secret_not_found(mock_db, secret_repo, test_fake_db):
    # Mock the database
    mock_db.return_value = test_fake_db
    result, secret = secret_repo.get_secret("nonexistent_secret")
    assert result is False
    assert secret is None

@patch('keyfort.repository.open_db')
def test_insert_secret(mock_db, secret_repo, test_secret, test_fake_db):
    mock_db.return_value = test_fake_db
    result = secret_repo.insert_secret(
        test_secret.name,
        test_secret.value,
        test_secret.metadata
    )
    item = secret_repo.get_secret(test_secret.name)
    assert result == item[1]['name']
    assert result == test_secret.name

@patch('keyfort.repository.open_db')
def test_get_secret_meta(mock_db, secret_repo, test_secret, test_fake_db):
    mock_db.return_value = test_fake_db
    metadata = secret_repo.get_secret_meta(test_secret.name)
    assert metadata.is_active is True
"""
@patch('keyfort.repository.open_db')
def test_update_secret(mock_db, secret_repo, test_secret):
    # Mock the database
    mock_db.get.return_value = msgpack.packb(test_secret.model_dump())
    mock_db.put = MagicMock()

    updated_secret = test_secret.copy()
    updated_secret.value = "updated_value"

    success, message = secret_repo.update_secret(test_secret.name, updated_secret)

    assert success is False
    assert message == "OK"
    mock_db.put.assert_called_once()

@patch('keyfort_repository.open_db')
def test_invalidate_secret(mock_db, secret_repo, test_secret):
    mock_db.get.return_value = msgpack.packb(test_secret.model_dump())
    mock_db.put = MagicMock()

    success, message = secret_repo.invalidate_secret(test_secret.name)

    assert success is True
    assert message == "OK"
    mock_db.put.assert_called_once()

@patch('keyfort.repository.open_db')
def test_invalidate_secret_not_found(mock_db, secret_repo):
    mock_db.get.return_value = None

    success, message = secret_repo.invalidate_secret("nonexistent_secret")

    assert success is False
    assert message == "Not Found"
    mock_db.get.assert_called_with("nonexistent_secret".encode())
"""
