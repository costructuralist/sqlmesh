"""
SQLMesh configuration for MySQL ODBC to Postgres test project.

This project demonstrates:
- Using MySQL ODBC as an external data source
- Postgres as the main data warehouse
- Multi-gateway configuration for cross-database operations
"""

from sqlmesh.core.config import Config, GatewayConfig
from sqlmesh.core.config.connection import MySQLConnectionConfig, PostgresConnectionConfig

# Get MySQL ODBC driver name dynamically
import pyodbc
mysql_drivers = [x for x in pyodbc.drivers() if 'MySQL' in x]
mysql_driver = mysql_drivers[-1] if mysql_drivers else "MySQL ODBC 9.3 Unicode Driver"

config = Config(
    # Default gateway uses Postgres for main data warehouse
    default_gateway="mysql_target",
    
    gateways={
        # MySQL ODBC gateway for external data source
        "mysql_source": GatewayConfig(
            connection=MySQLConnectionConfig(
                host="sii-server",
                user="ewuys", 
                password="your_password",
                database="sunshine",
                driver="pyodbc",
                driver_name=mysql_driver,
            ),
        ),
        
        # MySQL ODBC gateway for target
        "mysql_target": GatewayConfig(
            connection=MySQLConnectionConfig(
                host="sii-server",
                user="ewuys", 
                password="your_password",
                database="sqlmesh",
                driver="pyodbc",
                driver_name=mysql_driver,
            ),
        ),
    },
    
    # Environment configuration
    environment_ttl="in 7 days",
    snapshot_ttl="in 30 days",
    
    # Model defaults
    model_defaults={
        "dialect": "mysql",
    },
)
