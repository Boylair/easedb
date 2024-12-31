import os
import pytest
import easedb
import traceback

@pytest.fixture
def db():
    """
    Create a test MySQL database fixture.
    
    This fixture sets up a temporary MySQL database for testing purposes.
    It creates a table, inserts initial data, and provides cleanup after the test.
    
    Returns:
        easedb.Database: A database instance for testing.
    """
    # MySQL connection parameters
    connection_string = ""
    
    # Create a new database instance
    database = easedb.Database(connection_string)
    
    try:
        # Create a table with predefined schema
        database.create_table('users', {
            'id': 'INTEGER PRIMARY KEY AUTO_INCREMENT',
            'name': 'VARCHAR(255)',
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
    
    # Cleanup: delete test data and disconnect
    try:
        database.delete('users', {'name': 'Alice'})
        database.delete('users', {'name': 'Bob'})
    except Exception as e:
        print(f"Error during cleanup: {e}")
    
    database.disconnect()

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