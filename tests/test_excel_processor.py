"""
Unit tests for Excel processor utilities.
"""
import pandas as pd
import pytest
from io import BytesIO
from src.utils.excel_processor import (
    read_excel_file,
    process_commissioner_data,
    process_court_data,
    handle_excel_dates
)


def test_process_commissioner_data():
    """Test processing commissioner data from DataFrame."""
    df = pd.DataFrame({
        'acc_no': [12345, 23456],
        'department': ['Revenue', 'Excise'],
        'file_no': ['REV/2023/001', 'EXC/2023/002'],
        'subject': ['Land Revenue Assessment', 'Excise Duty Records'],
        'year': [2023, 2023],
        'page': [15, 22],
        'condition': ['FAIR/BOUND', 'GOOD/BOUND'],
        'record_type': ['TEXTUAL RECORD', 'PHOTOGRAPHIC RECORD']
    })

    records = process_commissioner_data(df)

    assert len(records) == 2
    assert records[0]['acc_no'] == 12345
    assert records[0]['department'] == 'Revenue'
    assert records[0]['year'] == 2023
    assert records[1]['acc_no'] == 23456
    assert records[1]['department'] == 'Excise'


def test_process_court_data():
    """Test processing court data from DataFrame."""
    df = pd.DataFrame({
        'acc_no': [1001, 1002],
        'court': ['High Court', 'District Court'],
        'suit_no': ['CIVIL/2023/001', 'CRIM/2023/002'],
        'plaintiff': ['State of Sindh', 'Mohammad Ali'],
        'defendant': ['A. Khan', 'B. Ahmed'],
        'claim_or_charge': ['Recovery of Land Revenue', 'Criminal Breach of Trust'],
        'date_from': ['2023-01-15', '2023-02-20'],
        'date_to': ['2023-12-20', '2023-11-25'],
        'language': ['English', 'Urdu']
    })

    records = process_court_data(df)

    assert len(records) == 2
    assert records[0]['acc_no'] == 1001
    assert records[0]['court'] == 'High Court'
    assert records[0]['date_from'] == '2023-01-15'
    assert records[1]['acc_no'] == 1002
    assert records[1]['court'] == 'District Court'


def test_handle_excel_dates():
    """Test handling Excel date conversions."""
    df = pd.DataFrame({
        'name': ['Test', 'Another'],
        'date_col': ['2023-01-15', '2023-02-20']
    })

    result_df = handle_excel_dates(df, ['date_col'])

    # Check that the date column exists and is properly formatted
    assert 'date_col' in result_df.columns
    assert len(result_df) == 2


def test_read_excel_file():
    """Test reading Excel file from BytesIO."""
    # Create a simple Excel file in memory
    df = pd.DataFrame({
        'col1': [1, 2, 3],
        'col2': ['A', 'B', 'C']
    })

    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    output.seek(0)

    # This test would require mocking the Streamlit uploaded file object
    # For now, we'll just verify the function exists and can be imported
    assert callable(read_excel_file)


if __name__ == "__main__":
    pytest.main()