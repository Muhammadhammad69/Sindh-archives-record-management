---
id: 2
title: Acc No Validation Plan
stage: plan
date: '2026-01-04'
surface: agent
model: claude-sonnet-4-5-20250929
feature: acc-no-validation
branch: 001-acc-no-validation
user: claude
command: /sp.plan
labels:
  - validation
  - database
  - records
  - planning
links:
  spec: specs/001-acc-no-validation/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-acc-no-validation/plan.md
  - specs/001-acc-no-validation/research.md
  - specs/001-acc-no-validation/data-model.md
  - specs/001-acc-no-validation/quickstart.md
tests: []
---

# Acc No Validation Plan

## User Input

```
001-acc-no-validation

Must run this command /sp.plan

Create a comprehensive implementation plan for adding acc_no uniqueness validation across both single record entry and bulk Excel upload modes for commissioner and court records. The plan will extend existing Phase 3 functionality without modifying database schema. Use existing DAO infrastructure and add new validation methods. Implement efficient bulk checking using set-based lookups. Use context7 MCP to fetch documentation for pandas duplicate detection, SQL optimization for uniqueness checks, and Streamlit UI patterns for validation feedback when planning each component.

TECHNOLOGY STACK:
- Database Queries: psycopg2 with existing connection pool for acc_no existence checks
- Duplicate Detection: pandas for finding duplicates within uploaded Excel files
- Performance: Python sets for O(1) lookup of existing acc_no values during bulk validation
- UI Feedback: Streamlit warning/error components for validation messages
- Existing Infrastructure: All Phase 1-3 components remain unchanged, only extended

PROJECT STRUCTURE ADDITIONS:
```
project-root/
├── src/
│   ├── database/
│   │   └── models
│   │       ├── commissioner_record.py     # Add acc_no_exists() method
│   │       └── court_record.py            # Add acc_no_exists() method
│   ├── utils/
│   │   ├── acc_no_validator.py            # NEW - acc_no uniqueness utilities
│   │   └── duplicate_detector.py          # NEW - Detect duplicates in Excel
│   ├── pages/
│   │   ├── add_commissioner.py            # Update single & bulk with acc_no check
│   │   └── add_court.py                   # Update single & bulk with acc_no check
└── tests/
    ├── test_acc_no_validator.py           # NEW - Test uniqueness validation
    └── test_duplicate_detection.py        # NEW - Test duplicate detection
```

IMPLEMENTATION PLAN (PLANNING ONLY - NO EXECUTION):

## Phase 1: DAO Layer Enhancement

### Task 1.1: Add acc_no_exists() to CommissionerRecordsDAO
**File:** src/models/commissioner.py
**What to add:**
- Method signature: `def acc_no_exists(self, acc_no: int) -> bool`
- SQL query: `SELECT EXISTS(SELECT 1 FROM commissioner_records WHERE acc_no = %s)`
- Return True if acc_no exists, False otherwise
- Use existing connection pool via `with get_connection()`
- Add error handling for database connection issues
**Context7 checkpoint:** "Get PostgreSQL documentation for EXISTS vs COUNT performance comparison"

### Task 1.2: Add acc_no_exists() to CourtRecordsDAO
**File:** src/models/court.py
**What to add:**
- Identical implementation as commissioner but query court_records table
- Same method signature and error handling
- Independent check (commissioner and court acc_no are separate)

### Task 1.3: Add bulk acc_no fetching methods
**File:** src/models/commissioner.py and src/models/court.py
**What to add:**
- Method: `def get_all_acc_numbers(self) -> set[int]`
- SQL query: `SELECT acc_no FROM commissioner_records` (or court_records)
- Return as Python set for fast lookup
- Use for bulk upload validation (query once, check many)
**Context7 checkpoint:** "Get Python documentation for set performance and memory usage with large datasets"

## Phase 2: Validation Utilities

### Task 2.1: Create acc_no validator utility
**File:** src/utils/acc_no_validator.py
**Functions to implement:**
1. `validate_single_acc_no(acc_no: int, dao: DAO) -> tuple[bool, str]`
   - Calls dao.acc_no_exists()
   - Returns (is_valid, error_message)
   - Error message format: "acc_no {value} already exists"

2. `validate_bulk_acc_numbers(acc_numbers: list[int], existing_acc_numbers: set[int]) -> dict`
   - Takes list from Excel and set from database
   - Returns dict with:
     * valid_acc_numbers: list of unique acc_no
     * duplicate_acc_numbers: list of existing acc_no
     * duplicate_indices: list of row indices with duplicates
   - Use set operations: duplicates = set(acc_numbers) & existing_acc_numbers

3. `find_duplicates_in_list(acc_numbers: list[int]) -> dict`
   - Detect duplicates WITHIN the uploaded Excel file itself
   - Returns dict with duplicate values and their row positions
   - User should know if Excel has internal duplicates too
**Context7 checkpoint:** "Get pandas documentation for finding duplicate values in DataFrame column"

### Task 2.2: Create duplicate detection utility
**File:** src/utils/duplicate_detector.py
**Functions to implement:**
1. `detect_excel_duplicates(df: DataFrame, column: str) -> DataFrame`
   - Use pandas df.duplicated() to find internal duplicates
   - Return DataFrame with only duplicate rows
   - Include row numbers for user reference

2. `categorize_records(df: DataFrame, existing_acc_numbers: set[int]) -> dict`
   - Split DataFrame into three categories:
     * valid_records: DataFrame with unique acc_no
     * duplicate_records: DataFrame with existing acc_no
     * internal_duplicate_records: DataFrame with duplicates within Excel
   - Return all three with row indices

3. `generate_skip_report(duplicate_records: DataFrame) -> DataFrame`
   - Create report DataFrame with columns: Row, acc_no, Reason, Status
   - Reason: "acc_no exists in database" or "Duplicate within file"
   - Status: "Skipped"
   - For error report download

## Phase 3: Single Record Entry Updates

### Task 3.1: Update add_commissioner.py single mode
**File:** src/pages/add_commissioner.py
**Changes to make:**
- BEFORE creating CommissionerRecord object, add validation:
```python
  # After form submission and BEFORE record creation:
  dao = CommissionerRecordsDAO()
  if dao.acc_no_exists(acc_no):
      st.error(f"❌ This acc_no ({acc_no}) already exists in Commissioner Records.")
      st.warning("Please use a different acc_no.")
      # Do NOT proceed with insertion
      # Keep form data visible (don't clear)
      return  # Exit without inserting
```
- Add visual indicator (red border) on acc_no field if duplicate
- Success path remains unchanged
**Context7 checkpoint:** "Get Streamlit documentation for form state preservation and error handling"

### Task 3.2: Update add_court.py single mode
**File:** src/pages/add_court.py
**Changes to make:**
- Same validation structure as commissioner
- Check CourtRecordsDAO.acc_no_exists()
- Same error messages and UI feedback
- Independent validation (doesn't check commissioner table)

## Phase 4: Bulk Upload Enhancement

### Task 4.1: Add pre-upload acc_no validation - Commissioner
**File:** src/pages/add_commissioner.py (bulk upload section)
**Logic flow to add:**
1. After Excel file uploaded and columns validated
2. Before showing preview:
   - Get existing acc_no from database: `existing = dao.get_all_acc_numbers()`
   - Get acc_no from Excel: `uploaded = df['acc_no'].tolist()`
   - Find duplicates with database: `duplicates = set(uploaded) & existing`
   - Find duplicates within Excel: `internal_dupes = df[df.duplicated('acc_no')]`
3. Display summary section:
```
   📊 Validation Summary:
   - Total records in file: {total}
   - ✅ Valid records (unique acc_no): {valid_count}
   - ⚠️ Database duplicates: {db_dup_count}
   - ⚠️ Internal duplicates: {internal_dup_count}
```
4. Show expandable table of skipped records
5. Add confirmation button: "Insert {valid_count} Valid Records"
**Context7 checkpoint:** "Get pandas documentation for set operations on DataFrame columns"

### Task 4.2: Add pre-upload acc_no validation - Court
**File:** src/pages/add_court.py (bulk upload section)
**Logic flow:**
- Identical to commissioner but use CourtRecordsDAO
- Same validation summary display
- Same confirmation flow

### Task 4.3: Update bulk insert logic - Skip duplicates
**Files:** Both add_commissioner.py and add_court.py
**Changes to insert loop:**
```python
# Current: Insert all records
# New: Filter and insert only valid records

# Before insertion loop:
valid_records = df[~df['acc_no'].isin(existing_acc_numbers)]

# During insertion:
success_count = 0
skipped_count = 0
error_count = 0

for index, row in valid_records.iterrows():
    try:
        # Create and insert record
        success_count += 1
    except Exception as e:
        error_count += 1

skipped_count = len(df) - len(valid_records)

# Show summary after insertion
```
**Context7 checkpoint:** "Get pandas documentation for DataFrame filtering with isin() method"

## Phase 5: Error Reporting Enhancement

### Task 5.1: Update error report generation
**Files:** src/utils/ (create report_generator.py if needed)
**What to add:**
- Function: `generate_comprehensive_report()`
- Include three categories in CSV:
  1. Successfully inserted records (with new database IDs)
  2. Skipped due to duplicate acc_no
  3. Failed due to other errors
- CSV columns: Row, acc_no, Status, Reason, [all other fields]
- Color coding in Streamlit display:
  - Green background for inserted
  - Yellow for skipped duplicates
  - Red for errors
**Context7 checkpoint:** "Get pandas documentation for DataFrame styling and to_csv() options"

### Task 5.2: Add downloadable skip report
**Files:** add_commissioner.py and add_court.py
**What to add:**
- After bulk upload completes
- Generate CSV with skipped records only
- Include all original data so user can fix and re-upload
- Button: "Download Skipped Records (CSV)"
- Use st.download_button with DataFrame.to_csv()

## Phase 6: User Experience Improvements

### Task 6.1: Add informational messages
**Where:** Both add_commissioner.py and add_court.py
**Messages to add:**
- At top of single record form: st.info("💡 acc_no must be unique. The system will check for duplicates before saving.")
- At top of bulk upload: st.info("📋 Records with existing acc_no will be automatically skipped during import.")
- In validation summary: Use st.warning for duplicates (not error, since it's expected)

### Task 6.2: Add visual feedback during validation
**Where:** Bulk upload sections
**What to add:**
- Progress spinner during acc_no check: "Checking for duplicate acc_no values..."
- Success indicator when validation passes
- Warning badge with count of duplicates found
- Expandable section showing duplicate details

### Task 6.3: Add confirmation dialog
**Where:** Before bulk insert
**What to add:**
- Show summary: "Ready to insert {valid_count} records. {skip_count} will be skipped."
- Checkbox: "I understand that duplicate records will be skipped"
- Confirm button only enabled after checkbox checked
- Cancel button to abort upload

## Phase 7: Performance Optimization

### Task 7.1: Optimize database queries
**What to plan:**
- Use EXISTS instead of COUNT for single record checks (faster)
- Fetch all acc_no in one query for bulk (avoid N+1 queries)
- Consider adding database index on acc_no columns if not exists
- Use prepared statements for repeated queries
**Context7 checkpoint:** "Get PostgreSQL documentation for index creation and EXISTS query optimization"

### Task 7.2: Optimize pandas operations
**What to plan:**
- Use set operations instead of iterating rows
- Filter DataFrame once (valid_records) instead of checking each row
- Use vectorized operations where possible
- Cache existing_acc_numbers during upload session

### Task 7.3: Handle large Excel files
**What to plan:**
- For files > 1000 rows, show progress bar during validation
- Process in chunks if needed
- Set memory limits for DataFrame operations
- Test with 5000+ row files

## Phase 8: Testing Strategy

### Task 8.1: Unit tests for DAO methods
**File:** tests/test_acc_no_validator.py
**Test cases to write:**
- Test acc_no_exists() returns True when exists
- Test acc_no_exists() returns False when not exists
- Test get_all_acc_numbers() returns correct set
- Test database connection errors handled gracefully
- Test with empty tables
- Test with large number of existing records

### Task 8.2: Unit tests for validation utilities
**File:** tests/test_duplicate_detection.py
**Test cases:**
- Test find duplicates in list
- Test categorize records with various scenarios
- Test internal duplicate detection
- Test set operations correctness
- Test edge cases (empty DataFrame, all duplicates, no duplicates)

### Task 8.3: Integration tests for UI flows
**Test scenarios:**
1. Single record with new acc_no → Insert success
2. Single record with existing acc_no → Show error, don't insert
3. Bulk upload all unique → Insert all
4. Bulk upload all duplicates → Skip all, show message
5. Bulk upload mixed → Insert valid, skip duplicates, correct counts
6. Bulk with internal duplicates → Detect and report
7. Error report download → CSV contains correct data
8. Large file (1000 rows) → Performance acceptable

## Phase 9: Documentation

### Task 9.1: Update README
**Section to add:**
- "acc_no Uniqueness Validation"
- Explain that acc_no must be unique within each table
- Document single record validation behavior
- Document bulk upload skip behavior
- Include examples and screenshots

### Task 9.2: Add inline code documentation
**Where:** All new functions and methods
**What to include:**
- Docstrings with parameter descriptions
- Return value explanations
- Example usage
- Edge case handling notes

### Task 9.3: User guide for bulk upload
**Create:** docs/bulk_upload_guide.md
**Content:**
- How acc_no validation works
- What happens to duplicate records
- How to interpret validation summary
- How to use error reports
- Best practices for preparing Excel files

## Phase 10: Git Workflow Plan

### Commit Strategy:
1. Commit after Task 1 (DAO methods): "feat(dao): add acc_no uniqueness check methods"
2. Commit after Task 2 (utilities): "feat(validators): add acc_no validation utilities"
3. Commit after Task 3 (single mode): "feat(single-entry): add acc_no duplicate validation"
4. Commit after Task 4 (bulk pre-check): "feat(bulk-upload): add acc_no pre-validation before insert"
5. Commit after Task 4.3 (skip logic): "feat(bulk-upload): implement duplicate skipping during insert"
6. Commit after Task 5 (reporting): "feat(reports): add comprehensive error reporting with duplicates"
7. Commit after Task 6 (UX): "feat(ui): add user feedback for acc_no validation"
8. Commit after Task 7 (optimization): "perf(validation): optimize acc_no checking for large files"
9. Commit after Task 8 (tests): "test(validation): add comprehensive acc_no validation tests"
10. Commit after Task 9 (docs): "docs(validation): add acc_no uniqueness documentation"

### Branch Strategy:
- Create feature branch: `feature/acc-no-validation`
- Merge to main after all tests pass
- Tag release: `v3.1.0-acc-no-validation`

## Implementation Dependencies:

**Must be completed before starting:**
- Phase 3 bulk upload feature must be fully working
- Database must have commissioner_records and court_records tables
- DAO methods must be functional

**External dependencies:**
- No new package installations required
- Uses existing pandas, psycopg2, streamlit

**Context7 MCP usage planned for:**
- PostgreSQL EXISTS vs COUNT performance
- Python set operations and memory usage
- Pandas duplicate detection methods
- Pandas DataFrame filtering and set operations
- Streamlit form state and error handling
- Database index creation and optimization

This plan provides a complete roadmap for implementation without executing any code. Each task has clear inputs, outputs, and dependencies defined.
```

## Response Summary

Created comprehensive implementation plan for acc_no uniqueness validation feature. The plan includes:

- Technical context with language, dependencies, and performance goals
- Constitution check ensuring compliance with security, data integrity, and code quality principles
- Detailed project structure with source code organization
- Data model defining entities and validation rules
- Quickstart guide for using the feature
- Research findings on optimal approaches for EXISTS vs COUNT, Python sets, pandas operations, etc.

The plan addresses all requirements from the feature specification while maintaining alignment with the project's architectural principles. Key technical decisions include using PostgreSQL EXISTS for efficient duplicate checking, Python sets for O(1) lookups during bulk validation, and pandas operations for internal duplicate detection. The implementation will enhance both single record entry and bulk Excel upload modes with comprehensive validation and user feedback.