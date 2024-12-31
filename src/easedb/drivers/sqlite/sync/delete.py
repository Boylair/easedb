"""Synchronous SQLite delete operation."""

from typing import Any, Dict

def delete_record(connection: Any, table: str, query: Dict[str, Any]) -> bool:
    """Delete a record from SQLite database."""
    try:
        where_clause = ' AND '.join([f"{k} = ?" for k in query.keys()])
        sql = f"DELETE FROM {table} WHERE {where_clause}"
        
        connection.execute(sql, list(query.values()))
        connection.commit()
        
        return True
        
    except Exception as e:
        if connection:
            connection.rollback()
        print(f"Error deleting record: {e}")
        return False
