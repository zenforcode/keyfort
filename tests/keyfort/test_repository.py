import pytest
from unittest.mock import MagicMock, patch
from keyfort.models import Secret, Metadata, Version
from datetime import datetime
import msgpack
from keyfort.repository import SecretRepository, NotCreatedException, IN_MEMORY_DB

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

@patch('keyfort.repository.IN_MEMORY_DB')
def test_get_secret_success(mock_db, secret_repo, test_secret):
    # Mock the database
    mock_db.get.return_value = msgpack.packb(test_secret.model_dump())

    result, secret = secret_repo.get_secret(test_secret.name)

    assert result is True
    assert secret['name'] == test_secret.name
    mock_db.get.assert_called_with(test_secret.name.encode())

@patch('keyfort.repository.IN_MEMORY_DB')
def test_get_secret_not_found(mock_db, secret_repo):
    # Mock the database
    mock_db.get.return_value = None

    result, secret = secret_repo.get_secret("nonexistent_secret")

    assert result is False
    assert secret is None
    mock_db.get.assert_called_with("nonexistent_secret".encode())

@patch('keyfort.repository.IN_MEMORY_DB')
def test_insert_secret(mock_db, secret_repo, test_secret):
    # Mock the database
    mock_db.put = MagicMock()

    result = secret_repo.insert_secret(
        test_secret.name,
        test_secret.value,
        test_secret.metadata
    )

    assert result == test_secret.name
    mock_db.put.assert_called_once()

@patch('keyfort.repository.IN_MEMORY_DB')
def test_get_secret_info(mock_db, secret_repo, test_secret):
    mock_db.get.return_value = msgpack.packb(test_secret.model_dump())

    metadata = secret_repo.get_secret_info(test_secret.name)

    assert metadata.is_active is True
    mock_db.get.assert_called_with(test_secret.name.encode())

@patch('keyfort.repository.IN_MEMORY_DB')
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

@patch('keyfort_repository.IN_MEMORY_DB')
def test_invalidate_secret(mock_db, secret_repo, test_secret):
    mock_db.get.return_value = msgpack.packb(test_secret.model_dump())
    mock_db.put = MagicMock()

    success, message = secret_repo.invalidate_secret(test_secret.name)

    assert success is True
    assert message == "OK"
    mock_db.put.assert_called_once()

@patch('keyfort.repository.IN_MEMORY_DB')
def test_invalidate_secret_not_found(mock_db, secret_repo):
    mock_db.get.return_value = None

    success, message = secret_repo.invalidate_secret("nonexistent_secret")

    assert success is False
    assert message == "Not Found"
    mock_db.get.assert_called_with("nonexistent_secret".encode())
