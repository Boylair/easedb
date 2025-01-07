"""Synchronous MySQL set operation."""

from typing import Any, Dict

from ..utils import format_placeholders
from ....logger import logger

def set_record(connection: Any, table: str, data: Dict[str, Any]) -> bool:
    """Insert a record into MySQL database."""
    try:
        cursor = connection.cursor()
        columns = ', '.join(data.keys())
        placeholders = format_placeholders(data)
        sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        
        logger.info(f"Executing SQL: {sql} | Data: {data}")
        
        cursor.execute(sql, list(data.values()))
        connection.commit()
        cursor.close()

        logger.info(f"Record inserted successfully into {table}")

        return True
        
    except Exception as e:
        if connection:
            connection.rollback()
        logger.error(f"Error inserting record into {table}: {e}")
        return False
