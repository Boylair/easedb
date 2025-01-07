"""Asynchronous SQLite get operation."""

from typing import Any, Dict, Optional

from ..utils import row_to_dict, get_columns_from_cursor
from ....logger import logger

async def get_record(connection: Any, table: str, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Get a record from SQLite database asynchronously."""
    try:
        where_clause = ' AND '.join([f"{k} = ?" for k in query.keys()])
        sql = f"SELECT * FROM {table} WHERE {where_clause}"
        
        logger.debug(f"Preparing SQL Query: {sql} | Parameters: {list(query.values())}")

        async with connection.execute(sql, list(query.values())) as cursor:
            columns = get_columns_from_cursor(cursor)
            row = await cursor.fetchone()

            if row:
                # Info log for successful retrieval
                logger.info(f"Record retrieved from {table}: {row}")
                return row_to_dict(row, columns)
            else:
                # Debug log if no record found
                logger.debug(f"No record found in {table} matching: {query}")
                return None
                
    except Exception as e:
        logger.error(f"Error retrieving record from {table}: {e}")
        return None
