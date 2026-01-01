"""
User model for the application.

This module defines the User entity with all required fields and relationships.
"""
from typing import Optional, Dict, Any
from src.database.models.base import BaseModel, get_base_field_definitions
from src.security.password_utils import hash_password
from src.utils.validators import validate_email


class User(BaseModel):
    """
    User model representing system users with authentication credentials and role-based access.
    """

    def __init__(self, name: str = None, email: str = None, password: str = None,
                 role: str = 'user', id: Optional[int] = None):
        """
        Initialize a User instance.

        Args:
            name: User's full name
            email: User's email address
            password: User's password (will be hashed)
            role: User's access role (admin or user)
            id: Optional user ID for existing users
        """
        super().__init__()
        self.id = id
        self.name = name
        self.email = email
        self.password = password  # This will be stored as a hash
        self.role = role if role in ['admin', 'user'] else 'user'

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the user instance to a dictionary.

        Returns:
            Dictionary representation of the user
        """
        result = {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'role': self.role,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
        # Don't include the password in the dictionary for security
        return result

    def set_password(self, plain_password: str):
        """
        Set the user's password by hashing it.

        Args:
            plain_password: Plain text password to hash and store
        """
        self.password = hash_password(plain_password)

    def validate(self) -> tuple[bool, list[str]]:
        """
        Validate the user data.

        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []

        if not self.name or not self.name.strip():
            errors.append("Name is required")

        if not self.email or not self.email.strip():
            errors.append("Email is required")
        elif not validate_email(self.email)[0]:
            errors.append(f"Invalid email format: {self.email}")

        if not self.password:
            errors.append("Password is required")

        if self.role not in ['admin', 'user']:
            errors.append(f"Role must be 'admin' or 'user', got: {self.role}")

        return len(errors) == 0, errors

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'User':
        """
        Create a User instance from a dictionary.

        Args:
            data: Dictionary containing user data

        Returns:
            User instance populated with data from the dictionary
        """
        user = cls(
            id=data.get('id'),
            name=data.get('name'),
            email=data.get('email'),
            password=data.get('password'),  # Assuming this is already hashed
            role=data.get('role', 'user')
        )
        user.created_at = data.get('created_at')
        user.updated_at = data.get('updated_at')
        return user

    @staticmethod
    def get_table_schema() -> str:
        """
        Get the SQL schema definition for the users table.

        Returns:
            SQL string to create the users table
        """
        base_fields = get_base_field_definitions()
        return f"""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            role VARCHAR(20) NOT NULL CHECK (role IN ('admin', 'user')),
            {base_fields}
        );

        CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
        """

    @staticmethod
    def get_insert_query() -> str:
        """
        Get the SQL INSERT query for users.

        Returns:
            SQL INSERT query string
        """
        return """
        INSERT INTO users (name, email, password, role, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id, name, email, role, created_at, updated_at
        """

    @staticmethod
    def get_select_by_email_query() -> str:
        """
        Get the SQL SELECT query to find a user by email.

        Returns:
            SQL SELECT query string
        """
        return """
        SELECT id, name, email, password, role, created_at, updated_at
        FROM users
        WHERE email = %s
        """

    @staticmethod
    def get_update_query() -> str:
        """
        Get the SQL UPDATE query for users.

        Returns:
            SQL UPDATE query string
        """
        return """
        UPDATE users
        SET name = %s, email = %s, password = %s, role = %s, updated_at = CURRENT_TIMESTAMP
        WHERE id = %s
        """

    @staticmethod
    def get_select_all_query(limit: int = None, offset: int = 0) -> str:
        """
        Get the SQL SELECT query to retrieve all users.

        Args:
            limit: Maximum number of records to return
            offset: Number of records to skip

        Returns:
            SQL SELECT query string
        """
        query = "SELECT id, name, email, role, created_at, updated_at FROM users"
        params = []

        if limit:
            query += f" LIMIT %s OFFSET %s"
            params = [limit, offset]
        elif offset > 0:
            query += f" OFFSET %s"
            params = [offset]

        return query, params