"""Synchronous SQLite update operation."""

from typing import Any, Dict

def update_record(connection: Any, table: str, query: Dict[str, Any], data: Dict[str, Any]) -> bool:
    """Update a record in SQLite database."""
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
        connection.execute(sql, values)
        connection.commit()
        
        return True
        
    except Exception as e:
        if connection:
            connection.rollback()
        print(f"Error updating record: {e}")
        return False
