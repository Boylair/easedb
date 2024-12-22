import asyncio
import datetime
import decimal
from easedb import AsyncDatabase

async def async_mysql_advanced_example():
    """Advanced Asynchronous MySQL Operations"""
    # Create async MySQL database connection
    db = AsyncDatabase('mysql://<username>:<password>@<host>:<port>/<database>')
    
    async with db:
        # Create table
        await db.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                category VARCHAR(50),
                price DECIMAL(10,2),
                stock_quantity INT,
                last_updated DATETIME
            )
        ''')
        
        # Batch insert multiple products
        products_data = [
            {
                'name': 'Laptop',
                'category': 'Electronics',
                'price': decimal.Decimal('1250.00'),
                'stock_quantity': 50,
                'last_updated': datetime.datetime.now()
            },
            {
                'name': 'Smartphone',
                'category': 'Electronics',
                'price': decimal.Decimal('750.50'),
                'stock_quantity': 100,
                'last_updated': datetime.datetime.now()
            }
        ]
        
        # Batch insert
        await db.set('products', products_data)
        
        # Complex query
        electronics_products = await db.get_all('products', {
            'category': 'Electronics',
            'stock_quantity': {'>': 20},
            'price': {'<': decimal.Decimal('2000')}
        }, order_by='price ASC')
        
        print("Electronics products:", electronics_products)
        
        # Transaction handling
        try:
            await db.execute('START TRANSACTION')
            
            # Update product price
            await db.update('products', 
                {'name': 'Laptop'}, 
                {'price': decimal.Decimal('1200.00')}
            )
            
            # Decrease stock
            await db.execute('''
                UPDATE products 
                SET stock_quantity = stock_quantity - 1 
                WHERE name = 'Laptop'
            ''')
            
            await db.execute('COMMIT')
            print("Transaction successful")
        
        except Exception as e:
            await db.execute('ROLLBACK')
            print(f"Transaction failed: {e}")
        
        # Delete product
        await db.delete('products', {'name': 'Smartphone'})

async def main():
    await async_mysql_advanced_example()

if __name__ == '__main__':
    asyncio.run(main())
