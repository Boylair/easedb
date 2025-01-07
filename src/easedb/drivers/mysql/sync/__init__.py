"""Synchronous MySQL driver implementation."""

import mysql.connector
from typing import Any, Dict, Optional, Union, List
import traceback

from ...base import DatabaseDriver
from ..utils import parse_connection_string
from .get import get_record
from .get_all import get_all_records
from .set import set_record
from .update import update_record
from .delete import delete_record
from .execute import execute_query
from .create_table import create_table
from ....logger import logger

class MySQLDriver(DatabaseDriver):
    """Synchronous MySQL database driver."""
    
    def __init__(self, connection_string: str):
        """Initialize MySQL driver."""
        self.connection_string = connection_string
        self.connection_params = parse_connection_string(connection_string)
        
        # Add additional connection parameters with more verbose error handling
        self.connection_params.update({
            'raise_on_warnings': True,
            'buffered': True,
            'autocommit': False,
            'connect_timeout': 10,
            'use_pure': True,  # Force pure Python implementation for better error reporting
            'ssl_disabled': True  # Disable SSL to simplify connection
        })
        
        self.connection = None
        self.connected = False
        
        # Attempt to establish connection during initialization
        try:
            self.connect()
        except Exception as e:
            print(f"Failed to establish initial connection: {e}")
            print(f"Connection parameters: {self.connection_params}")
            print(traceback.format_exc())
    
    def connect(self) -> bool:
        """Establish connection to MySQL database."""
        try:
            if not self.connected:

                # Attempt to establish connection with detailed error tracking
                logger.info("Attempting to connect with parameters:")
                for key, value in self.connection_params.items():
                    if key not in ['password']:  # Avoid printing sensitive info
                        logger.info(f"{key}: {value}")
                
                self.connection = mysql.connector.connect(**self.connection_params)
                
                # Verify connection
                if not self.connection.is_connected():
                    logger.error("Connection failed: not connected")
                    return False
                
                self.connected = True
                logger.info("Connection established successfully")
            return True
        
        except mysql.connector.Error as err:
            logger.error(f"MySQL Connector Error: {err}")
            return False
        
        except Exception as e:
            logger.error(f"Unexpected connection error: {e}")
            return False
    
    def disconnect(self) -> bool:
        """Close MySQL database connection."""
        try:
            if self.connected and self.connection:
                self.connection.close()
                self.connected = False
                logger.info("Connection closed successfully.")
            return True
        except Exception as e:
            logger.error(f"Error disconnecting from the MySQL database: {e}")
            return False
    
    def get(self, table: str, query: Dict[str, Any], 
                keep_connection_open: bool = False) -> Optional[Dict[str, Any]]:
        """Get a record from MySQL database."""
        try:
            if not self.connected:
                self.connect()
            
            result = get_record(self.connection, table, query)
            
            if not keep_connection_open:
                self.disconnect()
            
            return result
        except Exception:
            if not keep_connection_open:
                self.disconnect()
            return None
    
    def get_all(self, table: str, query: Optional[Dict[str, Any]] = None, 
                   keep_connection_open: bool = False) -> List[Dict[str, Any]]:
        """Get all records from MySQL database."""
        try:
            if not self.connected:
                self.connect()
            
            result = get_all_records(self.connection, table, query)
            
            if not keep_connection_open:
                self.disconnect()
            
            return result
        except Exception:
            if not keep_connection_open:
                self.disconnect()
            return []
    
    def set(self, table: str, data: Dict[str, Any], 
                keep_connection_open: bool = False) -> bool:
        """Insert a record into MySQL database."""
        try:
            if not self.connected:
                self.connect()
            
            result = set_record(self.connection, table, data)
            
            if not keep_connection_open:
                self.disconnect()
            
            return result
        except Exception:
            if not keep_connection_open:
                self.disconnect()
            return False
    
    def update(self, table: str, query: Dict[str, Any], data: Dict[str, Any], 
                  keep_connection_open: bool = False) -> bool:
        """Update a record in MySQL database."""
        try:
            if not self.connected:
                self.connect()
            
            result = update_record(self.connection, table, query, data)
            
            if not keep_connection_open:
                self.disconnect()
            
            return result
        except Exception:
            if not keep_connection_open:
                self.disconnect()
            return False
    
    def delete(self, table: str, query: Dict[str, Any], 
                  keep_connection_open: bool = False) -> bool:
        """Delete a record from MySQL database."""
        try:
            if not self.connected:
                self.connect()
            
            result = delete_record(self.connection, table, query)
            
            if not keep_connection_open:
                self.disconnect()
            
            return result
        except Exception:
            if not keep_connection_open:
                self.disconnect()
            return False
    
    def execute(self, query: str, 
                    params: Optional[Union[tuple, Dict[str, Any]]] = None, 
                    keep_connection_open: bool = False) -> Any:
        """Execute a raw SQL query."""
        try:
            if not self.connected:
                self.connect()
            
            result = execute_query(self.connection, query, params)
            
            if not keep_connection_open:
                self.disconnect()
            
            return result
        except Exception:
            if not keep_connection_open:
                self.disconnect()
            return None

    def create_table(self, table: str, schema: Dict[str, str], 
                     primary_key: str = 'id', 
                     auto_increment: bool = True,
                     if_not_exists: bool = True,
                     keep_connection_open: bool = False) -> bool:
        """Create a table in MySQL database."""
        try:
            if not self.connected:
                self.connect()
            
            result = create_table(self.connection, table, schema, 
                                  primary_key, auto_increment, if_not_exists)
            
            if not keep_connection_open:
                self.disconnect()
            
            return result
        except Exception:
            if not keep_connection_open:
                self.disconnect()
            return False
