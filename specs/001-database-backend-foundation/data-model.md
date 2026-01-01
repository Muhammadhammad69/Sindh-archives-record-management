# Data Model: Database and Backend Foundation

## Overview
This document defines the data model for the secure PostgreSQL record management system backend foundation, based on the feature specification requirements.

## Entity Models

### User Entity
- **Table Name**: `users`
- **Description**: Represents system users with authentication credentials and role-based access

**Fields**:
- `id` (INTEGER, PRIMARY KEY, AUTO_INCREMENT) - Unique identifier
- `name` (VARCHAR, NOT NULL) - User's full name
- `email` (VARCHAR, UNIQUE, NOT NULL) - User's email address
- `password` (VARCHAR, NOT NULL) - Hashed password
- `role` (ENUM: 'admin', 'user', NOT NULL) - User's access role
- `created_at` (TIMESTAMP, NOT NULL, DEFAULT CURRENT_TIMESTAMP) - Record creation timestamp
- `updated_at` (TIMESTAMP, NOT NULL, DEFAULT CURRENT_TIMESTAMP) - Record update timestamp

**Validation Rules**:
- Email must be valid email format
- Role must be either 'admin' or 'user'
- Name and email cannot be empty
- Password must be provided (hashed before storage)

**Relationships**:
- No direct relationships with other entities in this model

### Commissioner Record Entity
- **Table Name**: `commissioner_records`
- **Description**: Legal records managed by commissioners with identification fields and metadata

**Fields**:
- `id` (INTEGER, PRIMARY KEY, AUTO_INCREMENT) - Unique identifier
- `acc_no` (INTEGER, NOT NULL) - Account number
- `department` (VARCHAR, NOT NULL) - Department name
- `file_no` (VARCHAR, NOT NULL) - File number
- `subject` (TEXT, NOT NULL) - Subject matter
- `year` (INTEGER, NOT NULL) - Year
- `page` (INTEGER, NOT NULL) - Page number
- `condition` (VARCHAR, NOT NULL) - Condition of the record
- `record_type` (VARCHAR, NOT NULL) - Type of record
- `created_at` (TIMESTAMP, NOT NULL, DEFAULT CURRENT_TIMESTAMP) - Record creation timestamp
- `updated_at` (TIMESTAMP, NOT NULL, DEFAULT CURRENT_TIMESTAMP) - Record update timestamp

**Validation Rules**:
- All fields are required
- acc_no must be a positive integer
- year must be a valid year
- page must be a positive integer

**Relationships**:
- No direct relationships with other entities in this model

### Court Record Entity
- **Table Name**: `court_records`
- **Description**: Legal records from court proceedings with case identifiers and parties

**Fields**:
- `id` (INTEGER, PRIMARY KEY, AUTO_INCREMENT) - Unique identifier
- `acc_no` (INTEGER, NOT NULL) - Account number
- `court` (VARCHAR, NOT NULL) - Court name
- `suit_no` (VARCHAR, NOT NULL) - Suit number
- `plaintiff` (VARCHAR, NOT NULL) - Plaintiff name
- `defendant` (VARCHAR, NOT NULL) - Defendant name
- `claim_or_charge` (TEXT, NOT NULL) - Claim or charge details
- `date_from` (DATE, NOT NULL) - Start date
- `date_to` (DATE, NOT NULL) - End date
- `language` (VARCHAR, NOT NULL) - Language of proceedings
- `created_at` (TIMESTAMP, NOT NULL, DEFAULT CURRENT_TIMESTAMP) - Record creation timestamp
- `updated_at` (TIMESTAMP, NOT NULL, DEFAULT CURRENT_TIMESTAMP) - Record update timestamp

**Validation Rules**:
- All fields are required
- acc_no must be a positive integer
- date_to must be after date_from
- date fields must be valid dates

**Relationships**:
- No direct relationships with other entities in this model

## Database Schema

### SQL DDL (Data Definition Language)

```sql
-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('admin', 'user')),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Commissioner records table
CREATE TABLE commissioner_records (
    id SERIAL PRIMARY KEY,
    acc_no INTEGER NOT NULL,
    department VARCHAR(255) NOT NULL,
    file_no VARCHAR(255) NOT NULL,
    subject TEXT NOT NULL,
    year INTEGER NOT NULL,
    page INTEGER NOT NULL,
    condition VARCHAR(255) NOT NULL,
    record_type VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Court records table
CREATE TABLE court_records (
    id SERIAL PRIMARY KEY,
    acc_no INTEGER NOT NULL,
    court VARCHAR(255) NOT NULL,
    suit_no VARCHAR(255) NOT NULL,
    plaintiff VARCHAR(255) NOT NULL,
    defendant VARCHAR(255) NOT NULL,
    claim_or_charge TEXT NOT NULL,
    date_from DATE NOT NULL,
    date_to DATE NOT NULL,
    language VARCHAR(50) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_commissioner_records_acc_no ON commissioner_records(acc_no);
CREATE INDEX idx_court_records_acc_no ON court_records(acc_no);
```

## State Transitions

### User Entity
- **Creation**: New user registration with validation
- **Update**: Password change, role modification (admin only)
- **Deletion**: Account removal (admin only)

### Record Entities
- **Creation**: New record entry with validation
- **Update**: Record modification with audit trail
- **Deletion**: Record removal (admin only)

## Validation Rules Summary

### Common Validation
- All entities have created_at and updated_at fields with automatic timestamps
- All required fields must be present and valid
- Email format validation for user emails
- Date validation for court record date fields

### Business Rules
- User role must be either 'admin' or 'user'
- Court record date_to must be after date_from
- Account numbers must be positive integers
- All string fields have appropriate length limits