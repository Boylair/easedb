"""Synchronous SQLite get_all operation."""

from typing import Any, Dict, List, Optional

from ..utils import row_to_dict, get_columns_from_cursor

from ....logger import logger

def get_all_records(connection: Any, table: str, query: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    """
    Get all records from SQLite database synchronously.
    
    :param connection: Active database connection
    :param table: Name of the table to retrieve records from
    :param query: Optional dictionary of conditions to filter records
    :return: List of records matching the query
    """
    try:
        if query is None:
            # If no query is provided, fetch all records
            sql = f"SELECT * FROM {table}"
            params = []
            logger.debug(f"Executing query: {sql} with no parameters")
        else:
            # Construct a parameterized query with the provided conditions
            where_clause = ' AND '.join([f"{k} = ?" for k in query.keys()])
            sql = f"SELECT * FROM {table} WHERE {where_clause}"
            params = list(query.values())
            logger.debug(f"Executing query: {sql} with parameters: {params}")
        
        cursor = connection.execute(sql, params)
        columns = get_columns_from_cursor(cursor)
        rows = cursor.fetchall()
        result = [row_to_dict(row, columns) for row in rows]

        logger.debug(f"Query result: {result}")

        return result
            
    except Exception as e:
        logger.error(f"Error getting all records from {table}. SQL: {sql}, Parameters: {params}, Error: {str(e)}")
        return []
