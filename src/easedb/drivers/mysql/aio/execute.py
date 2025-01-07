"""Asynchronous MySQL execute operation."""

from typing import Any, Dict, Optional, Union, List

from ..utils import row_to_dict, get_columns_from_cursor

from ....logger import logger

async def execute_query(connection: Any, query: str, params: Optional[Union[tuple, Dict[str, Any]]] = None) -> Any:
    """Execute a raw SQL query asynchronously."""
    try:
        logger.info(f"Executing query: {query} with params: {params}")
        cursor = await connection.cursor()
        await cursor.execute(query, params or ())
        
        if query.strip().upper().startswith('SELECT'):
            columns = get_columns_from_cursor(cursor)
            rows = await cursor.fetchall()
            await cursor.close()

            logger.info(f"Query executed successfully, retrieved {len(rows)} rows")

            return [row_to_dict(row, columns) for row in rows]
        else:
            await connection.commit()
            await cursor.close()

            logger.info("Query executed successfully: Changes committed.")

            return True
            
    except Exception as e:
        if connection:
            await connection.rollback()
        logger.error(f"Error executing query: {query}. Error: {str(e)}")
        return None
