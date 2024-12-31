"""Synchronous SQLite set operation."""

from typing import Any, Dict

def set_record(connection: Any, table: str, data: Dict[str, Any]) -> bool:
    """Insert a record into SQLite database."""
    try:
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?' for _ in data])
        sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        
        connection.execute(sql, list(data.values()))
        connection.commit()
        
        return True
        
    except Exception as e:
        if connection:
            connection.rollback()
        print(f"Error inserting record: {e}")
        return False
