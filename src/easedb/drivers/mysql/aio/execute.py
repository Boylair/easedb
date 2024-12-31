"""Asynchronous MySQL execute operation."""

from typing import Any, Dict, Optional, Union, List

from ..utils import row_to_dict, get_columns_from_cursor

async def execute_query(connection: Any, query: str, params: Optional[Union[tuple, Dict[str, Any]]] = None) -> Any:
    """Execute a raw SQL query asynchronously."""
    try:
        cursor = await connection.cursor()
        await cursor.execute(query, params or ())
        
        if query.strip().upper().startswith('SELECT'):
            columns = get_columns_from_cursor(cursor)
            rows = await cursor.fetchall()
            await cursor.close()
            return [row_to_dict(row, columns) for row in rows]
        else:
            await connection.commit()
            await cursor.close()
            return True
            
    except Exception as e:
        if connection:
            await connection.rollback()
        print(f"Error executing query: {e}")
        return None
