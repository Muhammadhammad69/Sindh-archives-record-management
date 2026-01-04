"""
Unit tests for duplicate_detector utility functions.
"""
import pytest
import pandas as pd
from src.utils.duplicate_detector import detect_excel_duplicates, categorize_records, generate_skip_report


def test_detect_excel_duplicates_no_duplicates():
    """Test detecting duplicates in a DataFrame with no duplicates."""
    df = pd.DataFrame({
        'acc_no': [100, 101, 102],
        'department': ['A', 'B', 'C']
    })

    result = detect_excel_duplicates(df)

    assert result['has_duplicates'] is False
    assert result['duplicate_count'] == 0
    assert result['duplicate_rows'].empty
    assert result['duplicate_acc_nos'] == []


def test_detect_excel_duplicates_with_duplicates():
    """Test detecting duplicates in a DataFrame with duplicate acc_no values."""
    df = pd.DataFrame({
        'acc_no': [100, 101, 100, 102],  # 100 appears twice
        'department': ['A', 'B', 'C', 'D']
    })

    result = detect_excel_duplicates(df)

    assert result['has_duplicates'] is True
    assert result['duplicate_count'] == 1  # Only one acc_no value is duplicated
    assert len(result['duplicate_rows']) == 2  # Both rows with acc_no 100
    assert result['duplicate_acc_nos'] == [100]


def test_detect_excel_duplicates_empty_df():
    """Test detecting duplicates in an empty DataFrame."""
    df = pd.DataFrame()

    result = detect_excel_duplicates(df)

    assert result['has_duplicates'] is False
    assert result['duplicate_count'] == 0
    assert result['duplicate_rows'].empty
    assert result['duplicate_acc_nos'] == []


def test_detect_excel_duplicates_missing_acc_no_column():
    """Test detecting duplicates when acc_no column is missing."""
    df = pd.DataFrame({
        'id': [1, 2, 3],
        'department': ['A', 'B', 'C']
    })

    result = detect_excel_duplicates(df)

    assert result['has_duplicates'] is False
    assert result['duplicate_count'] == 0
    assert result['duplicate_rows'].empty
    assert result['duplicate_acc_nos'] == []


def test_categorize_records_all_valid():
    """Test categorizing records where all are valid."""
    df = pd.DataFrame({
        'acc_no': [100, 101, 102],
        'department': ['A', 'B', 'C']
    })
    existing_acc_nos = {99, 103, 104}  # No overlap with df

    result = categorize_records(df, existing_acc_nos)

    assert len(result['valid']) == 3
    assert result['duplicate'].empty
    assert set(result['valid']['acc_no'].values) == {100, 101, 102}


def test_categorize_records_all_duplicate():
    """Test categorizing records where all are duplicates."""
    df = pd.DataFrame({
        'acc_no': [100, 101, 102],
        'department': ['A', 'B', 'C']
    })
    existing_acc_nos = {100, 101, 102}  # All in df exist in DB

    result = categorize_records(df, existing_acc_nos)

    assert result['valid'].empty
    assert len(result['duplicate']) == 3
    assert set(result['duplicate']['acc_no'].values) == {100, 101, 102}


def test_categorize_records_mixed():
    """Test categorizing records with a mix of valid and duplicate."""
    df = pd.DataFrame({
        'acc_no': [100, 101, 102, 103],
        'department': ['A', 'B', 'C', 'D']
    })
    existing_acc_nos = {100, 102}  # 100 and 102 exist in DB

    result = categorize_records(df, existing_acc_nos)

    assert len(result['valid']) == 2  # 101 and 103
    assert len(result['duplicate']) == 2  # 100 and 102
    assert set(result['valid']['acc_no'].values) == {101, 103}
    assert set(result['duplicate']['acc_no'].values) == {100, 102}


def test_categorize_records_empty_df():
    """Test categorizing records with an empty DataFrame."""
    df = pd.DataFrame()
    existing_acc_nos = {100, 101, 102}

    result = categorize_records(df, existing_acc_nos)

    assert result['valid'].empty
    assert result['duplicate'].empty


def test_categorize_records_missing_acc_no_column():
    """Test categorizing records when acc_no column is missing."""
    df = pd.DataFrame({
        'id': [1, 2, 3],
        'department': ['A', 'B', 'C']
    })
    existing_acc_nos = {100, 101, 102}

    result = categorize_records(df, existing_acc_nos)

    assert result['valid'].empty
    assert result['duplicate'].empty


def test_generate_skip_report_empty():
    """Test generating a skip report from an empty DataFrame."""
    df = pd.DataFrame()

    report = generate_skip_report(df)

    assert report.empty


def test_generate_skip_report_with_data():
    """Test generating a skip report from a DataFrame with data."""
    df = pd.DataFrame({
        'acc_no': [100, 101, 102],
        'department': ['A', 'B', 'C'],
        'file_no': ['F1', 'F2', 'F3']
    })

    report = generate_skip_report(df, "Test reason")

    assert len(report) == 3
    assert list(report['acc_no']) == [100, 101, 102]
    assert list(report['skip_reason']) == ["Test reason", "Test reason", "Test reason"]
    assert list(report['row_number']) == [2, 3, 4]  # Starting from 2 (header row + 1)
    assert 'department' in report.columns
    assert 'file_no' in report.columns


def test_generate_skip_report_custom_reason():
    """Test generating a skip report with a custom reason."""
    df = pd.DataFrame({
        'acc_no': [100],
        'department': ['A']
    })

    report = generate_skip_report(df, "Custom duplicate reason")

    assert len(report) == 1
    assert report['skip_reason'].iloc[0] == "Custom duplicate reason"
    assert report['row_number'].iloc[0] == 2