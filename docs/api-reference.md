# API Reference for Sindh Archives Backend

This document outlines the API endpoints available in the Sindh Archives Backend system.

## Authentication

The API uses JWT (JSON Web Token) based authentication. To access protected endpoints, include the JWT token in the Authorization header:

```
Authorization: Bearer <your-jwt-token>
```

## User Management Endpoints

### Create User
- **Endpoint**: `POST /api/users`
- **Description**: Creates a new user account
- **Authentication**: Admin role required
- **Request Body**:
  ```json
  {
    "name": "string (required)",
    "email": "string (required, unique)",
    "password": "string (required, will be hashed)",
    "role": "enum ['admin', 'user'] (required)"
  }
  ```
- **Response**:
  - 201 Created: User created successfully
  - 400 Bad Request: Validation error
  - 409 Conflict: Email already exists

### Get User
- **Endpoint**: `GET /api/users/{id}`
- **Description**: Retrieves user information
- **Authentication**: Admin role required or self-access
- **Response**:
  - 200 OK: User retrieved successfully
  - 404 Not Found: User not found

### Update User
- **Endpoint**: `PUT /api/users/{id}`
- **Description**: Updates user information
- **Authentication**: Admin role required or self-update
- **Request Body**:
  ```json
  {
    "name": "string (optional)",
    "email": "string (optional, unique)",
    "role": "enum ['admin', 'user'] (optional)"
  }
  ```
- **Response**:
  - 200 OK: User updated successfully
  - 400 Bad Request: Validation error
  - 404 Not Found: User not found

### Delete User
- **Endpoint**: `DELETE /api/users/{id}`
- **Description**: Deletes a user account
- **Authentication**: Admin role required
- **Response**:
  - 204 No Content: User deleted successfully
  - 404 Not Found: User not found

### User Login
- **Endpoint**: `POST /api/auth/login`
- **Description**: Authenticates user credentials
- **Request Body**:
  ```json
  {
    "email": "string (required)",
    "password": "string (required)"
  }
  ```
- **Response**:
  - 200 OK: Authentication successful with token
  - 401 Unauthorized: Invalid credentials

## Record Management Endpoints

### Commissioner Records

#### Create Commissioner Record
- **Endpoint**: `POST /api/commissioner-records`
- **Description**: Creates a new commissioner record
- **Authentication**: Admin or authorized user role
- **Request Body**:
  ```json
  {
    "acc_no": "integer (required)",
    "department": "string (required)",
    "file_no": "string (required)",
    "subject": "string (required)",
    "year": "integer (required)",
    "page": "integer (required)",
    "condition": "string (required)",
    "record_type": "string (required)"
  }
  ```
- **Response**:
  - 201 Created: Record created successfully
  - 400 Bad Request: Validation error

#### Get Commissioner Record
- **Endpoint**: `GET /api/commissioner-records/{id}`
- **Description**: Retrieves a commissioner record
- **Authentication**: Admin or authorized user role
- **Response**:
  - 200 OK: Record retrieved successfully
  - 404 Not Found: Record not found

#### Search Commissioner Records
- **Endpoint**: `GET /api/commissioner-records`
- **Description**: Searches commissioner records with filters
- **Authentication**: Admin or authorized user role
- **Query Parameters**:
  - `acc_no`: Filter by account number
  - `department`: Filter by department
  - `year`: Filter by year
- **Response**:
  - 200 OK: Array of records retrieved

### Court Records

#### Create Court Record
- **Endpoint**: `POST /api/court-records`
- **Description**: Creates a new court record
- **Authentication**: Admin or authorized user role
- **Request Body**:
  ```json
  {
    "acc_no": "integer (required)",
    "court": "string (required)",
    "suit_no": "string (required)",
    "plaintiff": "string (required)",
    "defendant": "string (required)",
    "claim_or_charge": "string (required)",
    "date_from": "date (required)",
    "date_to": "date (required)",
    "language": "string (required)"
  }
  ```
- **Response**:
  - 201 Created: Record created successfully
  - 400 Bad Request: Validation error

#### Get Court Record
- **Endpoint**: `GET /api/court-records/{id}`
- **Description**: Retrieves a court record
- **Authentication**: Admin or authorized user role
- **Response**:
  - 200 OK: Record retrieved successfully
  - 404 Not Found: Record not found

#### Search Court Records
- **Endpoint**: `GET /api/court-records`
- **Description**: Searches court records with filters
- **Authentication**: Admin or authorized user role
- **Query Parameters**:
  - `acc_no`: Filter by account number
  - `court`: Filter by court name
  - `date_from`: Filter by start date
  - `date_to`: Filter by end date
- **Response**:
  - 200 OK: Array of records retrieved

## Error Responses

All error responses follow this format:
```json
{
  "error": "error_code",
  "message": "human-readable error message",
  "details": "optional detailed information"
}
```

## Common Error Codes

- `400 Bad Request`: Validation error or malformed request
- `401 Unauthorized`: Missing or invalid authentication token
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Requested resource does not exist
- `409 Conflict`: Resource already exists (e.g., duplicate email)
- `500 Internal Server Error`: Unexpected server error