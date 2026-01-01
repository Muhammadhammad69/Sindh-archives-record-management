---
id: 1
title: "Create Specification for Streamlit UI and Admin System"
stage: "spec"
date: "2026-01-01"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "002-streamlit-ui-admin"
branch: "002-streamlit-ui-admin"
user: "user"
command: "sp.specify 002-Application-UI-and-Admin-System"
labels: ["specification", "streamlit", "ui", "admin-system", "web-application"]
links:
  spec: "specs/002-streamlit-ui-admin/spec.md"
  ticket: null
  adr: null
  pr: null
files:
  - "specs/002-streamlit-ui-admin/spec.md"
  - "specs/002-streamlit-ui-admin/checklists/requirements.md"
tests: []
---

# Create Specification for Streamlit UI and Admin System

## Prompt Text

```
002-Application-UI-and-Admin-System

Must run this command /sp.specify
Branch Name: 002-Application-UI-and-Admin-System

Build a complete Streamlit-based web application for the record management system (Phase 2: Application, UI & Admin System). This phase creates the full user interface with public record viewing and admin data management capabilities. Use uv for package management, Streamlit for the web interface, pandas for data display, and context7 MCP to fetch official documentation for Streamlit components, session state management, and authentication patterns when needed.

CORE REQUIREMENTS:

1. Home Page (Public Interface):
   Create a centered card layout with a persistent sidebar. The main card displays two prominent action buttons: "Commissioner Records" and "Court Records". When clicked, each button navigates to its respective records viewing page where data is fetched from the database via existing DAOs and displayed in a clean, searchable table format using st.dataframe or pandas. If no records exist, show a user-friendly empty state message like "No records found in the system."

2. Sidebar Navigation (Persistent Across All Pages):
   Implement a sidebar that remains visible on all pages with a single navigation item: "Admin Dashboard". Clicking this item redirects users to the admin login page. The sidebar should use Streamlit's st.sidebar for consistent placement and styling.

3. Records Viewing Pages (Public Access):
   - Commissioner Records Page: Display all commissioner records in a sortable, filterable table with columns: acc_no, department, file_no, subject, year, page, condition, record_type. Use pandas DataFrame with st.dataframe for interactive features like sorting and searching. Include record count display.
   - Court Records Page: Display all court records with columns: acc_no, court, suit_no, plaintiff, defendant, claim_or_charge, date_from, date_to, language. Format dates properly (dd/mm/yyyy display format). Include filtering options by date range or court name if feasible.

4. Admin Login System (Protected Route):
   Create a dedicated login page with email and password input fields using st.text_input (password field with type="password"). On form submission:
   - Fetch user from database using UsersDAO by email
   - If user doesn't exist, display error: "Invalid email or password"
   - If user exists but role is not 'admin', display error: "Access denied. Admin privileges required."
   - If user exists and role is 'admin', verify password using existing password verification utility
   - On successful authentication, store admin session in st.session_state (store user_id, email, role, is_authenticated=True)
   - Redirect to Admin Dashboard on successful login

5. Admin Dashboard (Protected Area - Admin Only):
   Create a protected dashboard page that checks st.session_state for authentication before rendering. If not authenticated or role is not admin, redirect to login page with warning message. The dashboard displays a centered card with two action buttons: "Add Commissioner Records" and "Add Court Records". Each button navigates to its respective data entry form.

6. Add Commissioner Records Form (Admin Only):
   Build a comprehensive form with input fields for all commissioner record attributes:
   - acc_no (number input, required, positive integer)
   - department (text input, required)
   - file_no (text input, required)
   - subject (text area, required)
   - year (number input, required, 1800-2100 range validation)
   - page (number input, required, positive integer)
   - condition (selectbox with options: FAIR/BOUND, GOOD/BOUND, POOR/UNBOUND, EXCELLENT/BOUND)
   - record_type (selectbox with options: TEXTUAL RECORD, PHOTOGRAPHIC RECORD, DIGITAL RECORD)

   On form submission, validate all fields, call CommissionerRecordsDAO.create(), display success message with st.success, and clear form for next entry. Handle errors with st.error displaying specific validation failures.

7. Add Court Records Form (Admin Only):
   Build a form with input fields for all court record attributes:
   - acc_no (number input, required, positive integer)
   - court (text input, required)
   - suit_no (text input, required)
   - plaintiff (text input, required)
   - defendant (text input, required)
   - claim_or_charge (text area, required)
   - date_from (date input, required)
   - date_to (date input, required, must be after date_from)
   - language (text input, required, example: "English, Hindi")

   Validate date_from is before date_to. On submission, call CourtRecordsDAO.create(), show success message, clear form. Handle validation errors appropriately.

8. Session Management & Authentication Flow:
   Implement proper session state management using st.session_state to track:
   - is_authenticated (boolean)
   - user_id (integer)
   - user_email (string)
   - user_role (string: 'admin' or 'user')

   Create authentication check functions that can be reused across protected pages. Implement logout functionality accessible from admin pages that clears session state and redirects to home page.

9. Navigation & Routing:
   Use Streamlit's st.navigation or query parameters to handle page routing between:
   - Home page (/)
   - Commissioner Records page (/commissioner-records)
   - Court Records page (/court-records)
   - Admin Login page (/admin-login)
   - Admin Dashboard page (/admin-dashboard)
   - Add Commissioner Form page (/admin/add-commissioner)
   - Add Court Form page (/admin/add-court)

10. Error Handling & User Experience:
    - Display loading spinners (st.spinner) during database operations
    - Show clear success messages after successful data insertion
    - Display user-friendly error messages for validation failures, database errors, or authentication issues
    - Implement empty state messages when no records are found
    - Add confirmation dialogs for critical actions if needed
    - Ensure responsive layout that works on different screen sizes

11. UI/UX Standards:
    - Use Streamlit's built-in theming for consistent look
    - Center important cards using st.columns for layout
    - Use st.form for all data entry forms to batch input and submit
    - Implement proper spacing with st.divider or empty containers
    - Add descriptive labels and help text for form fields
    - Use icons or emojis for visual appeal where appropriate
    - Maintain consistent button styling and placement

TECHNICAL CONSTRAINTS:
- Use uv for all package management and running the app
- Streamlit as the web framework (install via uv: streamlit)
- Reuse all existing Phase 1 infrastructure (DAOs, models, database connection, security utilities)
- Use pandas for data display and manipulation
- Use context7 MCP whenever you need Streamlit documentation for:
  * Session state management patterns
  * Multi-page app structure
  * Form handling and validation
  * Authentication implementation
  * Data table display options
  * Navigation and routing
- No additional authentication libraries (use existing bcrypt utilities from Phase 1)
- Store session data in st.session_state only (no external session management)

SECURITY REQUIREMENTS:
- Never display passwords in UI
- Hash passwords remain in database only
- Protected pages must check authentication before rendering
- Role verification must happen on every protected page load
- Session state should be validated on each page access
- Implement logout functionality to clear sensitive session data

DELIVERABLES FOR PHASE 2:
- Main Streamlit app entry point (app.py or main.py)
- Page modules for each route (home, records views, login, dashboard, forms)
- Authentication utilities for session management
- Reusable UI components (headers, protected route wrapper)
- Updated requirements in pyproject.toml
- README section for running the Streamlit app with uv
- Testing instructions for UI flows

Run the app with: `uv run streamlit run app.py`

This phase builds upon the tested Phase 1 backend foundation and creates a production-ready web interface for both public users and administrators.
```

## Response Text

Created comprehensive feature specification for the Streamlit-based web application for record management system. The specification includes:

- User scenarios and testing with 4 prioritized user stories covering public record viewing, admin authentication, and record addition functionality
- 20 functional requirements detailing all system capabilities
- Key entities identification
- 8 measurable success criteria

The specification follows the template structure and addresses all core requirements from the feature description, including home page, sidebar navigation, record viewing pages, admin login, dashboard, and forms for adding records. A quality checklist was also created to validate the specification meets all requirements.