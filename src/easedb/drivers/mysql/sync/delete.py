"""Synchronous MySQL delete operation."""

from typing import Any, Dict

def delete_record(connection: Any, table: str, query: Dict[str, Any]) -> bool:
    """Delete a record from MySQL database."""
    try:
        cursor = connection.cursor()
        where_clause = ' AND '.join([f"{k} = %s" for k in query.keys()])
        sql = f"DELETE FROM {table} WHERE {where_clause}"
        
        cursor.execute(sql, list(query.values()))
        connection.commit()
        cursor.close()
        
        return True
        
    except Exception as e:
        if connection:
            connection.rollback()
        print(f"Error deleting record: {e}")
        return False
