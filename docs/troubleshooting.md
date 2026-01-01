# Troubleshooting Guide for Sindh Archives Backend

This guide covers common issues and their solutions when working with the Sindh Archives Backend system.

## Installation and Setup Issues

### Problem: Dependency Installation Failures
**Symptoms**: `pip install` fails with compilation errors or missing dependencies

**Solution**:
1. Ensure you have the PostgreSQL development headers installed:
   - Ubuntu/Debian: `sudo apt-get install libpq-dev python3-dev`
   - CentOS/RHEL: `sudo yum install postgresql-devel python3-devel`
   - macOS: `brew install postgresql`

2. Try installing with the `--no-cache-dir` flag:
   ```bash
   pip install --no-cache-dir -r requirements.txt
   ```

### Problem: Database Connection Errors
**Symptoms**: `psycopg2.OperationalError` or "could not connect to server"

**Solution**:
1. Verify that PostgreSQL is running:
   ```bash
   # Check if PostgreSQL service is running
   sudo systemctl status postgresql  # Linux
   brew services list | grep postgresql  # macOS
   ```

2. Verify your DATABASE_URL in `.env`:
   - Format: `postgresql://username:password@host:port/database_name`
   - Ensure the database exists: `createdb your_database_name`

3. Check PostgreSQL configuration (`postgresql.conf`) for:
   - `listen_addresses` includes the connection host
   - Port matches the one in your connection string

## Authentication Issues

### Problem: Invalid Credentials Error
**Symptoms**: Login fails with "Invalid credentials" despite correct email/password

**Solution**:
1. Verify the password was properly hashed when creating the user
2. Check that the bcrypt library is properly installed and functioning
3. Ensure the password comparison is done correctly in the authentication function

### Problem: JWT Token Expiration
**Symptoms**: API requests fail with 401 Unauthorized after a period of time

**Solution**:
1. The JWT token has an expiration time (default: 24 hours)
2. Implement token refresh functionality or re-authenticate to get a new token
3. Adjust the `JWT_EXPIRATION_HOURS` environment variable if needed

## Database Issues

### Problem: Connection Pool Exhaustion
**Symptoms**: Application hangs or throws "connection pool exhausted" errors

**Solution**:
1. Check the connection pool configuration in `.env`:
   - `DB_MIN_CONNECTIONS` (default: 2)
   - `DB_MAX_CONNECTIONS` (default: 10)

2. Ensure all database connections are properly closed:
   - Use context managers (`with` statements) when possible
   - Always return connections to the pool after use

### Problem: Slow Query Performance
**Symptoms**: Database operations take longer than expected (>1 second)

**Solution**:
1. Verify that proper indexes exist:
   - Index on `users.email`
   - Index on `commissioner_records.acc_no`
   - Index on `court_records.acc_no`

2. Check for missing indexes:
   ```sql
   -- Check existing indexes
   SELECT * FROM pg_indexes WHERE tablename IN ('users', 'commissioner_records', 'court_records');
   ```

## Data Validation Issues

### Problem: Record Creation Fails Validation
**Symptoms**: API returns 400 Bad Request with validation errors

**Solution**:
1. Check the validation rules for the specific entity:
   - **Users**: Email format, password strength, required fields
   - **Commissioner Records**: Positive acc_no, year, page values
   - **Court Records**: Valid date formats, date range validation

2. Verify the request body matches the expected format in the API documentation

### Problem: Date Format Errors
**Symptoms**: Court records fail to create with "Invalid date format" errors

**Solution**:
1. Ensure dates are in the format `YYYY-MM-DD`
2. Verify that `date_to` is not earlier than `date_from`

## Security Issues

### Problem: SQL Injection Vulnerabilities
**Symptoms**: Security scan detects potential SQL injection

**Solution**:
1. Ensure all database queries use parameterized queries with `%s` placeholders
2. Never concatenate user input directly into SQL strings
3. Use the provided DAO classes which automatically handle parameterization

### Problem: Weak Password Detection
**Symptoms**: Password creation fails despite meeting apparent requirements

**Solution**:
1. Verify password meets all strength requirements:
   - At least 8 characters long
   - Contains uppercase letter
   - Contains lowercase letter
   - Contains digit
   - Contains special character

## Environment Configuration

### Problem: Missing Environment Variables
**Symptoms**: Application fails to start with "Environment variable not set" errors

**Solution**:
1. Verify your `.env` file exists in the project root
2. Ensure all required variables are present:
   - `DATABASE_URL`
   - `USERS_TABLE_NAME`
   - `COMMISSIONER_TABLE_NAME`
   - `COURT_TABLE_NAME`

3. Check that the `.env` file is not in `.gitignore` (for local development)

### Problem: Permission Issues
**Symptoms**: Cannot access database or perform operations

**Solution**:
1. Verify database user has proper permissions:
   ```sql
   -- Grant necessary permissions
   GRANT ALL PRIVILEGES ON TABLE users TO your_db_user;
   GRANT ALL PRIVILEGES ON TABLE commissioner_records TO your_db_user;
   GRANT ALL PRIVILEGES ON TABLE court_records TO your_db_user;
   ```

## Testing Issues

### Problem: Tests Fail Due to Database Connection
**Symptoms**: Tests fail with database connection errors

**Solution**:
1. Ensure test database is set up and accessible
2. Check that `TEST_DATABASE_URL` is properly configured in your test environment
3. Verify the test database has the required tables (run initialization script)

### Problem: Flakey Integration Tests
**Symptoms**: Tests pass sometimes but fail at other times

**Solution**:
1. Ensure tests clean up after themselves (delete created records)
2. Use unique identifiers in tests to avoid conflicts
3. Consider using transactions that are rolled back after each test

## Performance Issues

### Problem: High Memory Usage
**Symptoms**: Application consumes excessive memory

**Solution**:
1. Check for memory leaks in connection handling
2. Monitor connection pool size and adjust if needed
3. Verify pandas operations are not loading unnecessary data

### Problem: Slow Startup Times
**Symptoms**: Application takes a long time to start

**Solution**:
1. Check if database connection initialization is taking too long
2. Verify that no unnecessary operations are performed at startup
3. Consider lazy loading of heavy components

## Contact Support

If you encounter an issue not covered in this guide:

1. Check the application logs for detailed error information
2. Verify you're using the latest version of the code
3. Consult the API documentation
4. Reach out to the development team with:
   - Detailed description of the problem
   - Steps to reproduce
   - Error messages and logs
   - Environment information (OS, Python version, PostgreSQL version)