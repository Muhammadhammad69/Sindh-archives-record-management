"""
Integration tests for database connection functionality.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from src.database.connection import ConnectionManager, get_db_connection, put_db_connection, get_db_cursor


class TestDatabaseConnection:
    """Test class for database connection functionality."""

    def test_singleton_connection_manager(self):
        """Test that ConnectionManager follows singleton pattern."""
        manager1 = ConnectionManager()
        manager2 = ConnectionManager()

        assert manager1 is manager2

    @patch('src.database.connection.pool.ThreadedConnectionPool')
    def test_connection_pool_creation(self, mock_pool_class):
        """Test that connection pool is created with correct parameters."""
        # Mock the environment variable
        with patch.dict('os.environ', {
            'DATABASE_URL': 'postgresql://test:test@localhost:5432/testdb',
            'DB_MIN_CONNECTIONS': '2',
            'DB_MAX_CONNECTIONS': '10'
        }):
            manager = ConnectionManager()

            # Verify the pool was created
            mock_pool_class.assert_called_once()
            # Check that it was called with the right parameters
            args, kwargs = mock_pool_class.call_args
            assert args[0] == 2  # minconn
            assert args[1] == 10  # maxconn

    @patch('src.database.connection.ConnectionManager.get_connection')
    def test_get_db_connection(self, mock_get_connection):
        """Test the get_db_connection function."""
        mock_connection = Mock()
        mock_get_connection.return_value = mock_connection

        connection = get_db_connection()

        assert connection is mock_connection
        mock_get_connection.assert_called_once()

    @patch('src.database.connection.ConnectionManager.put_connection')
    def test_put_db_connection(self, mock_put_connection):
        """Test the put_db_connection function."""
        mock_connection = Mock()

        put_db_connection(mock_connection)

        mock_put_connection.assert_called_once_with(mock_connection)

    @patch('src.database.connection.connection_manager')
    def test_get_db_cursor_context_manager(self, mock_connection_manager):
        """Test the get_db_cursor context manager."""
        mock_connection = Mock()
        mock_cursor = Mock()

        mock_connection_manager.get_db_connection.return_value.__enter__.return_value = mock_connection
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor

        # Test the context manager
        with get_db_cursor() as cursor:
            assert cursor is mock_cursor

        # Verify the connection and cursor were used properly
        mock_connection_manager.get_db_connection.assert_called_once()
        mock_connection.cursor.assert_called_once()

    @patch('src.database.connection.pool.ThreadedConnectionPool')
    def test_get_connection_calls_pool_getconn(self, mock_pool_class):
        """Test that get_connection calls the connection pool's getconn method."""
        mock_pool_instance = Mock()
        mock_pool_class.return_value = mock_pool_instance
        mock_connection = Mock()
        mock_pool_instance.getconn.return_value = mock_connection

        with patch.dict('os.environ', {
            'DATABASE_URL': 'postgresql://test:test@localhost:5432/testdb'
        }):
            manager = ConnectionManager()
            connection = manager.get_connection()

            assert connection is mock_connection
            mock_pool_instance.getconn.assert_called_once()

    @patch('src.database.connection.pool.ThreadedConnectionPool')
    def test_put_connection_calls_pool_putconn(self, mock_pool_class):
        """Test that put_connection calls the connection pool's putconn method."""
        mock_pool_instance = Mock()
        mock_pool_class.return_value = mock_pool_instance
        mock_connection = Mock()

        with patch.dict('os.environ', {
            'DATABASE_URL': 'postgresql://test:test@localhost:5432/testdb'
        }):
            manager = ConnectionManager()
            manager.put_connection(mock_connection)

            mock_pool_instance.putconn.assert_called_once_with(mock_connection)

    @patch('src.database.connection.pool.ThreadedConnectionPool')
    def test_close_all_connections_calls_pool_closeall(self, mock_pool_class):
        """Test that close_all_connections calls the connection pool's closeall method."""
        mock_pool_instance = Mock()
        mock_pool_class.return_value = mock_pool_instance

        with patch.dict('os.environ', {
            'DATABASE_URL': 'postgresql://test:test@localhost:5432/testdb'
        }):
            manager = ConnectionManager()
            manager.close_all_connections()

            mock_pool_instance.closeall.assert_called_once()

    @patch('src.database.connection.pool.ThreadedConnectionPool')
    def test_context_manager_transaction_handling(self, mock_pool_class):
        """Test that the context manager handles transactions properly."""
        mock_pool_instance = Mock()
        mock_pool_class.return_value = mock_pool_instance
        mock_connection = Mock()
        mock_cursor = Mock()

        mock_pool_instance.getconn.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor

        with patch.dict('os.environ', {
            'DATABASE_URL': 'postgresql://test:test@localhost:5432/testdb'
        }):
            manager = ConnectionManager()

            # Test the context manager
            with manager.get_db_connection() as conn:
                pass  # The context manager should handle commit/rollback

            # Verify transaction was committed
            mock_connection.commit.assert_called_once()
            # Verify the connection was returned to the pool
            mock_pool_instance.putconn.assert_called_once_with(mock_connection)

    @patch('src.database.connection.pool.ThreadedConnectionPool')
    def test_context_manager_rollback_on_error(self, mock_pool_class):
        """Test that the context manager rolls back on error."""
        mock_pool_instance = Mock()
        mock_pool_class.return_value = mock_pool_instance
        mock_connection = Mock()
        mock_cursor = Mock()

        mock_pool_instance.getconn.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor

        with patch.dict('os.environ', {
            'DATABASE_URL': 'postgresql://test:test@localhost:5432/testdb'
        }):
            manager = ConnectionManager()

            # Test the context manager with an exception
            try:
                with manager.get_db_connection() as conn:
                    raise Exception("Test exception")
            except Exception:
                pass  # Expected

            # Verify transaction was rolled back
            mock_connection.rollback.assert_called_once()
            # Verify the connection was still returned to the pool
            mock_pool_instance.putconn.assert_called_once_with(mock_connection)

    @patch('src.database.connection.os.getenv')
    def test_initialize_connection_pool(self, mock_getenv):
        """Test the initialize_connection_pool function."""
        mock_getenv.return_value = 'postgresql://test:test@localhost:5432/testdb'

        from src.database.connection import initialize_connection_pool
        # This should not raise an exception
        initialize_connection_pool()