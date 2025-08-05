import sys
import pyodbc

print("Python:", sys.version)
print("\nMySQL ODBC Drivers:")
for driver in pyodbc.drivers():
    if 'MySQL' in driver:
        print(f"  - '{driver}'")

# Test connection string formats
test_strings = [
    "DRIVER={MySQL ODBC 8.0 Unicode Driver};SERVER=localhost;PORT=3306;DATABASE=test;UID=root;PWD=password",
    "DRIVER={MySQL ODBC 8.0 ANSI Driver};SERVER=localhost;PORT=3306;DATABASE=test;UID=root;PWD=password",
]

for conn_str in test_strings:
    print(f"\nTesting: {conn_str.split(';')[0]}")
    try:
        conn = pyodbc.connect(conn_str.replace("password", "your_actual_password"))
        print("  ✓ Connection successful")
        conn.close()
    except Exception as e:
        print(f"  ✗ Failed: {e}")