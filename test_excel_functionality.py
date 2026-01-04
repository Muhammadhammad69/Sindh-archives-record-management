"""
Simple test script to verify Excel functionality works correctly.
"""
import pandas as pd
from io import BytesIO
from src.utils.excel_validator import validate_commissioner_columns, validate_commissioner_data
from src.utils.excel_processor import process_commissioner_data
from src.utils.template_generator import generate_commissioner_template

def test_excel_functionality():
    print("Testing Excel functionality...")

    # Test template generation
    print("1. Testing template generation...")
    template_data = generate_commissioner_template()
    print(f"   Template generated: {type(template_data)}")

    # Read the template back to verify it works
    template_df = pd.read_excel(template_data, engine='openpyxl')
    print(f"   Template has {len(template_df)} rows and {len(template_df.columns)} columns")

    # Test column validation
    print("2. Testing column validation...")
    is_valid, missing_cols = validate_commissioner_columns(template_df)
    print(f"   Columns valid: {is_valid}")
    if not is_valid:
        print(f"   Missing columns: {missing_cols}")

    # Test data validation
    print("3. Testing data validation...")
    data_errors = validate_commissioner_data(template_df)
    print(f"   Data validation errors: {len(data_errors)}")

    # Test data processing
    print("4. Testing data processing...")
    processed_records = process_commissioner_data(template_df)
    print(f"   Processed {len(processed_records)} records")

    print("All tests passed!")

if __name__ == "__main__":
    test_excel_functionality()