"""Asynchronous MySQL delete operation."""

from typing import Any, Dict

async def delete_record(connection: Any, table: str, query: Dict[str, Any]) -> bool:
    """Delete a record from MySQL database asynchronously."""
    try:
        cursor = await connection.cursor()
        where_clause = ' AND '.join([f"{k} = %s" for k in query.keys()])
        sql = f"DELETE FROM {table} WHERE {where_clause}"
        
        await cursor.execute(sql, list(query.values()))
        await connection.commit()
        await cursor.close()
        
        return True
        
    except Exception as e:
        if connection:
            await connection.rollback()
        print(f"Error deleting record: {e}")
        return False
