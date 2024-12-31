"""Base synchronous database driver interface."""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Union

class DatabaseDriver(ABC):
    """Abstract base class for synchronous database drivers."""
    
    @abstractmethod
    def connect(self) -> bool:
        """Establish connection to the database."""
        pass
    
    @abstractmethod
    def disconnect(self) -> bool:
        """Close the database connection."""
        pass
    
    @abstractmethod
    def get(self, table: str, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Get a record from the database."""
        pass
    
    @abstractmethod
    def set(self, table: str, data: Dict[str, Any]) -> bool:
        """Insert a record into the database."""
        pass
    
    @abstractmethod
    def update(self, table: str, data: Dict[str, Any]) -> bool:
        """Update a record in the database."""
        pass
    
    @abstractmethod
    def delete(self, table: str, query: Dict[str, Any]) -> bool:
        """Delete a record from the database."""
        pass
    
    @abstractmethod
    def execute(self, query: str, params: Optional[Union[tuple, Dict[str, Any]]] = None) -> Any:
        """Execute a raw SQL query."""
        pass
