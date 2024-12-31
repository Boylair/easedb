"""Synchronous MySQL set operation."""

from typing import Any, Dict

from ..utils import format_placeholders

def set_record(connection: Any, table: str, data: Dict[str, Any]) -> bool:
    """Insert a record into MySQL database."""
    try:
        cursor = connection.cursor()
        columns = ', '.join(data.keys())
        placeholders = format_placeholders(data)
        sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        
        cursor.execute(sql, list(data.values()))
        connection.commit()
        cursor.close()
        
        return True
        
    except Exception as e:
        if connection:
            connection.rollback()
        print(f"Error inserting record: {e}")
        return False
