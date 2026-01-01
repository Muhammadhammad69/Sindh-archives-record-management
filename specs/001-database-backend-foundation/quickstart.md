# Quickstart Guide: Database and Backend Foundation

## Overview
This guide provides quick setup instructions for the secure PostgreSQL record management system backend foundation.

## Prerequisites
- Python 3.11+
- PostgreSQL database (NeonDB recommended)
- `uv` package manager (or pip)

## Setup Instructions

### 1. Clone and Navigate to Project
```bash
git clone <repository-url>
cd <project-root>
```

### 2. Setup Virtual Environment
```bash
# Using uv (recommended)
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Or using standard Python
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
# Using uv
uv pip install -r requirements.txt
uv pip install -r requirements-dev.txt

# Or using pip
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### 4. Configure Environment Variables
Create a `.env` file based on `.env.example`:
```bash
cp .env.example .env
```

Edit `.env` with your database connection details:
```env
DATABASE_URL=postgresql://username:password@localhost:5432/database_name
USERS_TABLE_NAME=users
COMMISSIONER_TABLE_NAME=commissioner_records
COURT_TABLE_NAME=court_records
```

### 5. Initialize Database
Run the database initialization script:
```bash
python -m src.scripts.init_db
```

This will:
- Create all required tables
- Set up proper indexes
- Create an initial admin user (if not exists)

### 6. Run Tests
Verify the installation with tests:
```bash
pytest -v
```

### 7. Type Checking
Verify type hints:
```bash
mypy src/
```

### 8. Code Formatting
Format code with black:
```bash
black src/ tests/
```

## Basic Usage

### Database Connection
```python
from src.database.connection import ConnectionManager

# Initialize connection
db_manager = ConnectionManager()
connection = db_manager.get_connection()
```

### User Management
```python
from src.dao.user_dao import UserDAO
from src.security.password_utils import hash_password

# Create user DAO
user_dao = UserDAO()

# Create a new user
hashed_password = hash_password("plain_text_password")
user_data = {
    "name": "John Doe",
    "email": "john@example.com",
    "password": hashed_password,
    "role": "user"
}
new_user = user_dao.create(user_data)
```

### Record Management
```python
from src.dao.commissioner_dao import CommissionerDAO

# Create commissioner record DAO
commissioner_dao = CommissionerDAO()

# Create a new commissioner record
record_data = {
    "acc_no": 12345,
    "department": "Legal",
    "file_no": "L-001",
    "subject": "Case Review",
    "year": 2025,
    "page": 1,
    "condition": "Good",
    "record_type": "Review"
}
new_record = commissioner_dao.create(record_data)
```

## Project Structure
```
src/
├── database/          # Database connection and models
├── dao/              # Data access objects
├── security/         # Security utilities (password hashing, auth)
├── config/           # Configuration management
├── utils/            # Utility functions
└── scripts/          # Initialization scripts

tests/
├── unit/             # Unit tests
└── integration/      # Integration tests
```

## Development Commands
```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=src

# Run specific test file
pytest tests/unit/test_user_dao.py

# Format code
black src/ tests/

# Check types
mypy src/

# Lint code
pylint src/
```

## Troubleshooting
- If you get database connection errors, verify your DATABASE_URL in `.env`
- If tests fail, ensure the database is running and accessible
- For dependency issues, try `pip install --upgrade pip` then reinstall requirements