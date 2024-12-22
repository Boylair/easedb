# Database Column Types Guide

## Overview
Understanding column types is crucial for designing efficient and robust database schemas. This guide covers the most common and useful data types across different database systems.

## Primary Column Types

| Type | Description | Range/Size | Use Cases | Example Values | Constraints/Modifiers |
|------|-------------|------------|-----------|---------------|----------------------|
| **INTEGER** | Whole numbers | -2^63 to 2^63-1 | Counting, IDs, Indexes | 42, -17, 0 | PRIMARY KEY, AUTO INCREMENT, NOT NULL |
| **TEXT** | Variable-length strings | Up to 2GB | Names, Descriptions, Texts | "Hello World", "User123" | NOT NULL, UNIQUE |
| **VARCHAR(n)** | Variable-length string with max length | 0-65,535 chars | Short texts, Usernames | "John", "example@email.com" | LENGTH LIMIT |
| **DECIMAL(p,s)** | Precise decimal numbers | p: total digits, s: decimal places | Financial calculations, Prices | 1234.56, -0.01 | PRECISION CONTROL |
| **FLOAT/REAL** | Floating-point numbers | ±1.7E +/- 308 | Scientific calculations | 3.14159, -2.5 | APPROXIMATE PRECISION |
| **BOOLEAN** | True/False values | TRUE/FALSE or 1/0 | Flags, Statuses | TRUE, FALSE | DEFAULT VALUES |
| **DATETIME** | Date and time | '1000-01-01' to '9999-12-31' | Timestamps, Logs | '2024-12-22 20:30:00' | DEFAULT CURRENT_TIMESTAMP |
| **DATE** | Date only | '1000-01-01' to '9999-12-31' | Birthdays, Event Dates | '2024-12-22' | YEAR, MONTH, DAY |
| **TIME** | Time only | '-838:59:59' to '838:59:59' | Specific times | '14:30:00' | HOURS, MINUTES, SECONDS |

## Comprehensive Constraints and Modifiers

### Basic Constraints

| Constraint | Description | Usage | Example |
|-----------|-------------|-------|---------|
| `NOT NULL` | Prevents null/empty values | Ensures column always has a value | `username VARCHAR(50) NOT NULL` |
| `UNIQUE` | Ensures all values are different | No duplicate values allowed | `email VARCHAR(100) UNIQUE` |
| `PRIMARY KEY` | Unique identifier for each row | Automatically creates an index | `id INTEGER PRIMARY KEY` |
| `DEFAULT` | Sets a default value if no value provided | Automatic value assignment | `status BOOLEAN DEFAULT TRUE` |
| `AUTO INCREMENT` | Automatically increases value for new rows | Used for sequential IDs | `id INTEGER PRIMARY KEY AUTOINCREMENT` |

### Advanced Validation Constraints

| Constraint | Description | Usage | Example |
|-----------|-------------|-------|---------|
| `CHECK` | Adds custom validation rules | Enforce specific conditions | `age INTEGER CHECK (age >= 18)` |
| `FOREIGN KEY` | Creates relationship between tables | Ensures referential integrity | `user_id INTEGER REFERENCES users(id)` |

## Advanced Validation Techniques

### Complex Check Constraints
```sql
-- Multiple condition checks
CREATE TABLE employees (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    salary DECIMAL(10,2) CHECK (salary > 0),
    age INTEGER CHECK (age BETWEEN 18 AND 65),
    email TEXT CHECK (email LIKE '%@%.%')
)
```

### Validation Examples in EaseDB
```python
# Complex validation during table creation
db.create_table('users', {
    'id': 'INTEGER PRIMARY KEY',
    'username': 'VARCHAR(50) NOT NULL UNIQUE',
    'email': 'VARCHAR(100) NOT NULL CHECK (email LIKE "%@%.%")',
    'age': 'INTEGER CHECK (age >= 18 AND age <= 120)',
    'salary': 'DECIMAL(10,2) CHECK (salary >= 0)',
    'registration_date': 'DATETIME CHECK (registration_date <= CURRENT_TIMESTAMP)'
})
```

### Validation Patterns

1. **Range Validation**
   - Limit numeric values
   - Ensure values are within acceptable ranges
   ```sql
   CHECK (value >= min_value AND value <= max_value)
   ```

2. **Pattern Matching**
   - Validate text formats
   - Use LIKE or REGEX
   ```sql
   CHECK (email LIKE '%@%.%')
   CHECK (phone_number REGEXP '^[0-9]{10}$')
   ```

3. **Conditional Logic**
   - Complex multi-condition checks
   ```sql
   CHECK (
     (status = 'active' AND last_login IS NOT NULL) OR 
     (status = 'inactive' AND last_login IS NULL)
   )
   ```

## Performance Considerations for Constraints
- Constraints add validation overhead
- Use sparingly and strategically
- Index complex check conditions
- Consider application-level validation for performance-critical systems

## Common Validation Scenarios

| Scenario | SQL Constraint | Description |
|----------|----------------|-------------|
| Age Verification | `CHECK (age >= 18)` | Ensure user is of legal age |
| Positive Values | `CHECK (value > 0)` | Prevent negative prices/quantities |
| Email Format | `CHECK (email LIKE '%@%.%')` | Basic email validation |
| Date Ranges | `CHECK (start_date < end_date)` | Validate date logic |
| Enum-like Validation | `CHECK (status IN ('active', 'inactive', 'suspended'))` | Limit to specific values |

## Security and Data Integrity
- Constraints prevent invalid data entry
- Reduce risk of data corruption
- Enforce business rules at database level
- Complement application-level validations

## Best Practices
1. Use constraints to enforce data rules
2. Keep validation logic simple
3. Balance between database and application validation
4. Consider performance impact
5. Use meaningful error messages

## Example: Complex User Registration Validation
```python
db.create_table('user_profiles', {
    'id': 'INTEGER PRIMARY KEY',
    'username': 'VARCHAR(50) NOT NULL UNIQUE CHECK (LENGTH(username) >= 3)',
    'email': 'VARCHAR(100) NOT NULL UNIQUE CHECK (email LIKE "%@%.%")',
    'age': 'INTEGER CHECK (age >= 18 AND age <= 120)',
    'registration_date': 'DATETIME DEFAULT CURRENT_TIMESTAMP CHECK (registration_date <= CURRENT_TIMESTAMP)',
    'account_type': 'VARCHAR(20) CHECK (account_type IN ("basic", "premium", "enterprise"))'
})
```

## Best Practices
- Choose the smallest data type that fits your data
- Use constraints to maintain data integrity
- Consider storage and performance implications
- Be consistent across your database schema

## Examples

```python
# Creating a table with various column types
db.create_table('users', {
    'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
    'username': 'VARCHAR(50) NOT NULL UNIQUE',
    'email': 'VARCHAR(100) NOT NULL',
    'age': 'INTEGER CHECK (age >= 18)',
    'balance': 'DECIMAL(10,2) DEFAULT 0.00',
    'is_active': 'BOOLEAN DEFAULT TRUE',
    'registration_date': 'DATETIME DEFAULT CURRENT_TIMESTAMP'
})
```

## Performance and Storage Considerations
- **INTEGER** is fastest for numeric operations
- **TEXT** can be slower for large amounts of data
- **DECIMAL** is precise but slower than FLOAT
- Choose based on your specific use case and performance needs

## Common Pitfalls
- Avoid using TEXT for fixed-length data
- Be careful with floating-point precision
- Don't over-normalize your schema
- Consider database-specific type nuances
