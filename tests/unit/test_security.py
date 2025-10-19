"""
Unit tests for password hashing functions.
"""
import pytest
from app.utils.security import hash_password, verify_password


def test_hash_password():
    """Test that password hashing works"""
    password = "TestPassword123"
    hashed = hash_password(password)
    
    assert hashed != password
    assert len(hashed) > 0
    assert isinstance(hashed, str)


def test_verify_password_correct():
    """Test password verification with correct password"""
    password = "TestPassword123"
    hashed = hash_password(password)
    
    assert verify_password(password, hashed) is True


def test_verify_password_incorrect():
    """Test password verification with wrong password"""
    password = "TestPassword123"
    wrong_password = "WrongPassword456"
    hashed = hash_password(password)
    
    assert verify_password(wrong_password, hashed) is False


def test_different_passwords_different_hashes():
    """Test that same password generates different hashes (due to salt)"""
    password = "TestPassword123"
    hash1 = hash_password(password)
    hash2 = hash_password(password)
    
    assert hash1 != hash2
    assert verify_password(password, hash1) is True
    assert verify_password(password, hash2) is True
