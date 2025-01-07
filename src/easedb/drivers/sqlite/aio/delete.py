"""Asynchronous SQLite delete operation."""

from typing import Any, Dict

from ....logger import logger

async def delete_record(connection: Any, table: str, query: Dict[str, Any]) -> bool:
    """Delete a record from SQLite database asynchronously."""
    try:
        where_clause = ' AND '.join([f"{k} = ?" for k in query.keys()])
        sql = f"DELETE FROM {table} WHERE {where_clause}"

        logger.debug(f"Executing delete query: {sql}")
        logger.trace(f"Parameters: {query}")
        
        async with connection.execute(sql, list(query.values())) as cursor:
            await connection.commit()
        
        logger.info(f"Record deleted successfully from '{table}' with query: {query}")
        return True
        
    except Exception as e:
        if connection:
            await connection.rollback()
        logger.error(f"Error deleting record from table '{table}': {e}")
        logger.trace(f"Failed query: {sql} | Parameters: {query}")
        
        return False
