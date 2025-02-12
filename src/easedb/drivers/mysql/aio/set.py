"""Asynchronous MySQL set operation."""

from typing import Any, Dict

from ..utils import format_placeholders

from ....logger import logger


async def set_record(connection: Any, table: str, data: Dict[str, Any]) -> bool:
    """Insert a record into MySQL database asynchronously."""
    try:
        cursor = await connection.cursor()
        # Ensure column names are properly escaped/quoted
        columns = ', '.join([f"`{col}`" for col in data.keys()])
        placeholders = format_placeholders(data)
        sql = f"INSERT INTO `{table}` ({columns}) VALUES ({placeholders})"
        
        logger.info(f"Executing SQL: {sql} | Data: {data}")

        await cursor.execute(sql, list(data.values()))
        await connection.commit()
        await cursor.close()
        
        return True
        
    except Exception as e:
        if connection:
            await connection.rollback()
        logger.error(f"Error inserting record into {table}: {e}")
        return False