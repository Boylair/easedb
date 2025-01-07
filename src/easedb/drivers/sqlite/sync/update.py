"""Synchronous SQLite update operation."""

from typing import Any, Dict

def update_record(connection: Any, table: str, query: Dict[str, Any], data: Dict[str, Any]) -> bool:
    """Update a record in SQLite database."""
    try:
        # If no query is provided, we cannot determine what to update
        if not query:
            raise ValueError("Update requires a query to identify records")
        
        # If no data is provided, no update will occur
        if not data:
            logger.info(f"No data provided to update for table {table} with query: {query}")
            return False
        
        # Construct the query condition
        where_clause = ' AND '.join([f"{k} = ?" for k in query.keys()])
        set_clause = ', '.join([f"{k} = ?" for k in data.keys()])
        
        # Construct SQL query
        sql = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"
        
        # Prepare values
        values = list(data.values()) + list(query.values())

        logger.info(f"Attempting to update record in {table}. SQL: {sql}, Query Parameters: {list(query.values())}, Data: {list(data.values())}")
        
        # Execute query
        connection.execute(sql, values)
        connection.commit()

        logger.info(f"Successfully updated record in {table}. SQL: {sql}, Query Parameters: {list(query.values())}, Data: {list(data.values())}")

        return True
        
    except Exception as e:
        if connection:
            connection.rollback()
        logger.error(f"Error updating record in {table}. SQL: {sql}, Query Parameters: {list(query.values())}, Data: {list(data.values())}, Error: {str(e)}")
        return False
