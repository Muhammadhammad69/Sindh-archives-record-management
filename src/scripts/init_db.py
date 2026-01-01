"""
Database initialization script.

This script creates all required tables, indexes, and initial admin user
for the application.
"""
import sys
import os
from typing import Optional

# Add the project root to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database.connection import connection_manager
from src.database.models.user import User
from src.database.models.commissioner_record import CommissionerRecord
from src.database.models.court_record import CourtRecord
from src.dao.user_dao import UserDAO
from src.security.password_utils import hash_password
from src.config.settings import get_settings
from src.utils.logging import get_app_logger


def initialize_database():
    """
    Initialize the database with all required tables and indexes.
    """
    logger = get_app_logger()
    settings = get_settings()

    logger.info("Starting database initialization", {
        'component': 'database_initialization'
    })

    try:
        # Create connection
        with connection_manager.get_db_connection() as conn:
            with conn.cursor() as cursor:
                # Create users table
                logger.info("Creating users table", {
                    'component': 'database_initialization'
                })
                cursor.execute(User.get_table_schema())

                # Create commissioner records table
                logger.info("Creating commissioner records table", {
                    'component': 'database_initialization'
                })
                cursor.execute(CommissionerRecord.get_table_schema())

                # Create court records table
                logger.info("Creating court records table", {
                    'component': 'database_initialization'
                })
                cursor.execute(CourtRecord.get_table_schema())

                # Commit the changes
                conn.commit()

                logger.info("Database tables created successfully", {
                    'component': 'database_initialization'
                })

    except Exception as e:
        logger.error(f"Error creating database tables: {e}", {
            'error': str(e),
            'component': 'database_initialization'
        })
        raise


def create_initial_admin_user():
    """
    Create an initial admin user if one doesn't already exist.
    """
    logger = get_app_logger()
    user_dao = UserDAO()

    logger.info("Checking for existing admin users", {
        'component': 'database_initialization'
    })

    # Check if any admin users already exist
    try:
        admin_users = user_dao.get_all_admins()
        if admin_users:
            logger.info(f"Found {len(admin_users)} existing admin users, skipping initial admin creation", {
                'admin_count': len(admin_users),
                'component': 'database_initialization'
            })
            return

        # Create initial admin user
        admin_email = os.getenv('INITIAL_ADMIN_EMAIL', 'admin@sindh-archives.org')
        admin_password = os.getenv('INITIAL_ADMIN_PASSWORD', 'SecurePassword123!')

        admin_data = {
            'name': 'System Administrator',
            'email': admin_email,
            'role': 'admin',
            'password': admin_password  # This will be hashed by the DAO
        }

        logger.info(f"Creating initial admin user with email: {admin_email}", {
            'component': 'database_initialization'
        })

        admin_user = user_dao.create(admin_data)

        logger.info(f"Initial admin user created successfully with ID: {admin_user.id}", {
            'user_id': admin_user.id,
            'email': admin_user.email,
            'component': 'database_initialization'
        })

        print(f"\nInitial admin user created successfully!")
        print(f"Email: {admin_user.email}")
        print(f"Please change the default password on first login.")

    except Exception as e:
        logger.error(f"Error creating initial admin user: {e}", {
            'error': str(e),
            'component': 'database_initialization'
        })
        raise


def run_initialization():
    """
    Run the complete database initialization process.
    """
    logger = get_app_logger()

    logger.info("Starting complete database initialization process", {
        'component': 'database_initialization'
    })

    try:
        # Initialize database tables
        initialize_database()

        # Create initial admin user
        create_initial_admin_user()

        logger.info("Database initialization completed successfully", {
            'component': 'database_initialization'
        })

        print("\nDatabase initialization completed successfully!")
        print("All tables, indexes, and initial admin user have been created.")

    except Exception as e:
        logger.error(f"Database initialization failed: {e}", {
            'error': str(e),
            'component': 'database_initialization'
        })
        print(f"\nDatabase initialization failed: {e}")
        raise


if __name__ == "__main__":
    # Load environment variables
    from src.config.environment import initialize_environment
    initialize_environment()

    # Run the initialization
    run_initialization()