# Quickstart: Acc No Uniqueness Validation

## Overview
This feature adds acc_no uniqueness validation to both commissioner and court record entry systems for single record mode and bulk Excel upload mode. The acc_no field must be unique within each table, with commissioner_records and court_records having separate acc_no sequences.

## Setup

### Prerequisites
- Python 3.11+
- PostgreSQL database with existing commissioner_records and court_records tables
- Existing Phase 1-3 components installed and configured

### Installation
No additional packages required - uses existing dependencies (psycopg2-binary, pandas, Streamlit, etc.)

## Running the Application

1. Start the Streamlit application:
```bash
streamlit run main.py
```

2. Access the application through your web browser

## Using the Feature

### Single Record Entry

#### Adding Commissioner Records
1. Navigate to the "Add Commissioner" page
2. Fill in the form fields, including the acc_no
3. Before submission, the system will check if the acc_no already exists in commissioner_records
4. If the acc_no is unique, the record will be inserted
5. If the acc_no already exists, you'll see an error: "❌ This acc_no ({acc_no}) already exists in Commissioner Records. Please use a different acc_no."
6. The form data will be preserved so you can modify just the acc_no field

#### Adding Court Records
1. Navigate to the "Add Court" page
2. Fill in the form fields, including the acc_no
3. Before submission, the system will check if the acc_no already exists in court_records
4. If the acc_no is unique, the record will be inserted
5. If the acc_no already exists, you'll see an error: "❌ This acc_no ({acc_no}) already exists in Court Records. Please use a different acc_no."
6. The form data will be preserved so you can modify just the acc_no field

### Bulk Excel Upload

#### Commissioner Records
1. Prepare your Excel file with the required columns
2. Navigate to the "Add Commissioner" page and select "Bulk Upload" mode
3. Upload your Excel file
4. The system will validate the file format and check for acc_no duplicates
5. You'll see a validation summary:
   - Total records in file
   - Valid records (unique acc_no)
   - Database duplicates (acc_no already exists)
   - Internal duplicates (duplicate acc_no within the uploaded file)
6. A table will show details of skipped records
7. Confirm to insert only the valid records
8. After insertion, you'll see a summary of results

#### Court Records
1. Prepare your Excel file with the required columns
2. Navigate to the "Add Court" page and select "Bulk Upload" mode
3. Upload your Excel file
4. The system will validate the file format and check for acc_no duplicates
5. You'll see a validation summary and details of skipped records
6. Confirm to insert only the valid records
7. After insertion, you'll see a summary of results

## Key Features

### Acc No Uniqueness
- acc_no must be unique within each table (commissioner_records and court_records)
- The same acc_no can exist in both tables (independent sequences)
- Duplicate acc_no values are detected and prevented from insertion

### Validation Feedback
- Clear error messages for duplicate acc_no values
- Preservation of form data when validation fails
- Detailed validation summary for bulk uploads
- Visual indicators for validation results

### Bulk Upload Improvements
- Pre-upload validation of acc_no uniqueness
- Categorization of records (valid, duplicate, internal duplicate)
- Confirmation step before insertion
- Detailed reporting of insertion results

## API Endpoints
No new API endpoints are created. The validation occurs within the existing page logic.

## Error Handling
- Database connection errors are handled gracefully
- Form data is preserved when validation fails
- Clear error messages guide users on how to correct issues