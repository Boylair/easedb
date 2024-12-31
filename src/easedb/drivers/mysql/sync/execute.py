"""Synchronous MySQL execute operation."""

from typing import Any, Dict, Optional, Union, List

from ..utils import row_to_dict, get_columns_from_cursor

def execute_query(connection: Any, query: str, params: Optional[Union[tuple, Dict[str, Any]]] = None) -> Any:
    """Execute a raw SQL query."""
    try:
        cursor = connection.cursor()
        cursor.execute(query, params or ())
        
        if query.strip().upper().startswith('SELECT'):
            columns = get_columns_from_cursor(cursor)
            result = [row_to_dict(row, columns) for row in cursor.fetchall()]
            cursor.close()
            return result
        else:
            connection.commit()
            cursor.close()
            return True
            
    except Exception as e:
        if connection:
            connection.rollback()
        print(f"Error executing query: {e}")
        return None
