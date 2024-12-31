"""Utility functions for MySQL driver."""

from typing import Dict, Any, Optional, Tuple
from urllib.parse import urlparse, parse_qs

def parse_connection_string(connection_string: str) -> Dict[str, Any]:
    """Parse MySQL connection string."""
    parsed = urlparse(connection_string)
    if parsed.scheme != 'mysql':
        raise ValueError("Invalid connection string scheme. Must be 'mysql'")
    
    params = {
        'host': parsed.hostname or 'localhost',
        'port': parsed.port or 3306,
        'user': parsed.username,
        'password': parsed.password,
        'db': parsed.path[1:] if parsed.path else None,  # Change 'database' to 'db' for aiomysql
        'charset': 'utf8mb4'
    }
    
    # Remove None values
    params = {k: v for k, v in params.items() if v is not None}
    
    # Parse additional options from query string
    if parsed.query:
        query_params = parse_qs(parsed.query)
        for key, value in query_params.items():
            # Convert values like ['true'] to True
            if value[0].lower() == 'true':
                params[key] = True
            elif value[0].lower() == 'false':
                params[key] = False
            else:
                try:
                    params[key] = int(value[0])
                except ValueError:
                    params[key] = value[0]
    
    return params

def row_to_dict(row: Optional[tuple], columns: tuple) -> Optional[Dict[str, Any]]:
    """Convert MySQL row to dictionary."""
    if row is None:
        return None
    return {columns[i]: value for i, value in enumerate(row)}

def get_columns_from_cursor(cursor: Any) -> Tuple[str, ...]:
    """Get column names from cursor."""
    return tuple(col[0] for col in cursor.description)

def format_placeholders(data: Dict[str, Any]) -> str:
    """Format MySQL placeholders for parameterized queries."""
    return ', '.join(['%s' for _ in data])
