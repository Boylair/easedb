"""Asynchronous MySQL get operation."""

from typing import Any, Dict, Optional

from ..utils import row_to_dict, get_columns_from_cursor

async def get_record(connection: Any, table: str, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Get a record from MySQL database asynchronously."""
    try:
        cursor = await connection.cursor()
        where_clause = ' AND '.join([f"{k} = %s" for k in query.keys()])
        sql = f"SELECT * FROM {table} WHERE {where_clause}"
        
        await cursor.execute(sql, list(query.values()))
        columns = get_columns_from_cursor(cursor)
        row = await cursor.fetchone()
        await cursor.close()
        
        return row_to_dict(row, columns)
        
    except Exception:
        return None