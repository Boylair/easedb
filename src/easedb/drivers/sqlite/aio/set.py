"""Asynchronous SQLite set operation."""

from typing import Any, Dict


async def set_record(connection: Any, table: str, data: Dict[str, Any]) -> bool:
    """Insert a record into SQLite database asynchronously."""
    try:
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?' for _ in data])
        sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        
        async with connection.execute(sql, list(data.values())) as cursor:
            await connection.commit()
        
        return True
        
    except Exception as e:
        if connection:
            await connection.rollback()
        print(f"Error inserting record: {e}")
        return False
