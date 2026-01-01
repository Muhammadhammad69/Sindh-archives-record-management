"""
Court Record Data Access Object (DAO) for managing court record data.

This module provides methods for performing CRUD operations on court record data
with proper validation.
"""
from typing import Optional, List, Dict, Any
from src.dao.base_dao import BaseDAO
from src.database.models.court_record import CourtRecord
from src.utils.logging import get_app_logger
from src.utils.validators import validate_date_string, validate_date_range, validate_positive_integer


class CourtDAO(BaseDAO):
    """
    Data Access Object for managing CourtRecord entities.
    """

    def __init__(self):
        """Initialize the CourtDAO."""
        super().__init__('court_records')
        self.logger = get_app_logger()

    def validate_data(self, data: Dict[str, Any]) -> Dict[str, List[str]]:
        """
        Validate court record data before saving to database.

        Args:
            data: Dictionary containing the data to validate

        Returns:
            Dictionary with field names as keys and lists of error messages as values
        """
        errors = {}

        # Validate required fields
        required_fields = ['acc_no', 'court', 'suit_no', 'plaintiff', 'defendant', 'claim_or_charge', 'date_from', 'date_to', 'language']
        for field in required_fields:
            if field in data and (data[field] is None or (isinstance(data[field], str) and data[field].strip() == "")):
                if field not in errors:
                    errors[field] = []
                errors[field].append(f"{field} is required")

        # Validate acc_no is positive integer
        if 'acc_no' in data and data['acc_no'] is not None:
            is_valid, error_msg = validate_positive_integer(data['acc_no'], 'acc_no')
            if not is_valid:
                if 'acc_no' not in errors:
                    errors['acc_no'] = []
                errors['acc_no'].append(error_msg)

        # Validate dates
        if 'date_from' in data and data['date_from']:
            is_valid, error_msg = validate_date_string(data['date_from'])
            if not is_valid:
                if 'date_from' not in errors:
                    errors['date_from'] = []
                errors['date_from'].append(error_msg)

        if 'date_to' in data and data['date_to']:
            is_valid, error_msg = validate_date_string(data['date_to'])
            if not is_valid:
                if 'date_to' not in errors:
                    errors['date_to'] = []
                errors['date_to'].append(error_msg)

        # Validate date range
        if 'date_from' in data and 'date_to' in data and data['date_from'] and data['date_to']:
            is_valid, error_msg = validate_date_range(data['date_from'], data['date_to'])
            if not is_valid:
                if 'date_range' not in errors:
                    errors['date_range'] = []
                errors['date_range'].append(error_msg)

        return errors

    def create(self, record_data: Dict[str, Any]) -> CourtRecord:
        """
        Create a new court record with validation.

        Args:
            record_data: Dictionary containing court record information

        Returns:
            Created CourtRecord instance
        """
        # Validate input data
        validation_errors = self.validate_data(record_data)
        if validation_errors:
            error_messages = []
            for field, field_errors in validation_errors.items():
                error_messages.extend(field_errors)
            raise ValueError(f"Validation failed: {'; '.join(error_messages)}")

        # Prepare the data for insertion
        data_to_insert = {
            'acc_no': record_data.get('acc_no'),
            'court': record_data.get('court'),
            'suit_no': record_data.get('suit_no'),
            'plaintiff': record_data.get('plaintiff'),
            'defendant': record_data.get('defendant'),
            'claim_or_charge': record_data.get('claim_or_charge'),
            'date_from': record_data.get('date_from'),
            'date_to': record_data.get('date_to'),
            'language': record_data.get('language'),
        }
        data_to_insert.update(self._get_audit_fields())

        # Perform the database insert
        result = super().create(data_to_insert)

        # Create and return the CourtRecord object
        created_record = CourtRecord.from_dict(result)
        self.logger.info(f"Court record created successfully: {created_record.id}", {
            'record_id': created_record.id,
            'acc_no': created_record.acc_no,
            'court': created_record.court,
            'component': 'court_records'
        })

        return created_record

    def get_by_id(self, record_id: int) -> Optional[CourtRecord]:
        """
        Retrieve a court record by its ID.

        Args:
            record_id: ID of the record to retrieve

        Returns:
            CourtRecord instance if found, None otherwise
        """
        record_data = super().get_by_id(record_id)
        if record_data:
            record = CourtRecord.from_dict(record_data)
            self.logger.debug(f"Court record retrieved by ID: {record.id}", {
                'record_id': record.id,
                'component': 'court_records'
            })
            return record

        self.logger.debug(f"No court record found with ID: {record_id}", {
            'record_id': record_id,
            'component': 'court_records'
        })
        return None

    def get_by_acc_no(self, acc_no: int) -> List[CourtRecord]:
        """
        Retrieve all court records by account number.

        Args:
            acc_no: Account number to search for

        Returns:
            List of CourtRecord instances
        """
        records_data = self.find_by_criteria({'acc_no': acc_no})
        records = [CourtRecord.from_dict(data) for data in records_data]

        self.logger.debug(f"Retrieved {len(records)} court records for acc_no: {acc_no}", {
            'acc_no': acc_no,
            'record_count': len(records),
            'component': 'court_records'
        })

        return records

    def update(self, record_id: int, record_data: Dict[str, Any]) -> bool:
        """
        Update a court record's information.

        Args:
            record_id: ID of the record to update
            record_data: Dictionary containing fields to update

        Returns:
            True if the record was updated, False otherwise
        """
        # Validate input data
        validation_errors = self.validate_data(record_data)
        if validation_errors:
            error_messages = []
            for field, field_errors in validation_errors.items():
                error_messages.extend(field_errors)
            raise ValueError(f"Validation failed: {'; '.join(error_messages)}")

        # Update audit fields
        record_data = self._update_audit_fields(record_data)

        # Perform the update
        success = super().update_by_id(record_id, record_data)

        if success:
            self.logger.info(f"Court record updated successfully: {record_id}", {
                'record_id': record_id,
                'updated_fields': list(record_data.keys()),
                'component': 'court_records'
            })

        return success

    def delete(self, record_id: int) -> bool:
        """
        Delete a court record by its ID.

        Args:
            record_id: ID of the record to delete

        Returns:
            True if the record was deleted, False otherwise
        """
        success = super().delete_by_id(record_id)
        if success:
            self.logger.info(f"Court record deleted successfully: {record_id}", {
                'record_id': record_id,
                'component': 'court_records'
            })
        else:
            self.logger.warning(f"Attempted to delete non-existent court record: {record_id}", {
                'record_id': record_id,
                'component': 'court_records'
            })

        return success

    def get_all_by_court(self, court_name: str) -> List[CourtRecord]:
        """
        Get all court records for a specific court.

        Args:
            court_name: Court name to filter by

        Returns:
            List of CourtRecord instances
        """
        records_data = self.find_by_criteria({'court': court_name})
        records = [CourtRecord.from_dict(data) for data in records_data]

        self.logger.debug(f"Retrieved {len(records)} court records for court: {court_name}", {
            'court': court_name,
            'record_count': len(records),
            'component': 'court_records'
        })

        return records

    def get_all_by_date_range(self, date_from: str, date_to: str) -> List[CourtRecord]:
        """
        Get all court records within a specific date range.

        Args:
            date_from: Start date (inclusive)
            date_to: End date (inclusive)

        Returns:
            List of CourtRecord instances
        """
        # Validate the date range
        is_valid, error = validate_date_range(date_from, date_to)
        if not is_valid:
            raise ValueError(f"Invalid date range: {error}")

        # Find records where the date_from falls within the specified range
        query = """
        SELECT * FROM court_records
        WHERE date_from >= %s AND date_to <= %s
        """
        records_data = self._execute_query(query, (date_from, date_to))
        records = [CourtRecord.from_dict(data) for data in records_data]

        self.logger.debug(f"Retrieved {len(records)} court records for date range: {date_from} to {date_to}", {
            'date_from': date_from,
            'date_to': date_to,
            'record_count': len(records),
            'component': 'court_records'
        })

        return records

    def _get_audit_fields(self) -> Dict[str, Any]:
        """
        Get the audit fields for this model.

        Returns:
            Dictionary containing audit field names and their default values
        """
        from datetime import datetime
        now = datetime.utcnow()
        return {
            'created_at': now,
            'updated_at': now
        }

    def _update_audit_fields(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update audit fields in the provided data dictionary.

        Args:
            data: Dictionary containing record data

        Returns:
            Updated dictionary with audit fields
        """
        from datetime import datetime
        data['updated_at'] = datetime.utcnow()
        return data