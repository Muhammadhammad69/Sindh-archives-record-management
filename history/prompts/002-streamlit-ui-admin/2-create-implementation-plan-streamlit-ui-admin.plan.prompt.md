---
id: 2
title: "Create Implementation Plan for Streamlit UI Admin System"
stage: "plan"
date: "2026-01-01"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "002-streamlit-ui-admin"
branch: "002-streamlit-ui-admin"
user: "user"
command: "sp.plan 002-streamlit-ui-admin"
labels: ["planning", "streamlit", "ui", "admin-system", "architecture"]
links:
  spec: "specs/002-streamlit-ui-admin/spec.md"
  ticket: null
  adr: null
  pr: null
files:
  - "specs/002-streamlit-ui-admin/plan.md"
  - "specs/002-streamlit-ui-admin/research.md"
  - "specs/002-streamlit-ui-admin/data-model.md"
  - "specs/002-streamlit-ui-admin/contracts/api-contracts.json"
  - "specs/002-streamlit-ui-admin/quickstart.md"
tests: []
---

# Create Implementation Plan for Streamlit UI Admin System

## Prompt Text

```
002-streamlit-ui-admin

Must run this command /sp.plan

Use Python 3.11+ with uv for package management and Streamlit as the web framework. Build a multi-page Streamlit application with modular architecture separating concerns into authentication, page components, and data display utilities. Use context7 MCP to fetch official Streamlit documentation whenever implementing session state, multi-page navigation, forms, or authentication patterns.

TECHNOLOGY STACK:
- Web Framework: Streamlit (latest stable version)
- Data Display: pandas for DataFrame operations and st.dataframe for interactive tables
- Authentication: Reuse Phase 1 bcrypt utilities with Streamlit session_state
- Database Layer: Reuse Phase 1 DAOs (UsersDAO, CommissionerRecordsDAO, CourtRecordsDAO)
- Package Management: uv for all dependencies
- Version Control: Git with commit after each completed feature/task

PROJECT STRUCTURE:

project-root/
├── .env                          # Environment variables (already exists)
├── .gitignore                    # Updated with Streamlit cache folders
├── pyproject.toml                # Updated with Streamlit dependencies
├── README.md                     # Updated with Phase 2 instructions
├── app.py                        # Main Streamlit entry point
├── src/
│   ├── init.py
│   ├── config/                   # (Phase 1 - already exists)
│   ├── database/                 # (Phase 1 - already exists)
│   ├── models/                   # (Phase 1 - already exists)
│   ├── security/                 # (Phase 1 - already exists)
│   ├── utils/                    # (Phase 1 - already exists)
│   ├── pages/                    # Streamlit pages
│   │   ├── init.py
│   │   ├── home.py               # Home page with commissioner/court buttons
│   │   ├── commissioner_records.py  # View commissioner records
│   │   ├── court_records.py      # View court records
│   │   ├── admin_login.py        # Admin login page
│   │   ├── admin_dashboard.py    # Admin dashboard (protected)
│   │   ├── add_commissioner.py   # Add commissioner form (protected)
│   │   └── add_court.py          # Add court form (protected)
│   ├── components/               # Reusable UI components
│   │   ├── init.py
│   │   ├── sidebar.py            # Persistent sidebar navigation
│   │   ├── auth.py               # Authentication utilities and decorators
│   │   └── forms.py              # Form validation helpers
│   └── ui/                       # UI utilities
│       ├── init.py
│       └── styles.py             # Custom CSS and styling
└── tests/
├── init.py
├── test_pages/               # UI component tests
│   ├── test_auth.py
│   └── test_forms.py
└── conftest.py               # Pytest fixtures (updated)

IMPLEMENTATION APPROACH WITH GIT WORKFLOW:

1. **Update Project Dependencies (Commit Immediately)**:
   - Add Streamlit to pyproject.toml dependencies
   - Run `uv sync` to install Streamlit
   - Update .gitignore with Streamlit-specific patterns (.streamlit/, __pycache__/)
   - Test: Verify `uv run streamlit --version` works
   - Git commit: "feat(phase2): add Streamlit dependencies and update gitignore"

2. **Create Authentication Utilities (Test & Commit)**:
   - Implement src/components/auth.py with session management functions:
     * initialize_session_state() - sets up default session variables
     * is_authenticated() - checks if user is logged in
     * is_admin() - checks if user has admin role
     * login_user(user_id, email, role) - stores user in session
     * logout_user() - clears session state
     * require_auth() - decorator for protected pages
   - Use context7 MCP if needed: "Get Streamlit documentation for session_state management patterns"
   - Test: Create test script that simulates session operations
   - Git commit: "feat(auth): implement session state management utilities"

3. **Create Persistent Sidebar Component (Test & Commit)**:
   - Implement src/components/sidebar.py with render_sidebar() function
   - Use st.sidebar with navigation links
   - Include "Admin Dashboard" link that redirects to login if not authenticated
   - Test: Run minimal Streamlit app that calls render_sidebar()
   - Git commit: "feat(ui): add persistent sidebar navigation component"

4. **Build Main App Entry Point (Test & Commit)**:
   - Create app.py with page routing logic using st.navigation or query params
   - Initialize session state on app load
   - Implement basic routing structure for all pages
   - Use context7 MCP if needed: "Get Streamlit documentation for multi-page app structure"
   - Test: Run `uv run streamlit run app.py` and verify basic navigation
   - Git commit: "feat(app): create main entry point with page routing"

5. **Implement Home Page (Test & Commit)**:
   - Create src/pages/home.py with centered card layout
   - Add two buttons: "Commissioner Records" and "Court Records"
   - Implement navigation on button clicks using st.session_state or query params
   - Include persistent sidebar
   - Test: Verify buttons navigate to correct pages
   - Git commit: "feat(pages): implement home page with record navigation"

6. **Build Commissioner Records Viewing Page (Test & Commit)**:
   - Create src/pages/commissioner_records.py
   - Fetch all records using CommissionerRecordsDAO.get_all()
   - Display in st.dataframe with all columns visible
   - Add record count display
   - Handle empty state with friendly message
   - Include search/filter functionality if feasible
   - Test: Verify records display correctly, test with empty database
   - Git commit: "feat(pages): add commissioner records viewing page"

7. **Build Court Records Viewing Page (Test & Commit)**:
   - Create src/pages/court_records.py
   - Fetch all records using CourtRecordsDAO.get_all()
   - Format dates for display (dd/mm/yyyy)
   - Display in st.dataframe with proper column ordering
   - Add record count and optional filters
   - Handle empty state
   - Test: Verify date formatting, test with empty database
   - Git commit: "feat(pages): add court records viewing page"

8. **Implement Admin Login Page (Test & Commit)**:
   - Create src/pages/admin_login.py with st.form
   - Add email and password fields (password type="password")
   - Implement authentication logic:
     * Fetch user by email using UsersDAO
     * Verify password using Phase 1 security utilities
     * Check role == 'admin'
     * Display appropriate error messages
   - On success, call login_user() and redirect to dashboard
   - Use context7 MCP if needed: "Get Streamlit documentation for form handling and validation"
   - Test: Try valid admin login, invalid credentials, non-admin user
   - Git commit: "feat(auth): implement admin login page with validation"

9. **Build Admin Dashboard (Test & Commit)**:
   - Create src/pages/admin_dashboard.py with @require_auth decorator
   - Check authentication and admin role before rendering
   - Display centered card with two action buttons:
     * "Add Commissioner Records"
     * "Add Court Records"
   - Implement navigation to respective forms
   - Add logout button in sidebar or page
   - Test: Access without login (should redirect), access with admin login
   - Git commit: "feat(admin): add protected admin dashboard page"

10. **Create Add Commissioner Records Form (Test & Commit)**:
    - Create src/pages/add_commissioner.py with @require_auth protection
    - Build comprehensive st.form with all required fields:
      * acc_no (st.number_input, min_value=1)
      * department (st.text_input)
      * file_no (st.text_input)
      * subject (st.text_area)
      * year (st.number_input, min_value=1800, max_value=2100)
      * page (st.number_input, min_value=1)
      * condition (st.selectbox with predefined options)
      * record_type (st.selectbox with predefined options)
    - Implement form validation and error display
    - On submit, call CommissionerRecordsDAO.create()
    - Display success message and clear form
    - Use context7 MCP if needed: "Get Streamlit documentation for form widgets and validation"
    - Test: Submit valid record, test validation errors, verify database insertion
    - Git commit: "feat(admin): add commissioner records creation form"

11. **Create Add Court Records Form (Test & Commit)**:
    - Create src/pages/add_court.py with @require_auth protection
    - Build st.form with all court record fields:
      * acc_no (st.number_input, min_value=1)
      * court (st.text_input)
      * suit_no (st.text_input)
      * plaintiff (st.text_input)
      * defendant (st.text_input)
      * claim_or_charge (st.text_area)
      * date_from (st.date_input)
      * date_to (st.date_input)
      * language (st.text_input)
    - Validate date_to > date_from
    - On submit, call CourtRecordsDAO.create()
    - Display success and clear form
    - Test: Submit valid record, test date validation, verify database insertion
    - Git commit: "feat(admin): add court records creation form"

12. **Implement Logout Functionality (Test & Commit)**:
    - Add logout button to sidebar (visible only when authenticated)
    - Call logout_user() on click
    - Redirect to home page
    - Test: Login, logout, verify session cleared
    - Git commit: "feat(auth): add logout functionality"

13. **Add UI Styling & Polish (Test & Commit)**:
    - Create src/ui/styles.py with custom CSS if needed
    - Add consistent spacing, colors, and layout
    - Add loading spinners for database operations
    - Implement empty state designs
    - Add icons/emojis for visual appeal
    - Test: Review UI on different pages, check responsiveness
    - Git commit: "feat(ui): add styling and UX improvements"

14. **Comprehensive Integration Testing (Test & Commit)**:
    - Test complete user flow: home → view records → login → add records → logout
    - Test error scenarios: invalid login, unauthorized access, validation errors
    - Test with empty database and populated database
    - Verify all navigation works correctly
    - Test: Run through all user stories end-to-end
    - Git commit: "test(phase2): add integration tests for complete user flows"

15. **Update Documentation (Test & Commit)**:
    - Update README.md with Phase 2 instructions
    - Document how to run Streamlit app: `uv run streamlit run app.py`
    - Add screenshots or GIFs of UI if possible
    - Document admin credentials for testing
    - Add troubleshooting section for common Streamlit issues
    - Test: Follow README from scratch to verify completeness
    - Git commit: "docs(phase2): add Streamlit app documentation and usage guide"

TESTING STRATEGY:
- Test each page component immediately after implementation
- Verify authentication flows work correctly
- Test form validation and error handling
- Verify database operations from UI
- Test navigation between all pages
- Check session state persistence across pages
- Verify protected routes deny unauthorized access

GIT WORKFLOW (CRITICAL):
- **Commit after completing and testing each numbered task above**
- Use conventional commit format: feat/fix/test/docs
- Write descriptive commit messages mentioning what was tested
- Push to remote after every 2-3 commits
- Never commit untested code
- Example commits:
  - "feat(pages): add home page with navigation - tested button clicks"
  - "feat(auth): implement login validation - tested with admin/user roles"
  - "test(forms): add validation tests for commissioner form"
  - "fix(ui): handle empty records state - tested with empty database"

CONTEXT7 MCP USAGE:
Use context7 MCP to fetch official Streamlit documentation for:
- Session state management patterns
- Multi-page app architecture
- Form handling and validation
- st.dataframe customization options
- Authentication implementation patterns
- Navigation and routing best practices
- Error handling in Streamlit

DEPENDENCIES TO ADD:
- streamlit (latest stable)
- (All Phase 1 dependencies already installed)

VALIDATION CHECKLIST:
- [ ] Streamlit app runs without errors
- [ ] Home page displays with working navigation buttons
- [ ] Commissioner records page shows data from database
- [ ] Court records page shows data with formatted dates
- [ ] Admin login works with correct credentials
- [ ] Admin login rejects invalid credentials and non-admin users
- [ ] Admin dashboard accessible only to authenticated admins
- [ ] Add commissioner form validates and inserts data
- [ ] Add court form validates dates and inserts data
- [ ] Logout clears session and redirects properly
- [ ] Sidebar navigation works on all pages
- [ ] Protected routes redirect unauthenticated users
- [ ] All forms display clear error messages
- [ ] Empty states display friendly messages
- [ ] UI is clean and intuitive
- [ ] All tests passing
- [ ] Git history shows commits after each task completion
- [ ] README updated with Phase 2 instructions

This plan ensures systematic development with immediate testing and git commits after each feature completion. Every component is verified before moving forward, and all work is properly tracked with meaningful commits.
```

## Response Text

Successfully created the implementation plan for the Streamlit Web Application for Record Management System. The following artifacts were generated:

1. **Implementation Plan** (plan.md): Comprehensive plan with technical context, constitution check, and project structure
2. **Research Document** (research.md): Research on Streamlit-specific patterns, session state management, authentication, and multi-page architecture
3. **Data Model** (data-model.md): Detailed data model describing entities, relationships, validation rules, and state transitions
4. **API Contracts** (contracts/api-contracts.json): Interface contracts between Streamlit UI and existing DAO layer
5. **Quickstart Guide** (quickstart.md): Complete setup, running, and usage instructions

The plan ensures compliance with the project constitution across all areas (Security, Data Integrity, Code Quality, User Experience, Database Design, and Testing). The architecture reuses existing Phase 1 infrastructure while implementing a clean, modular design with proper separation of concerns.

The agent context was updated to include the new technologies: Python 3.11+, Streamlit, pandas, uv package management, and PostgreSQL integration.