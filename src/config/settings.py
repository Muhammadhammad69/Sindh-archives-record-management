"""
Application settings management.

This module provides a centralized configuration class that loads and validates
all application settings from environment variables with appropriate defaults.
"""
from typing import Optional
from src.config.environment import EnvironmentManager, get_required_variable, get_optional_variable


class Settings:
    """
    Application settings class that centralizes all configuration.

    Loads settings from environment variables with validation and provides
    default values where appropriate.
    """

    def __init__(self):
        """Initialize settings from environment variables."""
        self._env_manager = EnvironmentManager()

        # Database settings
        self.database_url: str = get_required_variable('DATABASE_URL')
        self.users_table_name: str = get_required_variable('USERS_TABLE_NAME')
        self.commissioner_table_name: str = get_required_variable('COMMISSIONER_TABLE_NAME')
        self.court_table_name: str = get_required_variable('COURT_TABLE_NAME')

        # Connection pool settings
        self.db_min_connections: int = int(get_optional_variable('DB_MIN_CONNECTIONS', '2'))
        self.db_max_connections: int = int(get_optional_variable('DB_MAX_CONNECTIONS', '10'))

        # Security settings
        self.bcrypt_rounds: int = int(get_optional_variable('BCRYPT_ROUNDS', '12'))
        self.jwt_secret: str = get_optional_variable('JWT_SECRET', 'default-secret-change-in-production')
        self.jwt_algorithm: str = get_optional_variable('JWT_ALGORITHM', 'HS256')
        self.jwt_expiration_hours: int = int(get_optional_variable('JWT_EXPIRATION_HOURS', '24'))

        # Application settings
        self.app_name: str = get_optional_variable('APP_NAME', 'Sindh Archives Backend')
        self.app_version: str = get_optional_variable('APP_VERSION', '0.1.0')
        self.debug_mode: bool = self._str_to_bool(get_optional_variable('DEBUG', 'False'))
        self.log_level: str = get_optional_variable('LOG_LEVEL', 'INFO')

        # Validation settings
        self.validate_settings()

    def validate_settings(self):
        """Validate that all settings have appropriate values."""
        errors = []

        # Validate database settings
        if not self.database_url:
            errors.append("DATABASE_URL is required")
        if not self.users_table_name:
            errors.append("USERS_TABLE_NAME is required")
        if not self.commissioner_table_name:
            errors.append("COMMISSIONER_TABLE_NAME is required")
        if not self.court_table_name:
            errors.append("COURT_TABLE_NAME is required")

        # Validate connection pool settings
        if self.db_min_connections <= 0:
            errors.append("DB_MIN_CONNECTIONS must be greater than 0")
        if self.db_max_connections <= 0:
            errors.append("DB_MAX_CONNECTIONS must be greater than 0")
        if self.db_min_connections > self.db_max_connections:
            errors.append("DB_MIN_CONNECTIONS cannot be greater than DB_MAX_CONNECTIONS")

        # Validate security settings
        if self.bcrypt_rounds < 4 or self.bcrypt_rounds > 31:
            errors.append("BCRYPT_ROUNDS should be between 4 and 31")
        if self.jwt_secret == 'default-secret-change-in-production':
            errors.append("JWT_SECRET is using default value - change for production")

        # Validate JWT settings
        if self.jwt_expiration_hours <= 0:
            errors.append("JWT_EXPIRATION_HOURS must be greater than 0")

        if errors:
            raise ValueError(f"Invalid settings: {'; '.join(errors)}")

    @staticmethod
    def _str_to_bool(value: str) -> bool:
        """
        Convert string value to boolean.

        Args:
            value: String value to convert

        Returns:
            Boolean representation of the string
        """
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.lower() in ('true', '1', 'yes', 'on', 'y', 't')
        return bool(value)

    def get_table_name(self, table_type: str) -> str:
        """
        Get the appropriate table name based on type.

        Args:
            table_type: Type of table ('users', 'commissioner', 'court')

        Returns:
            Table name for the specified type
        """
        table_mapping = {
            'users': self.users_table_name,
            'commissioner': self.commissioner_table_name,
            'court': self.court_table_name
        }

        if table_type not in table_mapping:
            raise ValueError(f"Unknown table type: {table_type}")

        return table_mapping[table_type]

    def get_database_config(self) -> dict:
        """
        Get database configuration as a dictionary.

        Returns:
            Dictionary containing database configuration
        """
        return {
            'database_url': self.database_url,
            'min_connections': self.db_min_connections,
            'max_connections': self.db_max_connections,
            'users_table': self.users_table_name,
            'commissioner_table': self.commissioner_table_name,
            'court_table': self.court_table_name
        }

    def get_security_config(self) -> dict:
        """
        Get security configuration as a dictionary.

        Returns:
            Dictionary containing security configuration
        """
        return {
            'bcrypt_rounds': self.bcrypt_rounds,
            'jwt_secret': self.jwt_secret,
            'jwt_algorithm': self.jwt_algorithm,
            'jwt_expiration_hours': self.jwt_expiration_hours
        }

    def get_app_config(self) -> dict:
        """
        Get application configuration as a dictionary.

        Returns:
            Dictionary containing application configuration
        """
        return {
            'app_name': self.app_name,
            'app_version': self.app_version,
            'debug_mode': self.debug_mode,
            'log_level': self.log_level
        }

    def __str__(self) -> str:
        """String representation of settings (excluding sensitive data)."""
        return (
            f"Settings(app_name='{self.app_name}', app_version='{self.app_version}', "
            f"debug_mode={self.debug_mode}, db_tables=[users:{self.users_table_name}, "
            f"commissioner:{self.commissioner_table_name}, court:{self.court_table_name}])"
        )

    def __repr__(self) -> str:
        """Detailed string representation of settings."""
        return self.__str__()


# Global settings instance
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """
    Get the application settings instance.

    Returns:
        Settings instance with loaded configuration
    """
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings


def reset_settings():
    """Reset the settings instance (useful for testing)."""
    global _settings
    _settings = None