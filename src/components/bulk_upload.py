"""
Reusable bulk upload component for handling Excel file uploads with validation,
preview, and progress tracking for both commissioner and court records.
"""
import streamlit as st
import pandas as pd
from typing import List, Dict, Any, Optional, Callable
from io import BytesIO
from src.utils.excel_validator import (
    validate_commissioner_columns, validate_court_columns,
    validate_commissioner_data, validate_court_data
)
from src.utils.excel_processor import (
    read_excel_file, process_commissioner_data, process_court_data
)


class BulkUploadHandler:
    """
    Reusable component for handling bulk upload functionality.
    """

    def __init__(self, record_type: str, max_rows: int = 1000, batch_size: int = 50):
        """
        Initialize the bulk upload handler.

        Args:
            record_type: "commissioner" or "court"
            max_rows: Maximum number of rows allowed (default: 1000)
            batch_size: Number of records to process per batch (default: 50)
        """
        self.record_type = record_type
        self.max_rows = max_rows
        self.batch_size = batch_size

        # Set validation functions based on record type
        if record_type == "commissioner":
            self.validate_columns_func = validate_commissioner_columns
            self.validate_data_func = validate_commissioner_data
            self.process_data_func = process_commissioner_data
        elif record_type == "court":
            self.validate_columns_func = validate_court_columns
            self.validate_data_func = validate_court_data
            self.process_data_func = process_court_data
        else:
            raise ValueError("record_type must be 'commissioner' or 'court'")

    def upload_file(self) -> Optional[BytesIO]:
        """
        Handle file upload with type restrictions.

        Returns:
            Uploaded file as BytesIO object or None if no file uploaded
        """
        allowed_types = ["xlsx", "xls"]

        uploaded_file = st.file_uploader(
            f"Upload Excel file ({self.record_type} records)",
            type=allowed_types,
            help=f"Upload an Excel file (.xlsx or .xls) containing {self.record_type} records"
        )

        if uploaded_file is not None:
            # Check file size (optional)
            file_size_mb = len(uploaded_file.getvalue()) / (1024 * 1024)
            if file_size_mb > 10:  # 10MB limit
                st.warning("File is large. This may take a moment to process.")

        return uploaded_file

    def validate_file(self, uploaded_file) -> Dict[str, Any]:
        """
        Validate the uploaded Excel file for structure and content.

        Args:
            uploaded_file: Streamlit uploaded file object

        Returns:
            Dictionary with validation results
        """
        result = {
            'valid': False,
            'data': None,
            'column_errors': [],
            'data_errors': [],
            'row_count': 0
        }

        try:
            # Read Excel file
            df = read_excel_file(uploaded_file)
            result['row_count'] = len(df)

            # Check row limit
            if result['row_count'] > self.max_rows:
                result['column_errors'].append(f"File has {result['row_count']} rows, which exceeds the limit of {self.max_rows} rows")
                return result

            # Validate column structure
            columns_valid, missing_columns = self.validate_columns_func(df)
            if not columns_valid:
                result['column_errors'] = [f"Missing required columns: {', '.join(missing_columns)}"]
                return result

            # Validate data content
            data_errors = self.validate_data_func(df)
            result['data_errors'] = data_errors

            # If no errors, set data
            if len(result['data_errors']) == 0:
                result['valid'] = True
                result['data'] = df

        except Exception as e:
            result['column_errors'] = [f"Error reading file: {str(e)}"]

        return result

    def preview_data(self, df: pd.DataFrame, num_rows: int = 5) -> None:
        """
        Display a preview of the Excel data.

        Args:
            df: DataFrame to preview
            num_rows: Number of rows to display (default: 5)
        """
        st.subheader("Data Preview")
        st.info(f"File contains {len(df)} records. Showing first {min(num_rows, len(df))} rows:")
        st.dataframe(df.head(num_rows))

    def bulk_insert(self, df: pd.DataFrame, dao: Any, progress_callback: Optional[Callable] = None) -> Dict[str, Any]:
        """
        Perform bulk insertion of records with progress tracking.

        Args:
            df: DataFrame containing validated records
            dao: Data Access Object for insertion
            progress_callback: Optional callback for progress updates

        Returns:
            Dictionary with insertion results
        """
        results = {
            'success_count': 0,
            'error_count': 0,
            'errors': [],
            'total_records': len(df)
        }

        # Process records in batches
        records = self.process_data_func(df)

        # Create progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()

        total_batches = (len(records) + self.batch_size - 1) // self.batch_size

        for batch_idx, i in enumerate(range(0, len(records), self.batch_size)):
            batch = records[i:i + self.batch_size]

            # Update progress
            progress = (batch_idx + 1) / total_batches
            progress_bar.progress(progress)
            status_text.text(f"Processing batch {batch_idx + 1}/{total_batches}...")

            # Process each record in the batch
            for j, record_data in enumerate(batch):
                try:
                    # Call the DAO's create method
                    dao.create(record_data)
                    results['success_count'] += 1
                except Exception as e:
                    results['error_count'] += 1
                    error_info = {
                        'row_number': i + j + 2,  # +2 for 1-indexed Excel + header row
                        'error': str(e),
                        'record_data': record_data
                    }
                    results['errors'].append(error_info)

            # Update progress text with counts
            status_text.text(f"Processed {min(i + self.batch_size, len(records))}/{len(records)} records | "
                            f"Success: {results['success_count']} | Errors: {results['error_count']}")

        # Clear progress indicators
        progress_bar.empty()
        status_text.empty()

        return results