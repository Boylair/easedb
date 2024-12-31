"""Asynchronous count method for SQLite database."""

from typing import Dict, Any, Optional
import aiosqlite

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
            async with connection.execute(f"SELECT COUNT(*) FROM {table}") as cursor:
                result = await cursor.fetchone()
                return result[0] if result else 0
        
        # Construct a parameterized query with the provided conditions
        where_clauses = [f"{k} = ?" for k in query.keys()]
        count_query = f"SELECT COUNT(*) FROM {table} WHERE {' AND '.join(where_clauses)}"
        
        async with connection.execute(count_query, list(query.values())) as cursor:
            result = await cursor.fetchone()
            return result[0] if result else 0
    
    except Exception as e:
        print(f"Error counting records: {e}")
        return 0
