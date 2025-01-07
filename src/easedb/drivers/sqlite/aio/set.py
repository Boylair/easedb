"""Asynchronous SQLite set operation."""

from typing import Any, Dict
from ....logger import logger



async def set_record(connection: Any, table: str, data: Dict[str, Any]) -> bool:
    """Insert a record into SQLite database asynchronously."""
    try:
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?' for _ in data])
        sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"

        logger.debug(f"Preparing SQL Query: {sql} | Parameters: {list(data.values())}")
        
        async with connection.execute(sql, list(data.values())) as cursor:
            await connection.commit()
        
        logger.info(f"Inserted record into {table}: {data}")

        return True
        
    except Exception as e:
        if connection:
            await connection.rollback()
        logger.error(f"Error inserting record into {table}: {e}")
        return False
