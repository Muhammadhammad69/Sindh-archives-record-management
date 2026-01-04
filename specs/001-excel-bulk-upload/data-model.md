# Data Model: Excel Bulk Upload

## Entities

### Commissioner Records (Excel Input)
- **acc_no**: integer (required) - Account number, must be positive integer
- **department**: string (required) - Department name, max 255 chars
- **file_no**: string (required) - File number, max 100 chars
- **subject**: text (required) - Subject description
- **year**: integer (required) - Year between 1800-2100
- **page**: integer (required) - Page number, must be positive
- **condition**: string (required) - Physical condition, max 50 chars
- **record_type**: string (required) - Type of record, max 50 chars

### Court Records (Excel Input)
- **acc_no**: integer (required) - Account number, must be positive integer
- **court**: string (required) - Court name, max 255 chars
- **suit_no**: string (required) - Suit number, max 100 chars
- **plaintiff**: string (required) - Plaintiff name, max 255 chars
- **defendant**: string (required) - Defendant name, max 255 chars
- **claim_or_charge**: text (required) - Claim or charge description
- **date_from**: date (required) - Start date in YYYY-MM-DD format
- **date_to**: date (required) - End date in YYYY-MM-DD format, must be after date_from
- **language**: string (required) - Language of records, max 50 chars

### Excel Upload Session
- **session_id**: string (required) - Unique identifier for upload session
- **file_name**: string (required) - Original filename
- **file_type**: string (required) - File extension (.xlsx, .xls)
- **row_count**: integer (required) - Total number of rows in file
- **valid_rows**: integer (required) - Number of rows that passed validation
- **invalid_rows**: integer (required) - Number of rows that failed validation
- **status**: string (required) - Current status (validating, processing, completed, failed)
- **created_at**: datetime (required) - Timestamp of upload
- **processed_at**: datetime (optional) - Timestamp of completion

### Validation Error
- **row_number**: integer (required) - Row number in Excel file (1-indexed)
- **field_name**: string (required) - Name of field that failed validation
- **error_message**: string (required) - Human-readable error description
- **original_value**: string (required) - Original value from Excel cell
- **error_type**: string (required) - Type of validation error (format, range, required, etc.)

## Relationships

### Commissioner Records
- Maps 1:1 to existing commissioner_records table in database
- All Excel input fields correspond to existing database columns
- Validation occurs before database insertion

### Court Records
- Maps 1:1 to existing court_records table in database
- All Excel input fields correspond to existing database columns
- Date validation ensures date_to is after date_from

## Validation Rules

### Commissioner Record Validation
1. **acc_no**: Must be a positive integer (>= 1)
2. **year**: Must be between 1800 and 2100 (inclusive)
3. **page**: Must be a positive integer (>= 1)
4. **department, file_no, condition, record_type**: Required fields, not empty
5. **subject**: Required field, not empty

### Court Record Validation
1. **acc_no**: Must be a positive integer (>= 1)
2. **date_from, date_to**: Must be valid dates in YYYY-MM-DD format
3. **date_to**: Must be after date_from
4. **court, suit_no, plaintiff, defendant, language**: Required fields, not empty
5. **claim_or_charge**: Required field, not empty

### Excel File Validation
1. **File Type**: Must be .xlsx or .xls format only
2. **Column Headers**: Must match expected column names exactly
3. **Required Columns**: All required columns must be present
4. **Extra Columns**: Permitted but will be ignored during processing
5. **Row Limits**: Maximum 1000 rows per file

## State Transitions

### Upload Session States
1. **uploaded**: File received, validation pending
2. **validating**: Column and data validation in progress
3. **validated**: All validation passed, ready for processing
4. **processing**: Bulk insert operation in progress
5. **completed**: All records inserted successfully
6. **failed**: Validation or insertion errors occurred

### Validation Process Flow
1. File type validation
2. Column structure validation
3. Data content validation
4. Database constraint validation
5. Bulk insertion