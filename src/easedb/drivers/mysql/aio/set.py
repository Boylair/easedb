"""Asynchronous MySQL set operation."""

from typing import Any, Dict

from ..utils import format_placeholders

async def set_record(connection: Any, table: str, data: Dict[str, Any]) -> bool:
    """Insert a record into MySQL database asynchronously."""
    try:
        cursor = await connection.cursor()
        columns = ', '.join(data.keys())
        placeholders = format_placeholders(data)
        sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        
        await cursor.execute(sql, list(data.values()))
        await connection.commit()
        await cursor.close()
        
        return True
        
    except Exception as e:
        if connection:
            await connection.rollback()
        print(f"Error inserting record: {e}")
        return False
