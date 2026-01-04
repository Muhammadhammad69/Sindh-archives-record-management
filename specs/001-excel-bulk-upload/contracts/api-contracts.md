# API Contracts: Excel Bulk Upload

## Excel Validation API

### validate_commissioner_columns(df: DataFrame) -> tuple[bool, list[str]]
**Purpose**: Validates that the Excel DataFrame contains all required columns for commissioner records
**Input**: pandas DataFrame with Excel data
**Output**:
- boolean: True if all required columns present, False otherwise
- list[str]: List of missing column names if validation fails

**Required Columns**:
- acc_no
- department
- file_no
- subject
- year
- page
- condition
- record_type

### validate_court_columns(df: DataFrame) -> tuple[bool, list[str]]
**Purpose**: Validates that the Excel DataFrame contains all required columns for court records
**Input**: pandas DataFrame with Excel data
**Output**:
- boolean: True if all required columns present, False otherwise
- list[str]: List of missing column names if validation fails

**Required Columns**:
- acc_no
- court
- suit_no
- plaintiff
- defendant
- claim_or_charge
- date_from
- date_to
- language

### validate_commissioner_data(df: DataFrame) -> list[dict]
**Purpose**: Validates data content in commissioner record DataFrame
**Input**: pandas DataFrame with Excel data
**Output**: List of validation errors with details
**Error Format**:
```python
[
    {
        "row_number": int,
        "field_name": str,
        "error_message": str,
        "original_value": str,
        "error_type": str
    }
]
```

### validate_court_data(df: DataFrame) -> list[dict]
**Purpose**: Validates data content in court record DataFrame
**Input**: pandas DataFrame with Excel data
**Output**: List of validation errors with details (same format as above)

## Excel Processing API

### read_excel_file(uploaded_file) -> DataFrame
**Purpose**: Reads Excel file from Streamlit upload component
**Input**: Streamlit uploaded file object
**Output**: pandas DataFrame with Excel data
**Error Handling**: Raises ValueError for invalid file formats

### process_commissioner_data(df: DataFrame) -> list[CommissionerRecord]
**Purpose**: Converts validated DataFrame to list of CommissionerRecord objects
**Input**: Validated pandas DataFrame
**Output**: List of CommissionerRecord objects ready for database insertion

### process_court_data(df: DataFrame) -> list[CourtRecord]
**Purpose**: Converts validated DataFrame to list of CourtRecord objects
**Input**: Validated pandas DataFrame
**Output**: List of CourtRecord objects ready for database insertion

### handle_excel_dates(df: DataFrame, date_columns: list) -> DataFrame
**Purpose**: Converts Excel date formats to Python datetime objects
**Input**:
- DataFrame with date columns
- List of column names containing dates
**Output**: DataFrame with properly formatted date columns

## Template Generation API

### generate_commissioner_template() -> BytesIO
**Purpose**: Creates Excel template for commissioner records with headers
**Output**: BytesIO object containing Excel file with headers and sample data

### generate_court_template() -> BytesIO
**Purpose**: Creates Excel template for court records with headers
**Output**: BytesIO object containing Excel file with headers and sample data

## Bulk Upload Component API

### BulkUploadHandler class
**Purpose**: Reusable component for handling bulk upload functionality

**Methods**:
- upload_file() -> FileUploadResult
- validate_file(file) -> ValidationResult
- preview_data(df) -> DataPreview
- bulk_insert(records) -> InsertResult

**Configuration Options**:
- record_type: "commissioner" or "court"
- max_rows: Maximum number of rows allowed (default: 1000)
- batch_size: Number of records to process per batch (default: 50)

## Streamlit UI Integration

### Mode Selection
**Component**: st.radio with options ["Add Single Record", "Upload Excel File"]
**Purpose**: Allows user to choose between single record entry and bulk upload

### File Upload
**Component**: st.file_uploader with type restrictions [".xlsx", ".xls"]
**Purpose**: Securely uploads Excel files with format validation

### Progress Tracking
**Components**: st.progress() and st.spinner() for visual feedback
**Purpose**: Shows progress during validation and insertion operations

### Error Display
**Components**: st.error() and st.dataframe() for validation errors
**Purpose**: Displays validation errors with row numbers and details

### Template Download
**Component**: st.download_button for Excel templates
**Purpose**: Allows users to download properly formatted Excel templates