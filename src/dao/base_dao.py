"""
Base Data Access Object (DAO) with common CRUD operations.

This module provides a base class for all data access objects that includes
common database operations using pandas for data manipulation and
parameterized queries for security.
"""
from typing import List, Dict, Any, Optional, Union
from abc import ABC, abstractmethod
import pandas as pd
import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
from src.database.connection import connection_manager
from src.utils.logging import get_app_logger


class BaseDAO(ABC):
    """
    Base Data Access Object with common CRUD operations.

    Provides common database operations that can be inherited by specific DAOs.
    Uses pandas for data manipulation and ensures all queries are parameterized
    to prevent SQL injection.
    """

    def __init__(self, table_name: str):
        """
        Initialize the base DAO.

        Args:
            table_name: Name of the database table this DAO manages
        """
        self.table_name = table_name
        self.logger = get_app_logger()

    def _execute_query(self, query: str, params: Optional[tuple] = None) -> List[Dict[str, Any]]:
        """
        Execute a SELECT query and return results as a list of dictionaries.

        Args:
            query: SQL query to execute
            params: Parameters for the query

        Returns:
            List of dictionaries representing the query results
        """
        try:
            with connection_manager.get_db_connection() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    self.logger.debug(f"Executing query: {query}", {
                        'table': self.table_name,
                        'query_type': 'SELECT'
                    })
                    cursor.execute(query, params)
                    results = cursor.fetchall()
                    return [dict(row) for row in results]
        except psycopg2.Error as e:
            self.logger.error(f"Database error executing query: {e}", {
                'table': self.table_name,
                'query': query,
                'error': str(e)
            })
            raise

    def _execute_update(self, query: str, params: Optional[tuple] = None) -> int:
        """
        Execute an INSERT, UPDATE, or DELETE query.

        Args:
            query: SQL query to execute
            params: Parameters for the query

        Returns:
            Number of affected rows
        """
        try:
            with connection_manager.get_db_connection() as conn:
                with conn.cursor() as cursor:
                    self.logger.debug(f"Executing update: {query}", {
                        'table': self.table_name,
                        'query_type': 'UPDATE'
                    })
                    cursor.execute(query, params)
                    return cursor.rowcount
        except psycopg2.Error as e:
            self.logger.error(f"Database error executing update: {e}", {
                'table': self.table_name,
                'query': query,
                'error': str(e)
            })
            raise

    def _execute_many(self, query: str, params_list: List[tuple]) -> int:
        """
        Execute a query multiple times with different parameter sets.

        Args:
            query: SQL query to execute
            params_list: List of parameter tuples

        Returns:
            Number of affected rows
        """
        try:
            with connection_manager.get_db_connection() as conn:
                with conn.cursor() as cursor:
                    self.logger.debug(f"Executing many: {query}", {
                        'table': self.table_name,
                        'query_type': 'UPDATE_MANY',
                        'count': len(params_list)
                    })
                    cursor.executemany(query, params_list)
                    return cursor.rowcount
        except psycopg2.Error as e:
            self.logger.error(f"Database error executing many: {e}", {
                'table': self.table_name,
                'query': query,
                'error': str(e)
            })
            raise

    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new record in the database.

        Args:
            data: Dictionary containing field-value pairs to insert

        Returns:
            Dictionary representing the created record
        """
        # Get column names and values
        columns = list(data.keys())
        values = list(data.values())

        # Build parameterized query
        placeholders = ', '.join(['%s'] * len(columns))
        column_names = ', '.join(columns)
        query = f"INSERT INTO {self.table_name} ({column_names}) VALUES ({placeholders}) RETURNING *"

        try:
            with connection_manager.get_db_connection() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    self.logger.info(f"Creating record in {self.table_name}", {
                        'table': self.table_name,
                        'data_keys': list(data.keys())
                    })
                    cursor.execute(query, values)
                    result = cursor.fetchone()
                    return dict(result) if result else {}
        except psycopg2.Error as e:
            self.logger.error(f"Database error creating record: {e}", {
                'table': self.table_name,
                'data': data,
                'error': str(e)
            })
            raise

    def get_by_id(self, record_id: Union[int, str], id_column: str = 'id') -> Optional[Dict[str, Any]]:
        """
        Retrieve a record by its ID.

        Args:
            record_id: The ID of the record to retrieve
            id_column: Name of the ID column (default 'id')

        Returns:
            Dictionary representing the record, or None if not found
        """
        query = f"SELECT * FROM {self.table_name} WHERE {id_column} = %s"
        results = self._execute_query(query, (record_id,))
        return results[0] if results else None

    def get_all(self, limit: Optional[int] = None, offset: Optional[int] = 0) -> List[Dict[str, Any]]:
        """
        Retrieve all records from the table.

        Args:
            limit: Maximum number of records to return
            offset: Number of records to skip

        Returns:
            List of dictionaries representing the records
        """
        query = f"SELECT * FROM {self.table_name}"
        if limit:
            query += f" LIMIT %s OFFSET %s"
            params = (limit, offset)
        elif offset > 0:
            query += f" OFFSET %s"
            params = (offset,)
        else:
            params = None

        return self._execute_query(query, params)

    def update_by_id(self, record_id: Union[int, str], data: Dict[str, Any],
                     id_column: str = 'id') -> bool:
        """
        Update a record by its ID.

        Args:
            record_id: The ID of the record to update
            data: Dictionary containing field-value pairs to update
            id_column: Name of the ID column (default 'id')

        Returns:
            True if the record was updated, False if not found
        """
        if not data:
            return False

        # Build SET clause with parameterized values
        set_clause = ', '.join([f"{key} = %s" for key in data.keys()])
        values = list(data.values()) + [record_id]  # Add ID to the end for WHERE clause
        query = f"UPDATE {self.table_name} SET {set_clause} WHERE {id_column} = %s"

        try:
            with connection_manager.get_db_connection() as conn:
                with conn.cursor() as cursor:
                    self.logger.info(f"Updating record in {self.table_name}", {
                        'table': self.table_name,
                        'id': record_id,
                        'data_keys': list(data.keys())
                    })
                    cursor.execute(query, values)
                    return cursor.rowcount > 0
        except psycopg2.Error as e:
            self.logger.error(f"Database error updating record: {e}", {
                'table': self.table_name,
                'id': record_id,
                'data': data,
                'error': str(e)
            })
            raise

    def delete_by_id(self, record_id: Union[int, str], id_column: str = 'id') -> bool:
        """
        Delete a record by its ID.

        Args:
            record_id: The ID of the record to delete
            id_column: Name of the ID column (default 'id')

        Returns:
            True if the record was deleted, False if not found
        """
        query = f"DELETE FROM {self.table_name} WHERE {id_column} = %s"

        try:
            with connection_manager.get_db_connection() as conn:
                with conn.cursor() as cursor:
                    self.logger.info(f"Deleting record from {self.table_name}", {
                        'table': self.table_name,
                        'id': record_id
                    })
                    cursor.execute(query, (record_id,))
                    return cursor.rowcount > 0
        except psycopg2.Error as e:
            self.logger.error(f"Database error deleting record: {e}", {
                'table': self.table_name,
                'id': record_id,
                'error': str(e)
            })
            raise

    def find_by_criteria(self, criteria: Dict[str, Any],
                         order_by: Optional[str] = None,
                         limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Find records matching specific criteria.

        Args:
            criteria: Dictionary of field-value pairs to match
            order_by: Field to order results by
            limit: Maximum number of records to return

        Returns:
            List of dictionaries representing matching records
        """
        if not criteria:
            return self.get_all(limit=limit)

        # Build WHERE clause with parameterized values
        where_conditions = []
        values = []
        for key, value in criteria.items():
            where_conditions.append(f"{key} = %s")
            values.append(value)

        where_clause = ' AND '.join(where_conditions)
        query = f"SELECT * FROM {self.table_name} WHERE {where_clause}"

        if order_by:
            query += f" ORDER BY {order_by}"
        if limit:
            query += f" LIMIT %s"
            values.append(limit)

        return self._execute_query(query, tuple(values))

    def bulk_create(self, records: List[Dict[str, Any]]) -> int:
        """
        Create multiple records in a single operation.

        Args:
            records: List of dictionaries containing field-value pairs to insert

        Returns:
            Number of records successfully created
        """
        if not records:
            return 0

        # Use the first record to determine column names
        columns = list(records[0].keys())
        column_names = ', '.join(columns)
        placeholders = ', '.join(['%s'] * len(columns))
        query = f"INSERT INTO {self.table_name} ({column_names}) VALUES ({placeholders})"

        # Prepare parameter tuples for each record
        params_list = [tuple(record.get(col) for col in columns) for record in records]

        return self._execute_many(query, params_list)

    def bulk_update(self, updates: List[Dict[str, Any]], id_column: str = 'id') -> int:
        """
        Update multiple records in a single operation.

        Args:
            updates: List of dictionaries containing ID and field-value pairs to update
            id_column: Name of the ID column (default 'id')

        Returns:
            Number of records successfully updated
        """
        if not updates:
            return 0

        updated_count = 0
        for update_data in updates:
            if id_column not in update_data:
                continue

            record_id = update_data.pop(id_column)  # Remove ID from update data
            success = self.update_by_id(record_id, update_data, id_column)
            if success:
                updated_count += 1

        return updated_count

    def to_dataframe(self, criteria: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
        """
        Get all records as a pandas DataFrame.

        Args:
            criteria: Optional dictionary of field-value pairs to filter records

        Returns:
            Pandas DataFrame containing the records
        """
        if criteria:
            records = self.find_by_criteria(criteria)
        else:
            records = self.get_all()

        if not records:
            # Return empty DataFrame with appropriate columns if we have any records to infer from
            return pd.DataFrame()

        return pd.DataFrame(records)

    def create_from_dataframe(self, df: pd.DataFrame) -> int:
        """
        Create records from a pandas DataFrame.

        Args:
            df: Pandas DataFrame containing the records to create

        Returns:
            Number of records successfully created
        """
        if df.empty:
            return 0

        # Convert DataFrame to list of dictionaries
        records = df.to_dict('records')
        return self.bulk_create(records)

    @abstractmethod
    def validate_data(self, data: Dict[str, Any]) -> Dict[str, List[str]]:
        """
        Validate data before saving to database.

        This method should be implemented by subclasses to provide
        specific validation logic for their data type.

        Args:
            data: Dictionary containing the data to validate

        Returns:
            Dictionary with field names as keys and lists of error messages as values
        """
        pass


def get_column_names(table_name: str) -> List[str]:
    """
    Get the column names for a given table.

    Args:
        table_name: Name of the table

    Returns:
        List of column names
    """
    query = """
    SELECT column_name
    FROM information_schema.columns
    WHERE table_name = %s
    ORDER BY ordinal_position
    """

    results = BaseDAO(table_name)._execute_query(query, (table_name,))
    return [row['column_name'] for row in results]


def table_exists(table_name: str) -> bool:
    """
    Check if a table exists in the database.

    Args:
        table_name: Name of the table to check

    Returns:
        True if the table exists, False otherwise
    """
    query = """
    SELECT EXISTS (
        SELECT FROM information_schema.tables
        WHERE table_name = %s
    )
    """

    results = BaseDAO(table_name)._execute_query(query, (table_name,))
    return results[0]['exists'] if results else False