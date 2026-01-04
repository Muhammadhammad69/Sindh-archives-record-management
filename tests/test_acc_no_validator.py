"""
Unit tests for acc_no_validator utility functions.
"""
import pytest
import pandas as pd
from unittest.mock import Mock, patch
from src.utils.acc_no_validator import validate_single_acc_no, validate_bulk_acc_numbers


def test_validate_single_acc_no_commissioner_valid():
    """Test validating a single acc_no that doesn't exist in commissioner records."""
    with patch('src.utils.acc_no_validator.CommissionerDAO') as mock_dao_class:
        mock_dao_instance = Mock()
        mock_dao_instance.get_by_acc_no.return_value = []
        mock_dao_class.return_value = mock_dao_instance

        is_valid, error_msg = validate_single_acc_no(123, 'commissioner')

        assert is_valid is True
        assert error_msg == ""
        mock_dao_instance.get_by_acc_no.assert_called_once_with(123)


def test_validate_single_acc_no_commissioner_invalid():
    """Test validating a single acc_no that already exists in commissioner records."""
    with patch('src.utils.acc_no_validator.CommissionerDAO') as mock_dao_class:
        mock_dao_instance = Mock()
        mock_dao_instance.get_by_acc_no.return_value = [{'id': 1, 'acc_no': 123}]
        mock_dao_class.return_value = mock_dao_instance

        is_valid, error_msg = validate_single_acc_no(123, 'commissioner')

        assert is_valid is False
        assert error_msg == "❌ This acc_no (123) already exists in Commissioner Records. Please use a different acc_no."
        mock_dao_instance.get_by_acc_no.assert_called_once_with(123)


def test_validate_single_acc_no_court_valid():
    """Test validating a single acc_no that doesn't exist in court records."""
    with patch('src.utils.acc_no_validator.CourtDAO') as mock_dao_class:
        mock_dao_instance = Mock()
        mock_dao_instance.get_by_acc_no.return_value = []
        mock_dao_class.return_value = mock_dao_instance

        is_valid, error_msg = validate_single_acc_no(456, 'court')

        assert is_valid is True
        assert error_msg == ""
        mock_dao_instance.get_by_acc_no.assert_called_once_with(456)


def test_validate_single_acc_no_court_invalid():
    """Test validating a single acc_no that already exists in court records."""
    with patch('src.utils.acc_no_validator.CourtDAO') as mock_dao_class:
        mock_dao_instance = Mock()
        mock_dao_instance.get_by_acc_no.return_value = [{'id': 1, 'acc_no': 456}]
        mock_dao_class.return_value = mock_dao_instance

        is_valid, error_msg = validate_single_acc_no(456, 'court')

        assert is_valid is False
        assert error_msg == "❌ This acc_no (456) already exists in Court Records. Please use a different acc_no."
        mock_dao_instance.get_by_acc_no.assert_called_once_with(456)


def test_validate_single_acc_no_invalid_record_type():
    """Test validating with an invalid record type."""
    with pytest.raises(ValueError) as exc_info:
        validate_single_acc_no(123, 'invalid_type')

    assert "Invalid record_type: invalid_type" in str(exc_info.value)


def test_validate_bulk_acc_numbers_empty_df():
    """Test validating an empty DataFrame."""
    df = pd.DataFrame()

    result = validate_bulk_acc_numbers(df, 'commissioner')

    assert result['valid_records'].empty
    assert result['duplicate_records'].empty
    assert result['internal_duplicates'].empty
    assert result['summary']['total_records'] == 0
    assert result['summary']['valid_count'] == 0
    assert result['summary']['duplicate_count'] == 0
    assert result['summary']['internal_duplicate_count'] == 0


def test_validate_bulk_acc_numbers_no_duplicates():
    """Test validating a DataFrame with no duplicates."""
    df = pd.DataFrame({
        'acc_no': [100, 101, 102],
        'department': ['A', 'B', 'C'],
        'file_no': ['F1', 'F2', 'F3']
    })

    with patch('src.utils.acc_no_validator.CommissionerDAO') as mock_dao_class:
        mock_dao_instance = Mock()
        mock_dao_instance.get_all_acc_numbers.return_value = {99, 103, 104}  # No overlap with df
        mock_dao_class.return_value = mock_dao_instance

        result = validate_bulk_acc_numbers(df, 'commissioner')

        assert len(result['valid_records']) == 3
        assert result['duplicate_records'].empty
        assert result['internal_duplicates'].empty
        assert result['summary']['total_records'] == 3
        assert result['summary']['valid_count'] == 3
        assert result['summary']['duplicate_count'] == 0
        assert result['summary']['internal_duplicate_count'] == 0


def test_validate_bulk_acc_numbers_with_db_duplicates():
    """Test validating a DataFrame with acc_no values that exist in the database."""
    df = pd.DataFrame({
        'acc_no': [100, 101, 102],
        'department': ['A', 'B', 'C'],
        'file_no': ['F1', 'F2', 'F3']
    })

    with patch('src.utils.acc_no_validator.CommissionerDAO') as mock_dao_class:
        mock_dao_instance = Mock()
        mock_dao_instance.get_all_acc_numbers.return_value = {100, 103}  # 100 exists in DB
        mock_dao_class.return_value = mock_dao_instance

        result = validate_bulk_acc_numbers(df, 'commissioner')

        assert len(result['valid_records']) == 2  # 101, 102
        assert len(result['duplicate_records']) == 1  # 100
        assert result['internal_duplicates'].empty
        assert result['summary']['total_records'] == 3
        assert result['summary']['valid_count'] == 2
        assert result['summary']['duplicate_count'] == 1
        assert result['summary']['internal_duplicate_count'] == 0


def test_validate_bulk_acc_numbers_with_internal_duplicates():
    """Test validating a DataFrame with internal duplicate acc_no values."""
    df = pd.DataFrame({
        'acc_no': [100, 101, 100],  # 100 appears twice
        'department': ['A', 'B', 'C'],
        'file_no': ['F1', 'F2', 'F3']
    })

    with patch('src.utils.acc_no_validator.CommissionerDAO') as mock_dao_class:
        mock_dao_instance = Mock()
        mock_dao_instance.get_all_acc_numbers.return_value = {102, 103}  # No overlap with df
        mock_dao_class.return_value = mock_dao_instance

        result = validate_bulk_acc_numbers(df, 'commissioner')

        # Only 101 is valid (not in DB and appears only once), 100 entries are internal duplicates
        assert len(result['valid_records']) == 1  # 101 is valid
        assert result['duplicate_records'].empty  # No DB duplicates
        assert len(result['internal_duplicates']) == 2  # Both 100 entries
        assert result['summary']['total_records'] == 3
        assert result['summary']['valid_count'] == 1  # Only 101 is valid
        assert result['summary']['duplicate_count'] == 0
        assert result['summary']['internal_duplicate_count'] == 2


def test_validate_bulk_acc_numbers_with_both_duplicate_types():
    """Test validating a DataFrame with both DB and internal duplicates."""
    df = pd.DataFrame({
        'acc_no': [100, 101, 100, 102],  # 100 is internal duplicate, 102 exists in DB
        'department': ['A', 'B', 'C', 'D'],
        'file_no': ['F1', 'F2', 'F3', 'F4']
    })

    with patch('src.utils.acc_no_validator.CommissionerDAO') as mock_dao_class:
        mock_dao_instance = Mock()
        mock_dao_instance.get_all_acc_numbers.return_value = {102, 103}  # 102 exists in DB
        mock_dao_class.return_value = mock_dao_instance

        result = validate_bulk_acc_numbers(df, 'commissioner')

        assert len(result['valid_records']) == 1  # Only 101 is valid
        assert len(result['duplicate_records']) == 1  # 102 exists in DB
        assert len(result['internal_duplicates']) == 2  # Both 100 entries
        assert result['summary']['total_records'] == 4
        assert result['summary']['valid_count'] == 1
        assert result['summary']['duplicate_count'] == 1
        assert result['summary']['internal_duplicate_count'] == 2