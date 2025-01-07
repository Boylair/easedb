"""Synchronous SQLite execute operation."""

from typing import Any, Dict, Optional, Union, List

from ..utils import row_to_dict, get_columns_from_cursor

from ....logger import logger

def execute_query(connection: Any, query: str, params: Optional[Union[tuple, Dict[str, Any]]] = None) -> Any:
    """Execute a raw SQL query."""
    try:
        logger.debug(f"Executing query: {query} with parameters: {params or ()}")
        cursor = connection.execute(query, params or ())
        
        if query.strip().upper().startswith('SELECT'):
            columns = get_columns_from_cursor(cursor)
            result = [row_to_dict(row, columns) for row in cursor.fetchall()]

            logger.debug(f"Query result: {result}")
            
            return result
        else:
            connection.commit()
            
            logger.info(f"Query executed successfully: {query}")
            return True
            
    except Exception as e:
        if connection:
            connection.rollback()
        logger.error(f"Error executing query: {query}, Parameters: {params}, Error: {str(e)}")
        return None
