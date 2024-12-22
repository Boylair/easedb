# EaseDB 🚀

## Fast, Simple, Reliable — Database Management Made Easy

EaseDB is a powerful, lightweight database management library designed to simplify database interactions in Python. It provides a clean, intuitive API that supports both synchronous and asynchronous operations across multiple database backends.

## 🌟 Key Features

- 🔄 Full Sync and Async Support
- 🗃️ Multi-Database Backend Compatibility
  - MySQL/MariaDB
  - SQLite
  - PostgreSQL (Coming Soon)
- 🚀 Simple, Pythonic API
- 🔒 Safe Connection Management
- 📦 Lightweight and Efficient

## 🚀 Quick Installation

```bash
pip install easedb
```

## 💡 Usage Examples

### Synchronous Database Operations (SQLite)

#### Basic Operation

```python
from easedb import Database

# Create a database connection
db = Database('sqlite:///example.db')

# Insert a record
db.set('users', {
    'name': 'John Doe',
    'age': 30,
    'email': 'john@example.com'
})

# Retrieve a record
user = db.get('users', {'name': 'John Doe'})
print(user)
```

### Synchronous MySQL Database Operations

#### Table Creation and Basic CRUD Operations

```python
from easedb import Database
import datetime
import decimal

# Create MySQL database connection
db = Database('mysql://user:password@localhost/database')

# Create a table
db.create_table('employees', {
    'id': 'INT AUTO_INCREMENT PRIMARY KEY',
    'name': 'VARCHAR(100) NOT NULL',
    'age': 'INT',
    'salary': 'DECIMAL(10,2)',
    'hire_date': 'DATETIME',
    'is_active': 'BOOLEAN DEFAULT TRUE'
})

# Insert a record
db.set('employees', {
    'name': 'Peter Smith',
    'age': 35,
    'salary': decimal.Decimal('75000.50'),
    'hire_date': datetime.datetime.now(),
    'is_active': True
})

# Retrieve a record
employee = db.get('employees', {'name': 'Peter Smith'})
print("Employee details:", employee)

# Retrieve multiple records
all_employees = db.get_all('employees')
print("All employees:", all_employees)

# Update a record
db.update('employees', 
    {'name': 'Peter Smith'}, 
    {'salary': decimal.Decimal('80000.75')}
)

# Delete a record
db.delete('employees', {'name': 'Peter Smith'})
```

#### Complex Queries

```python
# Query with complex conditions
active_senior_employees = db.get_all('employees', {
    'is_active': True, 
    'age': {'>=': 30}
})

# Sorting and limiting results
top_5_salaries = db.get_all('employees', 
    order_by='salary DESC', 
    limit=5
)
```

### Direct SQL Execution

#### Raw SQL Commands and Advanced Operations

```python
from easedb import Database
import datetime

# Create a database connection
db = Database('mysql://user:password@localhost/database')

# Create a complex table with a single execute command
db.execute('''
    CREATE TABLE IF NOT EXISTS advanced_users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        registration_date DATETIME,
        last_login DATETIME,
        login_count INT DEFAULT 0,
        account_status ENUM('active', 'inactive', 'suspended') DEFAULT 'active',
        total_purchases DECIMAL(10,2) DEFAULT 0.00
    )
''')

# Insert multiple records using execute
db.execute('''
    INSERT INTO advanced_users 
    (username, email, registration_date, last_login, login_count, account_status, total_purchases)
    VALUES 
    ('john_doe', 'john@example.com', %s, %s, 5, 'active', 1250.75),
    ('jane_smith', 'jane@example.com', %s, %s, 12, 'active', 3500.25)
''', (
    datetime.datetime.now(), 
    datetime.datetime.now(),
    datetime.datetime.now(), 
    datetime.datetime.now()
))

# Complex query with joins and aggregations
result = db.execute('''
    SELECT 
        u.username, 
        u.email, 
        COUNT(p.id) as purchase_count, 
        SUM(p.amount) as total_spent
    FROM 
        advanced_users u
    LEFT JOIN 
        purchases p ON u.id = p.user_id
    GROUP BY 
        u.id, u.username, u.email
    HAVING 
        total_spent > 1000
    ORDER BY 
        total_spent DESC
    LIMIT 10
''')

# Iterate through results
for row in result:
    print(f"Username: {row['username']}, Total Spent: {row['total_spent']}")

# Transaction example
try:
    db.execute('START TRANSACTION')
    
    # Multiple related operations
    db.execute('UPDATE accounts SET balance = balance - 500 WHERE id = 1')
    db.execute('UPDATE accounts SET balance = balance + 500 WHERE id = 2')
    
    db.execute('COMMIT')
except Exception as e:
    db.execute('ROLLBACK')
    print(f"Transaction failed: {e}")
```

#### Batch Operations and Prepared Statements

```python
# Batch insert with prepared statement
users_data = [
    ('alice', 'alice@example.com'),
    ('bob', 'bob@example.com'),
    ('charlie', 'charlie@example.com')
]

db.execute(
    'INSERT INTO users (username, email) VALUES (%s, %s)', 
    users_data
)
```

### Asynchronous Database Operations (MySQL)

```python
from easedb import AsyncDatabase
import asyncio
import datetime
import decimal

async def main():
    # Create an async database connection
    db = AsyncDatabase('mysql://user:password@localhost/database')
    
    # Create a table
    await db.create_table('products', {
        'id': 'INT AUTO_INCREMENT PRIMARY KEY',
        'name': 'VARCHAR(100) NOT NULL',
        'price': 'DECIMAL(10,2)',
        'created_at': 'DATETIME',
        'is_active': 'BOOLEAN DEFAULT TRUE'
    })
    
    # Insert a record
    await db.set('products', {
        'name': 'Laptop',
        'price': decimal.Decimal('1250.00'),
        'created_at': datetime.datetime.now(),
        'is_active': True
    })
    
    # Retrieve a record
    product = await db.get('products', {'name': 'Laptop'})
    print("Product details:", product)

asyncio.run(main())
```

## 🛠️ Advanced Features

- CRUD Operations
- Async and Sync Support
- Multiple Database Type Support
- Automatic Connection Management
- Error Handling and Retry Mechanisms
- Query Builder (Planned)
- Connection Pooling (Planned)

## 🧪 Testing

We use `pytest` for comprehensive testing.

### Running Tests

```bash
# Install test dependencies
pip install -r requirements.txt

# Run all tests
pytest

# Generate coverage report
pytest --cov=src/easedb
```

## 🤝 Contributing

Contributions are welcome! Please check our issues page or submit a pull request.

## 📄 License

MIT

## 🌐 Links

- GitHub Repository: https://github.com/Boylair/easydb 
- Documentation: https://github.com/Boylair/easydb/blob/main/docs/en/getting_started.md
- Issue Tracker: https://github.com/Boylair/easydb/issues

