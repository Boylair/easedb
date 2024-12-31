"""Asynchronous MySQL update operation."""

from typing import Any, Dict

async def update_record(connection: Any, table: str, query: Dict[str, Any], data: Dict[str, Any]) -> bool:
    """Update a record in MySQL database asynchronously."""
    try:
        # Ha nincs query, nem tudjuk, mit frissítsünk
        if not query:
            raise ValueError("Update requires a query to identify records")
        
        # Ha nincs adat, nem történik frissítés
        if not data:
            return False
        
        cursor = await connection.cursor()
        
        # Construct the SET clause for update values
        set_clause = ', '.join([f"{k} = %s" for k in data.keys()])
        
        # Construct the WHERE clause for the query conditions
        where_clause = ' AND '.join([f"{k} = %s" for k in query.keys()])
        
        # Combine the SQL statement
        sql = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"
        
        # Combine values: first update values, then query conditions
        values = list(data.values()) + list(query.values())
        
        await cursor.execute(sql, values)
        await connection.commit()
        await cursor.close()
        
        return True
        
    except Exception as e:
        if connection:
            await connection.rollback()
        print(f"Error updating record: {e}")
        return False
