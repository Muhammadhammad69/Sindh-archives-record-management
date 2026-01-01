"""
Structured logging utilities for the application.

This module provides utilities for structured logging with different levels
and formats appropriate for a secure application.
"""
import logging
import sys
from typing import Optional, Dict, Any
from datetime import datetime
import json
import os


class StructuredLogger:
    """
    Structured logger that provides consistent, searchable log formatting.

    Provides methods for logging with structured data that can be easily
    parsed and analyzed by log aggregation systems.
    """

    def __init__(self, name: str, level: str = 'INFO'):
        """
        Initialize the structured logger.

        Args:
            name: Name of the logger
            level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, level.upper()))

        # Prevent adding multiple handlers if logger already has handlers
        if not self.logger.handlers:
            # Create console handler with a higher log level
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(getattr(logging, level.upper()))

            # Create formatter with structured JSON output
            formatter = StructuredFormatter()
            console_handler.setFormatter(formatter)

            # Add handler to logger
            self.logger.addHandler(console_handler)

    def _log(self, level: str, message: str, extra_data: Optional[Dict[str, Any]] = None):
        """
        Internal method to log a message with structured data.

        Args:
            level: Log level
            message: Log message
            extra_data: Additional structured data to include in log
        """
        if extra_data is None:
            extra_data = {}

        # Add timestamp to extra data
        extra_data['timestamp'] = datetime.utcnow().isoformat()
        extra_data['level'] = level

        # Log the message with extra data
        log_method = getattr(self.logger, level.lower())
        log_method(message, extra=extra_data)

    def debug(self, message: str, extra_data: Optional[Dict[str, Any]] = None):
        """Log a debug message."""
        self._log('DEBUG', message, extra_data)

    def info(self, message: str, extra_data: Optional[Dict[str, Any]] = None):
        """Log an info message."""
        self._log('INFO', message, extra_data)

    def warning(self, message: str, extra_data: Optional[Dict[str, Any]] = None):
        """Log a warning message."""
        self._log('WARNING', message, extra_data)

    def error(self, message: str, extra_data: Optional[Dict[str, Any]] = None):
        """Log an error message."""
        self._log('ERROR', message, extra_data)

    def critical(self, message: str, extra_data: Optional[Dict[str, Any]] = None):
        """Log a critical message."""
        self._log('CRITICAL', message, extra_data)

    def log_db_operation(self, operation: str, table: str, success: bool,
                        extra_data: Optional[Dict[str, Any]] = None):
        """
        Log a database operation with appropriate context.

        Args:
            operation: Type of operation (SELECT, INSERT, UPDATE, DELETE)
            table: Name of the table involved
            success: Whether the operation was successful
            extra_data: Additional data about the operation
        """
        if extra_data is None:
            extra_data = {}

        extra_data.update({
            'operation': operation,
            'table': table,
            'success': success,
            'component': 'database'
        })

        level = 'INFO' if success else 'ERROR'
        message = f"Database {operation} on {table} {'succeeded' if success else 'failed'}"
        self._log(level, message, extra_data)

    def log_security_event(self, event_type: str, user_id: Optional[str] = None,
                         ip_address: Optional[str] = None, success: bool = True,
                         extra_data: Optional[Dict[str, Any]] = None):
        """
        Log a security-related event.

        Args:
            event_type: Type of security event (login, logout, access_denied, etc.)
            user_id: ID of the user involved
            ip_address: IP address of the request
            success: Whether the security event was successful
            extra_data: Additional security-related data
        """
        if extra_data is None:
            extra_data = {}

        extra_data.update({
            'event_type': event_type,
            'user_id': user_id,
            'ip_address': ip_address,
            'success': success,
            'component': 'security'
        })

        level = 'INFO' if success else 'WARNING'
        message = f"Security event: {event_type} {'succeeded' if success else 'failed'}"
        self._log(level, message, extra_data)

    def log_user_action(self, action: str, user_id: str,
                       extra_data: Optional[Dict[str, Any]] = None):
        """
        Log a user action for audit purposes.

        Args:
            action: Description of the action taken
            user_id: ID of the user who performed the action
            extra_data: Additional data about the action
        """
        if extra_data is None:
            extra_data = {}

        extra_data.update({
            'action': action,
            'user_id': user_id,
            'component': 'user_action'
        })

        message = f"User {user_id} performed action: {action}"
        self._log('INFO', message, extra_data)


class StructuredFormatter(logging.Formatter):
    """
    Custom formatter that outputs structured JSON logs.
    """

    def format(self, record):
        """
        Format the log record as structured JSON.

        Args:
            record: Log record to format

        Returns:
            Formatted log string
        """
        log_entry = {
            'timestamp': datetime.fromtimestamp(record.created).isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno,
        }

        # Add any extra fields that were passed
        if hasattr(record, '__dict__'):
            for key, value in record.__dict__.items():
                if key not in ['name', 'msg', 'args', 'levelname', 'levelno', 'pathname',
                              'filename', 'module', 'lineno', 'funcName', 'created',
                              'msecs', 'relativeCreated', 'thread', 'threadName',
                              'processName', 'process', 'getMessage', 'exc_info',
                              'exc_text', 'stack_info']:
                    log_entry[key] = value

        # Handle exception information if present
        if record.exc_info:
            log_entry['exception'] = self.formatException(record.exc_info)

        # Handle stack info if present
        if record.stack_info:
            log_entry['stack_info'] = self.formatStack(record.stack_info)

        return json.dumps(log_entry)


def setup_logging(level: str = 'INFO', log_file: Optional[str] = None) -> StructuredLogger:
    """
    Set up structured logging for the application.

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional file path to write logs to

    Returns:
        Configured StructuredLogger instance
    """
    # Set up basic configuration
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Create the structured logger
    logger = StructuredLogger('sindh_archives', level)

    # Add file handler if log_file is specified
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_formatter = StructuredFormatter()
        file_handler.setFormatter(file_formatter)
        logger.logger.addHandler(file_handler)

    return logger


def get_logger(name: str) -> StructuredLogger:
    """
    Get a logger instance with the specified name.

    Args:
        name: Name for the logger

    Returns:
        StructuredLogger instance
    """
    return StructuredLogger(name)


# Global logger instance
app_logger: Optional[StructuredLogger] = None


def get_app_logger() -> StructuredLogger:
    """
    Get the global application logger instance.

    Returns:
        Global StructuredLogger instance
    """
    global app_logger
    if app_logger is None:
        log_level = os.getenv('LOG_LEVEL', 'INFO')
        app_logger = setup_logging(log_level)
    return app_logger


def log_db_query(query: str, params: Optional[tuple] = None, duration: Optional[float] = None):
    """
    Log a database query with parameters and execution time.

    Args:
        query: The SQL query that was executed
        params: Parameters passed to the query (will be masked for security)
        duration: Query execution time in seconds
    """
    logger = get_app_logger()

    # Mask sensitive parameters
    safe_params = []
    if params:
        for param in params:
            # For security, we don't log sensitive data like passwords
            if isinstance(param, str) and ('password' in query.lower() or 'token' in query.lower()):
                safe_params.append('***MASKED***')
            else:
                safe_params.append(param)

    extra_data = {
        'query': query,
        'params_count': len(safe_params) if safe_params else 0,
        'duration_ms': round(duration * 1000, 2) if duration else None,
        'component': 'database_query'
    }

    logger.info(f"Executing query: {query.split()[0] if query.split() else 'UNKNOWN'}", extra_data)


def log_user_login(user_id: str, success: bool, ip_address: Optional[str] = None):
    """
    Log a user login attempt.

    Args:
        user_id: ID of the user attempting to log in
        success: Whether the login was successful
        ip_address: IP address of the login attempt
    """
    logger = get_app_logger()
    logger.log_security_event('login', user_id, ip_address, success)


def log_user_logout(user_id: str, ip_address: Optional[str] = None):
    """
    Log a user logout.

    Args:
        user_id: ID of the user logging out
        ip_address: IP address of the logout request
    """
    logger = get_app_logger()
    logger.log_security_event('logout', user_id, ip_address, True)