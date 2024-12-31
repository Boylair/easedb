"""Asynchronous disconnect method for database drivers."""

from abc import abstractmethod

class AsyncDisconnect:
    """Abstract base class for asynchronous disconnection method."""
    
    @abstractmethod
    async def disconnect(self) -> bool:
        """Close the database connection asynchronously."""
        pass
