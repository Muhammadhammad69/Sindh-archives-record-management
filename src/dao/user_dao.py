"""
User Data Access Object (DAO) for managing user data.

This module provides methods for performing CRUD operations on user data
with proper validation and security measures.
"""
from typing import Optional, List, Dict, Any
from src.dao.base_dao import BaseDAO
from src.database.models.user import User
from src.security.password_utils import hash_password, verify_password
from src.utils.logging import get_app_logger
from src.utils.validators import validate_email


class UserDAO(BaseDAO):
    """
    Data Access Object for managing User entities.
    """

    def __init__(self):
        """Initialize the UserDAO."""
        super().__init__('users')
        self.logger = get_app_logger()

    def validate_data(self, data: Dict[str, Any]) -> Dict[str, List[str]]:
        """
        Validate user data before saving to database.

        Args:
            data: Dictionary containing the data to validate

        Returns:
            Dictionary with field names as keys and lists of error messages as values
        """
        errors = {}

        # Validate email
        if 'email' in data:
            is_valid, error_msg = validate_email(data['email'])
            if not is_valid:
                errors['email'] = [error_msg]

        # Validate required fields
        required_fields = ['name', 'email', 'role']
        for field in required_fields:
            if field in data and (data[field] is None or (isinstance(data[field], str) and data[field].strip() == "")):
                if field not in errors:
                    errors[field] = []
                errors[field].append(f"{field} is required")

        # Validate role
        if 'role' in data and data['role'] not in ['admin', 'user']:
            if 'role' not in errors:
                errors['role'] = []
            errors['role'].append(f"Role must be 'admin' or 'user', got: {data['role']}")

        return errors

    def create(self, user_data: Dict[str, Any]) -> User:
        """
        Create a new user with proper password hashing and validation.

        Args:
            user_data: Dictionary containing user information

        Returns:
            Created User instance
        """
        # Validate input data
        validation_errors = self.validate_data(user_data)
        if validation_errors:
            error_messages = []
            for field, field_errors in validation_errors.items():
                error_messages.extend(field_errors)
            raise ValueError(f"Validation failed: {'; '.join(error_messages)}")

        # Check if user with this email already exists
        existing_user = self.get_by_email(user_data['email'])
        if existing_user:
            raise ValueError(f"User with email {user_data['email']} already exists")

        # Prepare data
        user = User.from_dict(user_data)

        # Hash the password if provided
        if user_data.get('password'):
            user.set_password(user_data['password'])

        # Prepare the data for insertion
        data_to_insert = {
            'name': user.name,
            'email': user.email,
            'password': user.password,
            'role': user.role,
        }
        data_to_insert.update(user.get_audit_fields())

        # Perform the database insert
        result = super().create(data_to_insert)

        # Create and return the User object
        created_user = User.from_dict(result)
        self.logger.info(f"User created successfully: {created_user.id}", {
            'user_id': created_user.id,
            'email': created_user.email,
            'role': created_user.role,
            'component': 'user_management'
        })

        return created_user

    def get_by_email(self, email: str) -> Optional[User]:
        """
        Retrieve a user by their email address.

        Args:
            email: Email address to search for

        Returns:
            User instance if found, None otherwise
        """
        query = "SELECT * FROM users WHERE email = %s"
        results = self._execute_query(query, (email,))

        if results:
            user_data = results[0]
            user = User.from_dict(user_data)
            self.logger.debug(f"User retrieved by email: {user.id}", {
                'user_id': user.id,
                'email': email,
                'component': 'user_management'
            })
            return user

        self.logger.debug(f"No user found with email: {email}", {
            'email': email,
            'component': 'user_management'
        })
        return None

    def get_by_id(self, user_id: int) -> Optional[User]:
        """
        Retrieve a user by their ID.

        Args:
            user_id: ID of the user to retrieve

        Returns:
            User instance if found, None otherwise
        """
        user_data = super().get_by_id(user_id)
        if user_data:
            user = User.from_dict(user_data)
            self.logger.debug(f"User retrieved by ID: {user.id}", {
                'user_id': user.id,
                'component': 'user_management'
            })
            return user

        self.logger.debug(f"No user found with ID: {user_id}", {
            'user_id': user_id,
            'component': 'user_management'
        })
        return None

    def update(self, user_id: int, user_data: Dict[str, Any]) -> bool:
        """
        Update a user's information.

        Args:
            user_id: ID of the user to update
            user_data: Dictionary containing fields to update

        Returns:
            True if the user was updated, False otherwise
        """
        # Validate input data
        validation_errors = self.validate_data(user_data)
        if validation_errors:
            error_messages = []
            for field, field_errors in validation_errors.items():
                error_messages.extend(field_errors)
            raise ValueError(f"Validation failed: {'; '.join(error_messages)}")

        # Check if email already exists for another user
        if 'email' in user_data:
            existing_user = self.get_by_email(user_data['email'])
            if existing_user and existing_user.id != user_id:
                raise ValueError(f"User with email {user_data['email']} already exists")

        # Hash password if it's being updated
        if 'password' in user_data:
            user_data['password'] = hash_password(user_data['password'])

        # Update audit fields
        user_data = self.update_audit_fields(user_data)

        # Perform the update
        success = super().update_by_id(user_id, user_data)

        if success:
            self.logger.info(f"User updated successfully: {user_id}", {
                'user_id': user_id,
                'updated_fields': list(user_data.keys()),
                'component': 'user_management'
            })

        return success

    def delete(self, user_id: int) -> bool:
        """
        Delete a user by their ID.

        Args:
            user_id: ID of the user to delete

        Returns:
            True if the user was deleted, False otherwise
        """
        success = super().delete_by_id(user_id)
        if success:
            self.logger.info(f"User deleted successfully: {user_id}", {
                'user_id': user_id,
                'component': 'user_management'
            })
        else:
            self.logger.warning(f"Attempted to delete non-existent user: {user_id}", {
                'user_id': user_id,
                'component': 'user_management'
            })

        return success

    def authenticate(self, email: str, password: str) -> Optional[User]:
        """
        Authenticate a user by email and password.

        Args:
            email: User's email address
            password: User's plain text password

        Returns:
            User instance if authentication successful, None otherwise
        """
        user = self.get_by_email(email)
        if not user:
            self.logger.warning(f"Authentication failed: user not found for email {email}", {
                'email': email,
                'component': 'authentication'
            })
            return None

        # Verify the password using the stored hash
        if verify_password(password, user.password):
            self.logger.info(f"User authenticated successfully: {user.id}", {
                'user_id': user.id,
                'email': email,
                'component': 'authentication'
            })
            return user
        else:
            self.logger.warning(f"Authentication failed: invalid password for user {user.id}", {
                'user_id': user.id,
                'email': email,
                'component': 'authentication'
            })
            return None

    def change_password(self, user_id: int, old_password: str, new_password: str) -> bool:
        """
        Change a user's password after verifying the old password.

        Args:
            user_id: ID of the user whose password to change
            old_password: User's current password
            new_password: User's new password

        Returns:
            True if the password was changed, False otherwise
        """
        user = self.get_by_id(user_id)
        if not user:
            self.logger.warning(f"Password change failed: user not found for ID {user_id}", {
                'user_id': user_id,
                'component': 'password_management'
            })
            return False

        # Verify the old password
        if not verify_password(old_password, user.password):
            self.logger.warning(f"Password change failed: invalid old password for user {user_id}", {
                'user_id': user_id,
                'component': 'password_management'
            })
            return False

        # Hash the new password
        hashed_new_password = hash_password(new_password)

        # Update the password
        success = super().update_by_id(user_id, {'password': hashed_new_password})

        if success:
            self.logger.info(f"Password changed successfully for user: {user_id}", {
                'user_id': user_id,
                'component': 'password_management'
            })

        return success

    def set_role(self, user_id: int, role: str) -> bool:
        """
        Set a user's role.

        Args:
            user_id: ID of the user whose role to set
            role: New role ('admin' or 'user')

        Returns:
            True if the role was set, False otherwise
        """
        if role not in ['admin', 'user']:
            raise ValueError(f"Invalid role: {role}. Role must be 'admin' or 'user'")

        success = super().update_by_id(user_id, {'role': role})

        if success:
            self.logger.info(f"Role set successfully for user: {user_id}", {
                'user_id': user_id,
                'new_role': role,
                'component': 'user_management'
            })

        return success

    def get_all_admins(self) -> List[User]:
        """
        Get all admin users.

        Returns:
            List of admin User instances
        """
        admins_data = self.find_by_criteria({'role': 'admin'})
        admins = [User.from_dict(data) for data in admins_data]

        self.logger.debug(f"Retrieved {len(admins)} admin users", {
            'admin_count': len(admins),
            'component': 'user_management'
        })

        return admins

    def update_audit_fields(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update audit fields in the provided data dictionary.

        Args:
            data: Dictionary containing user data

        Returns:
            Updated dictionary with audit fields
        """
        from datetime import datetime
        data['updated_at'] = datetime.utcnow()
        return data