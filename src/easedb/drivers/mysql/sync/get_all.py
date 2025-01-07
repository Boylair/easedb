"""Synchronous MySQL get all records operation."""

from typing import Any, Dict, List, Optional
import traceback

from easedb import logger

def get_all_records(connection: Any, table: str, query: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    """
    Retrieve all records from a MySQL database table.
    
    :param connection: Active database connection
    :param table: Name of the table to retrieve records from
    :param query: Optional dictionary of filter conditions
    :return: List of records matching the query
    """
    cursor = None
    try:
        # Create cursor with dictionary output
        cursor = connection.cursor(dictionary=True)
        
        # Construct base SQL query
        sql = f"SELECT * FROM {table}"

        
        # Add WHERE clause if query is provided
        params = []
        if query:
            conditions = []
            for key, value in query.items():
                conditions.append(f"{key} = %s")
                params.append(value)
            
            if conditions:
                sql += " WHERE " + " AND ".join(conditions)
        
        logger.info(f"Executing SQL: {sql} | Parameters: {params}")
        
        # Execute query
        if params:
            cursor.execute(sql, params)
        else:
            cursor.execute(sql)
        
        # Fetch all records
        records = cursor.fetchall()

        logger.info(f"Retrieved {len(records)} records from table {table}")
        
        return records
    
    except Exception as e:
        # Detailed error logging
        logger.error(f"Error retrieving records from table {table}: {e}")
        logger.trace(f"Detailed traceback: {traceback.format_exc()}")
        
        # Return an empty list in case of error
        return []
    
    finally:
        # Ensure cursor is closed
        try:
            if cursor:
                cursor.close()
        except Exception as close_error:
            logger.error(f"Error closing cursor: {close_error}")