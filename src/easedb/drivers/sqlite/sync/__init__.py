"""Synchronous SQLite driver implementation."""

import sqlite3
from typing import Any, Dict, Optional, Union, List

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

class SQLiteDriver(DatabaseDriver):
    """Synchronous SQLite database driver."""
    
    def __init__(self, connection_string: str):
        """Initialize SQLite driver."""
        self.connection_params = parse_connection_string(connection_string)
        self.connection = None
        self.connected = False
    
    def connect(self) -> bool:
        """Establish connection to SQLite database."""
        try:
            if not self.connected:
                logger.info("Attempting to connect to SQLite database with parameters:")
                for key, value in self.connection_params.items():
                    if key != 'password':  # Avoid printing sensitive info
                        logger.info(f"{key}: {value}")
                self.connection = sqlite3.connect(**self.connection_params)
                self.connected = True
                logger.info("SQLite connection established successfully.")
            return True
        except Exception as e:
            logger.error(f"Error connecting to database: {e}")
            return False
    
    def disconnect(self) -> bool:
        """Close SQLite database connection."""
        try:
            if self.connected and self.connection:
                self.connection.close()
                self.connected = False
                logger.info("SQLite connection closed successfully.")
            return True
        except Exception as e:
            logger.error(f"Error disconnecting from database: {e}")
            return False
    
    def get(self, table: str, query: Dict[str, Any], 
                keep_connection_open: bool = False) -> Optional[Dict[str, Any]]:
        """Get a record from SQLite database."""
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
        """Get all records from SQLite database."""
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
        """Insert a record into SQLite database."""
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
        """Update a record in SQLite database."""
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
        """Delete a record from SQLite database."""
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
        """Create a table in SQLite database."""
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
