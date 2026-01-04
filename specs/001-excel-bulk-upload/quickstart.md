# Quickstart Guide: Excel Bulk Upload

## Prerequisites

- Python 3.11+
- uv package manager
- Existing Phase 1 and 2 infrastructure (database, DAOs, Streamlit app)

## Setup

### 1. Install Dependencies
```bash
# Add Excel processing dependencies to pyproject.toml
[project.dependencies]
openpyxl = ">=3.1.0"
xlrd = ">=2.0.1"

# Install dependencies
uv sync
```

### 2. Verify Installation
```bash
uv run python -c "import openpyxl; import xlrd; import pandas; print('Excel libraries ready')"
```

## File Structure

The implementation adds the following components:

```
src/
├── utils/
│   ├── excel_validator.py    # Column and data validation
│   ├── excel_processor.py    # Excel reading and processing
│   └── template_generator.py # Excel template generation
├── components/
│   └── bulk_upload.py        # Reusable bulk upload component
├── pages/
│   ├── add_commissioner.py   # Dual-mode page (updated)
│   └── add_court.py          # Dual-mode page (updated)
└── templates/
    ├── commissioner_template.xlsx
    └── court_template.xlsx
```

## Usage

### 1. Access Pages
Navigate to either:
- `/add_commissioner` - for commissioner records
- `/add_court` - for court records

### 2. Select Mode
Choose between:
- "Add Single Record" - existing functionality
- "Upload Excel File" - new bulk upload functionality

### 3. For Bulk Upload

#### Download Template
- Click "Download Template" to get the correct Excel format
- Fill in the required columns with your data

#### Upload File
- Use the file uploader to select your .xlsx or .xls file
- Supported formats: .xlsx, .xls

#### Validation
- Column validation occurs first
- Data validation follows with detailed error reporting
- Preview shows first 5 rows of your data

#### Processing
- Confirm bulk insertion
- Monitor progress with progress bar
- View success/error summary after completion

## API Contracts

### Excel Validator Functions
```python
validate_commissioner_columns(df: DataFrame) -> tuple[bool, list[str]]
validate_court_columns(df: DataFrame) -> tuple[bool, list[str]]
validate_commissioner_data(df: DataFrame) -> list[dict]
validate_court_data(df: DataFrame) -> list[dict]
```

### Excel Processor Functions
```python
read_excel_file(uploaded_file) -> DataFrame
process_commissioner_data(df: DataFrame) -> list[CommissionerRecord]
process_court_data(df: DataFrame) -> list[CourtRecord]
```

### Template Generator Functions
```python
generate_commissioner_template() -> BytesIO
generate_court_template() -> BytesIO
```

## Error Handling

### Common Issues
1. **Invalid File Format**: Only .xlsx and .xls files accepted
2. **Missing Columns**: All required columns must be present
3. **Data Type Errors**: Values must match expected types
4. **Date Format Issues**: Dates must be in recognized format
5. **Empty Required Fields**: All required fields must have values

### Error Reports
- Failed records are reported with row numbers
- Error messages specify the field and issue
- Downloadable error report available as CSV

## Testing

### Unit Tests
```bash
# Test Excel validation utilities
uv run pytest tests/test_excel_validator.py

# Test Excel processing utilities
uv run pytest tests/test_excel_processor.py
```

### End-to-End Test
1. Start the Streamlit app: `uv run streamlit run app.py`
2. Navigate to a record page
3. Test single record mode (ensure unchanged)
4. Test bulk upload mode with valid file
5. Test bulk upload mode with invalid file
6. Verify records appear in database

## Performance Notes

- Files up to 1000 rows are supported
- Validation typically completes in <5 seconds
- Bulk insertion of 1000 records completes in <30 seconds
- Progress tracking updates every 50 records during insertion