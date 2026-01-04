---
id: 1
title: "Excel Bulk Upload Feature Spec"
stage: spec
date: "2026-01-04"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "excel-bulk-upload"
branch: "001-excel-bulk-upload"
user: "user"
command: "/sp.specify 003-add-file-upload-feature"
labels: ["feature", "specification", "excel", "bulk-upload"]
links:
  spec: "specs/001-excel-bulk-upload/spec.md"
  ticket: null
  adr: null
  pr: null
files:
  - "specs/001-excel-bulk-upload/spec.md"
  - "specs/001-excel-bulk-upload/checklists/requirements.md"
tests: []
---

# Prompt

```
  003-add-file-upload-feature

Must run this command /sp.specify
Branch Name: 003-add-file-upload-feature

Build an enhanced record management system (Phase 3: Bulk Upload via Excel) that extends the existing add_commissioner.py and add_court.py pages with dual-mode data entry. Users can choose between single record entry (existing functionality) or bulk upload via Excel files. Use uv for package management, pandas for Excel processing, and Streamlit for UI. Use context7 MCP to fetch documentation for pandas Excel operations, file upload handling, and data validation when needed.

CORE REQUIREMENTS:

1. Enhanced Commissioner Records Entry Page:
   Modify the existing "Add Commissioner Records" page to show TWO action buttons when the page loads:
   - Button 1: "Add Single Record" - Shows the existing form with all fields (acc_no, department, file_no, subject, year, page, condition, record_type)
   - Button 2: "Upload Excel File" - Shows file uploader component that accepts ONLY .xlsx and .xls files

   The page should use st.radio or st.tabs to let users choose between these two modes. Default to showing the choice screen, not the form directly.

2. Enhanced Court Records Entry Page:
   Modify the existing "Add Court Records" page with the same dual-mode structure:
   - Button 1: "Add Single Record" - Shows the existing form with all fields (acc_no, court, suit_no, plaintiff, defendant, claim_or_charge, date_from, date_to, language)
   - Button 2: "Upload Excel File" - Shows file uploader for .xlsx and .xls files only

   Same UI pattern as commissioner records page for consistency.

3. Excel File Upload Component (Commissioner Records):
   When user selects "Upload Excel File" option on commissioner page:
   - Display st.file_uploader with accept_multiple_files=False, type=['xlsx', 'xls']
   - If user uploads non-Excel file (PDF, DOC, CSV, etc.), show error: "Invalid file format. Please upload an Excel file (.xlsx or .xls only)"
   - Once valid Excel file is uploaded, read it using pandas.read_excel()
   - Display preview of first 5 rows in st.dataframe for user verification
   - Show total row count: "Found X records in the uploaded file"

4. Excel Column Validation (Commissioner Records):
   After reading the Excel file, validate that ALL required columns exist with EXACT names (case-sensitive):
   Required columns: acc_no, department, file_no, subject, year, page, condition, record_type

   Validation rules:
   - If ANY required column is missing, show error message: "Missing required columns: [list missing columns]. Please ensure your Excel file has these exact column headers: acc_no, department, file_no, subject, year, page, condition, record_type"
   - If extra columns exist, ignore them (only process required columns)
   - Column names must match exactly (case-sensitive)
   - Show a "Column Validation" status indicator: ✅ All columns present or ❌ Missing columns

5. Excel File Upload Component (Court Records):
   When user selects "Upload Excel File" option on court page:
   - Same file uploader component (accept .xlsx, .xls only)
   - Same error handling for invalid file types
   - Display preview of first 5 rows after upload
   - Show total row count

6. Excel Column Validation (Court Records):
   Validate required columns exist with EXACT names:
   Required columns: acc_no, court, suit_no, plaintiff, defendant, claim_or_charge, date_from, date_to, language

   Same validation rules as commissioner:
   - Show error if columns missing: "Missing required columns: [list]. Required columns are: acc_no, court, suit_no, plaintiff, defendant, claim_or_charge, date_from, date_to, language"
   - Ignore extra columns
   - Case-sensitive matching
   - Show validation status indicator

7. Data Validation Before Bulk Insert (Commissioner):
   After column validation passes, validate data in each row:
   - acc_no: Must be positive integer, not null
   - department: Must be non-empty string, not null
   - file_no: Must be non-empty string, not null
   - subject: Must be non-empty string, not null
   - year: Must be integer between 1800-2100, not null
   - page: Must be positive integer, not null
   - condition: Must be non-empty string, not null
   - record_type: Must be non-empty string, not null

   For each validation error found:
   - Show error with row number: "Row 5: acc_no must be a positive integer"
   - Display all validation errors at once (don't stop at first error)
  row {row_num}: {error_message}"
    - Partial success: "⚠️ Bulk upload completed with errors. Successfully inserted {success_count} records. Failed to insert {fail_count} records."

14. Data Processing Requirements:
    - Handle Excel files up to 1000 rows efficiently
    - Process dates correctly (Excel date format to Python date)
    - Handle empty cells appropriately (treat as null/None)
    - Trim whitespace from string fields
    - Validate data types match database schema
    - Add created_at and updated_at timestamps automatically during bulk insert

15. Existing Single Record Functionality:
    **CRITICAL: Do NOT modify the existing single record entry forms.** When user selects "Add Single Record":
    - Show the exact same form that currently exists
    - All existing validation logic remains unchanged
    - Same success/error handling
    - Same database insert process
    - Only add the mode selection UI before showing the form

TECHNICAL CONSTRAINTS:
- Use uv for package management
- Add openpyxl or xlrd for Excel file reading (pandas dependency)
- Reuse all existing Phase 1 and Phase 2 infrastructure
- Use pandas for Excel operations and data validation
- Use context7 MCP for:
  * pandas.read_excel() documentation and best practices
  * Excel date handling and format conversion
  * Streamlit file_uploader advanced options
  * Progress bar implementation patterns
  * DataFrame validation techniques
- No changes to database schema
- No changes to existing DAO methods
- No changes to authentication or navigation

DELIVERABLES FOR PHASE 3:
- Updated add_commissioner.py with dual-mode entry (single + bulk upload)
- Updated add_court.py with dual-mode entry (single + bulk upload)
- Excel template generator utility
- Data validation helper functions
- Bulk insert handler with progress tracking
- Error reporting and download functionality
- Updated requirements with Excel processing libraries
- README section for bulk upload feature
- Sample Excel templates included in repository

This phase enhances data entry efficiency while maintaining all existing functionality and validation rules from Phase 2.
```

# Response

Created feature specification for Excel bulk upload functionality. The specification includes dual-mode record entry allowing users to choose between single record entry and Excel file upload on both commissioner and court records pages. Key requirements validated include Excel file format validation (.xlsx, .xls only), column structure validation, data validation with row-specific error reporting, and preservation of existing single record functionality. The specification defines clear user scenarios, functional requirements, and success criteria with measurable outcomes.

# Outcome

Specification created successfully at specs/001-excel-bulk-upload/spec.md with comprehensive requirements for dual-mode data entry functionality. Quality checklist completed and all validation items passed. Ready for planning phase.