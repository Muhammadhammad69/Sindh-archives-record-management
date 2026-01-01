"""
Unit tests for Commissioner Record DAO.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from src.dao.commissioner_dao import CommissionerDAO
from src.database.models.commissioner_record import CommissionerRecord


class TestCommissionerDAO:
    """Test class for CommissionerDAO."""

    @pytest.fixture
    def commissioner_dao(self):
        """Create a CommissionerDAO instance for testing."""
        return CommissionerDAO()

    @pytest.fixture
    def sample_record_data(self):
        """Sample commissioner record data for testing."""
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

    def test_validate_data_valid(self, commissioner_dao, sample_record_data):
        """Test that valid commissioner record data passes validation."""
        errors = commissioner_dao.validate_data(sample_record_data)
        assert errors == {}

    def test_validate_data_missing_fields(self, commissioner_dao):
        """Test that missing required fields are detected."""
        # Test missing acc_no
        data = {
            'department': 'Legal',
            'file_no': 'L-001',
            'subject': 'Test Subject',
            'year': 2025,
            'page': 1,
            'condition': 'Good',
            'record_type': 'Document'
        }
        errors = commissioner_dao.validate_data(data)
        assert 'acc_no' in errors

        # Test missing department
        data = {
            'acc_no': 12345,
            'file_no': 'L-001',
            'subject': 'Test Subject',
            'year': 2025,
            'page': 1,
            'condition': 'Good',
            'record_type': 'Document'
        }
        errors = commissioner_dao.validate_data(data)
        assert 'department' in errors

    def test_validate_data_invalid_acc_no(self, commissioner_dao, sample_record_data):
        """Test that invalid acc_no is detected."""
        sample_record_data['acc_no'] = -1
        errors = commissioner_dao.validate_data(sample_record_data)
        assert 'acc_no' in errors

    def test_validate_data_invalid_year(self, commissioner_dao, sample_record_data):
        """Test that invalid year is detected."""
        sample_record_data['year'] = -1
        errors = commissioner_dao.validate_data(sample_record_data)
        assert 'year' in errors

    def test_validate_data_invalid_page(self, commissioner_dao, sample_record_data):
        """Test that invalid page number is detected."""
        sample_record_data['page'] = -1
        errors = commissioner_dao.validate_data(sample_record_data)
        assert 'page' in errors

    @patch('src.dao.base_dao.BaseDAO.create')
    def test_create_record_success(self, mock_base_create, commissioner_dao, sample_record_data):
        """Test successful commissioner record creation."""
        # Mock the dependencies
        mock_base_create.return_value = {
            'id': 1,
            'acc_no': sample_record_data['acc_no'],
            'department': sample_record_data['department'],
            'file_no': sample_record_data['file_no'],
            'subject': sample_record_data['subject'],
            'year': sample_record_data['year'],
            'page': sample_record_data['page'],
            'condition': sample_record_data['condition'],
            'record_type': sample_record_data['record_type']
        }

        # Create the record
        record = commissioner_dao.create(sample_record_data)

        # Verify the results
        assert record.acc_no == sample_record_data['acc_no']
        assert record.department == sample_record_data['department']
        assert record.file_no == sample_record_data['file_no']
        mock_base_create.assert_called_once()

    def test_update_audit_fields(self, commissioner_dao):
        """Test that audit fields are properly updated."""
        data = {'department': 'Updated Department'}
        updated_data = commissioner_dao._update_audit_fields(data)

        assert 'updated_at' in updated_data
        assert updated_data['department'] == 'Updated Department'

    @patch('src.dao.base_dao.BaseDAO.update_by_id')
    def test_update_record_success(self, mock_update_by_id, commissioner_dao):
        """Test successful commissioner record update."""
        mock_update_by_id.return_value = True
        record_data = {'department': 'Updated Department'}

        result = commissioner_dao.update(1, record_data)

        assert result is True
        mock_update_by_id.assert_called_once()

    @patch('src.dao.base_dao.BaseDAO.delete_by_id')
    def test_delete_record_success(self, mock_delete_by_id, commissioner_dao):
        """Test successful commissioner record deletion."""
        mock_delete_by_id.return_value = True

        result = commissioner_dao.delete(1)

        assert result is True
        mock_delete_by_id.assert_called_once_with(1)

    @patch('src.dao.base_dao.BaseDAO.get_by_id')
    def test_get_by_id_found(self, mock_get_by_id, commissioner_dao, sample_record_data):
        """Test retrieving a commissioner record by ID."""
        mock_get_by_id.return_value = sample_record_data

        record = commissioner_dao.get_by_id(1)

        assert record is not None
        assert record.acc_no == sample_record_data['acc_no']
        assert record.department == sample_record_data['department']

    @patch('src.dao.base_dao.BaseDAO.get_by_id')
    def test_get_by_id_not_found(self, mock_get_by_id, commissioner_dao):
        """Test retrieving a non-existent commissioner record by ID."""
        mock_get_by_id.return_value = None

        record = commissioner_dao.get_by_id(999)

        assert record is None