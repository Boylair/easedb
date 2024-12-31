"""Synchronous MySQL create table operation."""

from typing import Any, Dict

def create_table(connection: Any, table: str, schema: Dict[str, str], 
                 primary_key: str = 'id', 
                 auto_increment: bool = True,
                 if_not_exists: bool = True) -> bool:
    """
    Create a table in MySQL database.
    
    Args:
        connection: MySQL database connection
        table: Name of the table to create
        schema: Dictionary of column names and their SQL types
        primary_key: Name of the primary key column (default 'id')
        auto_increment: Whether to make the primary key auto-increment (default True)
        if_not_exists: Whether to use IF NOT EXISTS clause (default True)
    
    Returns:
        bool: True if table creation was successful, False otherwise
    """
    try:
        cursor = connection.cursor()
        
        # Construct column definitions
        column_defs = []
        for col_name, col_type in schema.items():
            col_def = f"`{col_name}` {col_type}"
            
            # Handle primary key with auto-increment
            if col_name == primary_key and auto_increment:
                col_def += " PRIMARY KEY AUTO_INCREMENT"
            
            column_defs.append(col_def)
        
        # Combine column definitions
        columns_str = ", ".join(column_defs)
        
        # Construct SQL statement
        if if_not_exists:
            sql = f"CREATE TABLE IF NOT EXISTS `{table}` ({columns_str})"
        else:
            sql = f"CREATE TABLE `{table}` ({columns_str})"
        
        # Execute table creation
        cursor.execute(sql)
        connection.commit()
        cursor.close()
        
        return True
    
    except Exception:
        if connection:
            connection.rollback()
        return False