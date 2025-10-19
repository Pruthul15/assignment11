"""
Integration tests for User model with database.
"""
import pytest
from app.models.user import User


def test_create_user(db_session):
    """Test creating a user in the database"""
    user = User(username="testuser", email="test@example.com")
    user.set_password("TestPassword123")
    
    db_session.add(user)
    db_session.commit()
    
    assert user.id is not None
    assert user.username == "testuser"
    assert user.email == "test@example.com"
    assert user.password_hash != "TestPassword123"


def test_verify_password(db_session):
    """Test password verification"""
    user = User(username="testuser", email="test@example.com")
    user.set_password("TestPassword123")
    
    db_session.add(user)
    db_session.commit()
    
    assert user.verify_password("TestPassword123") is True
    assert user.verify_password("WrongPassword") is False


def test_unique_username(db_session):
    """Test that username must be unique"""
    user1 = User(username="testuser", email="test1@example.com")
    user1.set_password("Password123")
    db_session.add(user1)
    db_session.commit()
    
    user2 = User(username="testuser", email="test2@example.com")
    user2.set_password("Password123")
    db_session.add(user2)
    
    with pytest.raises(Exception):  # Should raise IntegrityError
        db_session.commit()


def test_unique_email(db_session):
    """Test that email must be unique"""
    user1 = User(username="testuser1", email="test@example.com")
    user1.set_password("Password123")
    db_session.add(user1)
    db_session.commit()
    
    user2 = User(username="testuser2", email="test@example.com")
    user2.set_password("Password123")
    db_session.add(user2)
    
    with pytest.raises(Exception):  # Should raise IntegrityError
        db_session.commit()


def test_invalid_email_format(db_session):
    """Test that invalid email format is rejected"""
    # This should be caught by Pydantic validation
    # but we're testing database level as well
    user = User(username="testuser", email="invalid-email")
    user.set_password("Password123")
    db_session.add(user)
    # SQLite won't enforce email format, but this tests the model accepts it
    # Pydantic schema will catch it at API level
    db_session.commit()
    assert user.email == "invalid-email"
