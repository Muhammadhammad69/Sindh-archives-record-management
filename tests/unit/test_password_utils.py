"""
Unit tests for password utilities.
"""
import pytest
from src.security.password_utils import hash_password, verify_password, validate_password_strength, hash_password_with_validation


def test_hash_password():
    """Test that password hashing works correctly."""
    password = "SecurePassword123!"
    hashed = hash_password(password)

    # Verify the hash is not the same as the original password
    assert hashed != password
    # Verify the hash is a string
    assert isinstance(hashed, str)
    # Verify the hash is reasonably long (bcrypt hashes are typically 60 characters)
    assert len(hashed) > 50


def test_verify_password_correct():
    """Test that password verification works with correct password."""
    password = "SecurePassword123!"
    hashed = hash_password(password)

    assert verify_password(password, hashed) is True


def test_verify_password_incorrect():
    """Test that password verification fails with incorrect password."""
    password = "SecurePassword123!"
    wrong_password = "WrongPassword456@"
    hashed = hash_password(password)

    assert verify_password(wrong_password, hashed) is False


def test_verify_password_empty():
    """Test that password verification fails with empty inputs."""
    assert verify_password("", "") is False
    assert verify_password("password", "") is False
    assert verify_password("", "hashed") is False


def test_validate_password_strength_valid():
    """Test that valid passwords pass strength validation."""
    valid_passwords = [
        "SecurePassword123!",
        "AnotherValidP@ss9",
        "MyStrongP4ssword#",
    ]

    for password in valid_passwords:
        is_valid, errors = validate_password_strength(password)
        assert is_valid is True
        assert len(errors) == 0


def test_validate_password_strength_invalid():
    """Test that invalid passwords fail strength validation."""
    # Test short password
    is_valid, errors = validate_password_strength("weak")
    assert is_valid is False
    assert "at least 8 characters long" in errors[0]

    # Test password without uppercase
    is_valid, errors = validate_password_strength("alllowercase123!")
    assert is_valid is False
    assert "at least one uppercase letter" in errors[0]

    # Test password without lowercase
    is_valid, errors = validate_password_strength("ALLUPPERCASE123!")
    assert is_valid is False
    assert "at least one lowercase letter" in errors[0]

    # Test password without digit
    is_valid, errors = validate_password_strength("NoDigitsHere!")
    assert is_valid is False
    assert "at least one digit" in errors[0]

    # Test password without special character
    is_valid, errors = validate_password_strength("NoSpecialChar123")
    assert is_valid is False
    assert "at least one special character" in errors[0]


def test_hash_password_with_validation():
    """Test that password hashing with validation works for valid passwords."""
    valid_password = "SecurePassword123!"
    hashed = hash_password_with_validation(valid_password)

    assert hashed != valid_password
    assert isinstance(hashed, str)
    assert verify_password(valid_password, hashed) is True


def test_hash_password_with_validation_invalid():
    """Test that password hashing with validation fails for invalid passwords."""
    invalid_password = "weak"

    with pytest.raises(ValueError):
        hash_password_with_validation(invalid_password)


def test_hash_empty_password():
    """Test that hashing an empty password raises an error."""
    with pytest.raises(ValueError):
        hash_password("")


def test_hash_none_password():
    """Test that hashing a None password raises an error."""
    with pytest.raises(ValueError):
        hash_password(None)