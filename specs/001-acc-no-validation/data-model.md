# Data Model: Acc No Uniqueness Validation

## Entities

### Commissioner Record
- **Entity**: Commissioner Record
- **Fields**:
  - id: Integer (Primary Key, Auto-increment)
  - acc_no: Integer (Unique within commissioner_records table)
  - department: String
  - file_no: String
  - subject: Text
  - year: Integer
  - page: Integer
  - condition: String
  - record_type: String
  - created_at: DateTime (Timestamp)
  - updated_at: DateTime (Timestamp)

### Court Record
- **Entity**: Court Record
- **Fields**:
  - id: Integer (Primary Key, Auto-increment)
  - acc_no: Integer (Unique within court_records table, independent from commissioner acc_no sequence)
  - court: String
  - suit_no: String
  - plaintiff: String
  - defendant: String
  - claim_or_charge: Text
  - date_from: Date
  - date_to: Date
  - language: String
  - created_at: DateTime (Timestamp)
  - updated_at: DateTime (Timestamp)

## Validation Rules

### Acc No Uniqueness
- **Rule**: acc_no must be unique within each table (commissioner_records and court_records)
- **Scope**: Uniqueness is enforced within each table separately
- **Cross-table**: The same acc_no can exist in both commissioner_records and court_records tables
- **Validation Point**: Before insertion of any record (single or bulk)

### Data Constraints
- **acc_no**: Must be a positive integer
- **Required Fields**: All fields marked as non-nullable in the database schema
- **Field Lengths**: As defined in the existing database schema

## Relationships
- **Independent Tables**: commissioner_records and court_records have no direct relationship
- **Shared Identifier**: acc_no serves as a unique identifier within each table but is independent between tables

## State Transitions
- **New Record**: Valid acc_no → Record inserted successfully
- **Duplicate acc_no**: Invalid acc_no (already exists in same table) → Record rejected with error message
- **Bulk Upload**: Records categorized as valid/invalid before insertion