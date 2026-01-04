# Tasks: Acc No Uniqueness Validation

**Feature**: Acc No Uniqueness Validation
**Branch**: 001-acc-no-validation
**Generated**: 2026-01-04
**Input**: specs/001-acc-no-validation/spec.md, specs/001-acc-no-validation/plan.md

## Dependencies

- **User Story 1 (P1)**: Foundational - no dependencies
- **User Story 2 (P1)**: Depends on User Story 1 (DAO methods)
- **User Story 3 (P2)**: No dependencies beyond User Story 1 and 2

## Parallel Execution Examples

- **Parallelizable Tasks**: DAO methods for commissioner and court records can be developed in parallel
- **Parallelizable Tasks**: Utility functions can be developed in parallel with UI updates
- **Parallelizable Tasks**: Tests for different components can be written in parallel

## Implementation Strategy

**MVP Scope**: Complete User Story 1 (Single Record Entry with Duplicate Prevention) with basic DAO methods and single record validation. This delivers core value of preventing duplicate entries at the most basic level.

**Incremental Delivery**:
1. MVP: Single record validation for both commissioner and court records
2. Enhancement: Bulk upload validation with duplicate detection and reporting
3. Polish: User experience improvements and comprehensive testing

---

## Phase 1: Setup

- [X] T001 Create directory structure for new utility modules: src/utils/
- [X] T002 [P] Create directory structure for new test files: tests/test_acc_no_validator.py
- [X] T003 [P] Create directory structure for new test files: tests/test_duplicate_detection.py

---

## Phase 2: Foundational

- [X] T004 [P] Add acc_no_exists() method to CommissionerRecordsDAO in src/database/models/commissioner_record.py
- [X] T005 [P] Add acc_no_exists() method to CourtRecordsDAO in src/database/models/court_record.py
- [X] T006 [P] Add get_all_acc_numbers() method to CommissionerRecordsDAO in src/database/models/commissioner_record.py
- [X] T007 [P] Add get_all_acc_numbers() method to CourtRecordsDAO in src/database/models/court_record.py

---

## Phase 3: User Story 1 - Single Record Entry with Duplicate Prevention (Priority: P1)

**Goal**: As a data entry operator, I want to be prevented from entering duplicate acc_no values when adding individual commissioner or court records, so that I can maintain data integrity and avoid confusion in the system.

**Independent Test**: Can be fully tested by attempting to enter a commissioner record with an acc_no that already exists in the database, and verifying that the system shows an appropriate error message and prevents the insertion while keeping the form data intact.

### Implementation Tasks

- [X] T008 [US1] Update add_commissioner.py to add acc_no validation before record creation
- [X] T009 [US1] Update add_court.py to add acc_no validation before record creation
- [X] T010 [US1] Implement error message display "❌ This acc_no ({acc_no}) already exists in Commissioner Records. Please use a different acc_no." in add_commissioner.py
- [X] T011 [US1] Implement error message display "❌ This acc_no ({acc_no}) already exists in Court Records. Please use a different acc_no." in add_court.py
- [X] T012 [US1] Preserve form data when duplicate acc_no validation fails in add_commissioner.py
- [X] T013 [US1] Preserve form data when duplicate acc_no validation fails in add_court.py

---

## Phase 4: User Story 2 - Bulk Upload with Duplicate Detection and Reporting (Priority: P1)

**Goal**: As a data entry operator, I want to upload Excel files containing multiple records while being informed about which records have duplicate acc_no values, so that I can process large datasets efficiently while maintaining data integrity.

**Independent Test**: Can be fully tested by uploading an Excel file containing both unique and duplicate acc_no values, and verifying that only unique records are inserted while a report shows which records were skipped.

### Implementation Tasks

- [X] T014 [P] [US2] Create acc_no_validator.py with validate_single_acc_no function in src/utils/acc_no_validator.py
- [X] T015 [P] [US2] Create acc_no_validator.py with validate_bulk_acc_numbers function in src/utils/acc_no_validator.py
- [X] T016 [P] [US2] Create duplicate_detector.py with detect_excel_duplicates function in src/utils/duplicate_detector.py
- [X] T017 [P] [US2] Create duplicate_detector.py with categorize_records function in src/utils/duplicate_detector.py
- [X] T018 [P] [US2] Create duplicate_detector.py with generate_skip_report function in src/utils/duplicate_detector.py
- [X] T019 [US2] Update add_commissioner.py bulk upload section to add pre-upload acc_no validation
- [X] T020 [US2] Update add_court.py bulk upload section to add pre-upload acc_no validation
- [X] T021 [US2] Add validation summary display in add_commissioner.py bulk upload
- [X] T022 [US2] Add validation summary display in add_court.py bulk upload
- [X] T023 [US2] Implement bulk insert logic to skip duplicates in add_commissioner.py
- [X] T024 [US2] Implement bulk insert logic to skip duplicates in add_court.py
- [X] T025 [US2] Add confirmation dialog before bulk insertion in add_commissioner.py
- [X] T026 [US2] Add confirmation dialog before bulk insertion in add_court.py

---

## Phase 5: User Story 3 - Independent Acc No Sequences Between Tables (Priority: P2)

**Goal**: As a data entry operator, I want to be able to use the same acc_no value in both commissioner and court records, so that I can maintain separate numbering sequences for different record types.

**Independent Test**: Can be fully tested by adding a commissioner record with acc_no 100 and then successfully adding a court record with the same acc_no 100, verifying that the system allows this since they're in separate tables.

### Implementation Tasks

- [X] T027 [US3] Verify that commissioner and court records use independent acc_no sequences in DAO methods
- [X] T028 [US3] Add informational messages about independent sequences in add_commissioner.py
- [X] T029 [US3] Add informational messages about independent sequences in add_court.py

---

## Phase 6: Error Reporting Enhancement

### Implementation Tasks

- [X] T030 [P] Create report_generator.py with generate_comprehensive_report function in src/utils/report_generator.py
- [X] T031 Add comprehensive error reporting with color coding in add_commissioner.py
- [X] T032 Add comprehensive error reporting with color coding in add_court.py
- [X] T033 Add downloadable skip report functionality in add_commissioner.py
- [X] T034 Add downloadable skip report functionality in add_court.py

---

## Phase 7: User Experience Improvements

### Implementation Tasks

- [X] T035 Add informational messages at top of single record forms in add_commissioner.py
- [X] T036 Add informational messages at top of single record forms in add_court.py
- [X] T037 Add informational messages at top of bulk upload sections in add_commissioner.py
- [X] T038 Add informational messages at top of bulk upload sections in add_court.py
- [ ] T039 Add visual feedback during validation in add_commissioner.py bulk upload
- [ ] T040 Add visual feedback during validation in add_court.py bulk upload

---

## Phase 8: Performance Optimization

### Implementation Tasks

- [X] T041 [P] Add database index on acc_no column for commissioner_records table
- [X] T042 [P] Add database index on acc_no column for court_records table
- [X] T043 Optimize pandas operations in bulk validation using set operations
- [ ] T044 Add progress bar for large Excel files (>1000 rows) in bulk upload sections

---

## Phase 9: Testing

### Implementation Tasks

- [X] T045 [P] Create unit tests for acc_no_exists() methods in tests/test_acc_no_validator.py
- [X] T046 [P] Create unit tests for get_all_acc_numbers() methods in tests/test_acc_no_validator.py
- [X] T047 [P] Create unit tests for validation utilities in tests/test_acc_no_validator.py
- [X] T048 [P] Create unit tests for duplicate detection utilities in tests/test_duplicate_detection.py
- [ ] T049 Create integration tests for single record validation in tests/integration/
- [ ] T050 Create integration tests for bulk upload validation in tests/integration/

---

## Phase 10: Polish & Cross-Cutting Concerns

### Implementation Tasks

- [X] T051 Update README with acc_no uniqueness validation documentation
- [X] T052 Add inline code documentation to all new functions and methods
- [X] T053 Create bulk_upload_guide.md with instructions on acc_no validation
- [X] T054 Perform final testing of all user stories independently
- [X] T055 Verify all acceptance scenarios from spec are satisfied