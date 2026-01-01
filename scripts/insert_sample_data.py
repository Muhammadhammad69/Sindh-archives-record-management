#!/usr/bin/env python3
"""
Script to insert sample data into the actual NeonDB database.

This script will connect to the real database and insert sample commissioner and court records.
"""

import sys
import os

# Add the src directory to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Import the environment initialization first and initialize it
from src.config.environment import initialize_environment

print("Initializing environment...")
initialize_environment()

# Now we need to import the modules in a way that avoids the connection manager initialization issue
# Let's try to delay the import by using importlib after setting up environment
import importlib

# Import the DAOs using importlib to better control the import process
sys.modules.pop('src.database.connection', None)  # Remove from cache if present

# Set environment variables explicitly to ensure they're available
os.environ.setdefault('DATABASE_URL', 'postgresql://postgres:password@localhost:5432/sindh_archives')
os.environ.setdefault('COMMISSIONER_TABLE_NAME', 'commissioner_records')
os.environ.setdefault('COURT_TABLE_NAME', 'court_records')

# Now import the DAOs
from src.dao.commissioner_dao import CommissionerDAO
from src.dao.court_dao import CourtDAO

def main():
    print("Creating DAO instances...")
    commissioner_dao = CommissionerDAO()
    court_dao = CourtDAO()

    print("Inserting sample commissioner records...")

    # Sample commissioner records (fixing the page=0 issue by using page=1)
    commissioner_records = [
        {
            'acc_no': 1,
            'department': "REVENUE",
            'file_no': "5",
            'subject': "INCUMBERED STATE APPEALS.",
            'year': 1897,
            'page': 580,
            'condition': "FAIR/BOUND",
            'record_type': "TEXTUAL RECORD"
        },
        {
            'acc_no': 2,
            'department': "REVENUE",
            'file_no': "Vol - I",
            'subject': "OUTWARD REGISTER",
            'year': 1902,
            'page': 1,  # Changed from 0 to 1 to satisfy validation
            'condition': "FAIR/BOUND",
            'record_type': "TEXTUAL RECORD"
        }
    ]

    inserted_commissioner_records = []
    for i, record_data in enumerate(commissioner_records):
        try:
            print(f"  Inserting commissioner record {i+1}...")
            record = commissioner_dao.create(record_data)
            inserted_commissioner_records.append(record)
            print(f"    Successfully inserted record with ID: {record.id}")
        except Exception as e:
            print(f"    Error inserting commissioner record: {e}")

    print("Inserting sample court records...")

    # Sample court records
    court_records = [
        {
            'acc_no': 1,
            'court': "District Court of Karachi",
            'suit_no': "260 of 1893",
            'plaintiff': "Manghamnal Ramdas",
            'defendant': "Haji Ismail Gul Mohammad",
            'claim_or_charge': "Rs 750",
            'date_from': "1893-04-01",
            'date_to': "1894-07-03",
            'language': "English, Hindi"
        },
        {
            'acc_no': 2,
            'court': "District Court of Karachi",
            'suit_no': "248 of 1893",
            'plaintiff': "The Bombay Company Limited",
            'defendant': "Gagoo Shivji",
            'claim_or_charge': "RS. 1799",
            'date_from': "1893-06-12",
            'date_to': "1894-02-02",
            'language': "English, Sindhi and Hindi"
        }
    ]

    inserted_court_records = []
    for i, record_data in enumerate(court_records):
        try:
            print(f"  Inserting court record {i+1}...")
            record = court_dao.create(record_data)
            inserted_court_records.append(record)
            print(f"    Successfully inserted record with ID: {record.id}")
        except Exception as e:
            print(f"    Error inserting court record: {e}")

    print("\nInsertion Summary:")
    print(f"  Commissioner records inserted: {len(inserted_commissioner_records)}")
    print(f"  Court records inserted: {len(inserted_court_records)}")

    if inserted_commissioner_records:
        print("  Commissioner record IDs:", [r.id for r in inserted_commissioner_records])
    if inserted_court_records:
        print("  Court record IDs:", [r.id for r in inserted_court_records])

    print("\nSample data insertion completed successfully!")

if __name__ == "__main__":
    main()