"""
Court Record model for the application.

This module defines the CourtRecord entity with all required fields and relationships.
"""
from typing import Optional, Dict, Any
from datetime import datetime
from src.database.models.base import BaseModel, get_base_field_definitions
from src.utils.validators import validate_date_string, validate_date_range


class CourtRecord(BaseModel):
    """
    CourtRecord model representing legal records from court proceedings.
    """

    def __init__(self, acc_no: int = None, court: str = None, suit_no: str = None,
                 plaintiff: str = None, defendant: str = None, claim_or_charge: str = None,
                 date_from: str = None, date_to: str = None, language: str = None,
                 id: Optional[int] = None):
        """
        Initialize a CourtRecord instance.

        Args:
            acc_no: Account number
            court: Court name
            suit_no: Suit number
            plaintiff: Plaintiff name
            defendant: Defendant name
            claim_or_charge: Claim or charge details
            date_from: Start date (format: YYYY-MM-DD)
            date_to: End date (format: YYYY-MM-DD)
            language: Language of proceedings
            id: Optional record ID for existing records
        """
        super().__init__()
        self.id = id
        self.acc_no = acc_no
        self.court = court
        self.suit_no = suit_no
        self.plaintiff = plaintiff
        self.defendant = defendant
        self.claim_or_charge = claim_or_charge
        self.date_from = date_from
        self.date_to = date_to
        self.language = language

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the court record instance to a dictionary.

        Returns:
            Dictionary representation of the court record
        """
        return {
            'id': self.id,
            'acc_no': self.acc_no,
            'court': self.court,
            'suit_no': self.suit_no,
            'plaintiff': self.plaintiff,
            'defendant': self.defendant,
            'claim_or_charge': self.claim_or_charge,
            'date_from': self.date_from,
            'date_to': self.date_to,
            'language': self.language,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    def validate(self) -> tuple[bool, list[str]]:
        """
        Validate the court record data.

        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []

        if self.acc_no is None:
            errors.append("Account number (acc_no) is required")
        elif not isinstance(self.acc_no, int) or self.acc_no <= 0:
            errors.append(f"Account number must be a positive integer, got: {self.acc_no}")

        if not self.court or not self.court.strip():
            errors.append("Court name is required")

        if not self.suit_no or not self.suit_no.strip():
            errors.append("Suit number is required")

        if not self.plaintiff or not self.plaintiff.strip():
            errors.append("Plaintiff name is required")

        if not self.defendant or not self.defendant.strip():
            errors.append("Defendant name is required")

        if not self.claim_or_charge or not self.claim_or_charge.strip():
            errors.append("Claim or charge is required")

        if not self.date_from:
            errors.append("Start date (date_from) is required")
        else:
            is_valid, error = validate_date_string(self.date_from)
            if not is_valid:
                errors.append(f"Invalid start date format: {error}")

        if not self.date_to:
            errors.append("End date (date_to) is required")
        else:
            is_valid, error = validate_date_string(self.date_to)
            if not is_valid:
                errors.append(f"Invalid end date format: {error}")

        if self.date_from and self.date_to:
            is_valid, error = validate_date_range(self.date_from, self.date_to)
            if not is_valid:
                errors.append(f"Date range error: {error}")

        if not self.language or not self.language.strip():
            errors.append("Language is required")

        return len(errors) == 0, errors

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CourtRecord':
        """
        Create a CourtRecord instance from a dictionary.

        Args:
            data: Dictionary containing court record data

        Returns:
            CourtRecord instance populated with data from the dictionary
        """
        record = cls(
            id=data.get('id'),
            acc_no=data.get('acc_no'),
            court=data.get('court'),
            suit_no=data.get('suit_no'),
            plaintiff=data.get('plaintiff'),
            defendant=data.get('defendant'),
            claim_or_charge=data.get('claim_or_charge'),
            date_from=data.get('date_from'),
            date_to=data.get('date_to'),
            language=data.get('language')
        )
        record.created_at = data.get('created_at')
        record.updated_at = data.get('updated_at')
        return record

    @staticmethod
    def get_table_schema() -> str:
        """
        Get the SQL schema definition for the court_records table.

        Returns:
            SQL string to create the court_records table
        """
        base_fields = get_base_field_definitions()
        return f"""
        CREATE TABLE IF NOT EXISTS court_records (
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
            {base_fields}
        );

        CREATE INDEX IF NOT EXISTS idx_court_records_acc_no ON court_records(acc_no);
        """

    @staticmethod
    def get_insert_query() -> str:
        """
        Get the SQL INSERT query for court records.

        Returns:
            SQL INSERT query string
        """
        return """
        INSERT INTO court_records (acc_no, court, suit_no, plaintiff, defendant, claim_or_charge, date_from, date_to, language, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id, acc_no, court, suit_no, plaintiff, defendant, claim_or_charge, date_from, date_to, language, created_at, updated_at
        """

    @staticmethod
    def get_select_by_id_query() -> str:
        """
        Get the SQL SELECT query to find a court record by ID.

        Returns:
            SQL SELECT query string
        """
        return """
        SELECT id, acc_no, court, suit_no, plaintiff, defendant, claim_or_charge, date_from, date_to, language, created_at, updated_at
        FROM court_records
        WHERE id = %s
        """

    @staticmethod
    def get_select_by_acc_no_query() -> str:
        """
        Get the SQL SELECT query to find court records by account number.

        Returns:
            SQL SELECT query string
        """
        return """
        SELECT id, acc_no, court, suit_no, plaintiff, defendant, claim_or_charge, date_from, date_to, language, created_at, updated_at
        FROM court_records
        WHERE acc_no = %s
        """

    @staticmethod
    def get_update_query() -> str:
        """
        Get the SQL UPDATE query for court records.

        Returns:
            SQL UPDATE query string
        """
        return """
        UPDATE court_records
        SET acc_no = %s, court = %s, suit_no = %s, plaintiff = %s, defendant = %s, claim_or_charge = %s, date_from = %s, date_to = %s, language = %s, updated_at = CURRENT_TIMESTAMP
        WHERE id = %s
        """

    @staticmethod
    def get_select_all_query(limit: int = None, offset: int = 0) -> str:
        """
        Get the SQL SELECT query to retrieve all court records.

        Args:
            limit: Maximum number of records to return
            offset: Number of records to skip

        Returns:
            SQL SELECT query string
        """
        query = "SELECT id, acc_no, court, suit_no, plaintiff, defendant, claim_or_charge, date_from, date_to, language, created_at, updated_at FROM court_records"
        params = []

        if limit:
            query += f" LIMIT %s OFFSET %s"
            params = [limit, offset]
        elif offset > 0:
            query += f" OFFSET %s"
            params = [offset]

        return query, params

    @staticmethod
    def get_acc_no_exists_query() -> str:
        """
        Get the SQL query to check if an acc_no exists in court records.

        Returns:
            SQL EXISTS query string
        """
        return """
        SELECT EXISTS(
            SELECT 1 FROM court_records WHERE acc_no = %s
        ) AS acc_no_exists
        """

    @staticmethod
    def get_all_acc_numbers_query() -> str:
        """
        Get the SQL query to retrieve all acc_no values from court records.

        Returns:
            SQL SELECT query string
        """
        return """
        SELECT DISTINCT acc_no FROM court_records
        """