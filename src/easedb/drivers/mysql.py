import asyncio
import aiomysql
import pymysql
from typing import Any, Dict, List, Optional, Union
from ..base import DatabaseDriver
from ..async_base import AsyncDatabaseDriver
from urllib.parse import urlparse
from abc import ABC, abstractmethod

class MySQLDriver(DatabaseDriver):
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.conn_params = self._parse_connection_string(connection_string)
        self.connection = None
        self.cursor = None
    
    def _parse_connection_string(self, connection_string: str) -> Dict[str, str]:
        url = urlparse(connection_string)
        return {
            'host': url.hostname or 'localhost',
            'port': url.port or 3306,
            'user': url.username,
            'password': url.password,
            'database': url.path.lstrip('/'),
        }
    
    def connect(self):
        """Explicit connection method"""
        self.connection = pymysql.connect(**self.conn_params, cursorclass=pymysql.cursors.DictCursor)
        self.cursor = self.connection.cursor()
    
    def disconnect(self):
        """Explicit disconnection method"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
    
    def __enter__(self):
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()
    
    def _convert_value(self, value: Any) -> Any:
        """Konvertálja az értékeket a megfelelő Python típusokra"""
        if isinstance(value, int) and value in (0, 1):
            return bool(value)
        return value
    
    def get(self, table: str, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        conditions = ' AND '.join([f"{k} = %s" for k in query.keys()])
        sql = f"SELECT * FROM {table} WHERE {conditions} LIMIT 1"
        self.cursor.execute(sql, list(query.values()))
        result = self.cursor.fetchone()
        if result:
            return {k: self._convert_value(v) for k, v in result.items()}
        return None
    
    def get_all(self, table: str, query: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        try:
            if query:
                conditions = ' AND '.join([f"{k} = %s" for k in query.keys()])
                sql = f"SELECT * FROM {table} WHERE {conditions}"
                self.cursor.execute(sql, list(query.values()))
            else:
                sql = f"SELECT * FROM {table}"
                self.cursor.execute(sql)
            result = self.cursor.fetchall()
            return [{k: self._convert_value(v) for k, v in row.items()} for row in result] if result else []
        except Exception as e:
            print(f"Error in get_all: {e}")
            return []
    
    def set(self, table: str, data: Dict[str, Any]) -> bool:
        try:
            columns = ', '.join(data.keys())
            placeholders = ', '.join(['%s'] * len(data))
            sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
            self.cursor.execute(sql, list(data.values()))
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error in set: {e}")
            self.connection.rollback()
            return False
    
    def update(self, table: str, query: Dict[str, Any], data: Dict[str, Any]) -> bool:
        try:
            set_values = ', '.join([f"{k} = %s" for k in data.keys()])
            conditions = ' AND '.join([f"{k} = %s" for k in query.keys()])
            sql = f"UPDATE {table} SET {set_values} WHERE {conditions}"
            params = list(data.values()) + list(query.values())
            self.cursor.execute(sql, params)
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error in update: {e}")
            self.connection.rollback()
            return False
    
    def delete(self, table: str, query: Dict[str, Any]) -> bool:
        try:
            conditions = ' AND '.join([f"{k} = %s" for k in query.keys()])
            sql = f"DELETE FROM {table} WHERE {conditions}"
            self.cursor.execute(sql, list(query.values()))
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error in delete: {e}")
            self.connection.rollback()
            return False
    
    def execute(self, query: str, params: Optional[Union[tuple, Dict[str, Any]]] = None) -> Any:
        try:
            self.cursor.execute(query, params or ())
            if query.strip().upper().startswith('SELECT'):
                return list(self.cursor.fetchall())
            else:
                self.connection.commit()
                return True
        except Exception as e:
            print(f"Error in execute: {e}")
            self.connection.rollback()
            return False

class AsyncMySQLDriver(AsyncDatabaseDriver):
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.conn_params = self._parse_connection_string(connection_string)
        self.pool = None
    
    def _parse_connection_string(self, connection_string: str) -> Dict[str, str]:
        url = urlparse(connection_string)
        return {
            'host': url.hostname or 'localhost',
            'port': url.port or 3306,
            'user': url.username,
            'password': url.password,
            'db': url.path.lstrip('/'),
        }
    
    async def connect(self):
        """Explicit async connection method"""
        self.pool = await aiomysql.create_pool(**self.conn_params, cursorclass=aiomysql.DictCursor)
    
    async def disconnect(self):
        """Explicit async disconnection method"""
        if self.pool:
            self.pool.close()
            await self.pool.wait_closed()
    
    async def __aenter__(self):
        await self.connect()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.disconnect()
    
    async def _convert_value(self, value: Any) -> Any:
        """Konvertálja az értékeket a megfelelő Python típusokra"""
        if isinstance(value, int) and value in (0, 1):
            return bool(value)
        return value
    
    async def get(self, table: str, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                conditions = ' AND '.join([f"{k} = %s" for k in query.keys()])
                sql = f"SELECT * FROM {table} WHERE {conditions} LIMIT 1"
                await cur.execute(sql, list(query.values()))
                result = await cur.fetchone()
                if result:
                    return {k: await self._convert_value(v) for k, v in result.items()}
                return None
    
    async def get_all(self, table: str, query: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                try:
                    if query:
                        conditions = ' AND '.join([f"{k} = %s" for k in query.keys()])
                        sql = f"SELECT * FROM {table} WHERE {conditions}"
                        await cur.execute(sql, list(query.values()))
                    else:
                        sql = f"SELECT * FROM {table}"
                        await cur.execute(sql)
                    result = await cur.fetchall()
                    return [{k: await self._convert_value(v) for k, v in row.items()} for row in result] if result else []
                except Exception as e:
                    print(f"Error in async get_all: {e}")
                    return []
    
    async def set(self, table: str, data: Dict[str, Any]) -> bool:
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                try:
                    columns = ', '.join(data.keys())
                    placeholders = ', '.join(['%s'] * len(data))
                    sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
                    await cur.execute(sql, list(data.values()))
                    await conn.commit()
                    return True
                except Exception as e:
                    print(f"Error in async set: {e}")
                    await conn.rollback()
                    return False
    
    async def update(self, table: str, query: Dict[str, Any], data: Dict[str, Any]) -> bool:
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                try:
                    set_values = ', '.join([f"{k} = %s" for k in data.keys()])
                    conditions = ' AND '.join([f"{k} = %s" for k in query.keys()])
                    sql = f"UPDATE {table} SET {set_values} WHERE {conditions}"
                    params = list(data.values()) + list(query.values())
                    await cur.execute(sql, params)
                    await conn.commit()
                    return True
                except Exception as e:
                    print(f"Error in async update: {e}")
                    await conn.rollback()
                    return False
    
    async def delete(self, table: str, query: Dict[str, Any]) -> bool:
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                try:
                    conditions = ' AND '.join([f"{k} = %s" for k in query.keys()])
                    sql = f"DELETE FROM {table} WHERE {conditions}"
                    await cur.execute(sql, list(query.values()))
                    await conn.commit()
                    return True
                except Exception as e:
                    print(f"Error in async delete: {e}")
                    await conn.rollback()
                    return False
    
    async def execute(self, query: str, params: Optional[Union[tuple, Dict[str, Any]]] = None) -> Any:
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                try:
                    await cur.execute(query, params or ())
                    if query.strip().upper().startswith('SELECT'):
                        result = await cur.fetchall()
                        return list(result) if result else []
                    else:
                        await conn.commit()
                        return True
                except Exception as e:
                    print(f"Error in async execute: {e}")
                    await conn.rollback()
                    return False
