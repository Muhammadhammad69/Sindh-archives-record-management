"""
Pytest configuration and fixtures for the application tests.
"""
import pytest
import os
from unittest.mock import patch
from src.config.environment import initialize_environment
from src.database.connection import connection_manager


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """
    Set up the test environment before running tests.
    """
    # Set test environment variables
    os.environ['DATABASE_URL'] = os.getenv('TEST_DATABASE_URL', 'postgresql://test:test@localhost:5432/test_sindh_archives')
    os.environ['USERS_TABLE_NAME'] = 'test_users'
    os.environ['COMMISSIONER_TABLE_NAME'] = 'test_commissioner_records'
    os.environ['COURT_TABLE_NAME'] = 'test_court_records'
    os.environ['DB_MIN_CONNECTIONS'] = '1'
    os.environ['DB_MAX_CONNECTIONS'] = '2'

    # Initialize environment
    initialize_environment()

    yield

    # Cleanup if needed
    connection_manager.close_all_connections()


@pytest.fixture
def mock_db_connection():
    """
    Mock database connection for testing without actual database.
    """
    with patch('src.database.connection.connection_manager') as mock_conn:
        yield mock_conn


@pytest.fixture
def sample_user_data():
    """
    Sample user data for testing.
    """
    return {
        'name': 'Test User',
        'email': 'test@example.com',
        'password': 'SecurePassword123!',
        'role': 'user'
    }


@pytest.fixture
def sample_commissioner_record_data():
    """
    Sample commissioner record data for testing.
    """
    return {
        'acc_no': 12345,
        'department': 'Legal',
        'file_no': 'L-001',
        'subject': 'Test Subject',
        'year': 2025,
        'page': 1,
        'condition': 'Good',
        'record_type': 'Document'
    }


@pytest.fixture
def sample_court_record_data():
    """
    Sample court record data for testing.
    """
    return {
        'acc_no': 67890,
        'court': 'High Court',
        'suit_no': 'HC-2025-001',
        'plaintiff': 'Plaintiff Name',
        'defendant': 'Defendant Name',
        'claim_or_charge': 'Test Claim',
        'date_from': '2025-01-01',
        'date_to': '2025-12-31',
        'language': 'English'
    }