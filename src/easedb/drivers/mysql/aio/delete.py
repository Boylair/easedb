"""Asynchronous MySQL delete operation."""

from typing import Any, Dict

from ....logger import logger

async def delete_record(connection: Any, table: str, query: Dict[str, Any]) -> bool:
    """Delete a record from MySQL database asynchronously."""
    try:
        cursor = await connection.cursor()
        where_clause = ' AND '.join([f"{k} = %s" for k in query.keys()])
        sql = f"DELETE FROM {table} WHERE {where_clause}"
        
        logger.info(f"Attempting to delete record from {table}. SQL: {sql}, Parameters: {list(query.values())}")

        await cursor.execute(sql, list(query.values()))
        await connection.commit()
        await cursor.close()
        
        logger.info(f"Successfully deleted record from {table}. SQL: {sql}, Parameters: {list(query.values())}")

        return True
        
    except Exception as e:
        if connection:
            await connection.rollback()
        logger.error(f"Error deleting record from {table}. Error: {str(e)}")
        return False
