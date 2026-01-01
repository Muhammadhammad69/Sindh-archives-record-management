"""
Data validation utilities for the application.

This module provides common validation functions for various data types
including emails, dates, and other common formats.
"""
import re
from datetime import datetime
from typing import Union, Optional, List, Dict, Any
from src.utils.logging import get_app_logger


class DataValidator:
    """
    Collection of data validation utilities.

    Provides methods for validating various types of data inputs
    with clear error messages for invalid data.
    """

    def __init__(self):
        """Initialize the validator."""
        self.logger = get_app_logger()

    def validate_email(self, email: str) -> tuple[bool, Optional[str]]:
        """
        Validate an email address format.

        Args:
            email: Email address to validate

        Returns:
            Tuple of (is_valid, error_message_if_invalid)
        """
        if not email:
            return False, "Email is required"

        # Basic email regex pattern
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            return False, f"Invalid email format: {email}"

        # Check length
        if len(email) > 254:  # RFC 5321 limit
            return False, "Email address is too long (max 254 characters)"

        return True, None

    def validate_date_string(self, date_str: str, format_str: str = "%Y-%m-%d") -> tuple[bool, Optional[str]]:
        """
        Validate a date string against a specific format.

        Args:
            date_str: Date string to validate
            format_str: Expected date format (default is YYYY-MM-DD)

        Returns:
            Tuple of (is_valid, error_message_if_invalid)
        """
        if not date_str:
            return False, "Date is required"

        try:
            datetime.strptime(date_str, format_str)
            return True, None
        except ValueError:
            return False, f"Invalid date format. Expected format: {format_str}, got: {date_str}"

    def validate_date_range(self, start_date: str, end_date: str,
                           start_format: str = "%Y-%m-%d", end_format: str = "%Y-%m-%d") -> tuple[bool, Optional[str]]:
        """
        Validate that end date is after start date.

        Args:
            start_date: Start date string
            end_date: End date string
            start_format: Format of start date
            end_format: Format of end date

        Returns:
            Tuple of (is_valid, error_message_if_invalid)
        """
        start_valid, start_error = self.validate_date_string(start_date, start_format)
        if not start_valid:
            return False, f"Start date error: {start_error}"

        end_valid, end_error = self.validate_date_string(end_date, end_format)
        if not end_valid:
            return False, f"End date error: {end_error}"

        start_dt = datetime.strptime(start_date, start_format)
        end_dt = datetime.strptime(end_date, end_format)

        if end_dt < start_dt:
            return False, f"End date ({end_date}) must be after start date ({start_date})"

        return True, None

    def validate_positive_integer(self, value: Union[str, int, float],
                                 field_name: str = "value") -> tuple[bool, Optional[str]]:
        """
        Validate that a value is a positive integer.

        Args:
            value: Value to validate
            field_name: Name of the field for error messages

        Returns:
            Tuple of (is_valid, error_message_if_invalid)
        """
        if value is None:
            return False, f"{field_name} is required"

        try:
            num_value = int(value)
            if num_value <= 0:
                return False, f"{field_name} must be a positive integer, got: {value}"
            return True, None
        except (ValueError, TypeError):
            return False, f"{field_name} must be a valid integer, got: {value}"

    def validate_string_length(self, value: str, min_length: int = 0, max_length: int = None,
                              field_name: str = "value") -> tuple[bool, Optional[str]]:
        """
        Validate the length of a string.

        Args:
            value: String to validate
            min_length: Minimum allowed length
            max_length: Maximum allowed length (None for no limit)
            field_name: Name of the field for error messages

        Returns:
            Tuple of (is_valid, error_message_if_invalid)
        """
        if value is None:
            return False, f"{field_name} is required"

        if not isinstance(value, str):
            return False, f"{field_name} must be a string, got: {type(value).__name__}"

        if len(value) < min_length:
            return False, f"{field_name} must be at least {min_length} characters long, got: {len(value)}"

        if max_length is not None and len(value) > max_length:
            return False, f"{field_name} must be no more than {max_length} characters long, got: {len(value)}"

        return True, None

    def validate_required_fields(self, data: Dict[str, Any],
                                required_fields: List[str]) -> tuple[bool, List[str]]:
        """
        Validate that all required fields are present in the data.

        Args:
            data: Dictionary containing the data to validate
            required_fields: List of required field names

        Returns:
            Tuple of (is_valid, list_of_missing_fields)
        """
        missing_fields = []
        for field in required_fields:
            if field not in data or data[field] is None or (isinstance(data[field], str) and data[field].strip() == ""):
                missing_fields.append(field)

        return len(missing_fields) == 0, missing_fields

    def validate_enum_value(self, value: str, allowed_values: List[str],
                           field_name: str = "value") -> tuple[bool, Optional[str]]:
        """
        Validate that a value is one of the allowed enum values.

        Args:
            value: Value to validate
            allowed_values: List of allowed values
            field_name: Name of the field for error messages

        Returns:
            Tuple of (is_valid, error_message_if_invalid)
        """
        if value not in allowed_values:
            return False, f"{field_name} must be one of {allowed_values}, got: {value}"
        return True, None

    def validate_phone_number(self, phone: str) -> tuple[bool, Optional[str]]:
        """
        Validate a phone number format.

        Args:
            phone: Phone number to validate

        Returns:
            Tuple of (is_valid, error_message_if_invalid)
        """
        if not phone:
            return False, "Phone number is required"

        # Allow various phone number formats
        phone_pattern = r'^[\+]?[1-9][\d]{0,15}$|^[\+]?[1-9][\d\s\-\(\)]{4,19}$'
        if not re.match(phone_pattern, phone.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')):
            return False, f"Invalid phone number format: {phone}"

        return True, None

    def validate_url(self, url: str) -> tuple[bool, Optional[str]]:
        """
        Validate a URL format.

        Args:
            url: URL to validate

        Returns:
            Tuple of (is_valid, error_message_if_invalid)
        """
        if not url:
            return False, "URL is required"

        # Basic URL pattern
        url_pattern = r'^https?://(?:[-\w.])+(?:\:[0-9]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:\#(?:[\w.])*)?)?$'
        if not re.match(url_pattern, url):
            return False, f"Invalid URL format: {url}"

        return True, None

    def validate_json(self, json_str: str) -> tuple[bool, Optional[str]]:
        """
        Validate that a string is valid JSON.

        Args:
            json_str: JSON string to validate

        Returns:
            Tuple of (is_valid, error_message_if_invalid)
        """
        if not json_str:
            return False, "JSON string is required"

        try:
            import json as json_lib
            json_lib.loads(json_str)
            return True, None
        except ValueError as e:
            return False, f"Invalid JSON format: {str(e)}"

    def validate_field_types(self, data: Dict[str, Any],
                           field_types: Dict[str, type]) -> tuple[bool, List[str]]:
        """
        Validate that fields have the correct types.

        Args:
            data: Dictionary containing the data to validate
            field_types: Dictionary mapping field names to expected types

        Returns:
            Tuple of (is_valid, list_of_invalid_fields)
        """
        invalid_fields = []
        for field, expected_type in field_types.items():
            if field in data:
                actual_value = data[field]
                if actual_value is not None and not isinstance(actual_value, expected_type):
                    invalid_fields.append(f"{field} (expected {expected_type.__name__}, got {type(actual_value).__name__})")

        return len(invalid_fields) == 0, invalid_fields


# Global validator instance
_validator: Optional[DataValidator] = None


def get_validator() -> DataValidator:
    """
    Get the global data validator instance.

    Returns:
        DataValidator instance
    """
    global _validator
    if _validator is None:
        _validator = DataValidator()
    return _validator


# Convenience functions for common validations
def validate_email(email: str) -> tuple[bool, Optional[str]]:
    """
    Validate an email address format.

    Args:
        email: Email address to validate

    Returns:
        Tuple of (is_valid, error_message_if_invalid)
    """
    validator = get_validator()
    return validator.validate_email(email)


def validate_date_string(date_str: str, format_str: str = "%Y-%m-%d") -> tuple[bool, Optional[str]]:
    """
    Validate a date string against a specific format.

    Args:
        date_str: Date string to validate
        format_str: Expected date format (default is YYYY-MM-DD)

    Returns:
        Tuple of (is_valid, error_message_if_invalid)
    """
    validator = get_validator()
    return validator.validate_date_string(date_str, format_str)


def validate_date_range(start_date: str, end_date: str,
                       start_format: str = "%Y-%m-%d", end_format: str = "%Y-%m-%d") -> tuple[bool, Optional[str]]:
    """
    Validate that end date is after start date.

    Args:
        start_date: Start date string
        end_date: End date string
        start_format: Format of start date
        end_format: Format of end date

    Returns:
        Tuple of (is_valid, error_message_if_invalid)
    """
    validator = get_validator()
    return validator.validate_date_range(start_date, end_date, start_format, end_format)


def validate_positive_integer(value: Union[str, int, float],
                            field_name: str = "value") -> tuple[bool, Optional[str]]:
    """
    Validate that a value is a positive integer.

    Args:
        value: Value to validate
        field_name: Name of the field for error messages

    Returns:
        Tuple of (is_valid, error_message_if_invalid)
    """
    validator = get_validator()
    return validator.validate_positive_integer(value, field_name)


def validate_string_length(value: str, min_length: int = 0, max_length: int = None,
                          field_name: str = "value") -> tuple[bool, Optional[str]]:
    """
    Validate the length of a string.

    Args:
        value: String to validate
        min_length: Minimum allowed length
        max_length: Maximum allowed length (None for no limit)
        field_name: Name of the field for error messages

    Returns:
        Tuple of (is_valid, error_message_if_invalid)
    """
    validator = get_validator()
    return validator.validate_string_length(value, min_length, max_length, field_name)


def validate_required_fields(data: Dict[str, Any],
                           required_fields: List[str]) -> tuple[bool, List[str]]:
    """
    Validate that all required fields are present in the data.

    Args:
        data: Dictionary containing the data to validate
        required_fields: List of required field names

    Returns:
        Tuple of (is_valid, list_of_missing_fields)
    """
    validator = get_validator()
    return validator.validate_required_fields(data, required_fields)


def validate_enum_value(value: str, allowed_values: List[str],
                       field_name: str = "value") -> tuple[bool, Optional[str]]:
    """
    Validate that a value is one of the allowed enum values.

    Args:
        value: Value to validate
        allowed_values: List of allowed values
        field_name: Name of the field for error messages

    Returns:
        Tuple of (is_valid, error_message_if_invalid)
    """
    validator = get_validator()
    return validator.validate_enum_value(value, allowed_values, field_name)


def validate_phone_number(phone: str) -> tuple[bool, Optional[str]]:
    """
    Validate a phone number format.

    Args:
        phone: Phone number to validate

    Returns:
        Tuple of (is_valid, error_message_if_invalid)
    """
    validator = get_validator()
    return validator.validate_phone_number(phone)


def validate_url(url: str) -> tuple[bool, Optional[str]]:
    """
    Validate a URL format.

    Args:
        url: URL to validate

    Returns:
        Tuple of (is_valid, error_message_if_invalid)
    """
    validator = get_validator()
    return validator.validate_url(url)


def validate_json(json_str: str) -> tuple[bool, Optional[str]]:
    """
    Validate that a string is valid JSON.

    Args:
        json_str: JSON string to validate

    Returns:
        Tuple of (is_valid, error_message_if_invalid)
    """
    validator = get_validator()
    return validator.validate_json(json_str)


def validate_field_types(data: Dict[str, Any],
                        field_types: Dict[str, type]) -> tuple[bool, List[str]]:
    """
    Validate that fields have the correct types.

    Args:
        data: Dictionary containing the data to validate
        field_types: Dictionary mapping field names to expected types

    Returns:
        Tuple of (is_valid, list_of_invalid_fields)
    """
    validator = get_validator()
    return validator.validate_field_types(data, field_types)


# Specific validators for our application entities
def validate_user_data(user_data: Dict[str, Any]) -> List[str]:
    """
    Validate user data according to our requirements.

    Args:
        user_data: Dictionary containing user information

    Returns:
        List of validation errors
    """
    errors = []

    # Validate required fields
    required_fields = ['name', 'email', 'password']
    is_valid, missing_fields = validate_required_fields(user_data, required_fields)
    if not is_valid:
        errors.extend([f"Missing required field: {field}" for field in missing_fields])

    # Validate email format
    if 'email' in user_data:
        is_valid, error = validate_email(user_data['email'])
        if not is_valid:
            errors.append(error)

    # Validate name length
    if 'name' in user_data:
        is_valid, error = validate_string_length(user_data['name'], min_length=1, max_length=255, field_name='name')
        if not is_valid:
            errors.append(error)

    # Validate password strength (basic check - length)
    if 'password' in user_data:
        is_valid, error = validate_string_length(user_data['password'], min_length=8, field_name='password')
        if not is_valid:
            errors.append(error)

    # Validate role if provided
    if 'role' in user_data:
        is_valid, error = validate_enum_value(user_data['role'], ['admin', 'user'], 'role')
        if not is_valid:
            errors.append(error)

    return errors


def validate_commissioner_record_data(record_data: Dict[str, Any]) -> List[str]:
    """
    Validate commissioner record data according to our requirements.

    Args:
        record_data: Dictionary containing commissioner record information

    Returns:
        List of validation errors
    """
    errors = []

    # Validate required fields
    required_fields = ['acc_no', 'department', 'file_no', 'subject', 'year', 'page', 'condition', 'record_type']
    is_valid, missing_fields = validate_required_fields(record_data, required_fields)
    if not is_valid:
        errors.extend([f"Missing required field: {field}" for field in missing_fields])

    # Validate acc_no is positive integer
    if 'acc_no' in record_data:
        is_valid, error = validate_positive_integer(record_data['acc_no'], 'acc_no')
        if not is_valid:
            errors.append(error)

    # Validate year is positive integer
    if 'year' in record_data:
        is_valid, error = validate_positive_integer(record_data['year'], 'year')
        if not is_valid:
            errors.append(error)

    # Validate page is positive integer
    if 'page' in record_data:
        is_valid, error = validate_positive_integer(record_data['page'], 'page')
        if not is_valid:
            errors.append(error)

    # Validate string lengths
    string_fields = {
        'department': 255,
        'file_no': 255,
        'subject': None,  # No max length limit for subject
        'condition': 255,
        'record_type': 255
    }

    for field, max_length in string_fields.items():
        if field in record_data:
            is_valid, error = validate_string_length(record_data[field], min_length=1,
                                                    max_length=max_length, field_name=field)
            if not is_valid:
                errors.append(error)

    return errors


def validate_court_record_data(record_data: Dict[str, Any]) -> List[str]:
    """
    Validate court record data according to our requirements.

    Args:
        record_data: Dictionary containing court record information

    Returns:
        List of validation errors
    """
    errors = []

    # Validate required fields
    required_fields = ['acc_no', 'court', 'suit_no', 'plaintiff', 'defendant', 'claim_or_charge', 'date_from', 'date_to', 'language']
    is_valid, missing_fields = validate_required_fields(record_data, required_fields)
    if not is_valid:
        errors.extend([f"Missing required field: {field}" for field in missing_fields])

    # Validate acc_no is positive integer
    if 'acc_no' in record_data:
        is_valid, error = validate_positive_integer(record_data['acc_no'], 'acc_no')
        if not is_valid:
            errors.append(error)

    # Validate date range
    if 'date_from' in record_data and 'date_to' in record_data:
        is_valid, error = validate_date_range(record_data['date_from'], record_data['date_to'])
        if not is_valid:
            errors.append(error)

    # Validate string lengths
    string_fields = {
        'court': 255,
        'suit_no': 255,
        'plaintiff': 255,
        'defendant': 255,
        'claim_or_charge': None,  # No max length limit for claim_or_charge
        'language': 50
    }

    for field, max_length in string_fields.items():
        if field in record_data:
            is_valid, error = validate_string_length(record_data[field], min_length=1,
                                                    max_length=max_length, field_name=field)
            if not is_valid:
                errors.append(error)

    return errors