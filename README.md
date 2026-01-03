# Sindh Archives - Record Management System

A secure PostgreSQL record management system with both backend foundation and web-based UI for managing commissioner and court records. The system implements database connection pooling, secure user authentication with role-based access control, and an intuitive web interface for public record viewing and administrative data management.

## Features

- Secure database connection pooling with PostgreSQL
- Role-based access control with bcrypt password hashing
- Data access objects for managing commissioner and court records
- Comprehensive audit trails with timestamp tracking
- Environment-based configuration management
- Web-based UI for public record viewing and admin data entry
- Responsive design with search and filter capabilities

## Requirements

- Python 3.11+
- PostgreSQL database (NeonDB recommended)
- `uv` package manager

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies with uv:
   ```bash
   uv sync
   ```
4. Copy the environment template and configure your database settings:
   ```bash
   cp .env.example .env
   # Edit .env with your database connection details
   ```
5. Initialize the database:
   ```bash
   python -m src.scripts.init_db
   ```

## Running the Web Application

To start the Streamlit web application:
```bash
uv run streamlit run app.py
```

The application will be available at `http://localhost:8501` by default.

## Project Structure

```
project-root/
├── app.py                 # Main Streamlit entry point
├── src/
│   ├── pages/             # Streamlit pages
│   │   ├── home.py        # Home page with navigation
│   │   ├── commissioner_records.py  # View commissioner records
│   │   ├── court_records.py         # View court records
│   │   ├── admin_login.py           # Admin login page
│   │   ├── admin_dashboard.py       # Admin dashboard
│   │   ├── add_commissioner.py      # Add commissioner form
│   │   └── add_court.py             # Add court form
│   ├── components/        # Reusable UI components
│   │   ├── auth.py        # Authentication utilities
│   │   └── sidebar.py     # Sidebar navigation
│   ├── ui/                # UI utilities
│   │   └── styles.py      # Custom CSS styling
│   ├── database/          # Database connection and models
│   ├── dao/               # Data access objects
│   ├── security/          # Security utilities (password hashing, auth)
│   ├── config/            # Configuration management
│   ├── utils/             # Utility functions
│   └── scripts/           # Initialization scripts
├── tests/                 # Unit and integration tests
└── docs/                  # Documentation
```

## Usage

### Public Users
- Access the home page to view available record types
- Navigate to commissioner or court records pages
- Use search and filter functionality to find specific records
- View records in a sortable, filterable table format

### Admin Users
- Access the admin dashboard via the sidebar
- Log in with admin credentials
- Add new commissioner records through the form
- Add new court records through the form
- Manage records with proper authentication and authorization

## Development

Run tests:
```bash
uv run pytest
```

Run tests with coverage:
```bash
uv run pytest --cov=src
```

Format code:
```bash
uv run black src/ tests/
```

Run type checking:
```bash
uv run mypy src/
```

Run linting:
```bash
uv run pylint src/
```