import pytest
from pydantic import ValidationError
from app.schemas.register import RegisterSchema


def test_valid_register_data():
    payload = {
        "name": "Giorgi",
        "last_name": "Beridze",
        "username": "Utsu",
        "email": "giorgi@example.com",
        "password": "StrongPassword123",
        "repeat_password": "StrongPassword123",
        "birthday": "1980-01-01"
    }

    user_input = RegisterSchema(**payload)

    assert user_input.name == payload["name"]
    assert user_input.email == payload["email"]


def test_invalid_email_raises_error():
    # Arrange
    bad_payload = {
        "email": "not-an-email",
        "password": "StrongPassword123!",
        "username": "Utsu"
    }

    # Act & Assert
    with pytest.raises(ValidationError) as exc_info:
        RegisterSchema(**bad_payload)

    # Optional: check that the error specifically mentions the email field
    assert "email" in str(exc_info.value)