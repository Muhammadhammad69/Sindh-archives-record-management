---
id: 1
title: Acc No Uniqueness Validation Spec
stage: spec
date: '2026-01-04'
surface: agent
model: claude-sonnet-4-5-20250929
feature: acc-no-validation
branch: 001-acc-no-validation
user: claude
command: /sp.specify
labels:
  - validation
  - database
  - records
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-acc-no-validation/spec.md
  - specs/001-acc-no-validation/checklists/requirements.md
tests: []
---

# Acc No Uniqueness Validation Spec

## User Input

```
004-add-validation

Must run this command /sp.specify
Branch Name: 004-add-validation

Add acc_no uniqueness validation to both commissioner and court record entry systems (single record mode and bulk upload mode). The acc_no field must be unique within each table - commissioner_records and court_records have separate acc_no sequences. Before inserting any record (single or bulk), check if the acc_no already exists in the respective table. For single record entry, show an error message and prevent insertion if acc_no exists. For bulk Excel uploads, skip records with duplicate acc_no values, insert only unique ones, and provide a detailed report showing which records were skipped due to existing acc_no values and which were successfully inserted.

CORE REQUIREMENTS:

1. Database-Level Uniqueness Check (Commissioner):
   - Before inserting a commissioner record, query the commissioner_records table to check if acc_no already exists
   - Use query: SELECT COUNT(*) FROM commissioner_records WHERE acc_no = %s
   - If count > 0, the acc_no exists and record should not be inserted
   - This check applies to both single record entry and bulk upload

2. Database-Level Uniqueness Check (Court):
   - Before inserting a court record, query the court_records table to check if acc_no already exists
   - Use query: SELECT COUNT(*) FROM court_records WHERE acc_no = %s
   - If count > 0, the acc_no exists and record should not be inserted
   - Commissioner and court tables have INDEPENDENT acc_no sequences (acc_no=5 can exist in both tables)

3. Single Record Entry - Commissioner (add_commissioner.py):
   - When user submits the single record form, validate acc_no BEFORE creating the record object
   - If acc_no exists in database:
     * Show error message: "❌ This acc_no ({acc_no}) already exists in Commissioner Records. Please use a different acc_no."
     * Do NOT insert the record
     * Keep form filled with user's data so they can change acc_no
     * Highlight the acc_no field with red border or error indicator
   - If acc_no is unique, proceed with insertion as normal

4. Single Record Entry - Court (add_court.py):
   - Same validation logic as commissioner
   - Check court_records table for acc_no existence
   - Error message: "❌ This acc_no ({acc_no}) already exists in Court Records. Please use a different acc_no."
   - Keep form data, don't clear on validation error
   - Allow user to modify acc_no and resubmit

5. Bulk Upload - Commissioner (Excel Upload Mode):
   When processing Excel file for commissioner records:
   - After validating columns and data types, perform acc_no uniqueness check for ALL rows
   - Query database to get list of existing acc_no values: SELECT acc_no FROM commissioner_records
   - Compare uploaded acc_no values against existing ones
   - Categorize records into:
     * **Valid records**: acc_no does NOT exist in database (ready to insert)
     * **Duplicate records**: acc_no ALREADY exists in database (skip insertion)

   Display summary BEFORE insertion:
   - "Found {total_records} records in Excel file"
   - "✅ {valid_count} records with unique acc_no (will be inserted)"
   - "⚠️ {duplicate_count} records with existing acc_no (will be skipped)"

   Show table of duplicate records:
   - Columns: Row Number, acc_no, department, Reason
   - Reason: "acc_no {value} already exists in database"

   Add confirmation: "Proceed with inserting {valid_count} valid records?"

6. Bulk Upload - Court (Excel Upload Mode):
   Same logic as commissioner bulk upload:
   - Query existing acc_no values from court_records table
   - Categorize into valid (unique) and duplicate (existing) records
   - Show summary with counts
   - Display table of skipped records with acc_no and reason
   - Confirm insertion of only valid records

7. Bulk Insert Process - Skip Duplicates:
   During bulk insertion (both commissioner and court):
   - Insert ONLY records with unique acc_no values
   - Skip records where acc_no already exists
   - Track insertion results:
     * successfully_inserted: count and list
     * skipped_duplicates: count and list with acc_no values
     * failed_other_errors: count and list (for non-duplicate errors)

   After insertion, show detailed summary:
   - "✅ Successfully inserted {success_count} records. ⚠️ Skipped {duplicate_count} duplicate records."
   - Updated add_commissioner.py single mode with acc_no validation
- Updated add_court.py single mode with acc_no validation
- Updated bulk upload logic in both pages to skip duplicates
- Enhanced error reporting with duplicate tracking
- Utility function for bulk acc_no checking
- Test cases for duplicate acc_no scenarios
- Documentation update explaining acc_no uniqueness requirement

EXPECTED BEHAVIOR EXAMPLES:

**Example 1: Single Record with Existing acc_no**
- User enters acc_no = 100 in commissioner form
- System checks database: acc_no 100 exists
- Show error: "❌ This acc_no (100) already exists. Please use a different acc_no."
- Form remains filled, user changes acc_no to 101
- System checks: acc_no 101 is unique
- Record inserted successfully ✅

**Example 2: Bulk Upload with Mixed Records**
- Excel file has 10 commissioner records
- acc_no values: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10
- Database already has acc_no: 2, 5, 8
- System shows:
  * "✅ 7 records with unique acc_no (will be inserted)"
  * "⚠️ 3 records with existing acc_no (will be skipped): 2, 5, 8"
- User confirms
- System inserts records with acc_no: 1, 3, 4, 6, 7, 9, 10
- Summary: "✅ Successfully inserted 7 records. ⚠️ Skipped 3 duplicate records."

**Example 3: All Records Already Exist**
- Excel file has 5 court records
- All acc_no values exist in database
- System shows: "⚠️ All 5 records have existing acc_no values. No new records to insert."
- Provide option to download the skipped records list
- No insertion performed

This enhancement ensures data integrity by preventing duplicate acc_no values while providing clear feedback to users about which records were processed and which were skipped.
```

## Response Summary

Created comprehensive feature specification for acc_no uniqueness validation. The specification includes:

- User scenarios for single record entry with duplicate prevention
- Bulk upload with duplicate detection and reporting
- Independent acc_no sequences between commissioner and court records
- Functional requirements covering database checks, error messages, form handling, and bulk processing
- Success criteria with measurable outcomes
- Edge cases consideration

The specification ensures data integrity by preventing duplicate acc_no values while providing clear feedback to users about which records were processed and which were skipped.