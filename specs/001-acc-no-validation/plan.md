# Implementation Plan: Acc No Uniqueness Validation

**Branch**: `001-acc-no-validation` | **Date**: 2026-01-04 | **Spec**: specs/001-acc-no-validation/spec.md
**Input**: Feature specification from `/specs/001-acc-no-validation/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implement acc_no uniqueness validation across both single record entry and bulk Excel upload modes for commissioner and court records. This involves adding database-level validation methods to DAOs, creating validation utilities for single and bulk operations, updating UI pages to incorporate validation checks, and providing comprehensive feedback and reporting for duplicate scenarios. The solution uses PostgreSQL EXISTS queries for efficient duplicate checking, Python sets for O(1) lookups during bulk validation, and pandas operations for internal duplicate detection.

## Technical Context

**Language/Version**: Python 3.11
**Primary Dependencies**: psycopg2-binary (PostgreSQL), pandas, Streamlit, python-dotenv, bcrypt
**Storage**: PostgreSQL (NeonDB)
**Testing**: pytest
**Target Platform**: Linux server (web application)
**Project Type**: Web application
**Performance Goals**: <2 seconds for single record validation, <30 seconds for bulk validation of up to 1000 records
**Constraints**: <200ms p95 for single record validation, maintain existing UI workflow, preserve form data on validation failure
**Scale/Scope**: Up to 5000 records in bulk uploads, support existing commissioner and court record tables

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- Security & Authentication: Validation checks will use parameterized queries to prevent SQL injection
- Data Integrity: Acc_no uniqueness will be enforced at the application level to maintain data integrity
- Code Quality: All new code will follow Python best practices with type hints and proper error handling
- User Experience: Clear feedback will be provided to users about validation results
- Database Design: Efficient queries using EXISTS and proper indexing will be implemented
- Testing & Reliability: Unit tests will be created for all new validation logic

## Project Structure

### Documentation (this feature)

```text
specs/001-acc-no-validation/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
src/
├── database/
│   └── models
│       ├── commissioner_record.py     # Add acc_no_exists() method
│       └── court_record.py            # Add acc_no_exists() method
├── utils/
│   ├── acc_no_validator.py            # NEW - acc_no uniqueness utilities
│   └── duplicate_detector.py          # NEW - Detect duplicates in Excel
├── pages/
│   ├── add_commissioner.py            # Update single & bulk with acc_no check
│   └── add_court.py                   # Update single & bulk with acc_no check
└── tests/
    ├── test_acc_no_validator.py       # NEW - Test uniqueness validation
    └── test_duplicate_detection.py    # NEW - Test duplicate detection
```

### Testing Structure
```text
tests/
├── test_acc_no_validator.py           # Unit tests for validation utilities
├── test_duplicate_detection.py        # Unit tests for duplicate detection
└── integration/                       # Integration tests for UI flows
```

**Structure Decision**: The project follows a web application structure with clear separation of concerns. Database models handle data access, utilities provide reusable functions, pages contain UI logic, and tests ensure reliability. This structure maintains the existing architecture while adding the necessary validation functionality.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| New utility modules | Separate validation logic from UI and data access | Would create tightly coupled code that's hard to test and maintain |
| Additional DAO methods | Needed for efficient duplicate checking | Direct SQL queries would violate data access patterns established in the project |
