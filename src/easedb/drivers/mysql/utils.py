from typing import Dict, Any, Optional, Tuple
from urllib.parse import urlparse, parse_qs, unquote
import re

def parse_connection_string(connection_string: str) -> Dict[str, Any]:
    """Parse MySQL or SQLite connection string."""
    parsed = urlparse(connection_string)
    
    if parsed.scheme not in ('mysql', 'sqlite'):
        raise ValueError("Invalid connection string scheme. Must be 'mysql' or 'sqlite'")
    
    if parsed.scheme == 'sqlite':
        return {
            'database': unquote(parsed.path[1:] if parsed.path else ':memory:')
        }
    
    # For MySQL, decode URL-encoded characters in username and password
    params = {
        'host': parsed.hostname or 'localhost',
        'port': parsed.port or 3306,
        'user': unquote(parsed.username) if parsed.username else None,
        'password': unquote(parsed.password) if parsed.password else None,
        'db': unquote(parsed.path[1:]) if parsed.path else None,
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
                    params[key] = unquote(value[0])
    
    return params

def row_to_dict(row: Optional[tuple], columns: tuple) -> Optional[Dict[str, Any]]:
    """Convert database row to dictionary."""
    if row is None:
        return None
    return {columns[i]: value for i, value in enumerate(row)}

def get_columns_from_cursor(cursor: Any) -> Tuple[str, ...]:
    """Get column names from cursor."""
    return tuple(col[0] for col in cursor.description)

def format_placeholders(data: Dict[str, Any], dialect: str = 'mysql') -> str:
    """Format placeholders for parameterized queries based on database dialect."""
    if dialect == 'sqlite':
        return ', '.join(['?' for _ in data])
    return ', '.join(['%s' for _ in data])

def escape_special_chars(value: str) -> str:
    """Escape special characters in string values."""
    if not isinstance(value, str):
        return value
    # Escape special characters that might cause issues
    return re.sub(r'([%_\\])', r'\\\1', value)