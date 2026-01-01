---
id: 1
title: Create Database Backend Foundation Spec
stage: spec
date: 2025-12-31
surface: agent
model: claude-sonnet-4-5-20250929
feature: 001-database-backend-foundation
branch: 001-database-backend-foundation
user: Anonymous
command: sp.specify
labels: [database, backend, foundation, specification]
links:
  spec: specs/001-database-backend-foundation/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-database-backend-foundation/spec.md
  - specs/001-database-backend-foundation/checklists/requirements.md
tests:
  - none
---

## Prompt

```
001-Database-and-Backend-Foundation

Must run this command /sp.specify
Branch Name: 001-Database-and-Backend-Foundation


Build a secure PostgreSQL record management system (Phase 1: Database & Backend Foundation). The system will use NeonDB as the database, Python with uv for package management, pandas for data operations, and Streamlit for the future UI. This phase focuses ONLY on establishing the backend foundation - no UI implementation yet.

CORE REQUIREMENTS:
1. Database Connection Management: Create a centralized, reusable PostgreSQL connection module that reads credentials from environment variables (DATABASE_URL, USERS_TABLE_NAME, COMMISSIONER_TABLE_NAME, COURT_TABLE_NAME). Never hardcode credentials. Use psycopg2 or asyncpg for connection pooling.

2. Schema Design & Table Creation: Design and create three tables with proper constraints:
   - users table: id (PK, auto-increment), name (varchar, not null), email (varchar, unique, not null), password (varchar hashed, not null), role (enum: 'admin' or 'user', not null)
   - commissioner_records table: id (PK, auto-increment), acc_no (integer, not null), department (varchar, not null), file_no (varchar, not null), subject (text, not null), year (integer, not null), page (integer, not null), condition (varchar, not null), record_type (varchar, not null)
   - court_records table: id (PK, auto-increment), acc_no (integer, not null), court (varchar, not null), suit_no (varchar, not null), plaintiff (varchar, not null), defendant (varchar, not null), claim_or_charge (text, not null), date_from (date, not null), date_to (date, not null), language (varchar, not null)

3. Security Foundation: Implement password hashing using bcrypt or argon2. Create utility functions for hash generation and verification. Ensure all database queries use parameterized statements to prevent SQL injection. Add created_at and updated_at timestamps to all tables for audit trails.

4. Data Access Layer: Build a modular data access layer with separate classes/modules for each table (UsersDAO, CommissionerRecordsDAO, CourtRecordsDAO). Each DAO should provide CRUD operations (create, read, update, delete) using pandas DataFrames where applicable. Include proper error handling and logging.

5. Environment Configuration: Use python-dotenv to load environment variables from .env file. Validate that all required environment variables are present on startup. Provide clear error messages if configuration is missing.

6. Database Initialization: Create a database initialization script that checks if tables exist, creates them if needed with proper indexes (email index on users table, acc_no indexes on record tables), and optionally seeds an initial admin user with a secure default password that must be changed on first login.

TECHNICAL CONSTRAINTS:
- Use uv for Python package management and virtual environment
- Python 3.11+ required
- Use pandas for data manipulation where beneficial
- All database operations must be transactional
- Implement proper connection pooling
- Follow type hints and proper error handling
- Create comprehensive logging for all database operations
- No UI components in this phase - focus purely on backend

DELIVERABLES FOR PHASE 1:
- Database connection module with connection pooling
- SQL schema files for table creation
- Data access objects for all three tables
- Password hashing utilities
- Database initialization script
- Environment configuration module
- Basic logging setup
- Unit tests for critical database operations
- README with setup instructions for Phase 1

This is Phase 1 only - establish the foundation. Authentication flow, admin panel, and public UI will come in later phases.
```

## Response snapshot

Created comprehensive specification for the Database and Backend Foundation feature, including: User stories for database connection management (P1), user account management (P1), record management foundation (P2), and system initialization (P2). Defined functional requirements (FR-001 through FR-012) covering database connections, security, CRUD operations, and system initialization. Identified key entities (User, CommissionerRecord, CourtRecord, DatabaseConnection) and established measurable success criteria (SC-001 through SC-006) for performance, security, and reliability.

## Outcome

- ✅ Impact: Created complete specification for backend foundation phase
- 🧪 Tests: none
- 📁 Files: Created spec.md and requirements checklist
- 🔁 Next prompts: Ready for planning phase with /sp.plan
- 🧠 Reflection: Specification captures all core requirements while maintaining focus on backend foundation

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A