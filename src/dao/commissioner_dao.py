"""
Commissioner Record Data Access Object (DAO) for managing commissioner record data.

This module provides methods for performing CRUD operations on commissioner record data
with proper validation.
"""
from typing import Optional, List, Dict, Any
from src.dao.base_dao import BaseDAO
from src.database.models.commissioner_record import CommissionerRecord
from src.utils.logging import get_app_logger
from src.utils.validators import validate_positive_integer


class CommissionerDAO(BaseDAO):
    """
    Data Access Object for managing CommissionerRecord entities.
    """

    def __init__(self):
        """Initialize the CommissionerDAO."""
        super().__init__('commissioner_records')
        self.logger = get_app_logger()

    def validate_data(self, data: Dict[str, Any]) -> Dict[str, List[str]]:
        """
        Validate commissioner record data before saving to database.

        Args:
            data: Dictionary containing the data to validate

        Returns:
            Dictionary with field names as keys and lists of error messages as values
        """
        errors = {}

        # Validate required fields
        required_fields = ['acc_no', 'department', 'file_no', 'subject', 'year', 'page', 'condition', 'record_type']
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

        # Validate year is positive integer
        if 'year' in data and data['year'] is not None:
            is_valid, error_msg = validate_positive_integer(data['year'], 'year')
            if not is_valid:
                if 'year' not in errors:
                    errors['year'] = []
                errors['year'].append(error_msg)

        # Validate page is positive integer
        if 'page' in data and data['page'] is not None:
            is_valid, error_msg = validate_positive_integer(data['page'], 'page')
            if not is_valid:
                if 'page' not in errors:
                    errors['page'] = []
                errors['page'].append(error_msg)

        return errors

    def create(self, record_data: Dict[str, Any]) -> CommissionerRecord:
        """
        Create a new commissioner record with validation.

        Args:
            record_data: Dictionary containing commissioner record information

        Returns:
            Created CommissionerRecord instance
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
            'department': record_data.get('department'),
            'file_no': record_data.get('file_no'),
            'subject': record_data.get('subject'),
            'year': record_data.get('year'),
            'page': record_data.get('page'),
            'condition': record_data.get('condition'),
            'record_type': record_data.get('record_type'),
        }
        data_to_insert.update(self._get_audit_fields())

        # Perform the database insert
        result = super().create(data_to_insert)

        # Create and return the CommissionerRecord object
        created_record = CommissionerRecord.from_dict(result)
        self.logger.info(f"Commissioner record created successfully: {created_record.id}", {
            'record_id': created_record.id,
            'acc_no': created_record.acc_no,
            'department': created_record.department,
            'component': 'commissioner_records'
        })

        return created_record

    def get_by_id(self, record_id: int) -> Optional[CommissionerRecord]:
        """
        Retrieve a commissioner record by its ID.

        Args:
            record_id: ID of the record to retrieve

        Returns:
            CommissionerRecord instance if found, None otherwise
        """
        record_data = super().get_by_id(record_id)
        if record_data:
            record = CommissionerRecord.from_dict(record_data)
            self.logger.debug(f"Commissioner record retrieved by ID: {record.id}", {
                'record_id': record.id,
                'component': 'commissioner_records'
            })
            return record

        self.logger.debug(f"No commissioner record found with ID: {record_id}", {
            'record_id': record_id,
            'component': 'commissioner_records'
        })
        return None

    def get_by_acc_no(self, acc_no: int) -> List[CommissionerRecord]:
        """
        Retrieve all commissioner records by account number.

        Args:
            acc_no: Account number to search for

        Returns:
            List of CommissionerRecord instances
        """
        records_data = self.find_by_criteria({'acc_no': acc_no})
        records = [CommissionerRecord.from_dict(data) for data in records_data]

        self.logger.debug(f"Retrieved {len(records)} commissioner records for acc_no: {acc_no}", {
            'acc_no': acc_no,
            'record_count': len(records),
            'component': 'commissioner_records'
        })

        return records

    def update(self, record_id: int, record_data: Dict[str, Any]) -> bool:
        """
        Update a commissioner record's information.

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
            self.logger.info(f"Commissioner record updated successfully: {record_id}", {
                'record_id': record_id,
                'updated_fields': list(record_data.keys()),
                'component': 'commissioner_records'
            })

        return success

    def delete(self, record_id: int) -> bool:
        """
        Delete a commissioner record by its ID.

        Args:
            record_id: ID of the record to delete

        Returns:
            True if the record was deleted, False otherwise
        """
        success = super().delete_by_id(record_id)
        if success:
            self.logger.info(f"Commissioner record deleted successfully: {record_id}", {
                'record_id': record_id,
                'component': 'commissioner_records'
            })
        else:
            self.logger.warning(f"Attempted to delete non-existent commissioner record: {record_id}", {
                'record_id': record_id,
                'component': 'commissioner_records'
            })

        return success

    def get_all_by_department(self, department: str) -> List[CommissionerRecord]:
        """
        Get all commissioner records for a specific department.

        Args:
            department: Department name to filter by

        Returns:
            List of CommissionerRecord instances
        """
        records_data = self.find_by_criteria({'department': department})
        records = [CommissionerRecord.from_dict(data) for data in records_data]

        self.logger.debug(f"Retrieved {len(records)} commissioner records for department: {department}", {
            'department': department,
            'record_count': len(records),
            'component': 'commissioner_records'
        })

        return records

    def get_all_by_year(self, year: int) -> List[CommissionerRecord]:
        """
        Get all commissioner records for a specific year.

        Args:
            year: Year to filter by

        Returns:
            List of CommissionerRecord instances
        """
        records_data = self.find_by_criteria({'year': year})
        records = [CommissionerRecord.from_dict(data) for data in records_data]

        self.logger.debug(f"Retrieved {len(records)} commissioner records for year: {year}", {
            'year': year,
            'record_count': len(records),
            'component': 'commissioner_records'
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