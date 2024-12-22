# Database Transactions

## Overview
Transactions ensure data integrity by grouping multiple database operations into a single, atomic unit.

## Basic Transaction Usage
### Synchronous Transactions
```python
# Manual Transaction Management
try:
    db.execute('BEGIN TRANSACTION')
    
    # Multiple operations
    db.set('accounts', {'name': 'John', 'balance': 1000})
    db.update('accounts', 
        {'name': 'John'}, 
        {'balance': 500}
    )
    
    db.execute('COMMIT')
except Exception as e:
    db.execute('ROLLBACK')
    print(f"Transaction failed: {e}")
```

### Asynchronous Transactions
```python
async def transfer_money():
    async with async_db:
        try:
            await async_db.execute('START TRANSACTION')
            
            # Transfer money between accounts
            await async_db.update('accounts', 
                {'name': 'Sender'}, 
                {'balance': sender_balance - amount}
            )
            await async_db.update('accounts', 
                {'name': 'Receiver'}, 
                {'balance': receiver_balance + amount}
            )
            
            # Record transaction
            await async_db.set('transactions', {
                'sender': 'Sender',
                'receiver': 'Receiver',
                'amount': amount
            })
            
            await async_db.execute('COMMIT')
        except Exception as e:
            await async_db.execute('ROLLBACK')
            print(f"Transaction failed: {e}")
```

## Context Manager Transactions
```python
# Synchronous Context Manager
with db:
    db.set('users', {'name': 'Alice'})
    db.update('users', {'name': 'Alice'}, {'status': 'active'})

# Asynchronous Context Manager
async with async_db:
    await async_db.set('users', {'name': 'Bob'})
    await async_db.update('users', {'name': 'Bob'}, {'status': 'active'})
```

## Savepoints
```python
# Creating and Rolling Back to Savepoints
try:
    db.execute('BEGIN TRANSACTION')
    
    # First operation
    db.set('logs', {'action': 'start'})
    
    # Create a savepoint
    db.execute('SAVEPOINT my_savepoint')
    
    # Risky operation
    db.update('accounts', {'id': 1}, {'balance': -500})
    
    # If something goes wrong, rollback to savepoint
    db.execute('ROLLBACK TO SAVEPOINT my_savepoint')
    
    db.execute('COMMIT')
except Exception as e:
    db.execute('ROLLBACK')
```

## Best Practices
- Keep transactions as short as possible
- Only include necessary operations in a transaction
- Handle all potential exceptions
- Use appropriate isolation levels
- Avoid long-running transactions

## Common Pitfalls
- Nested transactions can be complex
- Deadlocks can occur with concurrent transactions
- Performance overhead for frequent transactions

## Error Handling
```python
try:
    with db:
        # Transaction operations
        pass
except TransactionError as e:
    # Handle specific transaction errors
    print(f"Transaction error: {e}")
except Exception as e:
    # Handle unexpected errors
    print(f"Unexpected error: {e}")
```

## Performance Considerations
- Minimize the number of operations in a transaction
- Use appropriate indexing
- Choose correct isolation level
- Monitor and optimize long-running transactions
