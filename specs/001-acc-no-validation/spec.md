# Feature Specification: Acc No Uniqueness Validation

**Feature Branch**: `001-acc-no-validation`
**Created**: 2026-01-04
**Status**: Draft
**Input**: User description: "Add acc_no uniqueness validation to both commissioner and court record entry systems (single record mode and bulk upload mode). The acc_no field must be unique within each table - commissioner_records and court_records have separate acc_no sequences. Before inserting any record (single or bulk), check if the acc_no already exists in the respective table. For single record entry, show an error message and prevent insertion if acc_no exists. For bulk Excel uploads, skip records with duplicate acc_no values, insert only unique ones, and provide a detailed report showing which records were skipped due to existing acc_no values and which were successfully inserted."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Single Record Entry with Duplicate Prevention (Priority: P1)

As a data entry operator, I want to be prevented from entering duplicate acc_no values when adding individual commissioner or court records, so that I can maintain data integrity and avoid confusion in the system.

**Why this priority**: This is the foundational requirement that ensures data integrity at the most basic level of data entry. Without this, the system becomes unreliable as duplicate records can be created through the most common user interaction.

**Independent Test**: Can be fully tested by attempting to enter a commissioner record with an acc_no that already exists in the database, and verifying that the system shows an appropriate error message and prevents the insertion while keeping the form data intact.

**Acceptance Scenarios**:

1. **Given** a commissioner record with acc_no 123 already exists in the database, **When** user attempts to add another commissioner record with acc_no 123, **Then** the system shows error message "❌ This acc_no (123) already exists in Commissioner Records. Please use a different acc_no." and prevents insertion

2. **Given** a court record with acc_no 456 already exists in the database, **When** user attempts to add another court record with acc_no 456, **Then** the system shows error message "❌ This acc_no (456) already exists in Court Records. Please use a different acc_no." and prevents insertion

3. **Given** a commissioner record with acc_no 789 does not exist in the database, **When** user enters acc_no 789 and submits, **Then** the record is successfully inserted

---
### User Story 2 - Bulk Upload with Duplicate Detection and Reporting (Priority: P1)

As a data entry operator, I want to upload Excel files containing multiple records while being informed about which records have duplicate acc_no values, so that I can process large datasets efficiently while maintaining data integrity.

**Why this priority**: This addresses the bulk data entry workflow which is critical for efficiency when processing large volumes of records. The reporting aspect ensures transparency about what data was processed.

**Independent Test**: Can be fully tested by uploading an Excel file containing both unique and duplicate acc_no values, and verifying that only unique records are inserted while a report shows which records were skipped.

**Acceptance Scenarios**:

1. **Given** an Excel file with 10 commissioner records where 3 have duplicate acc_no values, **When** user uploads the file, **Then** the system shows summary with counts and allows confirmation to insert only the 7 unique records

2. **Given** an Excel file with court records, **When** user uploads the file, **Then** the system categorizes records into valid (unique) and duplicate (existing) and displays appropriate summary

3. **Given** an Excel file where all records have duplicate acc_no values, **When** user uploads the file, **Then** the system shows "⚠️ All records have existing acc_no values. No new records to insert." and provides option to download skipped records list

---
### User Story 3 - Independent Acc No Sequences Between Tables (Priority: P2)

As a data entry operator, I want to be able to use the same acc_no value in both commissioner and court records, so that I can maintain separate numbering sequences for different record types.

**Why this priority**: This is important for data organization and user workflow, allowing independent numbering systems for different record types while maintaining uniqueness within each type.

**Independent Test**: Can be fully tested by adding a commissioner record with acc_no 100 and then successfully adding a court record with the same acc_no 100, verifying that the system allows this since they're in separate tables.

**Acceptance Scenarios**:

1. **Given** a commissioner record with acc_no 500 exists in the database, **When** user attempts to add a court record with acc_no 500, **Then** the court record is successfully inserted since the tables have independent acc_no sequences

2. **Given** a court record with acc_no 600 exists in the database, **When** user attempts to add a commissioner record with acc_no 600, **Then** the commissioner record is successfully inserted since the tables have independent acc_no sequences

---
### Edge Cases

- What happens when a user enters an acc_no that is very large or contains special characters?
- How does the system handle database connection failures during uniqueness checks?
- What occurs when multiple users simultaneously attempt to insert the same new acc_no?
- How does the system behave when an Excel file contains thousands of records?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST check if an acc_no already exists in the commissioner_records table before inserting a new commissioner record
- **FR-002**: System MUST check if an acc_no already exists in the court_records table before inserting a new court record
- **FR-003**: System MUST show error message "❌ This acc_no ({acc_no}) already exists in Commissioner Records. Please use a different acc_no." when duplicate acc_no is detected in commissioner records
- **FR-004**: System MUST show error message "❌ This acc_no ({acc_no}) already exists in Court Records. Please use a different acc_no." when duplicate acc_no is detected in court records
- **FR-005**: System MUST keep form data intact when duplicate acc_no validation fails, allowing users to modify only the acc_no field
- **FR-006**: System MUST allow the same acc_no value to exist in both commissioner_records and court_records tables (independent sequences)
- **FR-007**: System MUST identify duplicate acc_no values in bulk Excel uploads before insertion
- **FR-008**: System MUST display summary showing count of valid records (unique acc_no) and duplicate records (existing acc_no) before bulk insertion
- **FR-009**: System MUST show detailed table of duplicate records with Row Number, acc_no, department, and reason during bulk upload
- **FR-010**: System MUST insert only records with unique acc_no values during bulk upload, skipping duplicates
- **FR-011**: System MUST provide confirmation dialog before proceeding with bulk insertion of valid records
- **FR-012**: System MUST show detailed summary after bulk insertion with counts of successfully inserted records, skipped duplicates, and any other errors
- **FR-013**: System MUST query database using SELECT COUNT(*) FROM [table_name] WHERE acc_no = [value] for uniqueness checks

### Key Entities *(include if feature involves data)*

- **Commissioner Record**: A record in the commissioner_records table with acc_no as a unique identifier within this table
- **Court Record**: A record in the court_records table with acc_no as a unique identifier within this table
- **Acc No**: An integer identifier that must be unique within each table but can be shared between commissioner and court tables

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of duplicate acc_no attempts in single record entry are prevented with appropriate error messages displayed
- **SC-002**: 100% of duplicate acc_no records in bulk Excel uploads are identified and skipped during insertion
- **SC-003**: Users can complete duplicate acc_no validation for single records in under 2 seconds (including database query time)
- **SC-004**: Bulk upload validation for files with up to 1000 records completes in under 30 seconds
- **SC-005**: 95% of users successfully understand the duplicate acc_no error messages and can correct their input on first attempt
- **SC-006**: Zero duplicate acc_no values exist within each table type (commissioner_records and court_records) after feature implementation