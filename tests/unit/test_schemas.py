"""
Unit tests for Pydantic schema validation.
"""
import pytest
from pydantic import ValidationError
from app.schemas.base import UserCreate
from app.schemas.user import UserRead


def test_user_create_valid():
    """Test valid user creation schema"""
    data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "TestPass123"
    }
    user = UserCreate(**data)
    assert user.username == "testuser"
    assert user.email == "test@example.com"


def test_user_create_invalid_email():
    """Test that invalid email is rejected"""
    data = {
        "username": "testuser",
        "email": "invalid-email",
        "password": "TestPass123"
    }
    with pytest.raises(ValidationError):
        UserCreate(**data)


def test_user_create_short_password():
    """Test that short password is rejected"""
    data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "short"
    }
    with pytest.raises(ValidationError) as exc_info:
        UserCreate(**data)
    assert "at least 8" in str(exc_info.value).lower()


def test_user_create_no_uppercase():
    """Test password must have uppercase"""
    data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass123"
    }
    with pytest.raises(ValidationError) as exc_info:
        UserCreate(**data)
    assert "uppercase" in str(exc_info.value).lower()


def test_user_create_no_digit():
    """Test password must have digit"""
    data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "TestPassword"
    }
    with pytest.raises(ValidationError) as exc_info:
        UserCreate(**data)
    assert "digit" in str(exc_info.value).lower()
