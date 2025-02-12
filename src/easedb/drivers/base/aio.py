"""Base asynchronous database driver interface."""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Union

class AsyncDatabaseDriver(ABC):
    """Abstract base class for asynchronous database drivers."""
    
    @abstractmethod
    async def connect(self) -> bool:
        """Establish connection to the database asynchronously."""
        pass
    
    @abstractmethod
    async def disconnect(self) -> bool:
        """Close the database connection asynchronously."""
        pass
    
    @abstractmethod
    async def get(self, table: str, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Get a record from the database asynchronously."""
        pass
    
    @abstractmethod
    async def set(self, table: str, data: Dict[str, Any]) -> bool:
        """Insert a record into the database asynchronously."""
        pass
    
    @abstractmethod
    async def update(self, table: str, data: Dict[str, Any]) -> bool:
        """Update a record in the database asynchronously."""
        pass
    
    @abstractmethod
    async def delete(self, table: str, query: Dict[str, Any]) -> bool:
        """Delete a record from the database asynchronously."""
        pass
    
    @abstractmethod
    async def execute(self, query: str, params: Optional[Union[tuple, Dict[str, Any]]] = None) -> Any:
        """Execute a raw SQL query asynchronously."""
        pass
    
    @abstractmethod
    async def add(self, table: str, query: Dict[str, Any], value: Union[int, float]) -> bool:
        """
        Add a specified value to an existing numeric column in the database asynchronously.
        
        :param table: Name of the table
        :param query: Dictionary specifying which record(s) to update
        :param value: Numeric value to add to the existing value
        :return: True if update was successful, False otherwise
        """
        pass
    
    @abstractmethod
    async def sub(self, table: str, query: Dict[str, Any], value: Union[int, float]) -> bool:
        """
        Subtract a specified value from an existing numeric column in the database asynchronously.
        
        :param table: Name of the table
        :param query: Dictionary specifying which record(s) to update
        :param value: Numeric value to subtract from the existing value
        :return: True if update was successful, False otherwise
        """
        pass
