"""Synchronous SQLite get_all operation."""

from typing import Any, Dict, List, Optional

from ..utils import row_to_dict, get_columns_from_cursor

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
        else:
            # Construct a parameterized query with the provided conditions
            where_clause = ' AND '.join([f"{k} = ?" for k in query.keys()])
            sql = f"SELECT * FROM {table} WHERE {where_clause}"
            params = list(query.values())
        
        cursor = connection.execute(sql, params)
        columns = get_columns_from_cursor(cursor)
        rows = cursor.fetchall()
        
        return [row_to_dict(row, columns) for row in rows]
            
    except Exception as e:
        print(f"Error getting all records: {e}")
        return []
