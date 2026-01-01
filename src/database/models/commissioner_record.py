"""
Commissioner Record model for the application.

This module defines the CommissionerRecord entity with all required fields and relationships.
"""
from typing import Optional, Dict, Any
from datetime import datetime
from src.database.models.base import BaseModel, get_base_field_definitions
from src.utils.validators import validate_positive_integer


class CommissionerRecord(BaseModel):
    """
    CommissionerRecord model representing legal records managed by commissioners.
    """

    def __init__(self, acc_no: int = None, department: str = None, file_no: str = None,
                 subject: str = None, year: int = None, page: int = None,
                 condition: str = None, record_type: str = None, id: Optional[int] = None):
        """
        Initialize a CommissionerRecord instance.

        Args:
            acc_no: Account number
            department: Department name
            file_no: File number
            subject: Subject matter
            year: Year
            page: Page number
            condition: Condition of the record
            record_type: Type of record
            id: Optional record ID for existing records
        """
        super().__init__()
        self.id = id
        self.acc_no = acc_no
        self.department = department
        self.file_no = file_no
        self.subject = subject
        self.year = year
        self.page = page
        self.condition = condition
        self.record_type = record_type

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the commissioner record instance to a dictionary.

        Returns:
            Dictionary representation of the commissioner record
        """
        return {
            'id': self.id,
            'acc_no': self.acc_no,
            'department': self.department,
            'file_no': self.file_no,
            'subject': self.subject,
            'year': self.year,
            'page': self.page,
            'condition': self.condition,
            'record_type': self.record_type,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    def validate(self) -> tuple[bool, list[str]]:
        """
        Validate the commissioner record data.

        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []

        if self.acc_no is None:
            errors.append("Account number (acc_no) is required")
        elif not isinstance(self.acc_no, int) or self.acc_no <= 0:
            errors.append(f"Account number must be a positive integer, got: {self.acc_no}")

        if not self.department or not self.department.strip():
            errors.append("Department is required")

        if not self.file_no or not self.file_no.strip():
            errors.append("File number is required")

        if not self.subject or not self.subject.strip():
            errors.append("Subject is required")

        if self.year is None:
            errors.append("Year is required")
        elif not isinstance(self.year, int) or self.year <= 0:
            errors.append(f"Year must be a positive integer, got: {self.year}")

        if self.page is None:
            errors.append("Page number is required")
        elif not isinstance(self.page, int) or self.page <= 0:
            errors.append(f"Page must be a positive integer, got: {self.page}")

        if not self.condition or not self.condition.strip():
            errors.append("Condition is required")

        if not self.record_type or not self.record_type.strip():
            errors.append("Record type is required")

        return len(errors) == 0, errors

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CommissionerRecord':
        """
        Create a CommissionerRecord instance from a dictionary.

        Args:
            data: Dictionary containing commissioner record data

        Returns:
            CommissionerRecord instance populated with data from the dictionary
        """
        record = cls(
            id=data.get('id'),
            acc_no=data.get('acc_no'),
            department=data.get('department'),
            file_no=data.get('file_no'),
            subject=data.get('subject'),
            year=data.get('year'),
            page=data.get('page'),
            condition=data.get('condition'),
            record_type=data.get('record_type')
        )
        record.created_at = data.get('created_at')
        record.updated_at = data.get('updated_at')
        return record

    @staticmethod
    def get_table_schema() -> str:
        """
        Get the SQL schema definition for the commissioner_records table.

        Returns:
            SQL string to create the commissioner_records table
        """
        base_fields = get_base_field_definitions()
        return f"""
        CREATE TABLE IF NOT EXISTS commissioner_records (
            id SERIAL PRIMARY KEY,
            acc_no INTEGER NOT NULL,
            department VARCHAR(255) NOT NULL,
            file_no VARCHAR(255) NOT NULL,
            subject TEXT NOT NULL,
            year INTEGER NOT NULL,
            page INTEGER NOT NULL,
            condition VARCHAR(255) NOT NULL,
            record_type VARCHAR(255) NOT NULL,
            {base_fields}
        );

        CREATE INDEX IF NOT EXISTS idx_commissioner_records_acc_no ON commissioner_records(acc_no);
        """

    @staticmethod
    def get_insert_query() -> str:
        """
        Get the SQL INSERT query for commissioner records.

        Returns:
            SQL INSERT query string
        """
        return """
        INSERT INTO commissioner_records (acc_no, department, file_no, subject, year, page, condition, record_type, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id, acc_no, department, file_no, subject, year, page, condition, record_type, created_at, updated_at
        """

    @staticmethod
    def get_select_by_id_query() -> str:
        """
        Get the SQL SELECT query to find a commissioner record by ID.

        Returns:
            SQL SELECT query string
        """
        return """
        SELECT id, acc_no, department, file_no, subject, year, page, condition, record_type, created_at, updated_at
        FROM commissioner_records
        WHERE id = %s
        """

    @staticmethod
    def get_select_by_acc_no_query() -> str:
        """
        Get the SQL SELECT query to find commissioner records by account number.

        Returns:
            SQL SELECT query string
        """
        return """
        SELECT id, acc_no, department, file_no, subject, year, page, condition, record_type, created_at, updated_at
        FROM commissioner_records
        WHERE acc_no = %s
        """

    @staticmethod
    def get_update_query() -> str:
        """
        Get the SQL UPDATE query for commissioner records.

        Returns:
            SQL UPDATE query string
        """
        return """
        UPDATE commissioner_records
        SET acc_no = %s, department = %s, file_no = %s, subject = %s, year = %s, page = %s, condition = %s, record_type = %s, updated_at = CURRENT_TIMESTAMP
        WHERE id = %s
        """

    @staticmethod
    def get_select_all_query(limit: int = None, offset: int = 0) -> str:
        """
        Get the SQL SELECT query to retrieve all commissioner records.

        Args:
            limit: Maximum number of records to return
            offset: Number of records to skip

        Returns:
            SQL SELECT query string
        """
        query = "SELECT id, acc_no, department, file_no, subject, year, page, condition, record_type, created_at, updated_at FROM commissioner_records"
        params = []

        if limit:
            query += f" LIMIT %s OFFSET %s"
            params = [limit, offset]
        elif offset > 0:
            query += f" OFFSET %s"
            params = [offset]

        return query, params