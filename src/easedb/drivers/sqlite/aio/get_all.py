"""Asynchronous SQLite get_all operation."""

from typing import Any, Dict, List, Optional

from ..utils import row_to_dict, get_columns_from_cursor
from ....logger import logger  

async def get_all_records(
    connection: Any, 
    table: str, 
    query: Optional[Dict[str, Any]] = None, 
    page: Optional[int] = None, 
    page_size: Optional[int] = None
) -> List[Dict[str, Any]]:
    """
    Get all records from SQLite database asynchronously.
    
    :param connection: Active database connection
    :param table: Name of the table to retrieve records from
    :param query: Optional dictionary of conditions to filter records
    :param page: Optional page number for pagination (1-indexed)
    :param page_size: Optional number of records per page
    :return: List of records matching the query
    """
    try:
        if query is None:
            # If no query is provided, fetch all records
            sql = f"SELECT * FROM {table}"
            params = []
            logger.debug(f"Fetching all records from table '{table}'")
        else:
            # Construct a parameterized query with the provided conditions
            where_clause = ' AND '.join([f"{k} = ?" for k in query.keys()])
            sql = f"SELECT * FROM {table} WHERE {where_clause}"
            params = list(query.values())
            logger.debug(f"Fetching records from table '{table}' with query: {query}")

        # Add pagination if both page and page_size are provided
        if page is not None and page_size is not None:
            if page < 1 or page_size < 1:
                raise ValueError("Page and page_size must be positive integers")
            
            # Calculate OFFSET for pagination (convert to 0-indexed)
            offset = (page - 1) * page_size
            sql += " LIMIT ? OFFSET ?"
            params.extend([page_size, offset])
            logger.debug(f"Applying pagination: page {page}, page_size {page_size}")

        logger.trace(f"Executing SQL: {sql} | Parameters: {params}")
        
        async with connection.execute(sql, params) as cursor:
            columns = get_columns_from_cursor(cursor)
            rows = await cursor.fetchall()
            records = [row_to_dict(row, columns) for row in rows]

            if records:
                logger.info(f"Retrieved {len(records)} records from '{table}'")
            else:
                logger.debug(f"No records found in '{table}' with query: {query}")
            
            return records
            
    except Exception as e:
        logger.error(f"Error retrieving records from '{table}': {e}")
        return []