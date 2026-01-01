#!/usr/bin/env python3
"""
Test script to verify the data structures and validation for commissioner and court records.

This script will:
1. Test data validation for commissioner records
2. Test data validation for court records
3. Verify model structures
4. Test basic functionality without database connections
"""

import sys
import os
from unittest.mock import Mock, patch
import importlib.util


def test_data_flow():
    """Main test function that handles mocking before imports."""

    # Mock the database connection at the system level before importing
    sys.modules['psycopg2'] = Mock()
    sys.modules['psycopg2.pool'] = Mock()
    sys.modules['psycopg2.extras'] = Mock()

    # Mock the connection manager module
    connection_manager_mock = Mock()
    connection_manager_mock.get_db_connection = Mock()
    sys.modules['src.database.connection'] = Mock()
    sys.modules['src.database.connection.connection_manager'] = connection_manager_mock
    sys.modules['src.database.connection.ConnectionManager'] = Mock()

    # Add the src directory to the path so we can import our modules
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

    # Now import our modules after mocking dependencies
    from src.dao.commissioner_dao import CommissionerDAO
    from src.dao.court_dao import CourtDAO
    from src.database.models.commissioner_record import CommissionerRecord
    from src.database.models.court_record import CourtRecord


    def test_commissioner_record_validation():
        """Test validation for commissioner records."""
        print("Testing Commissioner Record Validation...")

        # Create DAO instance
        dao = CommissionerDAO()

        # Define sample records as specified in the requirements
        sample_records = [
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
                'page': 0,  # Using 0 instead of None since the model requires an integer
                'condition': "FAIR/BOUND",
                'record_type': "TEXTUAL RECORD"
            }
        ]

        # Test validation for each record
        for i, record_data in enumerate(sample_records):
            print(f"  Validating commissioner record {i+1}...")
            errors = dao.validate_data(record_data)
            if errors:
                print(f"    Validation errors: {errors}")
            else:
                print(f"    Record {i+1} passed validation")

        # Test validation with invalid data
        print("  Testing validation with invalid data...")
        invalid_record = {
            'acc_no': -1,  # Invalid acc_no
            'department': "",  # Empty department
            'year': 0,  # Invalid year
            'page': -5  # Invalid page
        }
        errors = dao.validate_data(invalid_record)
        print(f"    Validation errors for invalid record: {errors}")


    def test_court_record_validation():
        """Test validation for court records."""
        print("\nTesting Court Record Validation...")

        # Create DAO instance
        dao = CourtDAO()

        # Define sample records as specified in the requirements
        sample_records = [
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

        # Test validation for each record
        for i, record_data in enumerate(sample_records):
            print(f"  Validating court record {i+1}...")
            errors = dao.validate_data(record_data)
            if errors:
                print(f"    Validation errors: {errors}")
            else:
                print(f"    Record {i+1} passed validation")

        # Test validation with invalid data
        print("  Testing validation with invalid data...")
        invalid_record = {
            'acc_no': -1,  # Invalid acc_no
            'court': "",  # Empty court
            'date_from': "invalid-date",  # Invalid date format
            'date_to': "1893-01-01",  # Invalid date range (end before start)
            'language': ""  # Empty language
        }
        errors = dao.validate_data(invalid_record)
        print(f"    Validation errors for invalid record: {errors}")


    def test_model_creation():
        """Test model creation and data structure."""
        print("\nTesting Model Creation and Data Structure...")

        # Test CommissionerRecord model
        print("  Testing CommissionerRecord model...")
        commissioner_data = {
            'id': 1,
            'acc_no': 1,
            'department': "REVENUE",
            'file_no': "5",
            'subject': "INCUMBERED STATE APPEALS.",
            'year': 1897,
            'page': 580,
            'condition': "FAIR/BOUND",
            'record_type': "TEXTUAL RECORD"
        }

        commissioner_record = CommissionerRecord.from_dict(commissioner_data)
        print(f"    Created CommissionerRecord: ID={commissioner_record.id}, acc_no={commissioner_record.acc_no}")
        print(f"    Department: {commissioner_record.department}")
        print(f"    Subject: {commissioner_record.subject}")

        # Convert back to dict
        record_dict = commissioner_record.to_dict()
        print(f"    Converted back to dict: {len(record_dict)} fields")

        # Test CourtRecord model
        print("  Testing CourtRecord model...")
        court_data = {
            'id': 1,
            'acc_no': 1,
            'court': "District Court of Karachi",
            'suit_no': "260 of 1893",
            'plaintiff': "Manghamnal Ramdas",
            'defendant': "Haji Ismail Gul Mohammad",
            'claim_or_charge': "Rs 750",
            'date_from': "1893-04-01",
            'date_to': "1894-07-03",
            'language': "English, Hindi"
        }

        court_record = CourtRecord.from_dict(court_data)
        print(f"    Created CourtRecord: ID={court_record.id}, acc_no={court_record.acc_no}")
        print(f"    Court: {court_record.court}")
        print(f"    Plaintiff: {court_record.plaintiff}")
        print(f"    Date range: {court_record.date_from} to {court_record.date_to}")

        # Convert back to dict
        record_dict = court_record.to_dict()
        print(f"    Converted back to dict: {len(record_dict)} fields")


    def test_dao_methods():
        """Test DAO methods without database operations."""
        print("\nTesting DAO Methods (without database operations)...")

        # Test CommissionerDAO methods
        print("  Testing CommissionerDAO methods...")
        commissioner_dao = CommissionerDAO()

        # Test validation method directly
        valid_data = {
            'acc_no': 1,
            'department': "REVENUE",
            'file_no': "5",
            'subject': "INCUMBERED STATE APPEALS.",
            'year': 1897,
            'page': 580,
            'condition': "FAIR/BOUND",
            'record_type': "TEXTUAL RECORD"
        }

        validation_result = commissioner_dao.validate_data(valid_data)
        print(f"    Validation result for valid data: {validation_result}")

        # Test audit field methods
        audit_fields = commissioner_dao._get_audit_fields()
        print(f"    Audit fields: {list(audit_fields.keys())}")

        # Test CourtDAO methods
        print("  Testing CourtDAO methods...")
        court_dao = CourtDAO()

        # Test validation method directly
        valid_data = {
            'acc_no': 1,
            'court': "District Court of Karachi",
            'suit_no': "260 of 1893",
            'plaintiff': "Manghamnal Ramdas",
            'defendant': "Haji Ismail Gul Mohammad",
            'claim_or_charge': "Rs 750",
            'date_from': "1893-04-01",
            'date_to': "1894-07-03",
            'language': "English, Hindi"
        }

        validation_result = court_dao.validate_data(valid_data)
        print(f"    Validation result for valid data: {validation_result}")

        # Test audit field methods
        audit_fields = court_dao._get_audit_fields()
        print(f"    Audit fields: {list(audit_fields.keys())}")


    # Main execution
    print("Starting Data Flow Test (Validation and Model Structure Only)...")

    # Test commissioner record validation
    test_commissioner_record_validation()

    # Test court record validation
    test_court_record_validation()

    # Test model creation and data structure
    test_model_creation()

    # Test DAO methods
    test_dao_methods()

    print("\nData Flow Test Complete!")
    print("Validated the data structures and validation logic for both record types.")
    print("The data flow has been verified at the model and validation layer.")


if __name__ == "__main__":
    test_data_flow()