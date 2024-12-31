"""Asynchronous SQLite driver implementation."""

import aiosqlite
from typing import Any, Dict, Optional, Union, List

from ...base import AsyncDatabaseDriver
from ..utils import parse_connection_string
from .get import get_record
from .get_all import get_all_records
from .set import set_record
from .update import update_record
from .delete import delete_record
from .execute import execute_query
from .count import count_records
from .create_table import create_table

class AsyncSQLiteDriver(AsyncDatabaseDriver):
    """Asynchronous SQLite database driver."""
    
    def __init__(self, connection_string: str):
        """Initialize async SQLite driver."""
        self.connection_params = parse_connection_string(connection_string)
        self.connection = None
        self.connected = False
    
    async def connect(self) -> bool:
        """Establish connection to SQLite database asynchronously."""
        try:
            if not self.connected:
                self.connection = await aiosqlite.connect(**self.connection_params)
                self.connected = True
            return True
        except Exception as e:
            print(f"Error connecting to database: {e}")
            return False
    
    async def disconnect(self) -> bool:
        """Close SQLite database connection asynchronously."""
        try:
            if self.connected and self.connection:
                await self.connection.close()
                self.connected = False
            return True
        except Exception as e:
            print(f"Error disconnecting from database: {e}")
            return False
    
    async def get(self, table: str, query: Dict[str, Any], 
                keep_connection_open: bool = False) -> Optional[Dict[str, Any]]:
        """Get a record from SQLite database asynchronously."""
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
        """Get all records from SQLite database asynchronously."""
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
        """Insert a record into SQLite database asynchronously."""
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
        """Update a record in SQLite database asynchronously."""
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
        """Delete a record from SQLite database asynchronously."""
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
    
    async def count(self, table: str, query: Optional[Dict[str, Any]] = None) -> int:
        """Count records in SQLite database asynchronously."""
        if not self.connected:
            await self.connect()
        return await count_records(self.connection, table, query)

    async def create_table(self, table: str, schema: Dict[str, str], 
                           primary_key: str = 'id', 
                           auto_increment: bool = True,
                           if_not_exists: bool = True,
                           keep_connection_open: bool = False) -> bool:
        """Create a table in SQLite database asynchronously."""
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
