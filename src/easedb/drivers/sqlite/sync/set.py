"""Synchronous SQLite set operation."""

from typing import Any, Dict

from ....logger import logger

def set_record(connection: Any, table: str, data: Dict[str, Any]) -> bool:
    """Insert a record into SQLite database."""
    try:
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?' for _ in data])
        sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"

        logger.debug(f"Executing query: {sql} with parameters: {list(data.values())}")
        
        connection.execute(sql, list(data.values()))
        connection.commit()
        
        logger.info(f"Record inserted successfully: {data}")
        
        return True
        
    except Exception as e:
        if connection:
            connection.rollback()
        logger.error(f"Error inserting record into {table}. SQL: {sql}, Parameters: {list(data.values())}, Error: {str(e)}")
        return False
