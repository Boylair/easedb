"""Asynchronous SQLite get operation."""

from typing import Any, Dict, Optional

from ..utils import row_to_dict, get_columns_from_cursor

async def get_record(connection: Any, table: str, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Get a record from SQLite database asynchronously."""
    try:
        where_clause = ' AND '.join([f"{k} = ?" for k in query.keys()])
        sql = f"SELECT * FROM {table} WHERE {where_clause}"
        
        async with connection.execute(sql, list(query.values())) as cursor:
            columns = get_columns_from_cursor(cursor)
            row = await cursor.fetchone()
            
            return row_to_dict(row, columns)
            
    except Exception as e:
        print(f"Error getting record: {e}")
        return None
