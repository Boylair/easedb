"""Asynchronous connect method for database drivers."""

from abc import abstractmethod
from typing import Any

class AsyncConnect:
    """Abstract base class for asynchronous connection method."""
    
    @abstractmethod
    async def connect(self) -> bool:
        """Establish connection to the database asynchronously."""
        pass
