"""Synchronous SQLite get operation."""

from typing import Any, Dict, Optional

from ..utils import row_to_dict, get_columns_from_cursor

def get_record(connection: Any, table: str, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Get a record from SQLite database."""
    try:
        # Log the query parameters before execution
        where_clause = ' AND '.join([f"{k} = ?" for k in query.keys()])
        sql = f"SELECT * FROM {table} WHERE {where_clause}"
        params = list(query.values())
        logger.debug(f"Executing query: {sql} with parameters: {params}")

        cursor = connection.execute(sql, list(query.values()))
        columns = get_columns_from_cursor(cursor)
        row = cursor.fetchone()

        result = row_to_dict(row, columns) if row else None
        logger.debug(f"Query result: {result}")

        return result
        
    except Exception as e:
        logger.error(f"Error getting record from {table}. SQL: {sql}, Parameters: {list(query.values())}, Error: {str(e)}")
        return None
