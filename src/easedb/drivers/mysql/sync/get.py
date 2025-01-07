"""Synchronous MySQL get operation."""

from typing import Any, Dict, Optional

from ..utils import row_to_dict, get_columns_from_cursor
from ....logger import logger

def get_record(connection: Any, table: str, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Get a record from MySQL database."""
    try:
        cursor = connection.cursor()
        where_clause = ' AND '.join([f"{k} = %s" for k in query.keys()])
        sql = f"SELECT * FROM {table} WHERE {where_clause}"

        logger.info(f"Executing SQL: {sql} | Parameters: {list(query.values())}")
        
        cursor.execute(sql, list(query.values()))
        columns = get_columns_from_cursor(cursor)
        row = cursor.fetchone()
        cursor.close()

        if row:
            logger.info(f"Record retrieved: {row}")
        else:
            logger.info(f"No record found for query: {query}")
        
        return row_to_dict(row, columns) if row else None
        
    except Exception as e:
        # Log the error
        logger.error(f"Error retrieving record from table {table}: {e}")
        return None
