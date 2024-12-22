import datetime
from easedb import Database

def sqlite_transaction_example():
    """SQLite Transaction and Advanced Queries Demonstration"""
    # Create SQLite database connection
    db = Database('sqlite:///bank_transactions.db')
    
    # Create tables
    db.execute('''
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            balance REAL DEFAULT 0
        )
    ''')
    
    db.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY,
            from_account_id INTEGER,
            to_account_id INTEGER,
            amount REAL,
            transaction_date DATETIME,
            FOREIGN KEY(from_account_id) REFERENCES accounts(id),
            FOREIGN KEY(to_account_id) REFERENCES accounts(id)
        )
    ''')
    
    # Create initial accounts
    db.set('accounts', [
        {'name': 'Alice', 'balance': 1000.00},
        {'name': 'Bob', 'balance': 500.00}
    ])
    
    # Transaction handling
    try:
        # Start transaction
        db.execute('BEGIN TRANSACTION')
        
        # Transfer money from Alice to Bob
        sender = db.get('accounts', {'name': 'Alice'})
        receiver = db.get('accounts', {'name': 'Bob'})
        
        transfer_amount = 200.00
        
        # Update balances
        db.update('accounts', 
            {'name': 'Alice'}, 
            {'balance': sender['balance'] - transfer_amount}
        )
        
        db.update('accounts', 
            {'name': 'Bob'}, 
            {'balance': receiver['balance'] + transfer_amount}
        )
        
        # Record transaction
        db.set('transactions', {
            'from_account_id': sender['id'],
            'to_account_id': receiver['id'],
            'amount': transfer_amount,
            'transaction_date': datetime.datetime.now()
        })
        
        # Commit transaction
        db.execute('COMMIT')
        print("Transaction successful")
    
    except Exception as e:
        # Rollback in case of error
        db.execute('ROLLBACK')
        print(f"Transaction failed: {e}")
    
    # Query transactions
    transactions = db.get_all('transactions', 
        order_by='transaction_date DESC', 
        limit=5
    )
    
    print("Recent transactions:")
    for transaction in transactions:
        from_account = db.get('accounts', {'id': transaction['from_account_id']})
        to_account = db.get('accounts', {'id': transaction['to_account_id']})
        print(f"Sender: {from_account['name']}, Receiver: {to_account['name']}, Amount: {transaction['amount']}")

if __name__ == '__main__':
    sqlite_transaction_example()
