"""Synchronous MySQL update operation."""

from typing import Any, Dict

from ....logger import logger

def update_record(connection: Any, table: str, query: Dict[str, Any], data: Dict[str, Any]) -> bool:
    """Update a record in MySQL database."""
    try:

        if not query:
            logger.error("No query provided for the update operation.")
            raise ValueError("Update requires a query to identify records")
        
        if not data:
            logger.error("No data provided for the update operation.")
            return False

        cursor = connection.cursor()
        
        # Construct the SET clause for update values
        set_clause = ', '.join([f"{k} = %s" for k in data.keys()])
        
        # Construct the WHERE clause for the query conditions
        where_clause = ' AND '.join([f"{k} = %s" for k in query.keys()])
        
        # Combine the SQL statement
        sql = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"
        
        # Combine values: first update values, then query conditions
        values = list(data.values()) + list(query.values())
        
        logger.info(f"Executing SQL: {sql} | Values: {values}")

        cursor.execute(sql, values)
        connection.commit()
        cursor.close()
        
        logger.info(f"Record updated successfully in {table}")

        return True
        
    except Exception:
        if connection:
            connection.rollback()
        logger.error(f"Error updating record in {table}: {e}")
        return False
