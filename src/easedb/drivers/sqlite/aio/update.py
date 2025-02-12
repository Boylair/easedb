"""Asynchronous SQLite update operation."""

from typing import Any, Dict

from ....logger import logger

async def update_record(connection: Any, table: str, query: Dict[str, Any], data: Dict[str, Any]) -> bool:
    """Update a record in SQLite database asynchronously."""
    try:
        # If no query is provided, we cannot determine what to update
        if not query:
            raise ValueError("Update requires a query to identify records")
        
        # If no data is provided, no update will occur
        if not data:
            return False
        
        # Construct the query condition with double quotes for column names with spaces
        where_clause = ' AND '.join([f'"{k}" = ?' for k in query.keys()])
        set_clause = ', '.join([f'"{k}" = ?' for k in data.keys()])
        
        # Construct SQL query with proper table and column quoting
        sql = f'UPDATE "{table}" SET {set_clause} WHERE {where_clause}'
        
        # Prepare values
        values = list(data.values()) + list(query.values())

        logger.debug(f"Executing update query: {sql} | Parameters: {values}")
        
        # Execute query
        async with connection.cursor() as cursor:
            await cursor.execute(sql, values)
            await connection.commit()
        
        logger.info(f"Record updated successfully in '{table}' with query: {query} and data: {data}")
        
        return True
        
    except Exception as e:
        if connection:
            await connection.rollback()
        logger.error(f"Error updating record in table '{table}': {e}")
        logger.debug(f"Failed query: {sql if 'sql' in locals() else 'Unknown'} | Parameters: {values if 'values' in locals() else 'Unknown'}")        
        return False
        