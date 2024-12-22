import datetime
import decimal
from easedb import Database

def mysql_crud_example():
    """Detailed MySQL CRUD Operations Demonstration"""
    # Create MySQL database connection
    db = Database('your_database_connection_string')
    
    # Create table
    db.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            age INT,
            salary DECIMAL(10,2),
            hire_date DATETIME,
            is_active BOOLEAN DEFAULT TRUE
        )
    ''')
    
    # Create (Insert) - Add a new employee
    print("1. Inserting a new employee:")
    result = db.set('employees', {
        'name': 'John Smith',
        'age': 35,
        'salary': decimal.Decimal('75000.50'),
        'hire_date': datetime.datetime.now(),
        'is_active': True
    })
    print(f"Insertion successful: {result}\n")
    
    # Read - Retrieve an employee
    print("2. Retrieving an employee:")
    employee = db.get('employees', {'name': 'John Smith'})
    print(f"Employee details: {employee}\n")
    
    # Update - Modify employee details
    print("3. Updating employee details:")
    db.update('employees', 
        {'name': 'John Smith'}, 
        {'salary': decimal.Decimal('80000.75'), 'age': 36}
    )
    updated_employee = db.get('employees', {'name': 'John Smith'})
    print(f"Updated employee: {updated_employee}\n")
    
    # Complex Query
    print("4. Complex query:")
    active_senior_employees = db.get_all('employees', {
        'is_active': True,
        'age': {'>=': 30},
        'salary': {'>': decimal.Decimal('70000')}
    }, order_by='salary DESC', limit=5)
    print(f"Active senior employees (top 5 by salary): {active_senior_employees}\n")
    
    # Delete
    print("5. Deleting an employee:")
    db.delete('employees', {'name': 'John Smith'})
    deleted_employee = db.get('employees', {'name': 'John Smith'})
    print(f"Deleted employee: {deleted_employee}\n")

if __name__ == '__main__':
    mysql_crud_example()
