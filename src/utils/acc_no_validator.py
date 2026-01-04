"""
Acc No Validator - Utility functions for validating acc_no uniqueness.

This module provides functions for checking if acc_no values already exist in the database
for both commissioner and court records.
"""
from typing import List, Set, Dict, Any
import pandas as pd
from src.dao.commissioner_dao import CommissionerDAO
from src.dao.court_dao import CourtDAO


def validate_single_acc_no(acc_no: int, record_type: str) -> tuple[bool, str]:
    """
    Validate if a single acc_no exists in the specified record type table.

    Args:
        acc_no: The account number to validate
        record_type: 'commissioner' or 'court'

    Returns:
        Tuple of (is_valid, error_message)
    """
    if record_type == 'commissioner':
        dao = CommissionerDAO()
        existing_records = dao.get_by_acc_no(acc_no)
        if existing_records:
            return False, f"❌ This acc_no ({acc_no}) already exists in Commissioner Records. Please use a different acc_no."
    elif record_type == 'court':
        dao = CourtDAO()
        existing_records = dao.get_by_acc_no(acc_no)
        if existing_records:
            return False, f"❌ This acc_no ({acc_no}) already exists in Court Records. Please use a different acc_no."
    else:
        raise ValueError(f"Invalid record_type: {record_type}. Must be 'commissioner' or 'court'.")

    return True, ""


def validate_bulk_acc_numbers(df: pd.DataFrame, record_type: str) -> Dict[str, Any]:
    """
    Validate acc_no uniqueness for bulk upload and categorize records.

    Args:
        df: DataFrame containing records to validate
        record_type: 'commissioner' or 'court'

    Returns:
        Dictionary with validation results containing:
        - valid_records: DataFrame with unique acc_no values
        - duplicate_records: DataFrame with acc_no values that already exist in DB
        - internal_duplicates: DataFrame with acc_no values that are duplicated within the upload
        - summary: Dictionary with counts
    """
    if df.empty:
        return {
            'valid_records': pd.DataFrame(),
            'duplicate_records': pd.DataFrame(),
            'internal_duplicates': pd.DataFrame(),
            'summary': {
                'total_records': 0,
                'valid_count': 0,
                'duplicate_count': 0,
                'internal_duplicate_count': 0
            }
        }

    # Get all acc_no values from the dataframe
    acc_no_column = 'acc_no'
    if acc_no_column not in df.columns:
        raise ValueError(f"Column '{acc_no_column}' not found in DataFrame")

    # Identify internal duplicates (duplicates within the uploaded file)
    internal_duplicate_mask = df.duplicated(subset=[acc_no_column], keep=False)
    internal_duplicates_df = df[internal_duplicate_mask].copy()

    # Get unique acc_no values from the dataframe (excluding internal duplicates)
    unique_acc_nos_from_file = set(df[acc_no_column].unique())

    # Get all existing acc_no values from the database for this record type
    if record_type == 'commissioner':
        dao = CommissionerDAO()
    elif record_type == 'court':
        dao = CourtDAO()
    else:
        raise ValueError(f"Invalid record_type: {record_type}. Must be 'commissioner' or 'court'.")

    # Get all existing acc_no values from the database using the DAO method
    existing_acc_nos = dao.get_all_acc_numbers()

    # Identify which acc_no values from the file already exist in the database
    duplicate_acc_nos = unique_acc_nos_from_file.intersection(existing_acc_nos)

    # Create masks for different categories
    duplicate_mask = df[acc_no_column].isin(duplicate_acc_nos)
    valid_mask = ~duplicate_mask & ~internal_duplicate_mask

    # Separate the dataframes
    valid_records_df = df[valid_mask].copy()
    duplicate_records_df = df[duplicate_mask].copy()

    # Create summary
    summary = {
        'total_records': len(df),
        'valid_count': len(valid_records_df),
        'duplicate_count': len(duplicate_records_df),
        'internal_duplicate_count': len(internal_duplicates_df)
    }

    return {
        'valid_records': valid_records_df,
        'duplicate_records': duplicate_records_df,
        'internal_duplicates': internal_duplicates_df,
        'summary': summary
    }