"""
Duplicate Detector - Utility functions for detecting duplicate acc_no values in Excel files.

This module provides functions for identifying duplicate acc_no values both within uploaded
files and against existing database records.
"""
from typing import Dict, Any, List
import pandas as pd


def detect_excel_duplicates(df: pd.DataFrame, acc_no_column: str = 'acc_no') -> Dict[str, Any]:
    """
    Detect duplicate acc_no values within an Excel file.

    Args:
        df: DataFrame containing the Excel data
        acc_no_column: Name of the column containing acc_no values (default: 'acc_no')

    Returns:
        Dictionary with duplicate detection results
    """
    if df.empty or acc_no_column not in df.columns:
        return {
            'has_duplicates': False,
            'duplicate_count': 0,
            'duplicate_rows': pd.DataFrame(),
            'duplicate_acc_nos': []
        }

    # Find duplicates within the file
    duplicate_mask = df.duplicated(subset=[acc_no_column], keep=False)
    duplicate_rows = df[duplicate_mask].copy()

    # Get the duplicate acc_no values
    duplicate_acc_nos = df[duplicate_mask][acc_no_column].unique().tolist()

    return {
        'has_duplicates': len(duplicate_acc_nos) > 0,
        'duplicate_count': len(duplicate_acc_nos),
        'duplicate_rows': duplicate_rows,
        'duplicate_acc_nos': duplicate_acc_nos
    }


def categorize_records(df: pd.DataFrame, existing_acc_nos: set, acc_no_column: str = 'acc_no') -> Dict[str, pd.DataFrame]:
    """
    Categorize records into valid and duplicate based on existing acc_no values.

    Args:
        df: DataFrame containing the records to categorize
        existing_acc_nos: Set of acc_no values that already exist in the database
        acc_no_column: Name of the column containing acc_no values (default: 'acc_no')

    Returns:
        Dictionary with categorized DataFrames
    """
    if df.empty or acc_no_column not in df.columns:
        return {
            'valid': pd.DataFrame(),
            'duplicate': pd.DataFrame()
        }

    # Create masks for valid and duplicate records
    duplicate_mask = df[acc_no_column].isin(existing_acc_nos)
    valid_mask = ~duplicate_mask

    return {
        'valid': df[valid_mask].copy(),
        'duplicate': df[duplicate_mask].copy()
    }


def generate_skip_report(duplicate_records_df: pd.DataFrame, reason: str = "Duplicate acc_no in database") -> pd.DataFrame:
    """
    Generate a report of records that will be skipped during bulk upload.

    Args:
        duplicate_records_df: DataFrame containing records that will be skipped
        reason: Reason for skipping the records (default: "Duplicate acc_no in database")

    Returns:
        DataFrame with detailed skip report
    """
    if duplicate_records_df.empty:
        return pd.DataFrame()

    # Create a report with relevant information
    report_df = duplicate_records_df.copy()

    # Add a column to indicate the reason for skipping
    report_df['skip_reason'] = reason

    # Add row numbers (for Excel file reference)
    report_df['row_number'] = range(2, 2 + len(report_df))  # Start from 2 to account for header row

    # Reorder columns to put important ones first
    cols_order = ['row_number', 'acc_no']

    # Add other relevant columns if they exist
    other_cols = [col for col in report_df.columns if col not in cols_order]
    final_cols = cols_order + other_cols

    return report_df[final_cols]