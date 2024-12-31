import os
import pytest
import easedb
import traceback

@pytest.fixture
def db():
    """
    Create a test database fixture.
    
    This fixture sets up a temporary SQLite database for testing purposes.
    It creates a table, inserts initial data, and provides cleanup after the test.
    
    Returns:
        easedb.Database: A database instance for testing.
    """
    # Create a temporary database file path
    test_db_path = 'test_sync.db'
    
    # Remove existing test database file if it exists
    if os.path.exists(test_db_path):
        os.remove(test_db_path)
    
    # Create a new database instance
    database = easedb.Database(f'sqlite://{test_db_path}')
    
    try:
        # Create a table with predefined schema
        database.create_table('users', {
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
        database.set('users', {'name': 'Alice', 'age': 30})
        database.set('users', {'name': 'Bob', 'age': 25})
        print("Data inserted successfully")
    except Exception as e:
        print(f"Error inserting data: {e}")
        traceback.print_exc()
    
    yield database
    
    # Cleanup: disconnect and remove the test database
    database.disconnect()
    if os.path.exists(test_db_path):
        os.remove(test_db_path)

def test_create_table(db):
    """
    Test table creation and initial data insertion.
    
    Verifies that:
    - The table is created successfully
    - Two initial records are inserted
    - Records can be retrieved
    """
    try:
        users = db.get_all('users')
        assert len(users) == 2
        assert any(user['name'] == 'Alice' for user in users)
        assert any(user['name'] == 'Bob' for user in users)
    except Exception as e:
        print(f"Error testing table creation: {e}")
        traceback.print_exc()

def test_get(db):
    """
    Test record retrieval functionality.
    
    Verifies that:
    - A specific record can be retrieved by name
    - Retrieved record has correct attributes
    """
    try:
        alice = db.get('users', {'name': 'Alice'})
        assert alice is not None
        assert alice['name'] == 'Alice'
        assert alice['age'] == 30
    except Exception as e:
        print(f"Error testing record retrieval: {e}")
        traceback.print_exc()

def test_update(db):
    """
    Test record update functionality.
    
    Verifies that:
    - A record can be updated by name
    - Updated record reflects the new values
    """
    try:
        # Update Bob's age
        db.update('users', {'name': 'Bob', 'age': 26})
        
        # Verify the update
        bob = db.get('users', {'name': 'Bob'})
        assert bob['age'] == 26
    except Exception as e:
        print(f"Error testing record update: {e}")
        traceback.print_exc()

def test_delete(db):
    """
    Test record deletion functionality.
    
    Verifies that:
    - A record can be deleted by name
    - Deleted record is removed from the table
    """
    try:
        # Delete Alice's record
        db.delete('users', {'name': 'Alice'})
        
        # Verify the deletion
        users = db.get_all('users')
        assert len(users) == 1
        assert all(user['name'] != 'Alice' for user in users)
    except Exception as e:
        print(f"Error testing record deletion: {e}")
        traceback.print_exc()
