"""Asynchronous MySQL driver implementation."""

import aiomysql
from typing import Any, Dict, Optional, Union, List

from ...base import AsyncDatabaseDriver
from ..utils import parse_connection_string
from .get import get_record
from .get_all import get_all_records
from .set import set_record
from .update import update_record
from .delete import delete_record
from .execute import execute_query
from .create_table import create_table
from .add import add_record
from .sub import sub_record
from ....logger import logger

class AsyncMySQLDriver(AsyncDatabaseDriver):
    """Asynchronous MySQL database driver."""
    
    def __init__(self, connection_string: str):
        """Initialize async MySQL driver."""
        self.connection_params = parse_connection_string(connection_string)
        self.connection = None
        self.connected = False
    
    async def connect(self) -> bool:
        """Establish connection to MySQL database asynchronously."""
        try:
            if not self.connected:
                self.connection = await aiomysql.connect(**self.connection_params)
                self.connected = True
                logger.info("Successfully connected to the MySQL database.")
            return True
        except Exception as e:
            logger.error(f"Error connecting to the MySQL database: {e}")
            return False
    
    async def disconnect(self) -> bool:
        """Close MySQL database connection asynchronously."""
        try:
            if self.connected and self.connection:
                self.connection.close()
                self.connected = False
                logger.info("Successfully disconnected from the MySQL database.")
            return True
        except Exception as e:
            logger.error(f"Error disconnecting from the MySQL database: {e}")
            return False
    
    async def get(self, table: str, query: Dict[str, Any], 
                keep_connection_open: bool = False) -> Optional[Dict[str, Any]]:
        """Get a record from MySQL database asynchronously."""
        try:
            if not self.connected:
                await self.connect()
            
            result = await get_record(self.connection, table, query)
            
            if not keep_connection_open:
                await self.disconnect()
            
            return result
        except Exception:
            if not keep_connection_open:
                await self.disconnect()
            return None
    
    async def get_all(self, table: str, query: Optional[Dict[str, Any]] = None, 
                   keep_connection_open: bool = False) -> List[Dict[str, Any]]:
        """Get all records from MySQL database asynchronously."""
        try:
            if not self.connected:
                await self.connect()
            
            result = await get_all_records(self.connection, table, query)
            
            if not keep_connection_open:
                await self.disconnect()
            
            return result
        except Exception:
            if not keep_connection_open:
                await self.disconnect()
            return []
    
    async def set(self, table: str, data: Dict[str, Any], 
                keep_connection_open: bool = False) -> bool:
        """Insert a record into MySQL database asynchronously."""
        try:
            if not self.connected:
                await self.connect()
            
            result = await set_record(self.connection, table, data)
            
            if not keep_connection_open:
                await self.disconnect()
            
            return result
        except Exception:
            if not keep_connection_open:
                await self.disconnect()
            return False
    
    async def update(self, table: str, query: Dict[str, Any], data: Dict[str, Any], 
                      keep_connection_open: bool = False) -> bool:
        """Update a record in MySQL database asynchronously."""
        try:
            if not self.connected:
                await self.connect()
            
            result = await update_record(self.connection, table, query, data)
            
            if not keep_connection_open:
                await self.disconnect()
            
            return result
        except Exception:
            if not keep_connection_open:
                await self.disconnect()
            return False
    
    async def delete(self, table: str, query: Dict[str, Any], 
                      keep_connection_open: bool = False) -> bool:
        """Delete a record from MySQL database asynchronously."""
        try:
            if not self.connected:
                await self.connect()
            
            result = await delete_record(self.connection, table, query)
            
            if not keep_connection_open:
                await self.disconnect()
            
            return result
        except Exception:
            if not keep_connection_open:
                await self.disconnect()
            return False
    
    async def execute(self, query: str, 
                    params: Optional[Union[tuple, Dict[str, Any]]] = None, 
                    keep_connection_open: bool = False) -> Any:
        """Execute a raw SQL query asynchronously."""
        try:
            if not self.connected:
                await self.connect()
            
            result = await execute_query(self.connection, query, params)
            
            if not keep_connection_open:
                await self.disconnect()
            
            return result
        except Exception:
            if not keep_connection_open:
                await self.disconnect()
            return None

    async def create_table(self, table: str, schema: Dict[str, str], 
                           primary_key: str = 'id', 
                           auto_increment: bool = True,
                           if_not_exists: bool = True,
                           keep_connection_open: bool = False) -> bool:
        """Create a table in MySQL database asynchronously."""
        try:
            if not self.connected:
                await self.connect()
            
            result = await create_table(self.connection, table, schema, 
                                        primary_key, auto_increment, if_not_exists)
            
            if not keep_connection_open:
                await self.disconnect()
            
            return result
        except Exception:
            if not keep_connection_open:
                await self.disconnect()
            return False

    async def add(self, table: str, query: Dict[str, Any], value: Union[int, float], 
                column: str = 'value', keep_connection_open: bool = False) -> bool:
        """
        Add a specified value to an existing numeric column in the database.
        
        :param table: Name of the table
        :param query: Dictionary specifying which record(s) to update
        :param value: Numeric value to add to the existing value
        :param column: Name of the column to update (default: 'value')
        :param keep_connection_open: Whether to keep the connection open after operation
        :return: True if update was successful, False otherwise
        """
        try:
            if not self.connected:
                await self.connect()
            
            result = await add_record(self.connection, table, query, value, column)
            
            if not keep_connection_open:
                await self.disconnect()
            
            return result
        except Exception as e:
            logger.error(f"Error in add method: {e}")
            if not keep_connection_open:
                await self.disconnect()
            return False

    async def sub(self, table: str, query: Dict[str, Any], value: Union[int, float], 
                column: str = 'value', keep_connection_open: bool = False) -> bool:
        """
        Subtract a specified value from an existing numeric column in the database.
        
        :param table: Name of the table
        :param query: Dictionary specifying which record(s) to update
        :param value: Numeric value to subtract from the existing value
        :param column: Name of the column to update (default: 'value')
        :param keep_connection_open: Whether to keep the connection open after operation
        :return: True if update was successful, False otherwise
        """
        try:
            if not self.connected:
                await self.connect()
            
            result = await sub_record(self.connection, table, query, value, column)
            
            if not keep_connection_open:
                await self.disconnect()
            
            return result
        except Exception as e:
            logger.error(f"Error in sub method: {e}")
            if not keep_connection_open:
                await self.disconnect()
            return False
