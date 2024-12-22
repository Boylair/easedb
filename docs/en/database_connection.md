# Database Connection

## Overview
The EaseDB library provides flexible database connection methods for various database types.

## Supported Connection Types
- SQLite
- MySQL
- PostgreSQL
- Other SQL databases

## Synchronous Connection
```python
from easedb import Database

# SQLite Connection
db_sqlite = Database('sqlite:///example.db')

# MySQL Connection
db_mysql = Database('mysql://user:password@localhost/database')
```

## Asynchronous Connection
```python
from easedb import AsyncDatabase

# SQLite Async Connection
async_db_sqlite = AsyncDatabase('sqlite:///async_example.db')

# MySQL Async Connection
async_db_mysql = AsyncDatabase('mysql://user:password@localhost/database')
```

## Connection String Format
The connection string follows the format:
`dialect://username:password@host:port/database_name`

### Parameters
- `dialect`: Database type (sqlite, mysql, postgresql)
- `username`: Database user
- `password`: User password
- `host`: Database server address
- `port`: Database server port
- `database_name`: Name of the database

## Best Practices
- Always use environment variables for sensitive credentials
- Close database connections when not in use
- Use context managers for automatic connection handling

## Error Handling
```python
try:
    db = Database('sqlite:///example.db')
except ConnectionError as e:
    print(f"Database connection failed: {e}")
```

## Security Considerations
- Never hardcode database credentials
- Use secure connection methods
- Implement proper access controls
