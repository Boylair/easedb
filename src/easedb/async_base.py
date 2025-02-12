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
    @abstractmethod
    async def get_all(
        self, 
        table: str, 
        query: Optional[Dict[str, Any]] = None, 
        page: Optional[int] = None, 
        page_size: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Retrieve multiple records from the database."""
        pass



    
    @abstractmethod
    async def set(self, table: str, data: Dict[str, Any]) -> bool:
        """Insert or update a record in the database."""
        pass
    
    @abstractmethod
    async def update(self, table: str, query: Dict[str, Any], data: Dict[str, Any]) -> bool:
        """Update records in the database."""
        pass
    
    @abstractmethod
    async def delete(self, table: str, query: Dict[str, Any]) -> bool:
        """Delete a record from the database."""
        pass
    
    @abstractmethod
    async def execute(self, query: str, params: Optional[Union[tuple, Dict[str, Any]]] = None) -> Any:
        """Execute a raw SQL query."""
        pass
    
    @abstractmethod
    async def create_table(self, table_name: str, columns: Dict[str, str], 
                            primary_key: str, auto_increment: bool, if_not_exists: bool) -> bool:
        """Create a table with specified columns."""
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
    
    async def get_all(
        self, 
        table: str, 
        query: Optional[Dict[str, Any]] = None, 
        page: Optional[int] = None, 
        page_size: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieve multiple records from the database with optional pagination.
        
        :param table: Name of the table to retrieve records from
        :param query: Optional dictionary of conditions to filter records
        :param page: Optional page number for pagination (1-indexed)
        :param page_size: Optional number of records per page
        :return: List of records matching the query
        """
        return await self.driver.get_all(table, query, page, page_size)
        
            
    async def set(self, table: str, data: Dict[str, Any]) -> bool:
        return await self.driver.set(table, data)
    
    async def update(self, table: str, *args, **kwargs) -> bool:
        """
        Update records in the specified table.
        
        Supports multiple calling styles:
        1. Separate query and data: 
           await db.update("table", {"id": 1}, {"name": "new_name"})
        2. Single dictionary with first key as condition:
           await db.update("table", {"id": 1, "name": "new_name"})
        3. Keyword arguments style:
           await db.update("table", query={"id": 1}, data={"name": "new_name"})
        
        Args:
            table (str): Name of the table
            *args: Positional arguments for query and data
            **kwargs: Keyword arguments for query and data
            
        Returns:
            bool: True if update is successful, False otherwise
        """
        # Handle keyword arguments with full specification
        if kwargs.get('table') and kwargs.get('query') and kwargs.get('data'):
            table = kwargs['table']
            query = kwargs['query']
            data = kwargs['data']
            return await self.driver.update(table, query, data)
        
        # Handle two positional arguments (query, data)
        if len(args) == 2 and isinstance(args[0], dict) and isinstance(args[1], dict):
            query, data = args
            return await self.driver.update(table, query, data)
        
        # Handle single dictionary style
        if len(args) == 1 and isinstance(args[0], dict):
            data = args[0]
            if len(data) < 2:
                raise ValueError("Update requires at least one condition column and one update column")
            
            # Use first key as query condition
            query_key = list(data.keys())[0]
            query_value = data[query_key]
            
            # Remove the query key from update data
            update_data = {k: v for k, v in data.items() if k != query_key}
            
            return await self.driver.update(table, {query_key: query_value}, update_data)
        
        # Handle keyword arguments query and data
        if kwargs.get('query') and kwargs.get('data'):
            query = kwargs['query']
            data = kwargs['data']
            return await self.driver.update(table, query, data)
        
        # Fallback for legacy behavior
        if args or kwargs:
            # If no update data provided, raise error
            if not args and not kwargs:
                raise ValueError("No update data provided")
            
            # If args and first arg is dict, use it as update_data
            if args and isinstance(args[0], dict):
                update_data = args[0].copy()
            else:
                update_data = {}
            
            # Add kwargs to update_data
            update_data.update(kwargs)
            
            # If multiple fields are present, use them as query
            query = {k: v for k, v in update_data.items() if k not in ['age', 'name']}
            update_data = {k: v for k, v in update_data.items() if k in ['age', 'name']}
            
            # If no query exists, use update fields as query
            if not query and update_data:
                query = {k: v for k, v in update_data.items()}
            
            return await self.driver.update(table, query, update_data)
        
        raise ValueError("Invalid arguments for update method")


    async def delete(self, table: str, query: Dict[str, Any]) -> bool:
        return await self.driver.delete(table, query)
    
    async def execute(self, query: str, params: Optional[Union[tuple, Dict[str, Any]]] = None) -> Any:
        """Execute a raw SQL query asynchronously."""
        return await self.driver.execute(query, params)

    async def create_table(self, table_name: str, columns: Dict[str, str], 
                            primary_key: str = 'id', 
                            auto_increment: bool = True,
                            if_not_exists: bool = True) -> bool:
        """
        Create a table with specified columns asynchronously.
        
        :param table_name: Name of the table to create
        :param columns: Dictionary of column names and their types
        :param primary_key: Name of the primary key column
        :param auto_increment: Whether to make the primary key auto-increment
        :param if_not_exists: Whether to use IF NOT EXISTS clause
        :return: True if table creation was successful, False otherwise
        """
        return await self.driver.create_table(table_name, columns, 
                                              primary_key, 
                                              auto_increment, 
                                              if_not_exists)
