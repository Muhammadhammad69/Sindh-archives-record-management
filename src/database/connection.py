"""
Database connection management with connection pooling for PostgreSQL.

This module implements a thread-safe connection pool manager that follows
best practices for secure and efficient database connection management.
"""
import os
import threading
from typing import Optional
from psycopg2 import pool, extensions
from contextlib import contextmanager


class ConnectionManager:
    """
    Singleton class for managing PostgreSQL connection pools.

    Implements thread-safe connection pooling with proper resource management.
    """
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.connection_pool: Optional[pool.ThreadedConnectionPool] = None
            self.initialized = True
            self._create_pool()

    def _create_pool(self):
        """Create a thread-safe connection pool based on environment variables."""
        database_url = os.getenv('DATABASE_URL')
        if not database_url:
            raise ValueError("DATABASE_URL environment variable is required")

        # Extract connection parameters from DATABASE_URL
        # For now, we'll use a simplified approach - in production, use a proper URL parser
        if database_url.startswith('postgresql://'):
            # Parse the URL to extract components
            from urllib.parse import urlparse
            parsed = urlparse(database_url)

            minconn = int(os.getenv('DB_MIN_CONNECTIONS', '2'))
            maxconn = int(os.getenv('DB_MAX_CONNECTIONS', '10'))

            self.connection_pool = pool.ThreadedConnectionPool(
                minconn=minconn,
                maxconn=maxconn,
                host=parsed.hostname,
                port=parsed.port,
                database=parsed.path[1:],  # Remove leading '/'
                user=parsed.username,
                password=parsed.password
            )

    def get_connection(self):
        """Get a connection from the pool."""
        if not self.connection_pool:
            raise RuntimeError("Connection pool not initialized")
        return self.connection_pool.getconn()

    def put_connection(self, conn):
        """Return a connection to the pool."""
        if self.connection_pool:
            self.connection_pool.putconn(conn)

    def close_all_connections(self):
        """Close all connections in the pool."""
        if self.connection_pool:
            self.connection_pool.closeall()

    @contextmanager
    def get_db_connection(self):
        """
        Context manager for database connections.

        Automatically handles connection acquisition and return to pool,
        with proper transaction management.
        """
        conn = None
        try:
            conn = self.get_connection()
            # Test the connection with a simple query to ensure it's still valid
            try:
                with conn.cursor() as test_cursor:
                    test_cursor.execute("SELECT 1;")
                    test_cursor.fetchone()
            except psycopg2.OperationalError:
                # Connection is invalid, return it to pool and get a fresh one
                self.put_connection(conn)
                conn = self.get_connection()

            # Set proper isolation level
            conn.set_isolation_level(extensions.ISOLATION_LEVEL_READ_COMMITTED)
            yield conn
            conn.commit()
        except Exception as e:
            if conn:
                conn.rollback()
            raise
        finally:
            if conn:
                self.put_connection(conn)


# Global connection manager instance
connection_manager = ConnectionManager()


def get_db_connection():
    """
    Get a database connection from the pool.

    Returns:
        A database connection from the connection pool
    """
    return connection_manager.get_connection()


def put_db_connection(conn):
    """
    Return a database connection to the pool.

    Args:
        conn: The connection to return to the pool
    """
    connection_manager.put_connection(conn)


@contextmanager
def get_db_cursor():
    """
    Context manager that provides a database cursor.

    Automatically handles connection and cursor lifecycle,
    with proper transaction management.
    """
    with connection_manager.get_db_connection() as conn:
        with conn.cursor() as cursor:
            yield cursor


# Initialize the connection manager on module import
def initialize_connection_pool():
    """
    Initialize the connection pool.

    This function can be called at application startup to ensure
    the connection pool is properly initialized.
    """
    try:
        # Access the singleton to trigger initialization
        _ = connection_manager
    except Exception as e:
        print(f"Failed to initialize connection pool: {e}")
        raise