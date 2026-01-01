"""
Integration tests for court record CRUD operations.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from src.dao.court_dao import CourtDAO
from src.database.models.court_record import CourtRecord


class TestCourtCRUD:
    """Test class for court record CRUD operations."""

    @pytest.fixture
    def court_dao(self):
        """Create a CourtDAO instance for testing."""
        return CourtDAO()

    @pytest.fixture
    def sample_record_data(self):
        """Sample court record data for testing."""
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

    @patch('src.dao.base_dao.BaseDAO.create')
    def test_create_court_record_integration(self, mock_base_create, court_dao, sample_record_data):
        """Integration test for creating a court record."""
        # Mock the return value from the base create method
        mock_created_record = {
            'id': 1,
            'acc_no': sample_record_data['acc_no'],
            'court': sample_record_data['court'],
            'suit_no': sample_record_data['suit_no'],
            'plaintiff': sample_record_data['plaintiff'],
            'defendant': sample_record_data['defendant'],
            'claim_or_charge': sample_record_data['claim_or_charge'],
            'date_from': sample_record_data['date_from'],
            'date_to': sample_record_data['date_to'],
            'language': sample_record_data['language'],
            'created_at': '2025-01-01T00:00:00',
            'updated_at': '2025-01-01T00:00:00'
        }
        mock_base_create.return_value = mock_created_record

        # Call the create method
        created_record = court_dao.create(sample_record_data)

        # Verify the result
        assert created_record.id == 1
        assert created_record.acc_no == sample_record_data['acc_no']
        assert created_record.court == sample_record_data['court']
        assert created_record.suit_no == sample_record_data['suit_no']
        assert created_record.plaintiff == sample_record_data['plaintiff']
        assert created_record.defendant == sample_record_data['defendant']

        # Verify that the base create method was called
        mock_base_create.assert_called_once()

    @patch('src.dao.base_dao.BaseDAO.get_by_id')
    def test_get_court_record_by_id_integration(self, mock_get_by_id, court_dao):
        """Integration test for retrieving a court record by ID."""
        # Mock the return value from the base get_by_id method
        mock_record_data = {
            'id': 1,
            'acc_no': 67890,
            'court': 'High Court',
            'suit_no': 'HC-2025-001',
            'plaintiff': 'Plaintiff Name',
            'defendant': 'Defendant Name',
            'claim_or_charge': 'Test Claim',
            'date_from': '2025-01-01',
            'date_to': '2025-12-31',
            'language': 'English',
            'created_at': '2025-01-01T00:00:00',
            'updated_at': '2025-01-01T00:00:00'
        }
        mock_get_by_id.return_value = mock_record_data

        # Call the get_by_id method
        record = court_dao.get_by_id(1)

        # Verify the result
        assert record is not None
        assert record.id == 1
        assert record.acc_no == 67890
        assert record.court == 'High Court'
        assert record.plaintiff == 'Plaintiff Name'
        assert record.defendant == 'Defendant Name'

    @patch('src.dao.base_dao.BaseDAO.find_by_criteria')
    def test_get_court_records_by_acc_no_integration(self, mock_find_by_criteria, court_dao):
        """Integration test for retrieving court records by account number."""
        # Mock the return value
        mock_records_data = [
            {
                'id': 1,
                'acc_no': 67890,
                'court': 'High Court',
                'suit_no': 'HC-2025-001',
                'plaintiff': 'Plaintiff Name',
                'defendant': 'Defendant Name',
                'claim_or_charge': 'Test Claim 1',
                'date_from': '2025-01-01',
                'date_to': '2025-12-31',
                'language': 'English',
                'created_at': '2025-01-01T00:00:00',
                'updated_at': '2025-01-01T00:00:00'
            },
            {
                'id': 2,
                'acc_no': 67890,
                'court': 'District Court',
                'suit_no': 'DC-2025-002',
                'plaintiff': 'Another Plaintiff',
                'defendant': 'Another Defendant',
                'claim_or_charge': 'Test Claim 2',
                'date_from': '2025-02-01',
                'date_to': '2025-11-30',
                'language': 'Urdu',
                'created_at': '2025-01-01T00:00:00',
                'updated_at': '2025-01-01T00:00:00'
            }
        ]
        mock_find_by_criteria.return_value = mock_records_data

        # Call the get_by_acc_no method
        records = court_dao.get_by_acc_no(67890)

        # Verify the result
        assert len(records) == 2
        assert all(record.acc_no == 67890 for record in records)
        assert records[0].claim_or_charge == 'Test Claim 1'
        assert records[1].claim_or_charge == 'Test Claim 2'

    @patch('src.dao.base_dao.BaseDAO.update_by_id')
    def test_update_court_record_integration(self, mock_update_by_id, court_dao):
        """Integration test for updating a court record."""
        # Mock the return value (number of affected rows)
        mock_update_by_id.return_value = True

        # Data to update
        update_data = {
            'court': 'Supreme Court',
            'language': 'Urdu'
        }

        # Call the update method
        result = court_dao.update(1, update_data)

        # Verify the result
        assert result is True

        # Verify that the base update method was called
        mock_update_by_id.assert_called_once_with(1, update_data)

    @patch('src.dao.base_dao.BaseDAO.delete_by_id')
    def test_delete_court_record_integration(self, mock_delete_by_id, court_dao):
        """Integration test for deleting a court record."""
        # Mock the return value
        mock_delete_by_id.return_value = True

        # Call the delete method
        result = court_dao.delete(1)

        # Verify the result
        assert result is True

        # Verify that the base delete method was called
        mock_delete_by_id.assert_called_once_with(1)

    @patch('src.dao.base_dao.BaseDAO.find_by_criteria')
    def test_get_all_by_court_integration(self, mock_find_by_criteria, court_dao):
        """Integration test for retrieving all court records by court name."""
        # Mock the return value
        mock_records_data = [
            {
                'id': 1,
                'acc_no': 67890,
                'court': 'High Court',
                'suit_no': 'HC-2025-001',
                'plaintiff': 'Plaintiff Name',
                'defendant': 'Defendant Name',
                'claim_or_charge': 'Test Claim 1',
                'date_from': '2025-01-01',
                'date_to': '2025-12-31',
                'language': 'English',
                'created_at': '2025-01-01T00:00:00',
                'updated_at': '2025-01-01T00:00:00'
            },
            {
                'id': 2,
                'acc_no': 12345,
                'court': 'High Court',
                'suit_no': 'HC-2025-002',
                'plaintiff': 'Another Plaintiff',
                'defendant': 'Another Defendant',
                'claim_or_charge': 'Test Claim 2',
                'date_from': '2025-02-01',
                'date_to': '2025-11-30',
                'language': 'Urdu',
                'created_at': '2025-01-01T00:00:00',
                'updated_at': '2025-01-01T00:00:00'
            }
        ]
        mock_find_by_criteria.return_value = mock_records_data

        # Call the get_all_by_court method
        records = court_dao.get_all_by_court('High Court')

        # Verify the result
        assert len(records) == 2
        assert all(record.court == 'High Court' for record in records)
        assert records[0].claim_or_charge == 'Test Claim 1'
        assert records[1].claim_or_charge == 'Test Claim 2'

    def test_validate_data_valid_integration(self, court_dao, sample_record_data):
        """Integration test for validating valid court record data."""
        errors = court_dao.validate_data(sample_record_data)

        # No errors should be returned for valid data
        assert errors == {}

    def test_validate_data_invalid_acc_no_integration(self, court_dao, sample_record_data):
        """Integration test for validating invalid acc_no."""
        sample_record_data['acc_no'] = -1
        errors = court_dao.validate_data(sample_record_data)

        # Should have an error for acc_no
        assert 'acc_no' in errors

    def test_validate_data_invalid_date_format_integration(self, court_dao, sample_record_data):
        """Integration test for validating invalid date format."""
        sample_record_data['date_from'] = 'invalid-date'
        errors = court_dao.validate_data(sample_record_data)

        # Should have an error for date_from
        assert 'date_from' in errors

    def test_validate_data_invalid_date_range_integration(self, court_dao, sample_record_data):
        """Integration test for validating invalid date range."""
        sample_record_data['date_from'] = '2025-12-31'
        sample_record_data['date_to'] = '2025-01-01'  # End date before start date
        errors = court_dao.validate_data(sample_record_data)

        # Should have an error for date range
        assert 'date_range' in errors

    def test_validate_data_missing_required_fields_integration(self, court_dao):
        """Integration test for validating missing required fields."""
        # Create data with missing required fields
        incomplete_data = {
            'acc_no': 67890,
            'court': 'High Court',
            # Missing other required fields
        }

        errors = court_dao.validate_data(incomplete_data)

        # Should have errors for missing required fields
        assert 'suit_no' in errors
        assert 'plaintiff' in errors
        assert 'defendant' in errors
        assert 'claim_or_charge' in errors
        assert 'date_from' in errors
        assert 'date_to' in errors
        assert 'language' in errors

    @patch('src.dao.base_dao.BaseDAO._execute_query')
    def test_get_all_by_date_range_integration(self, mock_execute_query, court_dao):
        """Integration test for retrieving all court records by date range."""
        # Mock the return value
        mock_records_data = [
            {
                'id': 1,
                'acc_no': 67890,
                'court': 'High Court',
                'suit_no': 'HC-2025-001',
                'plaintiff': 'Plaintiff Name',
                'defendant': 'Defendant Name',
                'claim_or_charge': 'Test Claim 1',
                'date_from': '2025-03-01',
                'date_to': '2025-03-31',
                'language': 'English',
                'created_at': '2025-01-01T00:00:00',
                'updated_at': '2025-01-01T00:00:00'
            }
        ]
        mock_execute_query.return_value = mock_records_data

        # Call the get_all_by_date_range method
        records = court_dao.get_all_by_date_range('2025-01-01', '2025-12-31')

        # Verify the result
        assert len(records) == 1
        assert records[0].date_from == '2025-03-01'
        assert records[0].date_to == '2025-03-31'

    def test_validate_date_range_invalid_integration(self, court_dao):
        """Integration test for validating date range with invalid dates."""
        with pytest.raises(ValueError, match="Invalid date range"):
            court_dao.get_all_by_date_range('2025-12-31', '2025-01-01')  # End date before start date