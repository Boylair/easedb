# CRUD Operations

## Overview
EaseDB provides simple and intuitive methods for Create, Read, Update, and Delete (CRUD) operations.

## Create (Insert) Operations
### Single Record Insertion
```python
# Synchronous
db.set('users', {
    'name': 'John Doe',
    'email': 'john@example.com',
    'age': 30
})

# Asynchronous
await async_db.set('users', {
    'name': 'Jane Doe',
    'email': 'jane@example.com',
    'age': 25
})
```

### Batch Record Insertion
```python
# Synchronous
db.set('users', [
    {'name': 'Alice', 'email': 'alice@example.com'},
    {'name': 'Bob', 'email': 'bob@example.com'}
])

# Asynchronous
await async_db.set('users', [
    {'name': 'Charlie', 'email': 'charlie@example.com'},
    {'name': 'David', 'email': 'david@example.com'}
])
```

## Read (Query) Operations
### Get Single Record
```python
# Synchronous
user = db.get('users', {'name': 'John Doe'})

# Asynchronous
user = await async_db.get('users', {'name': 'Jane Doe'})
```

### Get Multiple Records
```python
# Synchronous: All users
all_users = db.get_all('users')

# Synchronous: Filtered users
active_users = db.get_all('users', {
    'is_active': True,
    'age': {'>=': 18}
}, order_by='age DESC', limit=10)

# Asynchronous equivalents
all_users = await async_db.get_all('users')
active_users = await async_db.get_all('users', {...})
```

## Update Operations
```python
# Synchronous: Update single record
db.update('users', 
    {'name': 'John Doe'},  # Filter
    {'age': 31, 'email': 'john.new@example.com'}  # Updates
)

# Asynchronous
await async_db.update('users', 
    {'name': 'Jane Doe'},
    {'age': 26}
)
```

## Delete Operations
```python
# Synchronous
db.delete('users', {'name': 'John Doe'})

# Asynchronous
await async_db.delete('users', {'name': 'Jane Doe'})
```

## Advanced Querying
### Complex Filters
```python
# Users between 25 and 35, sorted by registration date
complex_users = db.get_all('users', {
    'age': {'>=': 25, '<=': 35},
    'registration_date': {'>=': '2022-01-01'}
}, order_by='registration_date DESC')
```

## Best Practices
- Always validate input data before CRUD operations
- Use parameterized queries to prevent SQL injection
- Handle potential exceptions during database operations
- Use transactions for complex, multi-step operations
