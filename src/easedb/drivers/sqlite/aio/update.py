"""Asynchronous SQLite update operation."""

from typing import Any, Dict

async def update_record(connection: Any, table: str, query: Dict[str, Any], data: Dict[str, Any]) -> bool:
    """Update a record in SQLite database asynchronously."""
    try:
        # If no query is provided, we cannot determine what to update
        if not query:
            raise ValueError("Update requires a query to identify records")
        
        # If no data is provided, no update will occur
        if not data:
            return False
        
        # Construct the query condition
        where_clause = ' AND '.join([f"{k} = ?" for k in query.keys()])
        set_clause = ', '.join([f"{k} = ?" for k in data.keys()])
        
        # Construct SQL query
        sql = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"
        
        # Prepare values
        values = list(data.values()) + list(query.values())
        
        # Execute query
        async with connection.execute(sql, values) as cursor:
            await connection.commit()
        
        return True
        
    except Exception as e:
        if connection:
            await connection.rollback()
        print(f"Error updating record: {e}")
        return False
