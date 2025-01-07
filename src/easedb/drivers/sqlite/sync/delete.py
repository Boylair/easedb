"""Synchronous SQLite delete operation."""

from typing import Any, Dict

from ....logger import logger

def delete_record(connection: Any, table: str, query: Dict[str, Any]) -> bool:
    """Delete a record from SQLite database."""
    try:
        where_clause = ' AND '.join([f"{k} = ?" for k in query.keys()])
        sql = f"DELETE FROM {table} WHERE {where_clause}"

        logger.debug(f"Executing delete query: {sql} with parameters: {list(query.values())}")
        
        connection.execute(sql, list(query.values()))
        connection.commit()
        
        logger.info(f"Record deleted from table '{table}' where {query}.")
        return True
        
    except Exception as e:
        if connection:
            connection.rollback()
        logger.error(f"Error deleting record from {table}. SQL: {sql}, Parameters: {list(query.values())}, Error: {str(e)}")
        return False
