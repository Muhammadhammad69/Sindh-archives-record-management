"""
Base model with audit fields for all database entities.

This module provides a base class that includes common audit fields
like created_at and updated_at that are required for all entities.
"""
from datetime import datetime
from typing import Optional
import psycopg2.extras


class BaseModel:
    """
    Base model class providing common audit fields and operations.

    All database models should inherit from this class to ensure
    consistent audit trail functionality.
    """

    def __init__(self):
        self.created_at: Optional[datetime] = None
        self.updated_at: Optional[datetime] = None

    @classmethod
    def get_audit_fields(cls) -> dict:
        """
        Get the audit fields for this model.

        Returns:
            Dictionary containing audit field names and their default values
        """
        now = datetime.utcnow()
        return {
            'created_at': now,
            'updated_at': now
        }

    @classmethod
    def update_audit_fields(cls, data: dict) -> dict:
        """
        Update audit fields in the provided data dictionary.

        Args:
            data: Dictionary containing model data

        Returns:
            Updated dictionary with audit fields
        """
        data['updated_at'] = datetime.utcnow()
        if 'created_at' not in data or data['created_at'] is None:
            data['created_at'] = datetime.utcnow()
        return data

    def to_dict(self) -> dict:
        """
        Convert the model instance to a dictionary.

        Returns:
            Dictionary representation of the model
        """
        result = {}
        if hasattr(self, '__dict__'):
            result.update(self.__dict__)
        return result

    @classmethod
    def from_db_row(cls, row: tuple, field_names: list):
        """
        Create a model instance from a database row.

        Args:
            row: Database row as a tuple
            field_names: List of field names corresponding to the row values

        Returns:
            Instance of the model populated with data from the row
        """
        instance = cls()
        for i, field_name in enumerate(field_names):
            if i < len(row):
                setattr(instance, field_name, row[i])
        return instance


def get_base_fields() -> list:
    """
    Get the list of base audit field names.

    Returns:
        List of base field names that should be included in all models
    """
    return ['created_at', 'updated_at']


def get_base_field_definitions() -> str:
    """
    Get SQL definition for base audit fields.

    Returns:
        String containing SQL column definitions for audit fields
    """
    return """
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    """


def get_updated_at_trigger_sql(table_name: str) -> str:
    """
    Generate SQL for a trigger that automatically updates the updated_at field.

    Args:
        table_name: Name of the table for which to create the trigger

    Returns:
        SQL string to create the trigger
    """
    trigger_name = f"{table_name}_updated_at_trigger"
    function_name = f"{table_name}_set_updated_at"

    return f"""
    CREATE OR REPLACE FUNCTION {function_name}()
    RETURNS TRIGGER AS $$
    BEGIN
        NEW.updated_at = CURRENT_TIMESTAMP;
        RETURN NEW;
    END;
    $$ language 'plpgsql';

    DROP TRIGGER IF EXISTS {trigger_name} ON {table_name};
    CREATE TRIGGER {trigger_name}
        BEFORE UPDATE ON {table_name}
        FOR EACH ROW
        EXECUTE FUNCTION {function_name}();
    """