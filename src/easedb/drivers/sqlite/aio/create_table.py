"""Asynchronous SQLite create table operation."""

from typing import Any, Dict, Optional

from ....logger import logger

async def create_table(connection: Any, table: str, schema: Dict[str, str], 
                       primary_key: Optional[str] = None, 
                       auto_increment: bool = True,
                       if_not_exists: bool = True) -> bool:
    """
    Create a table in SQLite database asynchronously.
    
    Args:
        connection: SQLite database connection
        table: Name of the table to create
        schema: Dictionary of column names and their SQL types
        primary_key: Optional name of the primary key column (default None)
        auto_increment: Whether to make the primary key auto-increment (default True)
        if_not_exists: Whether to use IF NOT EXISTS clause (default True)
    
    Returns:
        bool: True if table creation was successful, False otherwise
    """
    try:
        async with connection.cursor() as cursor:
            # Construct column definitions
            column_defs = []
            for col_name, col_type in schema.items():
                col_def = f"`{col_name}` {col_type}"
                
                # Add PRIMARY KEY AUTOINCREMENT only if it's the primary key
                if primary_key == col_name:
                    if auto_increment:
                        col_def = f"`{col_name}` INTEGER PRIMARY KEY AUTOINCREMENT"
                    else:
                        col_def += " PRIMARY KEY"
                
                column_defs.append(col_def)
            
            # Combine column definitions
            columns_str = ", ".join(column_defs)
            
            # Construct SQL statement
            if if_not_exists:
                sql = f"CREATE TABLE IF NOT EXISTS `{table}` ({columns_str})"
            else:
                sql = f"CREATE TABLE `{table}` ({columns_str})"

            logger.debug(f"Executing table creation query: {sql}")
            
            # Execute table creation
            await cursor.execute(sql)
        
        logger.info(f"Table '{table}' created successfully.")
        
        return True
    
    except Exception:
        logger.error(f"Error creating table '{table}': {e}")
        logger.trace(f"Failed table creation query: {sql}")
        return False
