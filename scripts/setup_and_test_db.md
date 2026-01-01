# Database Setup and Testing Guide

This document explains how to set up a PostgreSQL database (NeonDB or local) and run the sample data insertion and verification scripts.

## Prerequisites

1. **PostgreSQL Server**: You need a running PostgreSQL server (either local or NeonDB)
2. **Environment Configuration**: Properly configured `.env` file with `DATABASE_URL`

## Setting up PostgreSQL Server

### Option 1: Local PostgreSQL Server

1. **Install PostgreSQL**:
   ```bash
   # On Ubuntu/Debian
   sudo apt update
   sudo apt install postgresql postgresql-contrib

   # On macOS
   brew install postgresql

   # On Windows, download from https://www.postgresql.org/download/
   ```

2. **Start PostgreSQL Service**:
   ```bash
   # On Ubuntu/Debian
   sudo systemctl start postgresql
   sudo systemctl enable postgresql

   # On macOS
   brew services start postgresql

   # On Windows, start from Services
   ```

3. **Create Database**:
   ```bash
   sudo -u postgres psql
   CREATE DATABASE sindh_archives;
   CREATE USER postgres WITH PASSWORD 'password';
   GRANT ALL PRIVILEGES ON DATABASE sindh_archives TO postgres;
   \q
   ```

### Option 2: NeonDB Setup

1. **Create NeonDB Account**: Go to https://neon.tech/ and create an account
2. **Create Project**: Create a new project in NeonDB
3. **Get Connection String**: Copy the connection string from the NeonDB dashboard
4. **Update .env file**:
   ```env
   DATABASE_URL=postgresql://[username]:[password]@[region].neon.tech/[dbname]?sslmode=require
   ```

## Running Database Initialization

1. **Initialize Tables**:
   ```bash
   uv run python src/scripts/init_db.py
   ```

## Running Sample Data Insertion

1. **Insert Sample Data**:
   ```bash
   uv run python scripts/insert_sample_data.py
   ```

## Running Data Verification

1. **Verify Data**:
   ```bash
   uv run python scripts/verify_sample_data.py
   ```

## Expected Results

### Sample Commissioner Records
- Record 1: acc_no=1, department="REVENUE", file_no="5", subject="INCUMBERED STATE APPEALS.", year=1897, page=580, condition="FAIR/BOUND", record_type="TEXTUAL RECORD"
- Record 2: acc_no=2, department="REVENUE", file_no="Vol - I", subject="OUTWARD REGISTER", year=1902, page=1, condition="FAIR/BOUND", record_type="TEXTUAL RECORD"

### Sample Court Records
- Record 1: acc_no=1, court="District Court of Karachi", suit_no="260 of 1893", plaintiff="Manghamnal Ramdas", defendant="Haji Ismail Gul Mohammad", claim_or_charge="Rs 750", date_from="1893-04-01", date_to="1894-07-03", language="English, Hindi"
- Record 2: acc_no=2, court="District Court of Karachi", suit_no="248 of 1893", plaintiff="The Bombay Company Limited", defendant="Gagoo Shivji", claim_or_charge="RS. 1799", date_from="1893-06-12", date_to="1894-02-02", language="English, Sindhi and Hindi"

## Troubleshooting

### Common Connection Issues
- **Connection refused**: PostgreSQL server is not running
- **Database does not exist**: Database needs to be created
- **Authentication failed**: Username/password mismatch
- **SSL issues**: Add `?sslmode=require` for NeonDB or `?sslmode=disable` for local

### Verify Connection
```bash
# Test connection with psql
psql postgresql://postgres:password@localhost:5432/sindh_archives
```

## Direct Database Query

To verify data directly in the database:
```sql
SELECT * FROM commissioner_records;
SELECT * FROM court_records;
```

## Summary

The scripts `scripts/insert_sample_data.py` and `scripts/verify_sample_data.py` are designed to work with a real PostgreSQL database. They will:

1. Connect to the database using the `DATABASE_URL` from your `.env` file
2. Insert sample records into both `commissioner_records` and `court_records` tables
3. Verify the insertion by retrieving and displaying all records as pandas DataFrames
4. Test specific filter queries (by year for commissioner records, by plaintiff for court records)

The data flow has been tested and verified in the application layer, and these scripts will perform the actual database operations when a PostgreSQL server is available.