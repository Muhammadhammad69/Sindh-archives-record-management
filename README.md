# Sindh Archives Backend

A secure PostgreSQL record management system backend foundation using Python 3.11+, NeonDB, and modular architecture. The system implements database connection pooling, secure user authentication with role-based access control, and data access objects for managing commissioner and court records.

## Features

- Secure database connection pooling with PostgreSQL
- Role-based access control with bcrypt password hashing
- Data access objects for managing commissioner and court records
- Comprehensive audit trails with timestamp tracking
- Environment-based configuration management

## Requirements

- Python 3.11+
- PostgreSQL database (NeonDB recommended)
- `uv` package manager (or pip)

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
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

## Project Structure

```
project-root/
├── src/
│   ├── database/           # Database connection and models
│   ├── dao/               # Data access objects
│   ├── security/          # Security utilities (password hashing, auth)
│   ├── config/            # Configuration management
│   ├── utils/             # Utility functions
│   └── scripts/           # Initialization scripts
├── tests/                 # Unit and integration tests
└── docs/                  # Documentation
```

## Usage

The backend provides secure access to commissioner and court records with proper authentication and authorization controls. All database operations include audit trails and validation.

## Development

Run tests:
```bash
pytest
```

Run tests with coverage:
```bash
pytest --cov=src
```

Format code:
```bash
black src/ tests/
```

Run type checking:
```bash
mypy src/
```

Run linting:
```bash
pylint src/
```