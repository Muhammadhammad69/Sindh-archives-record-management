"""
Authentication utilities for the application.

This module provides functions for user authentication and authorization
including token generation and validation.
"""
import jwt
import bcrypt
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from src.config.settings import get_settings
from src.utils.logging import get_app_logger
from src.dao.user_dao import UserDAO
from src.database.models.user import User


class AuthenticationManager:
    """
    Authentication manager for handling user authentication and authorization.
    """

    def __init__(self):
        """Initialize the authentication manager."""
        self.settings = get_settings()
        self.logger = get_app_logger()
        self.user_dao = UserDAO()

    def generate_token(self, user_id: int, user_email: str, user_role: str) -> str:
        """
        Generate a JWT token for the authenticated user.

        Args:
            user_id: ID of the authenticated user
            user_email: Email of the authenticated user
            user_role: Role of the authenticated user

        Returns:
            JWT token as a string
        """
        try:
            payload = {
                'user_id': user_id,
                'email': user_email,
                'role': user_role,
                'exp': datetime.utcnow() + timedelta(hours=self.settings.jwt_expiration_hours),
                'iat': datetime.utcnow()
            }

            token = jwt.encode(payload, self.settings.jwt_secret, algorithm=self.settings.jwt_algorithm)
            self.logger.info(f"JWT token generated for user {user_id}", {
                'user_id': user_id,
                'email': user_email,
                'role': user_role,
                'component': 'authentication'
            })
            return token
        except Exception as e:
            self.logger.error(f"Error generating JWT token: {e}", {
                'user_id': user_id,
                'error': str(e),
                'component': 'authentication'
            })
            raise

    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Verify a JWT token and return the payload if valid.

        Args:
            token: JWT token to verify

        Returns:
            Token payload if valid, None if invalid
        """
        try:
            payload = jwt.decode(token, self.settings.jwt_secret, algorithms=[self.settings.jwt_algorithm])
            self.logger.debug(f"JWT token verified for user {payload.get('user_id')}", {
                'user_id': payload.get('user_id'),
                'email': payload.get('email'),
                'component': 'authentication'
            })
            return payload
        except jwt.ExpiredSignatureError:
            self.logger.warning("JWT token has expired", {
                'component': 'authentication'
            })
            return None
        except jwt.InvalidTokenError as e:
            self.logger.warning(f"Invalid JWT token: {e}", {
                'error': str(e),
                'component': 'authentication'
            })
            return None

    def authenticate_user(self, email: str, password: str) -> Optional[Dict[str, Any]]:
        """
        Authenticate a user with email and password.

        Args:
            email: User's email address
            password: User's plain text password

        Returns:
            Dictionary with user info and token if authentication successful, None otherwise
        """
        try:
            # Find user by email
            user = self.user_dao.get_by_email(email)
            if not user:
                self.logger.warning(f"Authentication failed: user not found for email {email}", {
                    'email': email,
                    'component': 'authentication'
                })
                return None

            # Verify password
            if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                self.logger.warning(f"Authentication failed: invalid password for user {user.id}", {
                    'user_id': user.id,
                    'email': email,
                    'component': 'authentication'
                })
                return None

            # Generate token
            token = self.generate_token(user.id, user.email, user.role)

            self.logger.info(f"User authenticated successfully: {user.id}", {
                'user_id': user.id,
                'email': user.email,
                'role': user.role,
                'component': 'authentication'
            })

            return {
                'user_id': user.id,
                'email': user.email,
                'role': user.role,
                'token': token
            }
        except Exception as e:
            self.logger.error(f"Error during user authentication: {e}", {
                'email': email,
                'error': str(e),
                'component': 'authentication'
            })
            return None

    def authorize_user(self, token: str, required_role: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Authorize a user based on their token and optional role requirement.

        Args:
            token: JWT token to validate
            required_role: Optional role that the user must have

        Returns:
            User info dictionary if authorized, None otherwise
        """
        try:
            payload = self.verify_token(token)
            if not payload:
                return None

            # Check role if required
            if required_role and payload.get('role') != required_role:
                self.logger.warning(f"Authorization failed: insufficient role for user {payload.get('user_id')}", {
                    'user_id': payload.get('user_id'),
                    'required_role': required_role,
                    'user_role': payload.get('role'),
                    'component': 'authorization'
                })
                return None

            return payload
        except Exception as e:
            self.logger.error(f"Error during user authorization: {e}", {
                'error': str(e),
                'component': 'authorization'
            })
            return None

    def refresh_token(self, token: str) -> Optional[str]:
        """
        Refresh an existing token (generate a new one with extended expiration).

        Args:
            token: Existing JWT token

        Returns:
            New JWT token if refresh successful, None otherwise
        """
        try:
            payload = self.verify_token(token)
            if not payload:
                return None

            # Generate new token with extended expiration
            new_payload = {
                'user_id': payload['user_id'],
                'email': payload['email'],
                'role': payload['role'],
                'exp': datetime.utcnow() + timedelta(hours=self.settings.jwt_expiration_hours),
                'iat': datetime.utcnow()
            }

            new_token = jwt.encode(new_payload, self.settings.jwt_secret, algorithm=self.settings.jwt_algorithm)
            self.logger.info(f"Token refreshed for user {payload['user_id']}", {
                'user_id': payload['user_id'],
                'component': 'authentication'
            })
            return new_token
        except Exception as e:
            self.logger.error(f"Error refreshing token: {e}", {
                'error': str(e),
                'component': 'authentication'
            })
            return None


class PasswordManager:
    """
    Password management utilities for user password operations.
    """

    def __init__(self):
        """Initialize the password manager."""
        self.logger = get_app_logger()

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verify a plain text password against a hashed password.

        Args:
            plain_password: Plain text password to verify
            hashed_password: Previously hashed password to compare against

        Returns:
            True if the password matches the hash, False otherwise
        """
        try:
            return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
        except Exception as e:
            self.logger.error(f"Error verifying password: {e}", {
                'error': str(e),
                'component': 'password_verification'
            })
            return False

    def hash_password(self, password: str) -> str:
        """
        Hash a password using bcrypt.

        Args:
            password: Plain text password to hash

        Returns:
            Hashed password as a string
        """
        try:
            salt = bcrypt.gensalt(rounds=get_settings().bcrypt_rounds)
            hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
            return hashed.decode('utf-8')
        except Exception as e:
            self.logger.error(f"Error hashing password: {e}", {
                'error': str(e),
                'component': 'password_hashing'
            })
            raise

    def is_password_compromised(self, password: str) -> bool:
        """
        Check if a password is compromised (basic check - should integrate with a service in production).

        Args:
            password: Password to check

        Returns:
            True if the password is likely compromised, False otherwise
        """
        # Basic checks - in production, integrate with a service like Have I Been Pwned
        common_passwords = ['password', '123456', 'qwerty', 'admin', 'letmein']
        return password.lower() in common_passwords or len(password) < 8


# Global authentication manager instance
_auth_manager: Optional[AuthenticationManager] = None


def get_auth_manager() -> AuthenticationManager:
    """
    Get the global authentication manager instance.

    Returns:
        AuthenticationManager instance
    """
    global _auth_manager
    if _auth_manager is None:
        _auth_manager = AuthenticationManager()
    return _auth_manager


def authenticate_user(email: str, password: str) -> Optional[Dict[str, Any]]:
    """
    Authenticate a user with email and password using the global authentication manager.

    Args:
        email: User's email address
        password: User's plain text password

    Returns:
        Dictionary with user info and token if authentication successful, None otherwise
    """
    auth_manager = get_auth_manager()
    return auth_manager.authenticate_user(email, password)


def verify_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Verify a JWT token using the global authentication manager.

    Args:
        token: JWT token to verify

    Returns:
        Token payload if valid, None if invalid
    """
    auth_manager = get_auth_manager()
    return auth_manager.verify_token(token)


def authorize_user(token: str, required_role: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """
    Authorize a user based on their token using the global authentication manager.

    Args:
        token: JWT token to validate
        required_role: Optional role that the user must have

    Returns:
        User info dictionary if authorized, None otherwise
    """
    auth_manager = get_auth_manager()
    return auth_manager.authorize_user(token, required_role)


def generate_token(user_id: int, user_email: str, user_role: str) -> str:
    """
    Generate a JWT token for the authenticated user using the global authentication manager.

    Args:
        user_id: ID of the authenticated user
        user_email: Email of the authenticated user
        user_role: Role of the authenticated user

    Returns:
        JWT token as a string
    """
    auth_manager = get_auth_manager()
    return auth_manager.generate_token(user_id, user_email, user_role)


def refresh_token(token: str) -> Optional[str]:
    """
    Refresh an existing token using the global authentication manager.

    Args:
        token: Existing JWT token

    Returns:
        New JWT token if refresh successful, None otherwise
    """
    auth_manager = get_auth_manager()
    return auth_manager.refresh_token(token)


def verify_password_strength(password: str) -> tuple[bool, list[str]]:
    """
    Verify the strength of a password.

    Args:
        password: Password to check

    Returns:
        Tuple of (is_strong, list_of_issues)
    """
    issues = []

    if len(password) < 8:
        issues.append("Password must be at least 8 characters long")

    if not any(c.isupper() for c in password):
        issues.append("Password must contain at least one uppercase letter")

    if not any(c.islower() for c in password):
        issues.append("Password must contain at least one lowercase letter")

    if not any(c.isdigit() for c in password):
        issues.append("Password must contain at least one digit")

    if not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
        issues.append("Password should contain at least one special character")

    # Check if password is compromised
    password_manager = PasswordManager()
    if password_manager.is_password_compromised(password):
        issues.append("Password is too common and may be compromised")

    return len(issues) == 0, issues