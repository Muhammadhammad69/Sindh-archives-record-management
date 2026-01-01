"""
Unit tests for Court Record DAO.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from src.dao.court_dao import CourtDAO
from src.database.models.court_record import CourtRecord


class TestCourtDAO:
    """Test class for CourtDAO."""

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

    def test_validate_data_valid(self, court_dao, sample_record_data):
        """Test that valid court record data passes validation."""
        errors = court_dao.validate_data(sample_record_data)
        assert errors == {}

    def test_validate_data_missing_fields(self, court_dao):
        """Test that missing required fields are detected."""
        # Test missing acc_no
        data = {
            'court': 'High Court',
            'suit_no': 'HC-2025-001',
            'plaintiff': 'Plaintiff Name',
            'defendant': 'Defendant Name',
            'claim_or_charge': 'Test Claim',
            'date_from': '2025-01-01',
            'date_to': '2025-12-31',
            'language': 'English'
        }
        errors = court_dao.validate_data(data)
        assert 'acc_no' in errors

        # Test missing court
        data = {
            'acc_no': 67890,
            'suit_no': 'HC-2025-001',
            'plaintiff': 'Plaintiff Name',
            'defendant': 'Defendant Name',
            'claim_or_charge': 'Test Claim',
            'date_from': '2025-01-01',
            'date_to': '2025-12-31',
            'language': 'English'
        }
        errors = court_dao.validate_data(data)
        assert 'court' in errors

    def test_validate_data_invalid_acc_no(self, court_dao, sample_record_data):
        """Test that invalid acc_no is detected."""
        sample_record_data['acc_no'] = -1
        errors = court_dao.validate_data(sample_record_data)
        assert 'acc_no' in errors

    def test_validate_data_invalid_dates(self, court_dao, sample_record_data):
        """Test that invalid dates are detected."""
        sample_record_data['date_from'] = 'invalid-date'
        errors = court_dao.validate_data(sample_record_data)
        assert 'date_from' in errors

        sample_record_data['date_from'] = '2025-01-01'
        sample_record_data['date_to'] = 'invalid-date'
        errors = court_dao.validate_data(sample_record_data)
        assert 'date_to' in errors

    def test_validate_data_invalid_date_range(self, court_dao, sample_record_data):
        """Test that invalid date ranges are detected."""
        sample_record_data['date_from'] = '2025-12-31'
        sample_record_data['date_to'] = '2025-01-01'  # End date before start date
        errors = court_dao.validate_data(sample_record_data)
        assert 'date_range' in errors

    @patch('src.dao.base_dao.BaseDAO.create')
    def test_create_record_success(self, mock_base_create, court_dao, sample_record_data):
        """Test successful court record creation."""
        # Mock the dependencies
        mock_base_create.return_value = {
            'id': 1,
            'acc_no': sample_record_data['acc_no'],
            'court': sample_record_data['court'],
            'suit_no': sample_record_data['suit_no'],
            'plaintiff': sample_record_data['plaintiff'],
            'defendant': sample_record_data['defendant'],
            'claim_or_charge': sample_record_data['claim_or_charge'],
            'date_from': sample_record_data['date_from'],
            'date_to': sample_record_data['date_to'],
            'language': sample_record_data['language']
        }

        # Create the record
        record = court_dao.create(sample_record_data)

        # Verify the results
        assert record.acc_no == sample_record_data['acc_no']
        assert record.court == sample_record_data['court']
        assert record.suit_no == sample_record_data['suit_no']
        mock_base_create.assert_called_once()

    def test_update_audit_fields(self, court_dao):
        """Test that audit fields are properly updated."""
        data = {'court': 'Updated Court'}
        updated_data = court_dao._update_audit_fields(data)

        assert 'updated_at' in updated_data
        assert updated_data['court'] == 'Updated Court'

    @patch('src.dao.base_dao.BaseDAO.update_by_id')
    def test_update_record_success(self, mock_update_by_id, court_dao):
        """Test successful court record update."""
        mock_update_by_id.return_value = True
        record_data = {'court': 'Updated Court'}

        result = court_dao.update(1, record_data)

        assert result is True
        mock_update_by_id.assert_called_once()

    @patch('src.dao.base_dao.BaseDAO.delete_by_id')
    def test_delete_record_success(self, mock_delete_by_id, court_dao):
        """Test successful court record deletion."""
        mock_delete_by_id.return_value = True

        result = court_dao.delete(1)

        assert result is True
        mock_delete_by_id.assert_called_once_with(1)

    @patch('src.dao.base_dao.BaseDAO.get_by_id')
    def test_get_by_id_found(self, mock_get_by_id, court_dao, sample_record_data):
        """Test retrieving a court record by ID."""
        mock_get_by_id.return_value = sample_record_data

        record = court_dao.get_by_id(1)

        assert record is not None
        assert record.acc_no == sample_record_data['acc_no']
        assert record.court == sample_record_data['court']

    @patch('src.dao.base_dao.BaseDAO.get_by_id')
    def test_get_by_id_not_found(self, mock_get_by_id, court_dao):
        """Test retrieving a non-existent court record by ID."""
        mock_get_by_id.return_value = None

        record = court_dao.get_by_id(999)

        assert record is None

    @patch('src.dao.base_dao.BaseDAO.find_by_criteria')
    def test_get_by_acc_no(self, mock_find_by_criteria, court_dao, sample_record_data):
        """Test retrieving court records by account number."""
        mock_find_by_criteria.return_value = [sample_record_data]

        records = court_dao.get_by_acc_no(67890)

        assert len(records) == 1
        assert records[0].acc_no == sample_record_data['acc_no']
        assert records[0].court == sample_record_data['court']