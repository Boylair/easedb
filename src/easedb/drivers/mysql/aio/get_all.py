"""Asynchronous MySQL get all records operation."""

from typing import Any, Dict, List, Optional
import traceback

async def get_all_records(connection: Any, table: str, query: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    """
    Retrieve all records from a MySQL database table asynchronously.
    
    :param connection: Active database connection
    :param table: Name of the table to retrieve records from
    :param query: Optional dictionary of filter conditions
    :return: List of records matching the query
    """
    cursor = None
    try:
        # Create cursor with dictionary output
        cursor = await connection.cursor(dictionary=True)
        
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
        
        print(f"Executing SQL: {sql}")
        print(f"Query parameters: {params}")
        
        # Execute query
        if params:
            await cursor.execute(sql, params)
        else:
            await cursor.execute(sql)
        
        # Fetch all records
        records = await cursor.fetchall()
        
        print(f"Retrieved {len(records)} records")
        
        return records
    
    except Exception as e:
        # Detailed error logging
        print(f"Error in get_all_records: {e}")
        traceback.print_exc()
        return []
    finally:
        # Ensure cursor is closed
        if cursor:
            await cursor.close()
