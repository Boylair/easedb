from typing import Any, Dict, Optional, Union
import traceback

from easedb.logger.logger import logger

async def sub_record(connection: Any, table: str, query: Dict[str, Any], value: Union[int, float], column: str = 'value') -> bool:
    """
    Subtract a specified value from an existing numeric column in the database.
    
    :param connection: Active database connection
    :param table: Name of the table to update
    :param query: Dictionary specifying which record(s) to update
    :param value: Numeric value to subtract from the existing value
    :param column: Name of the column to update (default: 'value')
    :return: True if update was successful, False otherwise
    """
    try:
        # Ellenőrzés, hogy a kivonandó érték numerikus-e
        if not isinstance(value, (int, float)):
            logger.error(f"Invalid value type. Must be int or float, got {type(value)}")
            return False
        
        # Ellenőrzés, hogy van-e legalább egy query feltétel
        if not query:
            logger.error("No query conditions provided to identify record(s)")
            return False
        
        cursor = await connection.cursor()
        
        # Konstruáljuk meg a WHERE záradékot a query alapján
        where_clause = ' AND '.join([f"{k} = %s" for k in query.keys()])
        
        # SQL utasítás, amely kivon egy értéket egy numerikus oszlopból
        sql = f"UPDATE {table} SET {column} = {column} - %s WHERE {where_clause}"
        
        # Kombináljuk a paramétereket
        params = [value] + list(query.values())
        
        logger.info(f"Executing SQL: {sql} | Parameters: {params}")
        
        await cursor.execute(sql, params)
        await connection.commit()
        
        await cursor.close()
        
        logger.info(f"Successfully subtracted {value} from {column} in record(s) in {table}")
        
        return True
        
    except Exception as e:
        if connection:
            await connection.rollback()
        logger.error(f"Error subtracting value from record in {table}. Error: {str(e)} | Traceback: {traceback.format_exc()}")
        return False
