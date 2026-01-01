#!/usr/bin/env python3
"""
Script to verify sample data in the NeonDB database.

This script will connect to the database and retrieve all commissioner and court records,
displaying them as pandas DataFrames with all columns.
"""

import sys
import os
import pandas as pd

# Add the src directory to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Import the environment initialization first and initialize it
from src.config.environment import initialize_environment

print("Initializing environment...")
initialize_environment()

# Import the DAOs after environment is initialized
from src.dao.commissioner_dao import CommissionerDAO
from src.dao.court_dao import CourtDAO

def main():
    print("Creating DAO instances...")
    commissioner_dao = CommissionerDAO()
    court_dao = CourtDAO()

    print("Retrieving all commissioner records...")
    try:
        # Get all commissioner records
        commissioner_records = commissioner_dao.get_all()
        print(f"  Retrieved {len(commissioner_records)} commissioner records")

        if commissioner_records:
            # Convert to DataFrame and display
            df_commissioner = pd.DataFrame(commissioner_records)
            print("  Commissioner Records DataFrame:")
            print(df_commissioner.to_string(index=False))
        else:
            print("  No commissioner records found")
    except Exception as e:
        print(f"  Error retrieving commissioner records: {e}")

    print("\nRetrieving all court records...")
    try:
        # Get all court records
        court_records = court_dao.get_all()
        print(f"  Retrieved {len(court_records)} court records")

        if court_records:
            # Convert to DataFrame and display
            df_court = pd.DataFrame(court_records)
            print("  Court Records DataFrame:")
            print(df_court.to_string(index=False))
        else:
            print("  No court records found")
    except Exception as e:
        print(f"  Error retrieving court records: {e}")

    print("\nVerification Summary:")
    print(f"  Total commissioner records: {len(commissioner_records) if 'commissioner_records' in locals() else 0}")
    print(f"  Total court records: {len(court_records) if 'court_records' in locals() else 0}")

    # Test specific filter queries
    print("\nTesting filter queries...")

    # Test commissioner records by year=1897
    try:
        records_1897 = commissioner_dao.get_all_by_year(1897)
        print(f"  Commissioner records from 1897: {len(records_1897)}")
    except Exception as e:
        print(f"  Error querying commissioner records by year: {e}")

    # Test court records by plaintiff name (if any records exist)
    if court_records:
        try:
            first_plaintiff = court_records[0].get('plaintiff') if court_records and isinstance(court_records[0], dict) else None
            if first_plaintiff:
                # Use find_by_criteria to search by plaintiff
                court_dao_instance = CourtDAO()
                records_by_plaintiff = court_dao_instance.find_by_criteria({'plaintiff': first_plaintiff})
                print(f"  Court records for plaintiff '{first_plaintiff}': {len(records_by_plaintiff)}")
        except Exception as e:
            print(f"  Error querying court records by plaintiff: {e}")

    print("\nSample data verification completed!")

if __name__ == "__main__":
    main()