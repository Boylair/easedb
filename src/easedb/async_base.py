from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union

class AsyncDatabaseDriver(ABC):
    """Base class for all async database drivers."""
    
    @abstractmethod
    async def connect(self) -> None:
        """Establish connection to the database."""
        pass
    
    @abstractmethod
    async def disconnect(self) -> None:
        """Close the database connection."""
        pass
    
    @abstractmethod
    async def get(self, table: str, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Retrieve a single record from the database."""
        pass
    
    @abstractmethod
    async def get_all(self, table: str, query: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Retrieve multiple records from the database."""
        pass
    
    @abstractmethod
    async def set(self, table: str, data: Dict[str, Any]) -> bool:
        """Insert or update a record in the database."""
        pass
    
    @abstractmethod
    async def update(self, table: str, query: Dict[str, Any], data: Dict[str, Any]) -> bool:
        """Update records in the database that match the query."""
        pass
    
    @abstractmethod
    async def delete(self, table: str, query: Dict[str, Any]) -> bool:
        """Delete a record from the database."""
        pass
    
    @abstractmethod
    async def execute(self, query: str, params: Optional[Union[tuple, Dict[str, Any]]] = None) -> Any:
        """Execute a raw SQL query."""
        pass

class AsyncDatabase:
    """Main database interface for asynchronous operations."""
    
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.driver = self._init_driver()
    
    def _init_driver(self) -> AsyncDatabaseDriver:
        """Initialize the appropriate async database driver based on the connection string."""
        if self.connection_string.startswith('sqlite'):
            from .drivers.sqlite import AsyncSQLiteDriver
            return AsyncSQLiteDriver(self.connection_string)
        elif self.connection_string.startswith(('mysql', 'mariadb')):
            from .drivers.mysql import AsyncMySQLDriver
            return AsyncMySQLDriver(self.connection_string)
        else:
            raise ValueError(f"Unsupported database type in connection string: {self.connection_string}")
    
    async def connect(self) -> None:
        """Explicit async connection method"""
        await self.driver.connect()
    
    async def disconnect(self) -> None:
        """Explicit async disconnection method"""
        await self.driver.disconnect()
    
    async def __aenter__(self):
        await self.connect()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        try:
            await self.disconnect()
        except Exception as e:
            print(f"Error during async connection cleanup: {e}")
            if exc_type is None:
                raise  # Only re-raise if there wasn't already an exception
    
    async def get(self, table: str, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        return await self.driver.get(table, query)
    
    async def get_all(self, table: str, query: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        return await self.driver.get_all(table, query)
    
    async def set(self, table: str, data: Dict[str, Any]) -> bool:
        return await self.driver.set(table, data)
    
    async def update(self, table: str, query: Dict[str, Any], data: Dict[str, Any]) -> bool:
        return await self.driver.update(table, query, data)
    
    async def delete(self, table: str, query: Dict[str, Any]) -> bool:
        return await self.driver.delete(table, query)
    
    async def execute(self, query: str, params: Optional[Union[tuple, Dict[str, Any]]] = None) -> Any:
        """Execute a raw SQL query asynchronously."""
        return await self.driver.execute(query, params)

    async def create_table(self, table_name: str, columns: Dict[str, str]) -> bool:
        """
        Create a table with specified columns asynchronously.
        
        :param table_name: Name of the table to create
        :param columns: Dictionary of column names and their types
        :return: True if table creation was successful, False otherwise
        """
        column_definitions = [f"{col_name} {col_type}" for col_name, col_type in columns.items()]
        create_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(column_definitions)})"
        return await self.execute(create_query)
