"""Synchronous MySQL update operation."""

from typing import Any, Dict

def update_record(connection: Any, table: str, query: Dict[str, Any], data: Dict[str, Any]) -> bool:
    """Update a record in MySQL database."""
    try:
        cursor = connection.cursor()
        
        # Construct the SET clause for update values
        set_clause = ', '.join([f"{k} = %s" for k in data.keys()])
        
        # Construct the WHERE clause for the query conditions
        where_clause = ' AND '.join([f"{k} = %s" for k in query.keys()])
        
        # Combine the SQL statement
        sql = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"
        
        # Combine values: first update values, then query conditions
        values = list(data.values()) + list(query.values())
        
        cursor.execute(sql, values)
        connection.commit()
        cursor.close()
        
        return True
        
    except Exception:
        if connection:
            connection.rollback()
        return False
