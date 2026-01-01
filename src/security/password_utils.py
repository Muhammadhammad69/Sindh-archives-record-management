"""
Password hashing utilities using bcrypt.

This module provides secure password hashing and verification functions
using the bcrypt library, following security best practices.
"""
import bcrypt
from typing import Union
from src.config.settings import get_settings
from src.utils.logging import get_app_logger


class PasswordHasher:
    """
    Secure password hashing utility using bcrypt.

    Provides methods for hashing passwords and verifying hashed passwords
    with configurable work factor for security.
    """

    def __init__(self, rounds: int = 12):
        """
        Initialize the password hasher.

        Args:
            rounds: Number of bcrypt rounds (higher = more secure but slower)
        """
        self.rounds = rounds
        self.logger = get_app_logger()

    def hash_password(self, password: str) -> str:
        """
        Hash a password using bcrypt with the configured number of rounds.

        Args:
            password: Plain text password to hash

        Returns:
            Hashed password as a string

        Raises:
            ValueError: If the password is empty or None
        """
        if not password:
            raise ValueError("Password cannot be empty or None")

        try:
            # Convert password to bytes if it's not already
            if isinstance(password, str):
                password = password.encode('utf-8')

            # Generate salt and hash the password
            salt = bcrypt.gensalt(rounds=self.rounds)
            hashed = bcrypt.hashpw(password, salt)

            # Convert bytes back to string for storage
            return hashed.decode('utf-8')
        except Exception as e:
            self.logger.error(f"Error hashing password: {e}", {
                'error': str(e),
                'component': 'password_hashing'
            })
            raise

    def verify_password(self, password: str, hashed: str) -> bool:
        """
        Verify a password against its hash.

        Args:
            password: Plain text password to verify
            hashed: Previously hashed password to compare against

        Returns:
            True if the password matches the hash, False otherwise
        """
        if not password or not hashed:
            return False

        try:
            # Convert inputs to bytes if they're strings
            if isinstance(password, str):
                password = password.encode('utf-8')
            if isinstance(hashed, str):
                hashed = hashed.encode('utf-8')

            # Verify the password
            return bcrypt.checkpw(password, hashed)
        except Exception as e:
            self.logger.error(f"Error verifying password: {e}", {
                'error': str(e),
                'component': 'password_verification'
            })
            return False

    def needs_rehash(self, hashed: str, new_rounds: int = None) -> bool:
        """
        Check if a hashed password needs to be rehashed with new parameters.

        Args:
            hashed: Previously hashed password
            new_rounds: New number of rounds to check against (defaults to current)

        Returns:
            True if the password should be rehashed, False otherwise
        """
        if not hashed:
            return False

        if new_rounds is None:
            new_rounds = self.rounds

        try:
            # Convert to bytes if needed
            if isinstance(hashed, str):
                hashed = hashed.encode('utf-8')

            # Check if the hash was created with different parameters
            return bcrypt.check_needs_rehash(hashed, new_rounds)
        except Exception as e:
            self.logger.error(f"Error checking if password needs rehash: {e}", {
                'error': str(e),
                'component': 'password_rehash_check'
            })
            return False


# Global password hasher instance
_password_hasher: Union[PasswordHasher, None] = None


def get_password_hasher() -> PasswordHasher:
    """
    Get the global password hasher instance.

    Returns:
        PasswordHasher instance with configured settings
    """
    global _password_hasher
    if _password_hasher is None:
        settings = get_settings()
        _password_hasher = PasswordHasher(settings.bcrypt_rounds)
    return _password_hasher


def hash_password(password: str) -> str:
    """
    Hash a password using the global password hasher.

    Args:
        password: Plain text password to hash

    Returns:
        Hashed password as a string
    """
    hasher = get_password_hasher()
    return hasher.hash_password(password)


def verify_password(password: str, hashed: str) -> bool:
    """
    Verify a password against its hash using the global password hasher.

    Args:
        password: Plain text password to verify
        hashed: Previously hashed password to compare against

    Returns:
        True if the password matches the hash, False otherwise
    """
    hasher = get_password_hasher()
    return hasher.verify_password(password, hashed)


def needs_rehash(hashed: str) -> bool:
    """
    Check if a hashed password needs to be rehashed with current parameters.

    Args:
        hashed: Previously hashed password

    Returns:
        True if the password should be rehashed, False otherwise
    """
    hasher = get_password_hasher()
    return hasher.needs_rehash(hashed)


def validate_password_strength(password: str) -> tuple[bool, list[str]]:
    """
    Validate password strength according to security requirements.

    Args:
        password: Password to validate

    Returns:
        Tuple of (is_valid, list_of_error_messages)
    """
    errors = []

    if len(password) < 8:
        errors.append("Password must be at least 8 characters long")

    if not any(c.isupper() for c in password):
        errors.append("Password must contain at least one uppercase letter")

    if not any(c.islower() for c in password):
        errors.append("Password must contain at least one lowercase letter")

    if not any(c.isdigit() for c in password):
        errors.append("Password must contain at least one digit")

    if not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
        errors.append("Password must contain at least one special character")

    return len(errors) == 0, errors


def hash_password_with_validation(password: str) -> str:
    """
    Hash a password after validating its strength.

    Args:
        password: Plain text password to hash

    Returns:
        Hashed password as a string

    Raises:
        ValueError: If the password doesn't meet strength requirements
    """
    is_valid, errors = validate_password_strength(password)
    if not is_valid:
        raise ValueError(f"Password does not meet strength requirements: {'; '.join(errors)}")

    return hash_password(password)


def generate_salt(rounds: int = None) -> bytes:
    """
    Generate a random salt for password hashing.

    Args:
        rounds: Number of bcrypt rounds (defaults to configured value)

    Returns:
        Randomly generated salt as bytes
    """
    if rounds is None:
        settings = get_settings()
        rounds = settings.bcrypt_rounds

    return bcrypt.gensalt(rounds=rounds)


# Convenience functions for common use cases
def create_user_password_hash(plain_password: str) -> str:
    """
    Create a password hash for a new user account.

    Args:
        plain_password: Plain text password from the user

    Returns:
        Securely hashed password
    """
    return hash_password_with_validation(plain_password)


def check_user_password(plain_password: str, stored_hash: str) -> bool:
    """
    Check if a user's entered password matches the stored hash.

    Args:
        plain_password: Password entered by the user
        stored_hash: Previously stored password hash

    Returns:
        True if the passwords match, False otherwise
    """
    return verify_password(plain_password, stored_hash)