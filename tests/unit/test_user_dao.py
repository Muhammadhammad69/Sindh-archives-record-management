"""
Unit tests for User DAO.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from src.dao.user_dao import UserDAO
from src.database.models.user import User


class TestUserDAO:
    """Test class for UserDAO."""

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

    def test_validate_data_valid(self, user_dao, sample_user_data):
        """Test that valid user data passes validation."""
        errors = user_dao.validate_data(sample_user_data)
        assert errors == {}

    def test_validate_data_missing_fields(self, user_dao):
        """Test that missing required fields are detected."""
        # Test missing name
        data = {'email': 'test@example.com', 'password': 'SecurePassword123!', 'role': 'user'}
        errors = user_dao.validate_data(data)
        assert 'name' in errors

        # Test missing email
        data = {'name': 'Test User', 'password': 'SecurePassword123!', 'role': 'user'}
        errors = user_dao.validate_data(data)
        assert 'email' in errors

        # Test missing role
        data = {'name': 'Test User', 'email': 'test@example.com', 'password': 'SecurePassword123!'}
        errors = user_dao.validate_data(data)
        assert 'role' in errors

    def test_validate_data_invalid_role(self, user_dao, sample_user_data):
        """Test that invalid role is detected."""
        sample_user_data['role'] = 'invalid_role'
        errors = user_dao.validate_data(sample_user_data)
        assert 'role' in errors

    def test_validate_data_invalid_email(self, user_dao, sample_user_data):
        """Test that invalid email is detected."""
        sample_user_data['email'] = 'invalid-email'
        errors = user_dao.validate_data(sample_user_data)
        assert 'email' in errors

    @patch('src.dao.user_dao.UserDAO.get_by_email')
    @patch('src.dao.user_dao.hash_password')
    @patch('src.dao.base_dao.BaseDAO.create')
    def test_create_user_success(self, mock_base_create, mock_hash, mock_get_by_email, user_dao, sample_user_data):
        """Test successful user creation."""
        # Mock the dependencies
        mock_get_by_email.return_value = None  # No existing user with this email
        mock_hash.return_value = 'hashed_password'
        mock_base_create.return_value = {
            'id': 1,
            'name': sample_user_data['name'],
            'email': sample_user_data['email'],
            'password': 'hashed_password',
            'role': sample_user_data['role']
        }

        # Create the user
        user = user_dao.create(sample_user_data)

        # Verify the results
        assert user.name == sample_user_data['name']
        assert user.email == sample_user_data['email']
        assert user.role == sample_user_data['role']
        mock_hash.assert_called_once_with(sample_user_data['password'])
        mock_base_create.assert_called_once()

    @patch('src.dao.user_dao.UserDAO.get_by_email')
    def test_create_user_duplicate_email(self, mock_get_by_email, user_dao, sample_user_data):
        """Test that creating a user with duplicate email raises an error."""
        # Mock that a user already exists with this email
        mock_get_by_email.return_value = User.from_dict(sample_user_data)

        # Attempt to create user should raise an error
        with pytest.raises(ValueError, match="already exists"):
            user_dao.create(sample_user_data)

    def test_update_audit_fields(self, user_dao):
        """Test that audit fields are properly updated."""
        data = {'name': 'Test User'}
        updated_data = user_dao._update_audit_fields(data)

        assert 'updated_at' in updated_data
        assert updated_data['name'] == 'Test User'

    @patch('src.dao.base_dao.BaseDAO.update_by_id')
    def test_update_user_success(self, mock_update_by_id, user_dao):
        """Test successful user update."""
        mock_update_by_id.return_value = True
        user_data = {'name': 'Updated Name'}

        result = user_dao.update(1, user_data)

        assert result is True
        mock_update_by_id.assert_called_once()

    @patch('src.dao.base_dao.BaseDAO.delete_by_id')
    def test_delete_user_success(self, mock_delete_by_id, user_dao):
        """Test successful user deletion."""
        mock_delete_by_id.return_value = True

        result = user_dao.delete(1)

        assert result is True
        mock_delete_by_id.assert_called_once_with(1)