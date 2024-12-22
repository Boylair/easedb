import pytest
from easedb import Database, AsyncDatabase
import datetime
import decimal

# Test connection configurations
TEST_MYSQL_CONNECTION = 'mysql://user:password@host:port/db'
TEST_SQLITE_CONNECTION = 'sqlite:///test_database.db'

def test_mysql_basic_operations():
    """Test basic MySQL operations"""
    db = Database(TEST_MYSQL_CONNECTION)
    
    # Create table
    db.execute('DROP TABLE IF EXISTS test_users')
    db.execute('''
        CREATE TABLE test_users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            age INT,
            balance DECIMAL(10,2)
        )
    ''')
    
    # Insert record
    result = db.set('test_users', {
        'name': 'Test User',
        'age': 30,
        'balance': decimal.Decimal('1000.50')
    })
    assert result is True
    
    # Retrieve record
    user = db.get('test_users', {'name': 'Test User'})
    assert user['name'] == 'Test User'
    assert user['age'] == 30
    
    # Update record
    db.update('test_users', {'name': 'Test User'}, {'age': 31})
    updated_user = db.get('test_users', {'name': 'Test User'})
    assert updated_user['age'] == 31
    
    # Delete record
    db.delete('test_users', {'name': 'Test User'})
    deleted_user = db.get('test_users', {'name': 'Test User'})
    assert deleted_user is None

@pytest.mark.asyncio
async def test_mysql_async_operations():
    """Test basic async MySQL operations"""
    db = AsyncDatabase(TEST_MYSQL_CONNECTION)
    
    # Create table
    await db.execute('DROP TABLE IF EXISTS test_async_users')
    await db.execute('''
        CREATE TABLE test_async_users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            age INT,
            balance DECIMAL(10,2)
        )
    ''')
    
    # Insert record
    result = await db.set('test_async_users', {
        'name': 'Async Test User',
        'age': 25,
        'balance': decimal.Decimal('2000.75')
    })
    assert result is True
    
    # Retrieve record
    user = await db.get('test_async_users', {'name': 'Async Test User'})
    assert user['name'] == 'Async Test User'
    assert user['age'] == 25
    
    # Update record
    await db.update('test_async_users', {'name': 'Async Test User'}, {'age': 26})
    updated_user = await db.get('test_async_users', {'name': 'Async Test User'})
    assert updated_user['age'] == 26
    
    # Delete record
    await db.delete('test_async_users', {'name': 'Async Test User'})
    deleted_user = await db.get('test_async_users', {'name': 'Async Test User'})
    assert deleted_user is None

def test_sqlite_basic_operations():
    """Test basic SQLite operations"""
    db = Database(TEST_SQLITE_CONNECTION)
    
    # Create table
    db.execute('DROP TABLE IF EXISTS test_sqlite_users')
    db.execute('''
        CREATE TABLE test_sqlite_users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            balance REAL
        )
    ''')
    
    # Insert record
    result = db.set('test_sqlite_users', {
        'name': 'SQLite User',
        'age': 40,
        'balance': 1500.25
    })
    assert result is True
    
    # Retrieve record
    user = db.get('test_sqlite_users', {'name': 'SQLite User'})
    assert user['name'] == 'SQLite User'
    assert user['age'] == 40
    
    # Update record
    db.update('test_sqlite_users', {'name': 'SQLite User'}, {'age': 41})
    updated_user = db.get('test_sqlite_users', {'name': 'SQLite User'})
    assert updated_user['age'] == 41
    
    # Delete record
    db.delete('test_sqlite_users', {'name': 'SQLite User'})
    deleted_user = db.get('test_sqlite_users', {'name': 'SQLite User'})
    assert deleted_user is None
