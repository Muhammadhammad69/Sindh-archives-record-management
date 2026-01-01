"""
Environment variable management and validation.

This module provides utilities for loading and validating environment variables
with proper error handling and clear error messages for missing configuration.
"""
import os
from typing import Optional, List, Dict, Any
from dotenv import load_dotenv


class EnvironmentManager:
    """
    Manager for environment variable validation and loading.

    Provides methods to load environment variables from .env files and validate
    that required variables are present with appropriate values.
    """

    def __init__(self, env_file: Optional[str] = None):
        """
        Initialize the environment manager.

        Args:
            env_file: Optional path to .env file to load from
        """
        # Load environment variables from .env file if provided
        if env_file and os.path.exists(env_file):
            load_dotenv(env_file)
        else:
            # Try to load from default .env file
            load_dotenv()

        self.required_vars: List[str] = []
        self.optional_vars: Dict[str, Any] = {}

    def add_required_variable(self, var_name: str):
        """
        Add a required environment variable to the validation list.

        Args:
            var_name: Name of the environment variable
        """
        if var_name not in self.required_vars:
            self.required_vars.append(var_name)

    def add_optional_variable(self, var_name: str, default_value: Any = None):
        """
        Add an optional environment variable with a default value.

        Args:
            var_name: Name of the environment variable
            default_value: Default value if the variable is not set
        """
        self.optional_vars[var_name] = default_value

    def validate_required_variables(self) -> Dict[str, str]:
        """
        Validate that all required environment variables are present.

        Returns:
            Dictionary of validated environment variables

        Raises:
            ValueError: If any required environment variable is missing
        """
        missing_vars = []
        validated_vars = {}

        for var_name in self.required_vars:
            value = os.getenv(var_name)
            if value is None or value.strip() == "":
                missing_vars.append(var_name)
            else:
                validated_vars[var_name] = value

        if missing_vars:
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing_vars)}. "
                f"Please check your .env file and ensure all required variables are set."
            )

        return validated_vars

    def get_variable(self, var_name: str, default: Optional[str] = None) -> Optional[str]:
        """
        Get an environment variable value.

        Args:
            var_name: Name of the environment variable
            default: Default value if the variable is not set

        Returns:
            Value of the environment variable or default value
        """
        return os.getenv(var_name, default)

    def get_variable_as_bool(self, var_name: str, default: bool = False) -> bool:
        """
        Get an environment variable as a boolean value.

        Args:
            var_name: Name of the environment variable
            default: Default value if the variable is not set

        Returns:
            Boolean value of the environment variable
        """
        value = os.getenv(var_name, "").lower().strip()
        if value in ('true', '1', 'yes', 'on', 'y', 't'):
            return True
        elif value in ('false', '0', 'no', 'off', 'n', 'f', ''):
            return default
        else:
            # If it's not a standard boolean value, raise an error
            raise ValueError(f"Invalid boolean value for {var_name}: {value}")

    def get_variable_as_int(self, var_name: str, default: Optional[int] = None) -> Optional[int]:
        """
        Get an environment variable as an integer value.

        Args:
            var_name: Name of the environment variable
            default: Default value if the variable is not set

        Returns:
            Integer value of the environment variable

        Raises:
            ValueError: If the variable value is not a valid integer
        """
        value = os.getenv(var_name)
        if value is None:
            return default
        try:
            return int(value)
        except ValueError:
            raise ValueError(f"Invalid integer value for {var_name}: {value}")

    def get_variable_as_float(self, var_name: str, default: Optional[float] = None) -> Optional[float]:
        """
        Get an environment variable as a float value.

        Args:
            var_name: Name of the environment variable
            default: Default value if the variable is not set

        Returns:
            Float value of the environment variable

        Raises:
            ValueError: If the variable value is not a valid float
        """
        value = os.getenv(var_name)
        if value is None:
            return default
        try:
            return float(value)
        except ValueError:
            raise ValueError(f"Invalid float value for {var_name}: {value}")

    def validate_database_url(self, var_name: str = 'DATABASE_URL') -> str:
        """
        Validate that the database URL is properly formatted.

        Args:
            var_name: Name of the database URL environment variable

        Returns:
            Validated database URL

        Raises:
            ValueError: If the database URL is invalid
        """
        db_url = os.getenv(var_name)
        if not db_url:
            raise ValueError(f"Database URL environment variable '{var_name}' is not set")

        # Basic validation for PostgreSQL URL format
        if not db_url.startswith(('postgresql://', 'postgres://', 'postgresql+psycopg2://')):
            raise ValueError(f"Database URL must start with 'postgresql://' or 'postgres://' or 'postgresql+psycopg2://'")

        return db_url

    def check_all_variables(self) -> Dict[str, str]:
        """
        Check all required and optional variables and return a comprehensive validation report.

        Returns:
            Dictionary with validation results
        """
        results = {
            'valid': True,
            'missing_required': [],
            'set_variables': {},
            'optional_with_defaults': {}
        }

        # Check required variables
        for var_name in self.required_vars:
            value = os.getenv(var_name)
            if value is None or value.strip() == "":
                results['missing_required'].append(var_name)
                results['valid'] = False
            else:
                results['set_variables'][var_name] = value

        # Check optional variables
        for var_name, default_value in self.optional_vars.items():
            value = os.getenv(var_name)
            if value is None or value.strip() == "":
                results['optional_with_defaults'][var_name] = default_value
            else:
                results['set_variables'][var_name] = value

        return results


# Global environment manager instance
env_manager = EnvironmentManager()


def initialize_environment(env_file: Optional[str] = None):
    """
    Initialize the environment manager and validate required variables.

    Args:
        env_file: Optional path to .env file to load from

    Returns:
        EnvironmentManager instance with validated configuration
    """
    global env_manager
    env_manager = EnvironmentManager(env_file)

    # Add required variables based on our application needs
    env_manager.add_required_variable('DATABASE_URL')
    env_manager.add_required_variable('USERS_TABLE_NAME')
    env_manager.add_required_variable('COMMISSIONER_TABLE_NAME')
    env_manager.add_required_variable('COURT_TABLE_NAME')

    # Validate required variables
    env_manager.validate_required_variables()

    return env_manager


def get_required_variable(var_name: str) -> str:
    """
    Get a required environment variable.

    Args:
        var_name: Name of the environment variable

    Returns:
        Value of the environment variable

    Raises:
        ValueError: If the environment variable is not set
    """
    value = os.getenv(var_name)
    if value is None or value.strip() == "":
        raise ValueError(f"Required environment variable '{var_name}' is not set")
    return value


def get_optional_variable(var_name: str, default: Optional[str] = None) -> Optional[str]:
    """
    Get an optional environment variable with a default value.

    Args:
        var_name: Name of the environment variable
        default: Default value if the variable is not set

    Returns:
        Value of the environment variable or default value
    """
    return os.getenv(var_name, default)