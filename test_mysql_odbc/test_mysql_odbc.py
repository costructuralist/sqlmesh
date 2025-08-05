#!/usr/bin/env python
"""Test MySQL ODBC functionality"""

import pyodbc
from sqlmesh.core.config.connection import MySQLConnectionConfig
from sqlmesh import Context

def list_mysql_drivers():
    """List available MySQL ODBC drivers"""
    print("Available MySQL ODBC Drivers:")
    drivers = [x for x in pyodbc.drivers() if 'MySQL' in x]
    for driver in drivers:
        print(f"  - {driver}")
    return drivers[0] if drivers else None

def test_connection_config():
    """Test MySQL connection configurations"""
    print("\n=== Testing Connection Configurations ===")
    
    # Test pymysql (default)
    config_pymysql = MySQLConnectionConfig(
        host="localhost",
        user="root",
        password="your_password",
        database="test",
    )
    print(f"PyMySQL driver: {config_pymysql.driver}")
    
    # Test pyodbc
    driver_name = list_mysql_drivers()
    if not driver_name:
        print("ERROR: No MySQL ODBC drivers found!")
        return
        
    config_pyodbc = MySQLConnectionConfig(
        host="localhost",
        user="root",
        password="your_password",
        database="test",
        driver="pyodbc",
        driver_name=driver_name,
    )
    print(f"PyODBC driver: {config_pyodbc.driver}")
    print(f"ODBC Driver Name: {config_pyodbc.driver_name}")

def test_sqlmesh_context():
    """Test SQLMesh context with both drivers"""
    print("\n=== Testing SQLMesh Context ===")
    
    driver_name = list_mysql_drivers()
    if not driver_name:
        return
    
    # Test configurations
    configs = {
        "pymysql": {
            "type": "mysql",
            "host": "localhost",
            "user": "root",
            "password": "your_password",
            "database": "test",
        },
        "pyodbc": {
            "type": "mysql",
            "host": "localhost", 
            "user": "root",
            "password": "your_password",
            "database": "test",
            "driver": "pyodbc",
            "driver_name": driver_name,
        }
    }
    
    for name, config in configs.items():
        print(f"\nTesting with {name}:")
        try:
            context = Context(config={"gateways": {"default": {"connection": config}}})
            
            # Test ping
            context._engine_adapter.ping()
            print("  ✓ Ping successful")
            
            # Test query
            df = context.fetchdf("SELECT VERSION() as version, DATABASE() as db")
            print(f"  ✓ Query successful: MySQL {df['version'][0]}")
            
        except Exception as e:
            print(f"  ✗ Error: {e}")

def test_raw_pyodbc():
    """Test raw pyodbc connection"""
    print("\n=== Testing Raw PyODBC Connection ===")
    
    driver_name = list_mysql_drivers()
    if not driver_name:
        return
        
    conn_str = f"DRIVER={{{driver_name}}};SERVER=localhost;DATABASE=test;UID=root;PWD=your_password"
    
    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()[0]
        print(f"✓ Raw PyODBC connection successful: MySQL {version}")
        conn.close()
    except Exception as e:
        print(f"✗ Raw PyODBC connection failed: {e}")

if __name__ == "__main__":
    # Update these with your MySQL credentials
    print("MySQL ODBC Testing Script")
    print("=" * 50)
    
    test_raw_pyodbc()
    test_connection_config()
    test_sqlmesh_context()