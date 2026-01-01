"""
Integration tests for user CRUD operations.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from src.dao.user_dao import UserDAO
from src.database.models.user import User


class TestUserCRUD:
    """Test class for user CRUD operations."""

    @pytest.fixture
    def user_dao(self):
        """Create a UserDAO instance for testing."""
        return UserDAO()

    @pytest.fixture
    def sample_user_data(self):
        """Sample user data for testing."""
        return {
            'name': 'Test User',
            'email': 'test@example.com',
            'password': 'SecurePassword123!',
            'role': 'user'
        }

    @patch('src.dao.base_dao.BaseDAO.create')
    def test_create_user_integration(self, mock_base_create, user_dao, sample_user_data):
        """Integration test for creating a user."""
        # Mock the return value from the base create method
        mock_created_user = {
            'id': 1,
            'name': sample_user_data['name'],
            'email': sample_user_data['email'],
            'role': sample_user_data['role'],
            'created_at': '2025-01-01T00:00:00',
            'updated_at': '2025-01-01T00:00:00'
        }
        mock_base_create.return_value = mock_created_user

        # Call the create method
        created_user = user_dao.create(sample_user_data)

        # Verify the result
        assert created_user.id == 1
        assert created_user.name == sample_user_data['name']
        assert created_user.email == sample_user_data['email']
        assert created_user.role == sample_user_data['role']

        # Verify that the base create method was called
        mock_base_create.assert_called_once()

    @patch('src.dao.base_dao.BaseDAO.get_by_id')
    def test_get_user_by_id_integration(self, mock_get_by_id, user_dao):
        """Integration test for retrieving a user by ID."""
        # Mock the return value from the base get_by_id method
        mock_user_data = {
            'id': 1,
            'name': 'Test User',
            'email': 'test@example.com',
            'role': 'user',
            'created_at': '2025-01-01T00:00:00',
            'updated_at': '2025-01-01T00:00:00'
        }
        mock_get_by_id.return_value = mock_user_data

        # Call the get_by_id method
        user = user_dao.get_by_id(1)

        # Verify the result
        assert user is not None
        assert user.id == 1
        assert user.name == 'Test User'
        assert user.email == 'test@example.com'
        assert user.role == 'user'

    @patch('src.dao.user_dao.UserDAO.get_by_email')
    def test_get_user_by_email_integration(self, mock_get_by_email, user_dao, sample_user_data):
        """Integration test for retrieving a user by email."""
        # Mock the return value
        mock_user = User.from_dict(sample_user_data)
        mock_user.id = 1
        mock_get_by_email.return_value = mock_user

        # Call the get_by_email method
        user = user_dao.get_by_email(sample_user_data['email'])

        # Verify the result
        assert user is not None
        assert user.id == 1
        assert user.email == sample_user_data['email']

    @patch('src.dao.base_dao.BaseDAO.update_by_id')
    def test_update_user_integration(self, mock_update_by_id, user_dao):
        """Integration test for updating a user."""
        # Mock the return value (number of affected rows)
        mock_update_by_id.return_value = True

        # Data to update
        update_data = {
            'name': 'Updated Name',
            'email': 'updated@example.com'
        }

        # Call the update method
        result = user_dao.update(1, update_data)

        # Verify the result
        assert result is True

        # Verify that the base update method was called
        mock_update_by_id.assert_called_once_with(1, update_data)

    @patch('src.dao.base_dao.BaseDAO.delete_by_id')
    def test_delete_user_integration(self, mock_delete_by_id, user_dao):
        """Integration test for deleting a user."""
        # Mock the return value
        mock_delete_by_id.return_value = True

        # Call the delete method
        result = user_dao.delete(1)

        # Verify the result
        assert result is True

        # Verify that the base delete method was called
        mock_delete_by_id.assert_called_once_with(1)

    @patch('src.dao.user_dao.UserDAO.get_by_email')
    @patch('src.dao.user_dao.hash_password')
    @patch('src.dao.base_dao.BaseDAO.create')
    def test_create_user_with_password_hashing_integration(self, mock_base_create, mock_hash, mock_get_by_email, user_dao, sample_user_data):
        """Integration test for creating a user with password hashing."""
        # Mock the dependencies
        mock_get_by_email.return_value = None  # No existing user with this email
        mock_hash.return_value = 'hashed_password'
        mock_created_user = {
            'id': 1,
            'name': sample_user_data['name'],
            'email': sample_user_data['email'],
            'password': 'hashed_password',  # This should be the hashed password
            'role': sample_user_data['role'],
            'created_at': '2025-01-01T00:00:00',
            'updated_at': '2025-01-01T00:00:00'
        }
        mock_base_create.return_value = mock_created_user

        # Call the create method
        created_user = user_dao.create(sample_user_data)

        # Verify the result
        assert created_user.id == 1
        assert created_user.name == sample_user_data['name']
        assert created_user.email == sample_user_data['email']
        assert created_user.role == sample_user_data['role']

        # Verify that password was hashed
        mock_hash.assert_called_once_with(sample_user_data['password'])

        # Verify that the base create method was called with the correct data
        expected_call_data = {
            'name': sample_user_data['name'],
            'email': sample_user_data['email'],
            'password': 'hashed_password',  # The hashed password should be passed
            'role': sample_user_data['role'],
        }
        # Check that the correct arguments were passed to the base create method
        args, kwargs = mock_base_create.call_args
        assert 'password' in args[0]  # The first argument is the data dict
        assert args[0]['password'] == 'hashed_password'

    @patch('src.dao.user_dao.UserDAO.get_by_email')
    def test_create_duplicate_user_raises_error(self, mock_get_by_email, user_dao, sample_user_data):
        """Test that creating a user with duplicate email raises an error."""
        # Mock that a user already exists with this email
        existing_user = User.from_dict(sample_user_data)
        existing_user.id = 999
        mock_get_by_email.return_value = existing_user

        # Attempt to create user should raise an error
        with pytest.raises(ValueError, match="already exists"):
            user_dao.create(sample_user_data)

    @patch('src.dao.base_dao.BaseDAO.find_by_criteria')
    def test_get_all_admins_integration(self, mock_find_by_criteria, user_dao):
        """Integration test for retrieving all admin users."""
        # Mock the return value
        mock_admin_users_data = [
            {
                'id': 1,
                'name': 'Admin User 1',
                'email': 'admin1@example.com',
                'role': 'admin',
                'created_at': '2025-01-01T00:00:00',
                'updated_at': '2025-01-01T00:00:00'
            },
            {
                'id': 2,
                'name': 'Admin User 2',
                'email': 'admin2@example.com',
                'role': 'admin',
                'created_at': '2025-01-01T00:00:00',
                'updated_at': '2025-01-01T00:00:00'
            }
        ]
        mock_find_by_criteria.return_value = mock_admin_users_data

        # Call the get_all_admins method
        admin_users = user_dao.get_all_admins()

        # Verify the result
        assert len(admin_users) == 2
        assert all(user.role == 'admin' for user in admin_users)
        assert admin_users[0].email == 'admin1@example.com'
        assert admin_users[1].email == 'admin2@example.com'

    @patch('src.dao.base_dao.BaseDAO.update_by_id')
    def test_set_role_integration(self, mock_update_by_id, user_dao):
        """Integration test for setting a user's role."""
        # Mock the return value
        mock_update_by_id.return_value = True

        # Call the set_role method
        result = user_dao.set_role(1, 'admin')

        # Verify the result
        assert result is True

        # Verify that the base update method was called with the correct data
        mock_update_by_id.assert_called_once_with(1, {'role': 'admin'})

    def test_set_role_invalid_role_raises_error(self, user_dao):
        """Test that setting an invalid role raises an error."""
        with pytest.raises(ValueError, match="Invalid role"):
            user_dao.set_role(1, 'invalid_role')