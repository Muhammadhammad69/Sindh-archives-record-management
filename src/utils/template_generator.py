"""
Excel template generation utilities for creating downloadable Excel templates
for commissioner and court records.
"""
import pandas as pd
from io import BytesIO


def generate_commissioner_template() -> BytesIO:
    """
    Create Excel template for commissioner records with headers and sample data.

    Returns:
        BytesIO object containing Excel file with headers and sample data
    """
    # Create sample data for commissioner records
    sample_data = {
        'acc_no': [12345, 23456, 34567],
        'department': ['Revenue', 'Excise', 'Registration'],
        'file_no': ['REV/2023/001', 'EXC/2023/002', 'REG/2023/003'],
        'subject': [
            'Land Revenue Assessment',
            'Excise Duty Records',
            'Property Registration Documents'
        ],
        'year': [2023, 2023, 2024],
        'page': [15, 22, 8],
        'condition': ['FAIR/BOUND', 'GOOD/BOUND', 'EXCELLENT/BOUND'],
        'record_type': ['TEXTUAL RECORD', 'PHOTOGRAPHIC RECORD', 'DIGITAL RECORD']
    }

    df = pd.DataFrame(sample_data)

    # Create BytesIO object
    output = BytesIO()

    # Write DataFrame to Excel in memory
    with pd.ExcelWriter(output, engine='openpyxl', mode='xlsx') as writer:
        df.to_excel(writer, index=False, sheet_name='Commissioner Records')

    # Seek to the beginning of the stream
    output.seek(0)

    return output


def generate_court_template() -> BytesIO:
    """
    Create Excel template for court records with headers and sample data.

    Returns:
        BytesIO object containing Excel file with headers and sample data
    """
    # Create sample data for court records
    sample_data = {
        'acc_no': [1001, 1002, 1003],
        'court': ['High Court', 'District Court', 'Sessions Court'],
        'suit_no': ['CIVIL/2023/001', 'CRIM/2023/002', 'CIVIL/2023/003'],
        'plaintiff': ['State of Sindh', 'Mohammad Ali', 'Karachi Development Authority'],
        'defendant': ['A. Khan', 'B. Ahmed', 'C. Properties Ltd.'],
        'claim_or_charge': [
            'Recovery of Land Revenue',
            'Criminal Breach of Trust',
            'Property Dispute'
        ],
        'date_from': ['2023-01-15', '2023-02-20', '2023-03-10'],
        'date_to': ['2023-12-20', '2023-11-25', '2024-01-15'],
        'language': ['English', 'Urdu', 'English']
    }

    df = pd.DataFrame(sample_data)

    # Create BytesIO object
    output = BytesIO()

    # Write DataFrame to Excel in memory
    with pd.ExcelWriter(output, engine='openpyxl', mode='xlsx') as writer:
        df.to_excel(writer, index=False, sheet_name='Court Records')

    # Seek to the beginning of the stream
    output.seek(0)

    return output