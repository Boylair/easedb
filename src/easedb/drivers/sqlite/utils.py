"""Utility functions for SQLite driver."""

import os
from typing import Dict, Any, Optional, Tuple
from urllib.parse import urlparse

def parse_connection_string(connection_string: str) -> Dict[str, Any]:
    """Parse SQLite connection string."""
    parsed = urlparse(connection_string)
    if parsed.scheme != 'sqlite':
        raise ValueError("Invalid connection string scheme. Must be 'sqlite'")
    
    # Remove leading slash for relative paths
    path = parsed.path
    if path.startswith('/'):
        path = path[1:]
    
    # Ensure directory exists
    directory = os.path.dirname(path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)
    
    return {'database': path}

def row_to_dict(row: Optional[tuple], columns: tuple) -> Optional[Dict[str, Any]]:
    """Convert SQLite row to dictionary."""
    if row is None:
        return None
    return {columns[i]: value for i, value in enumerate(row)}

def get_columns_from_cursor(cursor: Any) -> Tuple[str, ...]:
    """Get column names from cursor."""
    return tuple(col[0] for col in cursor.description)
