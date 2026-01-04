"""
Excel validation utilities for validating column structure and data content
for commissioner and court records Excel files.
"""
import pandas as pd
from typing import Tuple, List, Dict, Any


def validate_commissioner_columns(df: pd.DataFrame) -> Tuple[bool, List[str]]:
    """
    Validate that the Excel DataFrame contains all required columns for commissioner records.

    Args:
        df: pandas DataFrame containing Excel data

    Returns:
        Tuple of (is_valid, list_of_missing_columns)
    """
    required_columns = {
        'acc_no', 'department', 'file_no', 'subject',
        'year', 'page', 'condition', 'record_type'
    }

    actual_columns = set(str(col).strip().lower() for col in df.columns)

    # Check for required columns (case-insensitive)
    missing_columns = []
    for req_col in required_columns:
        if not any(actual_col == req_col for actual_col in actual_columns):
            missing_columns.append(req_col)

    return len(missing_columns) == 0, missing_columns


def validate_court_columns(df: pd.DataFrame) -> Tuple[bool, List[str]]:
    """
    Validate that the Excel DataFrame contains all required columns for court records.

    Args:
        df: pandas DataFrame containing Excel data

    Returns:
        Tuple of (is_valid, list_of_missing_columns)
    """
    required_columns = {
        'acc_no', 'court', 'suit_no', 'plaintiff',
        'defendant', 'claim_or_charge', 'date_from', 'date_to', 'language'
    }

    actual_columns = set(str(col).strip().lower() for col in df.columns)

    # Check for required columns (case-insensitive)
    missing_columns = []
    for req_col in required_columns:
        if not any(actual_col == req_col for actual_col in actual_columns):
            missing_columns.append(req_col)

    return len(missing_columns) == 0, missing_columns


def validate_commissioner_data(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    Validate data content in commissioner record DataFrame.

    Args:
        df: pandas DataFrame containing Excel data

    Returns:
        List of validation errors with details
    """
    errors = []

    for idx, row in df.iterrows():
        row_num = idx + 2  # +2 because Excel rows are 1-indexed and header is row 1

        # Validate required fields are not empty
        required_fields = ['department', 'file_no', 'subject']
        for field in required_fields:
            if field in df.columns:
                value = row[field]
                if pd.isna(value) or (isinstance(value, str) and value.strip() == ""):
                    errors.append({
                        "row_number": row_num,
                        "field_name": field,
                        "error_message": f"{field} is required",
                        "original_value": str(value) if not pd.isna(value) else "",
                        "error_type": "required"
                    })

        # Validate acc_no is positive integer
        if 'acc_no' in df.columns:
            acc_no = row['acc_no']
            try:
                acc_no_int = int(float(acc_no))  # Convert to float first to handle decimal values like 1.0
                if acc_no_int <= 0:
                    errors.append({
                        "row_number": row_num,
                        "field_name": "acc_no",
                        "error_message": "acc_no must be a positive integer",
                        "original_value": str(acc_no),
                        "error_type": "range"
                    })
            except (ValueError, TypeError):
                errors.append({
                    "row_number": row_num,
                    "field_name": "acc_no",
                    "error_message": "acc_no must be a valid integer",
                    "original_value": str(acc_no),
                    "error_type": "format"
                })

        # Validate year is reasonable
        if 'year' in df.columns:
            year = row['year']
            try:
                year_int = int(float(year))
                if year_int < 1800 or year_int > 2100:
                    errors.append({
                        "row_number": row_num,
                        "field_name": "year",
                        "error_message": "year must be between 1800 and 2100",
                        "original_value": str(year),
                        "error_type": "range"
                    })
            except (ValueError, TypeError):
                errors.append({
                    "row_number": row_num,
                    "field_name": "year",
                    "error_message": "year must be a valid integer",
                    "original_value": str(year),
                    "error_type": "format"
                })

        # Validate page is positive integer
        if 'page' in df.columns:
            page = row['page']
            try:
                page_int = int(float(page))
                if page_int <= 0:
                    errors.append({
                        "row_number": row_num,
                        "field_name": "page",
                        "error_message": "page must be a positive integer",
                        "original_value": str(page),
                        "error_type": "range"
                    })
            except (ValueError, TypeError):
                errors.append({
                    "row_number": row_num,
                    "field_name": "page",
                    "error_message": "page must be a valid integer",
                    "original_value": str(page),
                    "error_type": "format"
                })

    return errors


def validate_court_data(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    Validate data content in court record DataFrame.

    Args:
        df: pandas DataFrame containing Excel data

    Returns:
        List of validation errors with details
    """
    errors = []

    for idx, row in df.iterrows():
        row_num = idx + 2  # +2 because Excel rows are 1-indexed and header is row 1

        # Validate required fields are not empty
        required_fields = ['court', 'suit_no', 'plaintiff', 'defendant', 'claim_or_charge', 'language']
        for field in required_fields:
            if field in df.columns:
                value = row[field]
                if pd.isna(value) or (isinstance(value, str) and value.strip() == ""):
                    errors.append({
                        "row_number": row_num,
                        "field_name": field,
                        "error_message": f"{field} is required",
                        "original_value": str(value) if not pd.isna(value) else "",
                        "error_type": "required"
                    })

        # Validate acc_no is positive integer
        if 'acc_no' in df.columns:
            acc_no = row['acc_no']
            try:
                acc_no_int = int(float(acc_no))  # Convert to float first to handle decimal values like 1.0
                if acc_no_int <= 0:
                    errors.append({
                        "row_number": row_num,
                        "field_name": "acc_no",
                        "error_message": "acc_no must be a positive integer",
                        "original_value": str(acc_no),
                        "error_type": "range"
                    })
            except (ValueError, TypeError):
                errors.append({
                    "row_number": row_num,
                    "field_name": "acc_no",
                    "error_message": "acc_no must be a valid integer",
                    "original_value": str(acc_no),
                    "error_type": "format"
                })

        # Validate date_from and date_to
        date_from = None
        date_to = None

        if 'date_from' in df.columns:
            date_from_val = row['date_from']
            if not pd.isna(date_from_val):
                try:
                    # Try to parse the date
                    parsed_date = pd.to_datetime(date_from_val)
                    date_from = parsed_date.date()
                except:
                    errors.append({
                        "row_number": row_num,
                        "field_name": "date_from",
                        "error_message": "date_from must be a valid date (YYYY-MM-DD format)",
                        "original_value": str(date_from_val),
                        "error_type": "format"
                    })

        if 'date_to' in df.columns:
            date_to_val = row['date_to']
            if not pd.isna(date_to_val):
                try:
                    # Try to parse the date
                    parsed_date = pd.to_datetime(date_to_val)
                    date_to = parsed_date.date()
                except:
                    errors.append({
                        "row_number": row_num,
                        "field_name": "date_to",
                        "error_message": "date_to must be a valid date (YYYY-MM-DD format)",
                        "original_value": str(date_to_val),
                        "error_type": "format"
                    })

        # Validate date range if both dates are valid
        if date_from and date_to and date_to < date_from:
            errors.append({
                "row_number": row_num,
                "field_name": "date_range",
                "error_message": "date_to must be after date_from",
                "original_value": f"{date_from} to {date_to}",
                "error_type": "range"
            })

    return errors