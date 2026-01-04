"""
Report Generator - Utility functions for generating comprehensive reports for duplicate detection.

This module provides functions for creating detailed reports about duplicate acc_no values
during bulk uploads.
"""
from typing import Dict, Any, List
import pandas as pd


def generate_comprehensive_report(
    valid_records: pd.DataFrame,
    duplicate_records: pd.DataFrame,
    internal_duplicates: pd.DataFrame,
    record_type: str
) -> Dict[str, Any]:
    """
    Generate a comprehensive report of bulk upload validation results.

    Args:
        valid_records: DataFrame containing records that can be inserted
        duplicate_records: DataFrame containing records with acc_no that already exist in DB
        internal_duplicates: DataFrame containing records with acc_no duplicated within the upload
        record_type: 'commissioner' or 'court' - type of records being processed

    Returns:
        Dictionary containing comprehensive report information
    """
    # Calculate summary statistics
    total_records = len(valid_records) + len(duplicate_records) + len(internal_duplicates)

    report = {
        'summary': {
            'total_records': total_records,
            'valid_records': len(valid_records),
            'duplicate_records': len(duplicate_records),
            'internal_duplicate_records': len(internal_duplicates),
            'record_type': record_type,
            'success_rate': len(valid_records) / total_records if total_records > 0 else 0
        },
        'details': {
            'valid_records_sample': valid_records.head(5).to_dict('records') if not valid_records.empty else [],
            'duplicate_records_sample': duplicate_records.head(5).to_dict('records') if not duplicate_records.empty else [],
            'internal_duplicate_records_sample': internal_duplicates.head(5).to_dict('records') if not internal_duplicates.empty else []
        },
        'recommendations': []
    }

    # Add recommendations based on the validation results
    if len(duplicate_records) > 0:
        report['recommendations'].append(
            f"Review the {len(duplicate_records)} records with acc_no values that already exist in the {record_type} records table."
        )

    if len(internal_duplicates) > 0:
        report['recommendations'].append(
            f"Review the {len(internal_duplicates)} records with acc_no values that are duplicated within the uploaded file."
        )

    if len(valid_records) == 0 and total_records > 0:
        report['recommendations'].append(
            "All records in the upload have duplicate acc_no values. Consider reviewing the source data."
        )
    elif len(valid_records) > 0:
        report['recommendations'].append(
            f"{len(valid_records)} records can be successfully inserted. Proceed with bulk upload after review."
        )

    return report