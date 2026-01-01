"""
Integration tests for commissioner record CRUD operations.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from src.dao.commissioner_dao import CommissionerDAO
from src.database.models.commissioner_record import CommissionerRecord


class TestCommissionerCRUD:
    """Test class for commissioner record CRUD operations."""

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

    @patch('src.dao.base_dao.BaseDAO.create')
    def test_create_commissioner_record_integration(self, mock_base_create, commissioner_dao, sample_record_data):
        """Integration test for creating a commissioner record."""
        # Mock the return value from the base create method
        mock_created_record = {
            'id': 1,
            'acc_no': sample_record_data['acc_no'],
            'department': sample_record_data['department'],
            'file_no': sample_record_data['file_no'],
            'subject': sample_record_data['subject'],
            'year': sample_record_data['year'],
            'page': sample_record_data['page'],
            'condition': sample_record_data['condition'],
            'record_type': sample_record_data['record_type'],
            'created_at': '2025-01-01T00:00:00',
            'updated_at': '2025-01-01T00:00:00'
        }
        mock_base_create.return_value = mock_created_record

        # Call the create method
        created_record = commissioner_dao.create(sample_record_data)

        # Verify the result
        assert created_record.id == 1
        assert created_record.acc_no == sample_record_data['acc_no']
        assert created_record.department == sample_record_data['department']
        assert created_record.file_no == sample_record_data['file_no']
        assert created_record.subject == sample_record_data['subject']

        # Verify that the base create method was called
        mock_base_create.assert_called_once()

    @patch('src.dao.base_dao.BaseDAO.get_by_id')
    def test_get_commissioner_record_by_id_integration(self, mock_get_by_id, commissioner_dao):
        """Integration test for retrieving a commissioner record by ID."""
        # Mock the return value from the base get_by_id method
        mock_record_data = {
            'id': 1,
            'acc_no': 12345,
            'department': 'Legal',
            'file_no': 'L-001',
            'subject': 'Test Subject',
            'year': 2025,
            'page': 1,
            'condition': 'Good',
            'record_type': 'Document',
            'created_at': '2025-01-01T00:00:00',
            'updated_at': '2025-01-01T00:00:00'
        }
        mock_get_by_id.return_value = mock_record_data

        # Call the get_by_id method
        record = commissioner_dao.get_by_id(1)

        # Verify the result
        assert record is not None
        assert record.id == 1
        assert record.acc_no == 12345
        assert record.department == 'Legal'
        assert record.subject == 'Test Subject'

    @patch('src.dao.base_dao.BaseDAO.find_by_criteria')
    def test_get_commissioner_records_by_acc_no_integration(self, mock_find_by_criteria, commissioner_dao):
        """Integration test for retrieving commissioner records by account number."""
        # Mock the return value
        mock_records_data = [
            {
                'id': 1,
                'acc_no': 12345,
                'department': 'Legal',
                'file_no': 'L-001',
                'subject': 'Test Subject 1',
                'year': 2025,
                'page': 1,
                'condition': 'Good',
                'record_type': 'Document',
                'created_at': '2025-01-01T00:00:00',
                'updated_at': '2025-01-01T00:00:00'
            },
            {
                'id': 2,
                'acc_no': 12345,
                'department': 'Finance',
                'file_no': 'F-002',
                'subject': 'Test Subject 2',
                'year': 2024,
                'page': 2,
                'condition': 'Fair',
                'record_type': 'Financial',
                'created_at': '2025-01-01T00:00:00',
                'updated_at': '2025-01-01T00:00:00'
            }
        ]
        mock_find_by_criteria.return_value = mock_records_data

        # Call the get_by_acc_no method
        records = commissioner_dao.get_by_acc_no(12345)

        # Verify the result
        assert len(records) == 2
        assert all(record.acc_no == 12345 for record in records)
        assert records[0].subject == 'Test Subject 1'
        assert records[1].subject == 'Test Subject 2'

    @patch('src.dao.base_dao.BaseDAO.update_by_id')
    def test_update_commissioner_record_integration(self, mock_update_by_id, commissioner_dao):
        """Integration test for updating a commissioner record."""
        # Mock the return value (number of affected rows)
        mock_update_by_id.return_value = True

        # Data to update
        update_data = {
            'department': 'Updated Department',
            'condition': 'Excellent'
        }

        # Call the update method
        result = commissioner_dao.update(1, update_data)

        # Verify the result
        assert result is True

        # Verify that the base update method was called
        mock_update_by_id.assert_called_once_with(1, update_data)

    @patch('src.dao.base_dao.BaseDAO.delete_by_id')
    def test_delete_commissioner_record_integration(self, mock_delete_by_id, commissioner_dao):
        """Integration test for deleting a commissioner record."""
        # Mock the return value
        mock_delete_by_id.return_value = True

        # Call the delete method
        result = commissioner_dao.delete(1)

        # Verify the result
        assert result is True

        # Verify that the base delete method was called
        mock_delete_by_id.assert_called_once_with(1)

    @patch('src.dao.base_dao.BaseDAO.find_by_criteria')
    def test_get_all_by_department_integration(self, mock_find_by_criteria, commissioner_dao):
        """Integration test for retrieving all commissioner records by department."""
        # Mock the return value
        mock_records_data = [
            {
                'id': 1,
                'acc_no': 12345,
                'department': 'Legal',
                'file_no': 'L-001',
                'subject': 'Test Subject 1',
                'year': 2025,
                'page': 1,
                'condition': 'Good',
                'record_type': 'Document',
                'created_at': '2025-01-01T00:00:00',
                'updated_at': '2025-01-01T00:00:00'
            },
            {
                'id': 2,
                'acc_no': 67890,
                'department': 'Legal',
                'file_no': 'L-002',
                'subject': 'Test Subject 2',
                'year': 2024,
                'page': 2,
                'condition': 'Fair',
                'record_type': 'Document',
                'created_at': '2025-01-01T00:00:00',
                'updated_at': '2025-01-01T00:00:00'
            }
        ]
        mock_find_by_criteria.return_value = mock_records_data

        # Call the get_all_by_department method
        records = commissioner_dao.get_all_by_department('Legal')

        # Verify the result
        assert len(records) == 2
        assert all(record.department == 'Legal' for record in records)
        assert records[0].subject == 'Test Subject 1'
        assert records[1].subject == 'Test Subject 2'

    @patch('src.dao.base_dao.BaseDAO.find_by_criteria')
    def test_get_all_by_year_integration(self, mock_find_by_criteria, commissioner_dao):
        """Integration test for retrieving all commissioner records by year."""
        # Mock the return value
        mock_records_data = [
            {
                'id': 1,
                'acc_no': 12345,
                'department': 'Legal',
                'file_no': 'L-001',
                'subject': 'Test Subject 1',
                'year': 2025,
                'page': 1,
                'condition': 'Good',
                'record_type': 'Document',
                'created_at': '2025-01-01T00:00:00',
                'updated_at': '2025-01-01T00:00:00'
            }
        ]
        mock_find_by_criteria.return_value = mock_records_data

        # Call the get_all_by_year method
        records = commissioner_dao.get_all_by_year(2025)

        # Verify the result
        assert len(records) == 1
        assert all(record.year == 2025 for record in records)
        assert records[0].subject == 'Test Subject 1'

    def test_validate_data_valid_integration(self, commissioner_dao, sample_record_data):
        """Integration test for validating valid commissioner record data."""
        errors = commissioner_dao.validate_data(sample_record_data)

        # No errors should be returned for valid data
        assert errors == {}

    def test_validate_data_invalid_acc_no_integration(self, commissioner_dao, sample_record_data):
        """Integration test for validating invalid acc_no."""
        sample_record_data['acc_no'] = -1
        errors = commissioner_dao.validate_data(sample_record_data)

        # Should have an error for acc_no
        assert 'acc_no' in errors

    def test_validate_data_invalid_year_integration(self, commissioner_dao, sample_record_data):
        """Integration test for validating invalid year."""
        sample_record_data['year'] = -1
        errors = commissioner_dao.validate_data(sample_record_data)

        # Should have an error for year
        assert 'year' in errors

    def test_validate_data_invalid_page_integration(self, commissioner_dao, sample_record_data):
        """Integration test for validating invalid page number."""
        sample_record_data['page'] = -1
        errors = commissioner_dao.validate_data(sample_record_data)

        # Should have an error for page
        assert 'page' in errors

    def test_validate_data_missing_required_fields_integration(self, commissioner_dao):
        """Integration test for validating missing required fields."""
        # Create data with missing required fields
        incomplete_data = {
            'acc_no': 12345,
            'department': 'Legal',
            # Missing other required fields
        }

        errors = commissioner_dao.validate_data(incomplete_data)

        # Should have errors for missing required fields
        assert 'file_no' in errors
        assert 'subject' in errors
        assert 'year' in errors
        assert 'page' in errors
        assert 'condition' in errors
        assert 'record_type' in errors