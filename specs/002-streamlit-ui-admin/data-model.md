# Data Model: Streamlit Web Application for Record Management System

## Overview
This document defines the data model for the Streamlit web application, focusing on how existing database entities are used within the UI layer. The application reuses the existing Phase 1 database schema and DAOs, with the UI layer providing presentation and interaction logic.

## Entity Definitions

### Public User
**Description**: A visitor to the application who can view records but cannot add or modify them
- **Access Level**: Read-only access to public record data
- **Authentication**: Not required for viewing records
- **Session Data**: No persistent session data stored

### Admin User
**Description**: A privileged user with 'admin' role who can log in and add new records to the system
- **Access Level**: Read access to all records, write access to add new records
- **Authentication**: Required for admin functionality
- **Session Data**:
  - `user_id` (integer): Unique identifier from users table
  - `email` (string): User's email address
  - `role` (string): User role ('admin')
  - `is_authenticated` (boolean): Authentication status

### Commissioner Record
**Description**: A record with attributes for commissioner records as defined in Phase 1
- **Fields**:
  - `id` (integer): Primary key, auto-increment
  - `acc_no` (integer): Account number, required, positive integer
  - `department` (string): Department name, required
  - `file_no` (string): File number, required
  - `subject` (text): Subject description, required
  - `year` (integer): Year, required, range 1800-2100
  - `page` (integer): Page number, required, positive integer
  - `condition` (string): Record condition, one of: FAIR/BOUND, GOOD/BOUND, POOR/UNBOUND, EXCELLENT/BOUND
  - `record_type` (string): Record type, one of: TEXTUAL RECORD, PHOTOGRAPHIC RECORD, DIGITAL RECORD
  - `created_at` (datetime): Creation timestamp
  - `updated_at` (datetime): Last update timestamp

### Court Record
**Description**: A record with attributes for court records as defined in Phase 1
- **Fields**:
  - `id` (integer): Primary key, auto-increment
  - `acc_no` (integer): Account number, required, positive integer
  - `court` (string): Court name, required
  - `suit_no` (string): Suit number, required
  - `plaintiff` (string): Plaintiff name, required
  - `defendant` (string): Defendant name, required
  - `claim_or_charge` (text): Claim or charge description, required
  - `date_from` (date): Start date, required
  - `date_to` (date): End date, required, must be after date_from
  - `language` (string): Language of record, required
  - `created_at` (datetime): Creation timestamp
  - `updated_at` (datetime): Last update timestamp

### Session State
**Description**: Application state that tracks user authentication status and UI state
- **Fields**:
  - `is_authenticated` (boolean): Whether user is authenticated
  - `user_id` (integer): ID of authenticated user
  - `user_email` (string): Email of authenticated user
  - `user_role` (string): Role of authenticated user ('admin' or 'user')
  - `current_page` (string): Currently displayed page
  - `form_data` (dict): Temporary storage for form inputs during validation

## Relationships

### User to Records
- **Admin User** → **Commissioner Records**: Admin users can create commissioner records
- **Admin User** → **Court Records**: Admin users can create court records
- **All Users** → **All Records**: All users can view all records (read-only)

## Validation Rules

### Commissioner Record Validation
- `acc_no`: Must be a positive integer
- `department`: Required field, non-empty string
- `file_no`: Required field, non-empty string
- `subject`: Required field, non-empty text
- `year`: Required field, integer between 1800 and 2100
- `page`: Required field, positive integer
- `condition`: Required field, must be one of the allowed values
- `record_type`: Required field, must be one of the allowed values

### Court Record Validation
- `acc_no`: Must be a positive integer
- `court`: Required field, non-empty string
- `suit_no`: Required field, non-empty string
- `plaintiff`: Required field, non-empty string
- `defendant`: Required field, non-empty string
- `claim_or_charge`: Required field, non-empty text
- `date_from`: Required field, valid date
- `date_to`: Required field, valid date that is after date_from
- `language`: Required field, non-empty string

### User Authentication Validation
- Email format must be valid
- Password must match stored hash using bcrypt
- Role must be 'admin' for access to admin features

## State Transitions

### Authentication State
- **Unauthenticated** → **Authenticated**: User successfully logs in with valid admin credentials
- **Authenticated** → **Unauthenticated**: User logs out or session expires

### Form State
- **Empty** → **Filled**: User enters data into form fields
- **Filled** → **Validating**: User submits the form
- **Validating** → **Success**: Form data is valid and record is created
- **Validating** → **Error**: Form data is invalid, error messages displayed
- **Success** → **Empty**: Form is cleared after successful submission

## UI-Specific Data Transformations

### Date Formatting
- **Input**: Date objects from database
- **Display**: Formatted as dd/mm/yyyy for court records in the UI
- **Storage**: Stored as date objects in the database

### Empty State Handling
- **Condition**: When no records exist in the database
- **Display**: Friendly message "No records found in the system."
- **Action**: User can continue browsing or admin can add records

### Loading State
- **Condition**: During database operations (fetching, inserting)
- **Display**: Loading spinner component
- **Action**: Prevents user interaction until operation completes