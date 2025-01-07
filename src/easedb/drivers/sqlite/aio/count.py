"""Asynchronous count method for SQLite database."""

from typing import Dict, Any, Optional
import aiosqlite

from ....logger import logger

async def count_records(connection: aiosqlite.Connection, table: str, query: Optional[Dict[str, Any]] = None) -> int:
    """
    Asynchronously count records in a SQLite database table.
    
    :param connection: Active database connection
    :param table: Name of the table to count records from
    :param query: Optional dictionary of conditions to filter records
    :return: Number of records matching the query
    """
    try:
        # If no query is provided, count all records
        if query is None:
            # If no query is provided, count all records
            sql = f"SELECT COUNT(*) FROM {table}"
            params = []
        else:
            # Construct a parameterized query with the provided conditions
            where_clauses = [f"{k} = ?" for k in query.keys()]
            sql = f"SELECT COUNT(*) FROM {table} WHERE {' AND '.join(where_clauses)}"
            params = list(query.values())        

        logger.debug(f"Executing count query: {sql} | Parameters: {params}")
        
        async with connection.execute(sql, params) as cursor:
            result = await cursor.fetchone()
            count = result[0] if result else 0
            
            # Log the result
            logger.info(f"Count query result: {count} record(s) found in table '{table}'.")
            return count

    except Exception as e:
        logger.error(f"Error counting records in table '{table}': {e}")
        logger.debug(f"Failed query: {sql if 'sql' in locals() else 'Unknown'} | Parameters: {params if 'params' in locals() else 'Unknown'}")
        return 0
