"""Asynchronous SQLite execute operation."""

from typing import Any, Dict, Optional, Union, List

from ..utils import row_to_dict, get_columns_from_cursor
from ....logger import logger  

async def execute_query(connection: Any, query: str, params: Optional[Union[tuple, Dict[str, Any]]] = None) -> Any:
    """Execute a raw SQL query asynchronously."""
    try:
        async with connection.execute(query, params or ()) as cursor:
            if query.strip().upper().startswith('SELECT'):
                columns = get_columns_from_cursor(cursor)
                rows = await cursor.fetchall()
                records = [row_to_dict(row, columns) for row in rows]

                logger.info(f"Query executed successfully: {len(records)} records retrieved.")

                return records
            else:
                await connection.commit()
                logger.info("Query executed successfully: Changes committed.")

                return True
                
    except Exception as e:
        if connection:
            await connection.rollback()
        logger.error(f"Error executing query: {e}")
        logger.trace(f"Failed query: {query} | Parameters: {params}")

        return None
