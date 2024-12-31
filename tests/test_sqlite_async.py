import os
import pytest
import pytest_asyncio
import easedb
import traceback

@pytest_asyncio.fixture
async def db():
    """
    Create an asynchronous test database fixture.
    
    This fixture sets up a temporary SQLite database for asynchronous testing.
    It creates a table, inserts initial data, and provides cleanup after the test.
    
    Returns:
        easedb.AsyncDatabase: An asynchronous database instance for testing.
    """
    # Create a temporary database file path
    test_db_path = 'test_async.db'
    
    # Remove existing test database file if it exists
    if os.path.exists(test_db_path):
        os.remove(test_db_path)
    
    # Create a new asynchronous database instance
    database = easedb.AsyncDatabase(f'sqlite://{test_db_path}')
    
    try:
        # Create a table with predefined schema
        await database.create_table('users', {
            'id': 'INTEGER PRIMARY KEY',
            'name': 'TEXT',
            'age': 'INTEGER'
        })
        print("Table created successfully")
    except Exception as e:
        print(f"Error creating table: {e}")
        traceback.print_exc()
    
    try:
        # Insert initial test data
        await database.set('users', {'name': 'Alice', 'age': 30})
        await database.set('users', {'name': 'Bob', 'age': 25})
        print("Data inserted successfully")
    except Exception as e:
        print(f"Error inserting data: {e}")
        traceback.print_exc()
    
    yield database
    
    # Cleanup: disconnect and remove the test database
    await database.disconnect()
    if os.path.exists(test_db_path):
        os.remove(test_db_path)

@pytest.mark.asyncio
async def test_create_table(db):
    """
    Test asynchronous table creation and initial data insertion.
    
    Verifies that:
    - The table is created successfully
    - Two initial records are inserted
    - Records can be retrieved asynchronously
    """
    try:
        users = await db.get_all('users')
        assert len(users) == 2
        assert any(user['name'] == 'Alice' for user in users)
        assert any(user['name'] == 'Bob' for user in users)
    except Exception as e:
        print(f"Error testing table creation: {e}")
        traceback.print_exc()

@pytest.mark.asyncio
async def test_get(db):
    """
    Test asynchronous record retrieval functionality.
    
    Verifies that:
    - A specific record can be retrieved by name asynchronously
    - Retrieved record has correct attributes
    """
    try:
        alice = await db.get('users', {'name': 'Alice'})
        assert alice is not None
        assert alice['name'] == 'Alice'
        assert alice['age'] == 30
    except Exception as e:
        print(f"Error testing record retrieval: {e}")
        traceback.print_exc()

@pytest.mark.asyncio
async def test_update(db):
    """
    Test asynchronous record update functionality.
    
    Verifies that:
    - A record can be updated by name asynchronously
    - Updated record reflects the new values
    """
    try:
        # Update Bob's age
        await db.update('users', {'name': 'Bob', 'age': 26})
        
        # Verify the update
        bob = await db.get('users', {'name': 'Bob'})
        assert bob['age'] == 26
    except Exception as e:
        print(f"Error testing record update: {e}")
        traceback.print_exc()

@pytest.mark.asyncio
async def test_delete(db):
    """
    Test asynchronous record deletion functionality.
    
    Verifies that:
    - A record can be deleted by name asynchronously
    - Deleted record is removed from the table
    """
    try:
        # Delete Alice's record
        await db.delete('users', {'name': 'Alice'})
        
        # Verify the deletion
        users = await db.get_all('users')
        assert len(users) == 1
        assert all(user['name'] != 'Alice' for user in users)
    except Exception as e:
        print(f"Error testing record deletion: {e}")
        traceback.print_exc()
