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
from ....logger import logger

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
                logger.info("Attempting to connect to SQLite database with parameters:")
                for key, value in self.connection_params.items():
                    if key != 'password':  # Avoid printing sensitive info
                        logger.info(f"{key}: {value}")
                self.connection = await aiosqlite.connect(**self.connection_params)
                self.connected = True
                logger.info("SQLite connection established successfully.")
            return True
        except Exception as e:
            logger.error(f"Error connecting to database: {e}")
            return False
    
    async def disconnect(self) -> bool:
        """Close SQLite database connection asynchronously."""
        try:
            if self.connected and self.connection:
                await self.connection.close()
                self.connected = False
                logger.info("SQLite connection closed successfully.")
            return True
        except Exception as e:
            logger.error(f"Error disconnecting from database: {e}")
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
    
    async def get_all(
        self, 
        table: str, 
        query: Optional[Dict[str, Any]] = None, 
        page: Optional[int] = None, 
        page_size: Optional[int] = None,
        keep_connection_open: bool = False
    ) -> List[Dict[str, Any]]:
        """Get all records from SQLite database asynchronously with optional pagination."""
        try:
            if not self.connected:
                await self.connect()
            
            result = await get_all_records(
                self.connection, 
                table, 
                query=query, 
                page=page, 
                page_size=page_size
            )
            
            if not keep_connection_open:
                await self.disconnect()
            
            return result
        except Exception as e:
            logger.error(f"Error in get_all: {e}")
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
    
    async def update(self, table: str, *args, **kwargs) -> bool:
        """Update a record in SQLite database asynchronously.
        
        Four calling styles are supported:
        1. Separate query and data: 
           await db.update("table", {"id": 1}, {"name": "new_name"})
        2. Single dictionary with first key as condition:
           await db.update("table", {"id": 1, "name": "new_name"})
        3. Explicit query, data style:
           await db.update("table", query={"id": 1}, data={"name": "new_name"})
        4. Keyword arguments style:
           await db.update(table="table", query={"id": 1}, data={"name": "new_name"})
        """
        try:
            if not self.connected:
                await self.connect()
            
            # Handle keyword arguments
            if kwargs.get('table') and kwargs.get('query') and kwargs.get('data'):
                table = kwargs['table']
                query = kwargs['query']
                data = kwargs['data']
                result = await update_record(self.connection, table, query, data)
            
            # Handle two positional arguments
            elif len(args) == 2 and isinstance(args[0], dict) and isinstance(args[1], dict):
                query, data = args
                result = await update_record(self.connection, table, query, data)
            
            # Handle single dictionary style
            elif len(args) == 1 and isinstance(args[0], dict):
                # Single dictionary style
                data = args[0]
                if len(data) < 2:
                    raise ValueError("Update requires at least one condition column and one update column")
                
                # Use first key as query condition
                query_key = list(data.keys())[0]
                query_value = data[query_key]
                
                # Remove the query key from update data
                update_data = {k: v for k, v in data.items() if k != query_key}
                
                result = await update_record(
                    self.connection, 
                    table, 
                    {query_key: query_value}, 
                    update_data
                )
            
            # Handle keyword arguments query and data
            elif kwargs.get('query') and kwargs.get('data'):
                query = kwargs['query']
                data = kwargs['data']
                result = await update_record(self.connection, table, query, data)
            
            else:
                raise ValueError("Invalid arguments for update method")
            
            await self.disconnect()
            return result
        
        except Exception as e:
            logger.error(f"Error in update: {e}")
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
