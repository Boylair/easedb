# Table Management

## Overview
EaseDB provides flexible methods for creating, modifying, and managing database tables.

## Creating Tables
### Using `create_table()` Method
```python
# Basic Table Creation
db.create_table('users', {
    'id': 'INTEGER PRIMARY KEY',
    'name': 'TEXT NOT NULL',
    'email': 'TEXT UNIQUE',
    'age': 'INTEGER'
})

# Async Version
await async_db.create_table('users', {
    'id': 'INTEGER PRIMARY KEY',
    'name': 'TEXT NOT NULL',
    'email': 'TEXT UNIQUE',
    'age': 'INTEGER'
})
```

### Advanced Table Creation
```python
# Table with Complex Constraints
db.create_table('products', {
    'id': 'INTEGER PRIMARY KEY',
    'name': 'TEXT NOT NULL',
    'price': 'DECIMAL(10,2) CHECK (price >= 0)',
    'stock': 'INTEGER DEFAULT 0',
    'category': 'TEXT',
    'created_at': 'DATETIME DEFAULT CURRENT_TIMESTAMP'
})
```

## Modifying Tables
### Adding Columns
```python
# Synchronous
db.execute('ALTER TABLE users ADD COLUMN phone TEXT')

# Asynchronous
await async_db.execute('ALTER TABLE users ADD COLUMN phone TEXT')
```

### Renaming Columns
```python
db.execute('ALTER TABLE users RENAME COLUMN name TO username')
```

## Dropping Tables
```python
# Synchronous
db.execute('DROP TABLE IF EXISTS users')

# Asynchronous
await async_db.execute('DROP TABLE IF EXISTS users')
```

## Checking Table Existence
```python
# Check if table exists (raw SQL)
exists = db.execute('''
    SELECT name FROM sqlite_master 
    WHERE type='table' AND name='users'
''')
```

## Index Management
```python
# Create Index
db.execute('CREATE INDEX idx_users_email ON users(email)')

# Drop Index
db.execute('DROP INDEX IF EXISTS idx_users_email')
```

## Best Practices
- Always use `IF NOT EXISTS` when creating tables
- Validate table schemas before creation
- Use appropriate data types and constraints
- Consider performance implications of indexes
- Handle potential database-specific syntax differences

## Error Handling
```python
try:
    db.create_table('users', {...})
except DatabaseError as e:
    print(f"Table creation failed: {e}")
```

## Performance Considerations
- Minimize the number of columns
- Use appropriate indexing
- Avoid over-normalization
- Consider database-specific optimization techniques
