from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union

class DatabaseDriver(ABC):
    """Base class for all database drivers."""
    
    @abstractmethod
    def connect(self) -> None:
        """Establish connection to the database."""
        pass
    
    @abstractmethod
    def disconnect(self) -> None:
        """Close the database connection."""
        pass
    
    @abstractmethod
    def get(self, table: str, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Retrieve a single record from the database."""
        pass
    
    @abstractmethod
    def get_all(self, table: str, query: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Retrieve multiple records from the database."""
        pass
    
    @abstractmethod
    def set(self, table: str, data: Dict[str, Any]) -> bool:
        """Insert or update a record in the database."""
        pass
    
    @abstractmethod
    def update(self, table: str, query: Dict[str, Any], data: Dict[str, Any]) -> bool:
        """Update records in the database that match the query."""
        pass
    
    @abstractmethod
    def delete(self, table: str, query: Dict[str, Any]) -> bool:
        """Delete a record from the database."""
        pass
    
    @abstractmethod
    def execute(self, query: str, params: Optional[Union[tuple, Dict[str, Any]]] = None) -> Any:
        """Execute a raw SQL query."""
        pass

class Database:
    """Main database interface for synchronous operations."""
    
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.driver = self._init_driver()
    
    def _init_driver(self) -> DatabaseDriver:
        """Initialize the appropriate database driver based on the connection string."""
        if self.connection_string.startswith('sqlite'):
            from .drivers.sqlite import SQLiteDriver
            return SQLiteDriver(self.connection_string)
        elif self.connection_string.startswith(('mysql', 'mariadb')):
            from .drivers.mysql import MySQLDriver
            return MySQLDriver(self.connection_string)
        else:
            raise ValueError(f"Unsupported database type in connection string: {self.connection_string}")
    
    def connect(self) -> None:
        """Explicit connection method"""
        self.driver.connect()
    
    def disconnect(self) -> None:
        """Explicit disconnection method"""
        self.driver.disconnect()
    
    def __enter__(self):
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self.disconnect()
        except Exception as e:
            print(f"Error during connection cleanup: {e}")
            if exc_type is None:
                raise  # Only re-raise if there wasn't already an exception
    
    def get(self, table: str, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        return self.driver.get(table, query)
    
    def get_all(self, table: str, query: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        return self.driver.get_all(table, query)
    
    def set(self, table: str, data: Dict[str, Any]) -> bool:
        return self.driver.set(table, data)
    
    def update(self, table: str, query: Dict[str, Any], data: Dict[str, Any]) -> bool:
        return self.driver.update(table, query, data)
    
    def delete(self, table: str, query: Dict[str, Any]) -> bool:
        return self.driver.delete(table, query)
    
    def execute(self, query: str, params: Optional[Union[tuple, Dict[str, Any]]] = None) -> Any:
        """Execute a raw SQL query."""
        return self.driver.execute(query, params)

    def create_table(self, table_name: str, columns: Dict[str, str]) -> bool:
        """
        Create a table with specified columns.
        
        :param table_name: Name of the table to create
        :param columns: Dictionary of column names and their types
        :return: True if table creation was successful, False otherwise
        """
        column_definitions = [f"{col_name} {col_type}" for col_name, col_type in columns.items()]
        create_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(column_definitions)})"
        return self.execute(create_query)
