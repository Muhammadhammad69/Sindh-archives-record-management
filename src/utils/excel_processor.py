"""
Excel processing utilities for reading Excel files and converting them to
record objects for database insertion.
"""
import pandas as pd
from typing import List, Dict, Any
from io import BytesIO


def read_excel_file(uploaded_file) -> pd.DataFrame:
    """
    Read Excel file from Streamlit upload component.

    Args:
        uploaded_file: Streamlit uploaded file object

    Returns:
        pandas DataFrame with Excel data

    Raises:
        ValueError: If file format is not supported
    """
    try:
        # Read the Excel file using pandas
        df = pd.read_excel(uploaded_file, engine='openpyxl')
        return df
    except Exception as e:
        # If openpyxl fails, try xlrd for .xls files
        try:
            uploaded_file.seek(0)  # Reset file pointer
            df = pd.read_excel(uploaded_file, engine='xlrd')
            return df
        except Exception:
            raise ValueError(f"Invalid Excel file format: {str(e)}")


def process_commissioner_data(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    Convert validated DataFrame to list of commissioner record dictionaries.

    Args:
        df: Validated pandas DataFrame

    Returns:
        List of dictionaries ready for database insertion
    """
    records = []

    for _, row in df.iterrows():
        record = {
            'acc_no': int(float(row['acc_no'])) if not pd.isna(row['acc_no']) else None,
            'department': str(row['department']).strip() if not pd.isna(row['department']) else '',
            'file_no': str(row['file_no']).strip() if not pd.isna(row['file_no']) else '',
            'subject': str(row['subject']).strip() if not pd.isna(row['subject']) else '',
            'year': int(float(row['year'])) if not pd.isna(row['year']) else None,
            'page': int(float(row['page'])) if not pd.isna(row['page']) else None,
            'condition': str(row['condition']).strip() if not pd.isna(row['condition']) else '',
            'record_type': str(row['record_type']).strip() if not pd.isna(row['record_type']) else '',
        }
        records.append(record)

    return records


def process_court_data(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    Convert validated DataFrame to list of court record dictionaries.

    Args:
        df: Validated pandas DataFrame

    Returns:
        List of dictionaries ready for database insertion
    """
    records = []

    for _, row in df.iterrows():
        # Handle date conversion
        date_from = None
        date_to = None

        if 'date_from' in df.columns and not pd.isna(row['date_from']):
            date_from = pd.to_datetime(row['date_from']).strftime('%Y-%m-%d')

        if 'date_to' in df.columns and not pd.isna(row['date_to']):
            date_to = pd.to_datetime(row['date_to']).strftime('%Y-%m-%d')

        record = {
            'acc_no': int(float(row['acc_no'])) if not pd.isna(row['acc_no']) else None,
            'court': str(row['court']).strip() if not pd.isna(row['court']) else '',
            'suit_no': str(row['suit_no']).strip() if not pd.isna(row['suit_no']) else '',
            'plaintiff': str(row['plaintiff']).strip() if not pd.isna(row['plaintiff']) else '',
            'defendant': str(row['defendant']).strip() if not pd.isna(row['defendant']) else '',
            'claim_or_charge': str(row['claim_or_charge']).strip() if not pd.isna(row['claim_or_charge']) else '',
            'date_from': date_from,
            'date_to': date_to,
            'language': str(row['language']).strip() if not pd.isna(row['language']) else '',
        }
        records.append(record)

    return records


def handle_excel_dates(df: pd.DataFrame, date_columns: List[str]) -> pd.DataFrame:
    """
    Convert Excel date formats to Python datetime objects.

    Args:
        df: pandas DataFrame with potential date columns
        date_columns: List of column names containing dates

    Returns:
        DataFrame with properly formatted date columns
    """
    df_copy = df.copy()

    for col in date_columns:
        if col in df_copy.columns:
            # Convert to datetime, handling various date formats
            df_copy[col] = pd.to_datetime(df_copy[col], errors='coerce')

    return df_copy