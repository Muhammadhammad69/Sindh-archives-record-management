"""
Unit tests for Excel validator utilities.
"""
import pandas as pd
import pytest
from src.utils.excel_validator import (
    validate_commissioner_columns,
    validate_court_columns,
    validate_commissioner_data,
    validate_court_data
)


def test_validate_commissioner_columns_valid():
    """Test that valid commissioner columns pass validation."""
    df = pd.DataFrame({
        'acc_no': [12345],
        'department': ['Revenue'],
        'file_no': ['REV/2023/001'],
        'subject': ['Land Revenue Assessment'],
        'year': [2023],
        'page': [15],
        'condition': ['FAIR/BOUND'],
        'record_type': ['TEXTUAL RECORD']
    })

    is_valid, missing_columns = validate_commissioner_columns(df)
    assert is_valid is True
    assert missing_columns == []


def test_validate_commissioner_columns_missing():
    """Test that missing commissioner columns are detected."""
    df = pd.DataFrame({
        'acc_no': [12345],
        'department': ['Revenue'],
        # Missing required columns: file_no, subject, year, page, condition, record_type
    })

    is_valid, missing_columns = validate_commissioner_columns(df)
    assert is_valid is False
    expected_missing = ['file_no', 'subject', 'year', 'page', 'condition', 'record_type']
    assert set(missing_columns) == set(expected_missing)


def test_validate_court_columns_valid():
    """Test that valid court columns pass validation."""
    df = pd.DataFrame({
        'acc_no': [1001],
        'court': ['High Court'],
        'suit_no': ['CIVIL/2023/001'],
        'plaintiff': ['State of Sindh'],
        'defendant': ['A. Khan'],
        'claim_or_charge': ['Recovery of Land Revenue'],
        'date_from': ['2023-01-15'],
        'date_to': ['2023-12-20'],
        'language': ['English']
    })

    is_valid, missing_columns = validate_court_columns(df)
    assert is_valid is True
    assert missing_columns == []


def test_validate_court_columns_missing():
    """Test that missing court columns are detected."""
    df = pd.DataFrame({
        'acc_no': [1001],
        'court': ['High Court'],
        # Missing required columns: suit_no, plaintiff, defendant, claim_or_charge, date_from, date_to, language
    })

    is_valid, missing_columns = validate_court_columns(df)
    assert is_valid is False
    expected_missing = ['suit_no', 'plaintiff', 'defendant', 'claim_or_charge', 'date_from', 'date_to', 'language']
    assert set(missing_columns) == set(expected_missing)


def test_validate_commissioner_data_valid():
    """Test that valid commissioner data passes validation."""
    df = pd.DataFrame({
        'acc_no': [12345],
        'department': ['Revenue'],
        'file_no': ['REV/2023/001'],
        'subject': ['Land Revenue Assessment'],
        'year': [2023],
        'page': [15],
        'condition': ['FAIR/BOUND'],
        'record_type': ['TEXTUAL RECORD']
    })

    errors = validate_commissioner_data(df)
    assert errors == []


def test_validate_commissioner_data_invalid_acc_no():
    """Test that invalid acc_no is detected."""
    df = pd.DataFrame({
        'acc_no': [-1],  # Invalid: negative
        'department': ['Revenue'],
        'file_no': ['REV/2023/001'],
        'subject': ['Land Revenue Assessment'],
        'year': [2023],
        'page': [15],
        'condition': ['FAIR/BOUND'],
        'record_type': ['TEXTUAL RECORD']
    })

    errors = validate_commissioner_data(df)
    assert len(errors) == 1
    assert errors[0]['field_name'] == 'acc_no'
    assert 'positive integer' in errors[0]['error_message']


def test_validate_court_data_valid():
    """Test that valid court data passes validation."""
    df = pd.DataFrame({
        'acc_no': [1001],
        'court': ['High Court'],
        'suit_no': ['CIVIL/2023/001'],
        'plaintiff': ['State of Sindh'],
        'defendant': ['A. Khan'],
        'claim_or_charge': ['Recovery of Land Revenue'],
        'date_from': ['2023-01-15'],
        'date_to': ['2023-12-20'],
        'language': ['English']
    })

    errors = validate_court_data(df)
    assert errors == []


def test_validate_court_data_invalid_date_range():
    """Test that invalid date range is detected."""
    df = pd.DataFrame({
        'acc_no': [1001],
        'court': ['High Court'],
        'suit_no': ['CIVIL/2023/001'],
        'plaintiff': ['State of Sindh'],
        'defendant': ['A. Khan'],
        'claim_or_charge': ['Recovery of Land Revenue'],
        'date_from': ['2023-12-20'],  # Later date
        'date_to': ['2023-01-15'],    # Earlier date
        'language': ['English']
    })

    errors = validate_court_data(df)
    assert len(errors) == 1
    assert errors[0]['field_name'] == 'date_range'
    assert 'after' in errors[0]['error_message']


if __name__ == "__main__":
    pytest.main()