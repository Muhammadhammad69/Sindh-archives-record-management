#!/usr/bin/env python3
"""
Basic test to verify project setup and dependencies can be imported.
"""

def test_basic_imports():
    """Test that basic dependencies can be imported."""
    try:
        import psycopg2
        print("✓ psycopg2 imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import psycopg2: {e}")
        return False

    try:
        import pandas
        print("✓ pandas imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import pandas: {e}")
        return False

    try:
        import bcrypt
        print("✓ bcrypt imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import bcrypt: {e}")
        return False

    try:
        from dotenv import load_dotenv
        print("✓ python-dotenv imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import python-dotenv: {e}")
        return False

    print("\nAll basic imports successful!")
    return True

if __name__ == "__main__":
    success = test_basic_imports()
    if not success:
        exit(1)