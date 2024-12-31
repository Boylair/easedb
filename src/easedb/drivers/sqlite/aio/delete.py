"""Asynchronous SQLite delete operation."""

from typing import Any, Dict

async def delete_record(connection: Any, table: str, query: Dict[str, Any]) -> bool:
    """Delete a record from SQLite database asynchronously."""
    try:
        where_clause = ' AND '.join([f"{k} = ?" for k in query.keys()])
        sql = f"DELETE FROM {table} WHERE {where_clause}"
        
        async with connection.execute(sql, list(query.values())) as cursor:
            await connection.commit()
        
        return True
        
    except Exception as e:
        if connection:
            await connection.rollback()
        print(f"Error deleting record: {e}")
        return False
