#!/usr/bin/env python3
"""
Script to initialize the database tables if they don't exist.
"""

import sys
import os

# Add the src directory to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Import the environment initialization first and initialize it
from src.config.environment import initialize_environment

print("Initializing environment...")
initialize_environment()

# Import the initialization script components
from src.database.connection import connection_manager
from src.database.models.user import User
from src.database.models.commissioner_record import CommissionerRecord
from src.database.models.court_record import CourtRecord

def initialize_tables():
    print("Initializing database tables...")

    try:
        # Create connection
        with connection_manager.get_db_connection() as conn:
            with conn.cursor() as cursor:
                # Create users table
                print("Creating users table...")
                cursor.execute(User.get_table_schema())

                # Create commissioner records table
                print("Creating commissioner records table...")
                cursor.execute(CommissionerRecord.get_table_schema())

                # Create court records table
                print("Creating court records table...")
                cursor.execute(CourtRecord.get_table_schema())

                # Commit the changes
                conn.commit()

                print("Database tables created successfully!")

    except Exception as e:
        print(f"Error creating database tables: {e}")
        raise

if __name__ == "__main__":
    initialize_tables()