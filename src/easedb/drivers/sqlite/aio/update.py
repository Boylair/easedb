"""Asynchronous SQLite update operation."""

from typing import Any, Dict

async def update_record(connection: Any, table: str, query: Dict[str, Any], data: Dict[str, Any]) -> bool:
    """Update a record in SQLite database asynchronously."""
    try:
        # Ha nincs query, nem tudjuk, mit frissítsünk
        if not query:
            raise ValueError("Update requires a query to identify records")
        
        # Ha nincs adat, nem történik frissítés
        if not data:
            return False
        
        # Lekérdezési feltétel összeállítása
        where_clause = ' AND '.join([f"{k} = ?" for k in query.keys()])
        set_clause = ', '.join([f"{k} = ?" for k in data.keys()])
        
        # SQL lekérdezés összeállítása
        sql = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"
        
        # Értékek összeállítása
        values = list(data.values()) + list(query.values())
        
        # Lekérdezés végrehajtása
        async with connection.execute(sql, values) as cursor:
            await connection.commit()
        
        return True
        
    except Exception as e:
        if connection:
            await connection.rollback()
        print(f"Error updating record: {e}")
        return False
