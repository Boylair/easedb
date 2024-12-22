import sqlite3
import aiosqlite
from typing import Any, Dict, List, Optional, Union
from ..base import DatabaseDriver
from ..async_base import AsyncDatabaseDriver
from urllib.parse import urlparse

class SQLiteDriver(DatabaseDriver):
    def __init__(self, connection_string: str):
        self.database_path = self._parse_connection_string(connection_string)
        self.connection = None
        self.cursor = None
    
    def _parse_connection_string(self, connection_string: str) -> str:
        url = urlparse(connection_string)
        return url.path.lstrip('/')
    
    def connect(self) -> None:
        self.connection = sqlite3.connect(self.database_path)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()
    
    def disconnect(self) -> None:
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
    
    def get(self, table: str, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        conditions = ' AND '.join([f"{k} = ?" for k in query.keys()])
        sql = f"SELECT * FROM {table} WHERE {conditions} LIMIT 1"
        self.cursor.execute(sql, list(query.values()))
        row = self.cursor.fetchone()
        return dict(row) if row else None
    
    def get_all(self, table: str, query: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        if query:
            conditions = ' AND '.join([f"{k} = ?" for k in query.keys()])
            sql = f"SELECT * FROM {table} WHERE {conditions}"
            self.cursor.execute(sql, list(query.values()))
        else:
            sql = f"SELECT * FROM {table}"
            self.cursor.execute(sql)
        return [dict(row) for row in self.cursor.fetchall()]
    
    def set(self, table: str, data: Dict[str, Any]) -> bool:
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?'] * len(data))
        sql = f"INSERT OR REPLACE INTO {table} ({columns}) VALUES ({placeholders})"
        try:
            self.cursor.execute(sql, list(data.values()))
            self.connection.commit()
            return True
        except Exception:
            self.connection.rollback()
            return False
    
    def delete(self, table: str, query: Dict[str, Any]) -> bool:
        conditions = ' AND '.join([f"{k} = ?" for k in query.keys()])
        sql = f"DELETE FROM {table} WHERE {conditions}"
        try:
            self.cursor.execute(sql, list(query.values()))
            self.connection.commit()
            return True
        except Exception:
            self.connection.rollback()
            return False
    
    def execute(self, query: str, params: Optional[Union[tuple, Dict[str, Any]]] = None) -> Any:
        try:
            self.cursor.execute(query, params or ())
            if query.strip().upper().startswith('SELECT'):
                return [dict(row) for row in self.cursor.fetchall()]
            else:
                self.connection.commit()
                return True
        except Exception:
            self.connection.rollback()
            return False

class AsyncSQLiteDriver(AsyncDatabaseDriver):
    def __init__(self, connection_string: str):
        self.database_path = self._parse_connection_string(connection_string)
        self.connection = None
    
    def _parse_connection_string(self, connection_string: str) -> str:
        url = urlparse(connection_string)
        return url.path.lstrip('/')
    
    async def connect(self) -> None:
        self.connection = await aiosqlite.connect(self.database_path)
        self.connection.row_factory = aiosqlite.Row
    
    async def disconnect(self) -> None:
        if self.connection:
            await self.connection.close()
    
    async def get(self, table: str, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        conditions = ' AND '.join([f"{k} = ?" for k in query.keys()])
        sql = f"SELECT * FROM {table} WHERE {conditions} LIMIT 1"
        async with self.connection.execute(sql, list(query.values())) as cursor:
            row = await cursor.fetchone()
            return dict(row) if row else None
    
    async def get_all(self, table: str, query: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        if query:
            conditions = ' AND '.join([f"{k} = ?" for k in query.keys()])
            sql = f"SELECT * FROM {table} WHERE {conditions}"
            async with self.connection.execute(sql, list(query.values())) as cursor:
                rows = await cursor.fetchall()
        else:
            sql = f"SELECT * FROM {table}"
            async with self.connection.execute(sql) as cursor:
                rows = await cursor.fetchall()
        return [dict(row) for row in rows]
    
    async def set(self, table: str, data: Dict[str, Any]) -> bool:
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?'] * len(data))
        sql = f"INSERT OR REPLACE INTO {table} ({columns}) VALUES ({placeholders})"
        try:
            await self.connection.execute(sql, list(data.values()))
            await self.connection.commit()
            return True
        except Exception:
            await self.connection.rollback()
            return False
    
    async def delete(self, table: str, query: Dict[str, Any]) -> bool:
        conditions = ' AND '.join([f"{k} = ?" for k in query.keys()])
        sql = f"DELETE FROM {table} WHERE {conditions}"
        try:
            await self.connection.execute(sql, list(query.values()))
            await self.connection.commit()
            return True
        except Exception:
            await self.connection.rollback()
            return False
    
    async def execute(self, query: str, params: Optional[Union[tuple, Dict[str, Any]]] = None) -> Any:
        try:
            async with self.connection.execute(query, params or ()) as cursor:
                if query.strip().upper().startswith('SELECT'):
                    rows = await cursor.fetchall()
                    return [dict(row) for row in rows]
                else:
                    await self.connection.commit()
                    return True
        except Exception:
            await self.connection.rollback()
            return False
