# Quickstart Guide: Streamlit Web Application

## Overview
This guide provides instructions for setting up, running, and using the Streamlit-based web application for the record management system.

## Prerequisites
- Python 3.11+
- uv package manager
- PostgreSQL database (with existing Phase 1 schema and data)
- Environment variables configured in `.env` file

## Setup Instructions

### 1. Clone and Navigate to Project Directory
```bash
cd /path/to/your/project
```

### 2. Install Dependencies with uv
```bash
uv sync
```

### 3. Configure Environment Variables
Ensure your `.env` file contains the required database connection information:
```
DATABASE_URL=postgresql://username:password@localhost:5432/database_name
USERS_TABLE_NAME=users
COMMISSIONER_TABLE_NAME=commissioner_records
COURT_TABLE_NAME=court_records
```

### 4. Verify Database Connection
Make sure the Phase 1 database schema exists and is accessible with the configured credentials.

## Running the Application

### Start the Streamlit Application
```bash
uv run streamlit run app.py
```

The application will start on `http://localhost:8501` by default.

### Development Mode (with auto-reload)
```bash
uv run streamlit run app.py --server.runOnSave=true
```

## Using the Application

### Public User Features
1. **Home Page**: Upon visiting the application, you'll see a centered card with two buttons:
   - "Commissioner Records" - Click to view commissioner records
   - "Court Records" - Click to view court records

2. **Viewing Records**:
   - Browse commissioner records with sortable, filterable table
   - Browse court records with sortable, filterable table
   - View formatted dates (dd/mm/yyyy) for court records
   - See record counts at the top of each table

### Admin User Features
1. **Access Admin Dashboard**:
   - Click "Admin Dashboard" in the persistent sidebar
   - You'll be redirected to the login page

2. **Admin Login**:
   - Enter your admin email and password
   - Click "Login"
   - If credentials are valid and you have admin role, you'll be redirected to the admin dashboard

3. **Admin Dashboard**:
   - Two action buttons: "Add Commissioner Records" and "Add Court Records"
   - Click to navigate to respective data entry forms

4. **Adding Records**:
   - **Commissioner Records Form**:
     - Fill in all required fields (acc_no, department, file_no, subject, year, page, condition, record_type)
     - Click "Submit" to add the record
     - Form will clear after successful submission
   - **Court Records Form**:
     - Fill in all required fields (acc_no, court, suit_no, plaintiff, defendant, claim_or_charge, date_from, date_to, language)
     - Ensure date_to is after date_from
     - Click "Submit" to add the record
     - Form will clear after successful submission

5. **Logout**:
   - Click "Logout" in the sidebar to end your session

## Troubleshooting

### Common Issues

**Issue**: Application fails to start with database connection error
**Solution**: Verify your `.env` file has correct database credentials and the database server is running.

**Issue**: Admin login fails with "Invalid email or password"
**Solution**: Ensure you're using an existing admin user account with role='admin' in the users table.

**Issue**: Streamlit command not found
**Solution**: Make sure you've installed Streamlit and are running with uv: `uv run streamlit run app.py`

**Issue**: Forms show validation errors
**Solution**: Check that all required fields are filled with valid data:
- acc_no must be positive integers
- Year must be between 1800-2100 for commissioner records
- date_to must be after date_from for court records

### Performance Tips
- For large datasets, the application includes loading indicators
- The UI is optimized for responsive viewing across different screen sizes
- Empty states are handled gracefully with user-friendly messages

## Development

### Project Structure
```
project-root/
├── app.py                    # Main Streamlit entry point
├── src/
│   ├── pages/               # Streamlit pages
│   │   ├── home.py
│   │   ├── commissioner_records.py
│   │   ├── court_records.py
│   │   ├── admin_login.py
│   │   ├── admin_dashboard.py
│   │   ├── add_commissioner.py
│   │   └── add_court.py
│   ├── components/          # Reusable UI components
│   │   ├── sidebar.py
│   │   └── auth.py
│   └── ui/                  # UI utilities
│       └── styles.py
```

### Adding New Features
1. Create new page modules in `src/pages/`
2. Update routing logic in `app.py`
3. Follow the same authentication patterns used in existing pages
4. Use existing DAOs for database operations
5. Maintain consistent UI/UX patterns

## Testing

### Running Tests
```bash
uv run pytest tests/
```

### Test Structure
- `tests/test_pages/` - UI component tests
- `tests/unit/` - Unit tests for business logic
- `tests/integration/` - Integration tests for database operations

## Security Notes
- Passwords are hashed using bcrypt (stored in database, never in UI)
- Session state is maintained using Streamlit's secure session_state
- Admin access is restricted to users with 'admin' role
- All database queries use parameterized statements (via existing DAOs)
- Authentication checks are performed on all protected routes